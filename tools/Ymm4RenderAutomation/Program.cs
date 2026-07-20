using System.Diagnostics;
using System.IO;
using System.Linq;
using System.Text;
using System.Text.Json;
using System.Threading;
using System.Windows.Automation;

namespace Ymm4RenderAutomation;

internal static class Program
{
    private static string CurrentStage = "startup";
    private static readonly string[] OutputVideoNames = ["動画出力", "Video Output", "Output Video"];
    private static readonly string[] StartOutputNames = ["出力", "開始", "Output", "Start"];
    private static readonly string[] SaveNames = ["保存", "Save"];

    [STAThread]
    private static int Main(string[] args)
    {
        Console.OutputEncoding = new UTF8Encoding(encoderShouldEmitUTF8Identifier: false);
        Console.InputEncoding = Encoding.UTF8;
        try
        {
            var options = ParseArgs(args);
            return options.Command switch
            {
                "inspect" => Inspect(options),
                "render" => Render(options),
                _ => throw new InvalidOperationException("command must be inspect or render"),
            };
        }
        catch (Exception exception)
        {
            Console.Error.WriteLine(JsonSerializer.Serialize(new
            {
                status = "failed",
                error = exception.GetType().Name,
                message = exception.Message,
                stage = CurrentStage,
            }));
            return 1;
        }
    }

    private static int Inspect(Options options)
    {
        using var owned = Launch(options);
        var main = WaitForMainWindow(owned.Processes, options.TimeoutSeconds);
        var tree = DumpTree(main, maxDepth: 7);
        if (options.Output is not null)
        {
            File.WriteAllText(options.Output, tree, new UTF8Encoding(encoderShouldEmitUTF8Identifier: false));
        }
        else
        {
            Console.WriteLine(tree);
        }
        TryClose(main);
        WaitForExit(owned.Processes, 20);
        return 0;
    }

    private static int Render(Options options)
    {
        if (options.Output is null)
        {
            throw new InvalidOperationException("--output is required for render");
        }
        if (File.Exists(options.Output))
        {
            throw new IOException("render output already exists");
        }

        CurrentStage = "launch";
        using var owned = Launch(options);
        CurrentStage = "wait_main";
        var main = WaitForMainWindow(owned.Processes, options.TimeoutSeconds);
        CurrentStage = "open_video_output";
        OpenVideoOutput(main, owned.Processes);

        CurrentStage = "wait_output_window";
        var outputWindow = WaitForWindow(
            owned.Processes,
            window => ContainsAny(window.Current.Name, OutputVideoNames)
                || (window.Current.Name ?? string.Empty).Contains("Mp4ConfigViewModel", StringComparison.OrdinalIgnoreCase)
                || LooksLikeOutputWindow(window),
            timeoutSeconds: 60,
            excludeHandle: main.Current.NativeWindowHandle
        );

        CurrentStage = "configure_output";
        ConfigureOutput(outputWindow, owned.Processes, options);
        CurrentStage = "start_output";
        var start = FindNamedAction(outputWindow, StartOutputNames)
            ?? throw new InvalidOperationException("video-output start control was not found");
        Invoke(start);

        CurrentStage = "wait_save_dialog";
        var saveDialog = WaitForWindow(
            owned.Processes,
            window => IsSaveDialog(window),
            timeoutSeconds: 60,
            excludeHandle: outputWindow.Current.NativeWindowHandle,
            allowAnyProcess: true
        );
        CurrentStage = "set_save_path";
        SetSavePath(saveDialog, options.Output);
        CurrentStage = "confirm_save";
        var save = FindNamedAction(saveDialog, SaveNames)
            ?? throw new InvalidOperationException("save button was not found");
        Invoke(save);

        CurrentStage = "wait_render_file";
        WaitForFileStable(options.Output, options.TimeoutSeconds);
        CurrentStage = "close_owned_windows";
        TryClose(outputWindow);
        TryClose(main);
        HandleGeneratedProjectClosePrompt(owned.Processes);
        WaitForExit(owned.Processes, 30);

        var file = new FileInfo(options.Output);
        Console.WriteLine(JsonSerializer.Serialize(new
        {
            status = "passed",
            driver = "windows_uia",
            output_bytes = file.Length,
            video_bitrate_kbps_requested = options.VideoBitrateKbps,
            audio_bitrate_kbps_requested = options.AudioBitrateKbps,
            preview_playback = false,
            speaker_playback = false,
            process_cleanup = owned.Processes.All(process => process.HasExited),
        }));
        return 0;
    }

    private static OwnedProcesses Launch(Options options)
    {
        if (options.Executable is null || !File.Exists(options.Executable))
        {
            throw new FileNotFoundException("YMM4 executable is missing");
        }
        if (options.Project is null || !File.Exists(options.Project))
        {
            throw new FileNotFoundException("YMM4 project is missing");
        }
        var baseline = Process.GetProcessesByName("YukkuriMovieMaker").Select(p => p.Id).ToHashSet();
        if (baseline.Count != 0)
        {
            throw new InvalidOperationException("an existing YMM4 process is open; refusing to touch it");
        }
        var startInfo = new ProcessStartInfo
        {
            FileName = options.Executable!,
            UseShellExecute = false,
            WorkingDirectory = Path.GetDirectoryName(options.Executable!)!,
        };
        if (!startInfo.Environment.TryGetValue("WINDIR", out var windir)
            || string.IsNullOrWhiteSpace(windir))
        {
            if (!startInfo.Environment.TryGetValue("SystemRoot", out var systemRoot)
                || string.IsNullOrWhiteSpace(systemRoot))
            {
                throw new InvalidOperationException("WINDIR and SystemRoot are both unavailable");
            }
            startInfo.Environment["WINDIR"] = systemRoot;
        }
        startInfo.ArgumentList.Add(options.Project!);
        var launched = Process.Start(startInfo) ?? throw new InvalidOperationException("YMM4 launch failed");
        var processes = new List<Process> { launched };
        var deadline = DateTime.UtcNow.AddSeconds(3);
        while (DateTime.UtcNow < deadline)
        {
            foreach (var process in Process.GetProcessesByName("YukkuriMovieMaker"))
            {
                if (!baseline.Contains(process.Id) && processes.All(row => row.Id != process.Id))
                {
                    processes.Add(process);
                }
            }
            if (processes.Any(process => !process.HasExited))
            {
                Thread.Sleep(250);
            }
            else
            {
                break;
            }
        }
        return new OwnedProcesses(processes);
    }

    private static AutomationElement WaitForMainWindow(IReadOnlyList<Process> processes, int timeoutSeconds)
    {
        return WaitForWindow(
            processes,
            window =>
                window.Current.ControlType == ControlType.Window
                && !string.IsNullOrWhiteSpace(window.Current.Name)
                && !window.Current.Name.Contains("起動中", StringComparison.OrdinalIgnoreCase),
            timeoutSeconds,
            excludeHandle: null
        );
    }

    private static AutomationElement WaitForWindow(
        IReadOnlyList<Process> processes,
        Func<AutomationElement, bool> predicate,
        int timeoutSeconds,
        int? excludeHandle,
        bool allowAnyProcess = false)
    {
        var deadline = DateTime.UtcNow.AddSeconds(timeoutSeconds);
        while (DateTime.UtcNow < deadline)
        {
            var processIds = processes.Where(p => !p.HasExited).Select(p => p.Id).ToHashSet();
            var windows = AutomationElement.RootElement.FindAll(
                TreeScope.Descendants,
                new PropertyCondition(AutomationElement.ControlTypeProperty, ControlType.Window));
            foreach (AutomationElement window in windows)
            {
                try
                {
                    if (!allowAnyProcess && !processIds.Contains(window.Current.ProcessId))
                    {
                        continue;
                    }
                    if (excludeHandle.HasValue && window.Current.NativeWindowHandle == excludeHandle.Value)
                    {
                        continue;
                    }
                    if (predicate(window))
                    {
                        return window;
                    }
                }
                catch (ElementNotAvailableException)
                {
                    continue;
                }
            }
            Thread.Sleep(250);
        }
        throw new TimeoutException("timed out waiting for a YMM4 window");
    }

    private static AutomationElement? FindNamedAction(AutomationElement root, IEnumerable<string> names)
    {
        var descendants = root.FindAll(TreeScope.Descendants, Condition.TrueCondition);
        foreach (AutomationElement element in descendants)
        {
            if (!element.Current.IsEnabled || !ContainsAny(element.Current.Name, names))
            {
                continue;
            }
            if (element.TryGetCurrentPattern(InvokePattern.Pattern, out _)
                || element.TryGetCurrentPattern(SelectionItemPattern.Pattern, out _))
            {
                return element;
            }
        }
        return null;
    }

    private static bool LooksLikeOutputWindow(AutomationElement window)
    {
        try
        {
            var combos = window.FindAll(
                TreeScope.Descendants,
                new PropertyCondition(AutomationElement.ControlTypeProperty, ControlType.ComboBox));
            return combos.Count >= 5 && FindNamedAction(window, StartOutputNames) is not null;
        }
        catch (ElementNotAvailableException)
        {
            return false;
        }
    }

    private static void OpenVideoOutput(
        AutomationElement main,
        IReadOnlyList<Process> processes)
    {
        var fileMenu = main.FindAll(TreeScope.Descendants, Condition.TrueCondition)
            .Cast<AutomationElement>()
            .FirstOrDefault(element =>
                element.Current.IsEnabled
                && element.Current.ControlType == ControlType.MenuItem
                && ContainsAny(element.Current.Name, ["ファイル", "File"]));
        if (fileMenu is null)
        {
            throw new InvalidOperationException("YMM4 File menu was not found");
        }
        if (fileMenu.TryGetCurrentPattern(ExpandCollapsePattern.Pattern, out var expand))
        {
            ((ExpandCollapsePattern)expand).Expand();
        }
        else
        {
            Invoke(fileMenu);
        }

        var deadline = DateTime.UtcNow.AddSeconds(15);
        while (DateTime.UtcNow < deadline)
        {
            var processIds = processes.Where(process => !process.HasExited).Select(process => process.Id).ToHashSet();
            var action = AutomationElement.RootElement
                .FindAll(TreeScope.Descendants, Condition.TrueCondition)
                .Cast<AutomationElement>()
                .FirstOrDefault(element =>
                    processIds.Contains(element.Current.ProcessId)
                    && element.Current.IsEnabled
                    && ContainsAny(element.Current.Name, OutputVideoNames)
                    && (element.TryGetCurrentPattern(InvokePattern.Pattern, out _)
                        || element.TryGetCurrentPattern(SelectionItemPattern.Pattern, out _)));
            if (action is not null)
            {
                Invoke(action);
                return;
            }
            Thread.Sleep(250);
        }
        throw new InvalidOperationException("YMM4 video-output menu item was not found");
    }

    private static void ConfigureOutput(
        AutomationElement outputWindow,
        IReadOnlyList<Process> processes,
        Options options)
    {
        var combos = GetOutputCombos(outputWindow);
        SelectManualBitrate(combos[2]);
        Thread.Sleep(500);
        combos = GetOutputCombos(outputWindow);

        var numericEdit = outputWindow
            .FindAll(
                TreeScope.Descendants,
                new PropertyCondition(AutomationElement.ControlTypeProperty, ControlType.Edit))
            .Cast<AutomationElement>()
            .FirstOrDefault(element =>
            {
                if (!element.Current.IsEnabled
                    || !element.TryGetCurrentPattern(ValuePattern.Pattern, out var pattern))
                {
                    return false;
                }
                return int.TryParse(((ValuePattern)pattern).Current.Value, out _);
            });
        if (numericEdit is null
            || !numericEdit.TryGetCurrentPattern(ValuePattern.Pattern, out var numericPattern))
        {
            throw new InvalidOperationException("YMM4 video bitrate edit was not found");
        }
        ((ValuePattern)numericPattern).SetValue(options.VideoBitrateKbps.ToString());
        Thread.Sleep(250);
        combos = GetOutputCombos(outputWindow);
        combos[4].SetFocus();

        var expected = $"-b:v {options.VideoBitrateKbps * 1000}";
        var deadline = DateTime.UtcNow.AddSeconds(10);
        while (DateTime.UtcNow < deadline)
        {
            var confirmed = outputWindow
                .FindAll(
                    TreeScope.Descendants,
                    new PropertyCondition(AutomationElement.ControlTypeProperty, ControlType.Edit))
                .Cast<AutomationElement>()
                .Any(element =>
                    element.TryGetCurrentPattern(ValuePattern.Pattern, out var value)
                    && ((ValuePattern)value).Current.Value.Contains(expected, StringComparison.Ordinal));
            if (confirmed)
            {
                combos = GetOutputCombos(outputWindow);
                SelectAudioBitrate(combos[4], options.AudioBitrateKbps);
                return;
            }
            Thread.Sleep(250);
        }
        throw new InvalidOperationException("YMM4 did not commit the requested video bitrate");
    }

    private static List<AutomationElement> GetOutputCombos(AutomationElement outputWindow)
    {
        var combos = outputWindow
            .FindAll(
                TreeScope.Descendants,
                new PropertyCondition(AutomationElement.ControlTypeProperty, ControlType.ComboBox))
            .Cast<AutomationElement>()
            .Where(element => element.Current.IsEnabled)
            .OrderBy(element => element.Current.BoundingRectangle.Top)
            .ThenBy(element => element.Current.BoundingRectangle.Left)
            .ToList();
        if (combos.Count < 5)
        {
            throw new InvalidOperationException("YMM4 output combobox layout was not recognized");
        }
        return combos;
    }

    private static void SelectManualBitrate(AutomationElement combo)
    {
        combo.SetFocus();
        System.Windows.Forms.SendKeys.SendWait("{HOME}{DOWN}{ENTER}");
        Thread.Sleep(350);
    }

    private static void SelectAudioBitrate(AutomationElement combo, int bitrateKbps)
    {
        combo.SetFocus();
        System.Windows.Forms.SendKeys.SendWait(bitrateKbps.ToString());
        System.Windows.Forms.SendKeys.SendWait("{ENTER}");
        Thread.Sleep(350);
    }

    private static void Invoke(AutomationElement element)
    {
        if (element.TryGetCurrentPattern(InvokePattern.Pattern, out var invoke))
        {
            ((InvokePattern)invoke).Invoke();
            return;
        }
        if (element.TryGetCurrentPattern(SelectionItemPattern.Pattern, out var selection))
        {
            ((SelectionItemPattern)selection).Select();
            return;
        }
        throw new InvalidOperationException($"element is not invokable: {element.Current.Name}");
    }

    private static bool IsSaveDialog(AutomationElement window)
    {
        var name = window.Current.Name ?? string.Empty;
        if (name.Contains("名前を付けて保存", StringComparison.OrdinalIgnoreCase)
            || name.Equals("保存", StringComparison.OrdinalIgnoreCase)
            || name.Contains("Save As", StringComparison.OrdinalIgnoreCase))
        {
            return true;
        }
        var fileNameEdit = window.FindFirst(
            TreeScope.Descendants,
            new PropertyCondition(AutomationElement.AutomationIdProperty, "1001")
        );
        return fileNameEdit is not null;
    }

    private static void SetSavePath(AutomationElement dialog, string path)
    {
        var edit = dialog.FindFirst(
            TreeScope.Descendants,
            new PropertyCondition(AutomationElement.AutomationIdProperty, "1001")
        );
        if (edit is null)
        {
            var edits = dialog.FindAll(
                TreeScope.Descendants,
                new PropertyCondition(AutomationElement.ControlTypeProperty, ControlType.Edit)
            );
            edit = edits.Cast<AutomationElement>().LastOrDefault(element => element.Current.IsEnabled);
        }
        if (edit is null || !edit.TryGetCurrentPattern(ValuePattern.Pattern, out var value))
        {
            throw new InvalidOperationException("save filename edit was not found");
        }
        ((ValuePattern)value).SetValue(path);
    }

    private static void WaitForFileStable(string path, int timeoutSeconds)
    {
        var deadline = DateTime.UtcNow.AddSeconds(timeoutSeconds);
        long previousLength = -1;
        var stableSince = DateTime.MinValue;
        while (DateTime.UtcNow < deadline)
        {
            if (File.Exists(path))
            {
                var length = new FileInfo(path).Length;
                if (length > 0 && length == previousLength)
                {
                    if (stableSince == DateTime.MinValue)
                    {
                        stableSince = DateTime.UtcNow;
                    }
                    if ((DateTime.UtcNow - stableSince).TotalSeconds >= 3)
                    {
                        return;
                    }
                }
                else
                {
                    previousLength = length;
                    stableSince = DateTime.MinValue;
                }
            }
            Thread.Sleep(500);
        }
        throw new TimeoutException("timed out waiting for the render file to stabilize");
    }

    private static void TryClose(AutomationElement window)
    {
        try
        {
            if (window.TryGetCurrentPattern(WindowPattern.Pattern, out var pattern))
            {
                ((WindowPattern)pattern).Close();
            }
        }
        catch (ElementNotAvailableException)
        {
        }
    }

    private static void HandleGeneratedProjectClosePrompt(IReadOnlyList<Process> processes)
    {
        try
        {
            var prompt = WaitForWindow(
                processes,
                window =>
                    (window.Current.Name ?? string.Empty).Contains("確認", StringComparison.OrdinalIgnoreCase),
                timeoutSeconds: 3,
                excludeHandle: null
            );
            var no = FindNamedAction(prompt, ["いいえ", "No"]);
            if (no is not null)
            {
                Invoke(no);
            }
        }
        catch (TimeoutException)
        {
        }
    }

    private static void WaitForExit(IReadOnlyList<Process> processes, int timeoutSeconds)
    {
        var deadline = DateTime.UtcNow.AddSeconds(timeoutSeconds);
        while (DateTime.UtcNow < deadline && processes.Any(process => !process.HasExited))
        {
            Thread.Sleep(250);
        }
        foreach (var process in processes.Where(process => !process.HasExited))
        {
            process.Kill(entireProcessTree: true);
            process.WaitForExit(5000);
        }
    }

    private static bool ContainsAny(string? value, IEnumerable<string> needles)
    {
        var text = value ?? string.Empty;
        return needles.Any(needle => text.Contains(needle, StringComparison.OrdinalIgnoreCase));
    }

    private static string DumpTree(AutomationElement root, int maxDepth)
    {
        var lines = new List<string>();
        void Visit(AutomationElement element, int depth)
        {
            if (depth > maxDepth)
            {
                return;
            }
            var patterns = new List<string>();
            if (element.TryGetCurrentPattern(InvokePattern.Pattern, out _)) patterns.Add("Invoke");
            if (element.TryGetCurrentPattern(ValuePattern.Pattern, out _)) patterns.Add("Value");
            if (element.TryGetCurrentPattern(SelectionItemPattern.Pattern, out _)) patterns.Add("Select");
            lines.Add($"{new string(' ', depth * 2)}{element.Current.ControlType.ProgrammaticName}|name={element.Current.Name}|id={element.Current.AutomationId}|enabled={element.Current.IsEnabled}|patterns={string.Join(',', patterns)}");
            var children = element.FindAll(TreeScope.Children, Condition.TrueCondition);
            foreach (AutomationElement child in children)
            {
                Visit(child, depth + 1);
            }
        }
        Visit(root, 0);
        return string.Join(Environment.NewLine, lines);
    }

    private static Options ParseArgs(string[] args)
    {
        if (args.Length == 0)
        {
            throw new InvalidOperationException("missing command");
        }
        var values = new Dictionary<string, string>(StringComparer.OrdinalIgnoreCase);
        for (var index = 1; index < args.Length; index += 2)
        {
            if (index + 1 >= args.Length || !args[index].StartsWith("--", StringComparison.Ordinal))
            {
                throw new InvalidOperationException($"invalid argument near {args[index]}");
            }
            values[args[index][2..]] = args[index + 1];
        }
        return new Options(
            Command: args[0],
            Executable: Get(values, "exe"),
            Project: Get(values, "project"),
            Output: Get(values, "output"),
            VideoBitrateKbps: GetInt(values, "video-bitrate-kbps", 10000),
            AudioBitrateKbps: GetInt(values, "audio-bitrate-kbps", 192),
            TimeoutSeconds: GetInt(values, "timeout-seconds", 1200)
        );
    }

    private static string? Get(IReadOnlyDictionary<string, string> values, string key)
        => values.TryGetValue(key, out var value) ? Path.GetFullPath(value) : null;

    private static int GetInt(IReadOnlyDictionary<string, string> values, string key, int fallback)
        => values.TryGetValue(key, out var raw) && int.TryParse(raw, out var value) ? value : fallback;

    private sealed record Options(
        string Command,
        string? Executable,
        string? Project,
        string? Output,
        int VideoBitrateKbps,
        int AudioBitrateKbps,
        int TimeoutSeconds
    );

    private sealed class OwnedProcesses(IReadOnlyList<Process> processes) : IDisposable
    {
        public IReadOnlyList<Process> Processes { get; } = processes;

        public void Dispose()
        {
            foreach (var process in Processes)
            {
                try
                {
                    if (!process.HasExited)
                    {
                        process.Kill(entireProcessTree: true);
                        process.WaitForExit(5000);
                    }
                }
                catch (InvalidOperationException)
                {
                }
                process.Dispose();
            }
        }
    }
}
