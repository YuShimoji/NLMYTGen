using System.Diagnostics;
using System.IO;
using System.Linq;
using System.Runtime.InteropServices;
using System.Text;
using System.Text.Json;
using System.Text.Json.Nodes;
using System.Threading;
using System.Windows.Automation;
using Microsoft.VisualBasic.FileIO;

namespace Ymm4RenderAutomation;

internal static class Program
{
    private static string CurrentStage = "startup";
    private static readonly string[] OutputVideoNames = ["動画出力", "Video Output", "Output Video"];
    private static readonly string[] StartOutputNames = ["出力", "開始", "Output", "Start"];
    private static readonly string[] SaveNames = ["保存", "Save"];
    private static readonly string[] OpenNames = ["開く", "Open"];
    private static readonly string[] ToolsMenuNames = ["ツール", "Tools"];
    private static readonly string[] FileMenuNames = ["ファイル", "File"];
    private static readonly string[] ScriptImportNames = ["台本", "Script Import", "Import Script"];
    private static readonly string[] ImportConfirmNames = ["読み込み", "読込", "追加", "Import", "OK"];

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
                "import-script" => ImportScript(options),
                "render" => Render(options),
                _ => throw new InvalidOperationException("command must be inspect, import-script, or render"),
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
        WaitForProjectLoaded(main, owned.Processes, options.Project!, options.TimeoutSeconds);
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
        CurrentStage = "wait_project_loaded";
        WaitForProjectLoaded(main, owned.Processes, options.Project!, options.TimeoutSeconds);
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

    private static int ImportScript(Options options)
    {
        if (options.Project is null || !File.Exists(options.Project))
        {
            throw new FileNotFoundException("blank source project is missing");
        }
        if (options.Csv is null || !File.Exists(options.Csv))
        {
            throw new FileNotFoundException("script CSV is missing");
        }

        var project = new FileInfo(options.Project);
        var originalWriteTime = project.LastWriteTimeUtc;
        var originalLength = project.Length;

        CurrentStage = "launch_source_project";
        using var owned = Launch(options);
        CurrentStage = "wait_source_project";
        var main = WaitForMainWindow(owned.Processes, options.TimeoutSeconds);
        CurrentStage = "wait_source_project_loaded";
        WaitForProjectLoaded(main, owned.Processes, options.Project!, options.TimeoutSeconds);
        CurrentStage = "add_script_rows";
        var importedRows = AddScriptRows(main, owned.Processes, options.Csv);
        CurrentStage = "save_source_project";
        var save = FindNamedAction(main, ["プロジェクトを保存", "Save Project"])
            ?? FindProcessNamedAction(owned.Processes, ["プロジェクトを保存", "Save Project"])
            ?? throw new InvalidOperationException("project save control was not found");
        Invoke(save);
        CurrentStage = "wait_source_project_save";
        WaitForFileModifiedStable(options.Project, originalWriteTime, originalLength, options.TimeoutSeconds);

        CurrentStage = "close_owned_windows";
        TryClose(main);
        HandleGeneratedProjectClosePrompt(owned.Processes);
        WaitForExit(owned.Processes, 30);
        var timelineFrames = NormalizeSourceTimeline(
            options.Project,
            expectedVoiceCount: importedRows,
            trailingPaddingFrames: 30
        );

        project.Refresh();
        Console.WriteLine(JsonSerializer.Serialize(new
        {
            status = "passed",
            driver = "windows_uia",
            operation = "script_row_builder",
            imported_rows = importedRows,
            timeline_frames = timelineFrames,
            project_bytes = project.Length,
            source_csv = Path.GetFileName(options.Csv),
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
                && !window.Current.Name.Contains("起動中", StringComparison.OrdinalIgnoreCase)
                && LooksLikeReadyMainWindow(window),
            timeoutSeconds,
            excludeHandle: null
        );
    }

    private static void WaitForProjectLoaded(
        AutomationElement main,
        IReadOnlyList<Process> processes,
        string projectPath,
        int timeoutSeconds)
    {
        var projectName = Path.GetFileNameWithoutExtension(projectPath);
        var deadline = DateTime.UtcNow.AddSeconds(timeoutSeconds);
        var stableSince = DateTime.MinValue;
        while (DateTime.UtcNow < deadline)
        {
            try
            {
                if (HandleCharacterSettingsDialog(processes))
                {
                    stableSince = DateTime.MinValue;
                    Thread.Sleep(500);
                    continue;
                }
                var labels = main
                    .FindAll(
                        TreeScope.Descendants,
                        new PropertyCondition(
                            AutomationElement.ControlTypeProperty,
                            ControlType.Text))
                    .Cast<AutomationElement>()
                    .Select(element => element.Current.Name ?? string.Empty)
                    .Where(name => !string.IsNullOrWhiteSpace(name))
                    .ToList();
                var projectVisible = labels.Any(name =>
                    name.Contains(projectName, StringComparison.OrdinalIgnoreCase));
                var untitledVisible = labels.Any(name =>
                    name.Equals("無題", StringComparison.OrdinalIgnoreCase)
                    || name.Equals("Untitled", StringComparison.OrdinalIgnoreCase));
                if (projectVisible && !untitledVisible)
                {
                    if (stableSince == DateTime.MinValue)
                    {
                        stableSince = DateTime.UtcNow;
                    }
                    if ((DateTime.UtcNow - stableSince).TotalSeconds >= 2)
                    {
                        return;
                    }
                }
                else
                {
                    stableSince = DateTime.MinValue;
                }
            }
            catch (ElementNotAvailableException)
            {
                stableSince = DateTime.MinValue;
            }
            catch (COMException)
            {
                stableSince = DateTime.MinValue;
            }
            Thread.Sleep(250);
        }
        throw new TimeoutException($"YMM4 did not load project: {projectName}");
    }

    private static bool HandleCharacterSettingsDialog(IReadOnlyList<Process> processes)
    {
        var processIds = processes
            .Where(process => !process.HasExited)
            .Select(process => process.Id)
            .ToHashSet();
        var elements = AutomationElement.RootElement
            .FindAll(TreeScope.Descendants, Condition.TrueCondition)
            .Cast<AutomationElement>()
            .Where(element =>
            {
                try
                {
                    return processIds.Contains(element.Current.ProcessId);
                }
                catch (ElementNotAvailableException)
                {
                    return false;
                }
                catch (COMException)
                {
                    return false;
                }
            })
            .ToList();
        var promptVisible = elements.Any(element =>
            (element.Current.Name ?? string.Empty).Contains(
                "異なる設定のキャラクター",
                StringComparison.OrdinalIgnoreCase)
            || (element.Current.Name ?? string.Empty).Contains(
                "different character settings",
                StringComparison.OrdinalIgnoreCase));
        if (!promptVisible)
        {
            return false;
        }
        var keepCurrent = elements.FirstOrDefault(element =>
            element.Current.ControlType == ControlType.RadioButton
            && (
                (element.Current.Name ?? string.Empty).Equals(
                    "現在の設定で上書き",
                    StringComparison.OrdinalIgnoreCase)
                || (element.Current.Name ?? string.Empty).Contains(
                    "current settings",
                    StringComparison.OrdinalIgnoreCase)
            ))
            ?? throw new InvalidOperationException(
                "YMM4 character-settings dialog has no keep-current-settings choice");
        Invoke(keepCurrent);
        Thread.Sleep(250);
        var confirm = elements.FirstOrDefault(element =>
            element.Current.ControlType == ControlType.Button
            && (element.Current.Name ?? string.Empty).Equals(
                "OK",
                StringComparison.OrdinalIgnoreCase))
            ?? throw new InvalidOperationException(
                "YMM4 character-settings dialog has no OK button");
        Invoke(confirm);
        return true;
    }

    private static bool LooksLikeReadyMainWindow(AutomationElement window)
    {
        try
        {
            var descendants = window.FindAll(TreeScope.Descendants, Condition.TrueCondition)
                .Cast<AutomationElement>()
                .ToList();
            var hasProgressWindow = descendants.Any(element =>
                element.Current.ControlType == ControlType.Window
                && (
                    (element.Current.Name ?? string.Empty).Contains(
                        "ProgressViewModel",
                        StringComparison.OrdinalIgnoreCase
                    )
                    || (element.Current.Name ?? string.Empty).Contains(
                        "読み込み中",
                        StringComparison.OrdinalIgnoreCase
                    )
                ));
            var hasToolsMenu = descendants.Any(element =>
                element.Current.IsEnabled
                && element.Current.ControlType == ControlType.MenuItem
                && ContainsAny(element.Current.Name, ToolsMenuNames));
            return !hasProgressWindow && hasToolsMenu;
        }
        catch (ElementNotAvailableException)
        {
            return false;
        }
        catch (COMException)
        {
            return false;
        }
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
                catch (COMException)
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

    private static AutomationElement? FindProcessNamedAction(
        IReadOnlyList<Process> processes,
        IEnumerable<string> names)
    {
        var processIds = processes.Where(process => !process.HasExited).Select(process => process.Id).ToHashSet();
        return AutomationElement.RootElement
            .FindAll(TreeScope.Descendants, Condition.TrueCondition)
            .Cast<AutomationElement>()
            .LastOrDefault(element =>
            {
                try
                {
                    return processIds.Contains(element.Current.ProcessId)
                        && element.Current.IsEnabled
                        && !element.Current.IsOffscreen
                        && ContainsAny(element.Current.Name, names)
                        && (
                            element.TryGetCurrentPattern(InvokePattern.Pattern, out _)
                            || element.TryGetCurrentPattern(SelectionItemPattern.Pattern, out _)
                        );
                }
                catch (ElementNotAvailableException)
                {
                    return false;
                }
            });
    }

    private static int AddScriptRows(
        AutomationElement main,
        IReadOnlyList<Process> processes,
        string csvPath)
    {
        var rows = ReadScriptRows(csvPath);

        foreach (var row in rows)
        {
            var speakerCombo = FindSpeakerCombo(main);
            var textEdit = FindVoiceTextEdit(main);
            SelectComboValue(speakerCombo, processes, row.Speaker);
            if (!textEdit.TryGetCurrentPattern(ValuePattern.Pattern, out var value))
            {
                throw new InvalidOperationException("YMM4 voice text edit lost ValuePattern");
            }
            ((ValuePattern)value).SetValue(row.Text);

            var addDeadline = DateTime.UtcNow.AddSeconds(30);
            AutomationElement? add = null;
            while (DateTime.UtcNow < addDeadline)
            {
                add = main
                    .FindAll(
                        TreeScope.Descendants,
                        new PropertyCondition(
                            AutomationElement.ControlTypeProperty,
                            ControlType.Button
                        )
                    )
                    .Cast<AutomationElement>()
                    .LastOrDefault(element =>
                        element.Current.IsEnabled
                        && !element.Current.IsOffscreen
                        && element.Current.Name.Equals("追加", StringComparison.OrdinalIgnoreCase)
                        && element.TryGetCurrentPattern(InvokePattern.Pattern, out _)
                    );
                if (add is not null)
                {
                    break;
                }
                Thread.Sleep(100);
            }
            if (add is null)
            {
                throw new TimeoutException("timed out waiting for the YMM4 voice add button");
            }
            Invoke(add);

            var completionDeadline = DateTime.UtcNow.AddSeconds(60);
            while (DateTime.UtcNow < completionDeadline)
            {
                textEdit = FindVoiceTextEdit(main);
                if (
                    textEdit.TryGetCurrentPattern(ValuePattern.Pattern, out var current)
                    && string.IsNullOrEmpty(((ValuePattern)current).Current.Value)
                )
                {
                    break;
                }
                Thread.Sleep(100);
            }
            if (
                !textEdit.TryGetCurrentPattern(ValuePattern.Pattern, out var completed)
                || !string.IsNullOrEmpty(((ValuePattern)completed).Current.Value)
            )
            {
                throw new TimeoutException("timed out waiting for YMM4 voice generation");
            }
        }
        return rows.Count;
    }

    private static AutomationElement FindSpeakerCombo(AutomationElement main) => main
        .FindAll(
            TreeScope.Descendants,
            new PropertyCondition(AutomationElement.ControlTypeProperty, ControlType.ComboBox)
        )
        .Cast<AutomationElement>()
        .FirstOrDefault(element =>
            element.Current.IsEnabled
            && element.Current.AutomationId.Equals("combobox", StringComparison.OrdinalIgnoreCase)
        )
        ?? throw new InvalidOperationException("YMM4 speaker combo was not found");

    private static AutomationElement FindVoiceTextEdit(AutomationElement main) => main
        .FindAll(
            TreeScope.Descendants,
            new PropertyCondition(AutomationElement.ControlTypeProperty, ControlType.Edit)
        )
        .Cast<AutomationElement>()
        .FirstOrDefault(element =>
            element.Current.IsEnabled
            && element.Current.AutomationId.Equals("PARTS_TextBox", StringComparison.OrdinalIgnoreCase)
            && element.TryGetCurrentPattern(ValuePattern.Pattern, out _)
        )
        ?? throw new InvalidOperationException("YMM4 voice text edit was not found");

    private static void SelectComboValue(
        AutomationElement combo,
        IReadOnlyList<Process> processes,
        string expected)
    {
        if (combo.TryGetCurrentPattern(SelectionPattern.Pattern, out var currentSelection))
        {
            var selected = ((SelectionPattern)currentSelection).Current.GetSelection();
            if (selected.Any(element => element.Current.Name.Equals(expected, StringComparison.Ordinal)))
            {
                return;
            }
        }
        if (!combo.TryGetCurrentPattern(ExpandCollapsePattern.Pattern, out var expand))
        {
            throw new InvalidOperationException("YMM4 speaker combo is not expandable");
        }
        ((ExpandCollapsePattern)expand).Expand();

        var deadline = DateTime.UtcNow.AddSeconds(15);
        while (DateTime.UtcNow < deadline)
        {
            var processIds = processes.Where(process => !process.HasExited).Select(process => process.Id).ToHashSet();
            var visibleElements = AutomationElement.RootElement
                .FindAll(TreeScope.Descendants, Condition.TrueCondition)
                .Cast<AutomationElement>();
            var label = visibleElements.LastOrDefault(element =>
                {
                    try
                    {
                        return processIds.Contains(element.Current.ProcessId)
                            && element.Current.IsEnabled
                            && !element.Current.IsOffscreen
                            && element.Current.Name.Equals(expected, StringComparison.Ordinal);
                    }
                    catch (ElementNotAvailableException)
                    {
                        return false;
                    }
                });
            var choice = label;
            while (
                choice is not null
                && !choice.TryGetCurrentPattern(SelectionItemPattern.Pattern, out _)
            )
            {
                choice = TreeWalker.ControlViewWalker.GetParent(choice);
            }
            if (
                choice is not null
                && choice.TryGetCurrentPattern(SelectionItemPattern.Pattern, out var selection)
            )
            {
                ((SelectionItemPattern)selection).Select();
                if (
                    combo.TryGetCurrentPattern(ExpandCollapsePattern.Pattern, out var collapse)
                    && ((ExpandCollapsePattern)collapse).Current.ExpandCollapseState
                        != ExpandCollapseState.Collapsed
                )
                {
                    ((ExpandCollapsePattern)collapse).Collapse();
                }
                return;
            }
            Thread.Sleep(100);
        }
        var available = AutomationElement.RootElement
            .FindAll(TreeScope.Descendants, Condition.TrueCondition)
            .Cast<AutomationElement>()
            .Where(element =>
            {
                try
                {
                    return processes.Any(process =>
                            !process.HasExited && process.Id == element.Current.ProcessId
                        )
                        && !string.IsNullOrWhiteSpace(element.Current.Name)
                        && element.TryGetCurrentPattern(SelectionItemPattern.Pattern, out _);
                }
                catch (ElementNotAvailableException)
                {
                    return false;
                }
            })
            .Select(element => element.Current.Name)
            .Distinct()
            .Take(30);
        throw new TimeoutException(
            $"YMM4 speaker was not found: {expected}; selectable values: {string.Join(" | ", available)}"
        );
    }

    private static List<ScriptRow> ReadScriptRows(string path)
    {
        using var parser = new TextFieldParser(path, Encoding.UTF8, detectEncoding: true)
        {
            TextFieldType = FieldType.Delimited,
            HasFieldsEnclosedInQuotes = true,
            TrimWhiteSpace = false,
        };
        parser.SetDelimiters(",");
        var rows = new List<ScriptRow>();
        while (!parser.EndOfData)
        {
            var fields = parser.ReadFields();
            if (fields is null || fields.Length == 0)
            {
                continue;
            }
            if (fields.Length != 2 || fields.Any(string.IsNullOrWhiteSpace))
            {
                throw new InvalidDataException("script CSV rows must contain speaker and text");
            }
            rows.Add(new ScriptRow(fields[0], fields[1]));
        }
        if (rows.Count == 0)
        {
            throw new InvalidDataException("script CSV is empty");
        }
        return rows;
    }

    private static int NormalizeSourceTimeline(
        string path,
        int expectedVoiceCount,
        int trailingPaddingFrames)
    {
        var root = JsonNode.Parse(
                File.ReadAllText(path, Encoding.UTF8),
                nodeOptions: new JsonNodeOptions { PropertyNameCaseInsensitive = false },
                documentOptions: default
            )?.AsObject()
            ?? throw new InvalidDataException("saved YMM4 project root is invalid");
        var timelines = root["Timelines"]?.AsArray()
            ?? throw new InvalidDataException("saved YMM4 project has no timelines");
        if (timelines.Count != 1)
        {
            throw new InvalidDataException("saved YMM4 project must have one timeline");
        }
        var timeline = timelines[0]?.AsObject()
            ?? throw new InvalidDataException("saved YMM4 timeline is invalid");
        var items = timeline["Items"]?.AsArray()
            ?? throw new InvalidDataException("saved YMM4 timeline has no items");
        var voices = items
            .Select(node => node?.AsObject())
            .Where(item =>
                item is not null
                && (item["$type"]?.GetValue<string>() ?? string.Empty).StartsWith(
                    "YukkuriMovieMaker.Project.Items.VoiceItem",
                    StringComparison.Ordinal
                )
            )
            .Cast<JsonObject>()
            .ToList();
        if (voices.Count != expectedVoiceCount)
        {
            throw new InvalidDataException(
                $"saved YMM4 project has {voices.Count} voices; expected {expectedVoiceCount}"
            );
        }

        var frame = 0;
        foreach (var voice in voices)
        {
            var generatedLength = voice["Length"]?.GetValue<int>() ?? 0;
            if (generatedLength <= 0)
            {
                throw new InvalidDataException("saved YMM4 voice has an invalid length");
            }
            voice["Frame"] = frame;
            voice["Length"] = generatedLength + trailingPaddingFrames;
            SanitizeRootedPaths(voice["TachieFaceParameter"]);
            SanitizeRootedPaths(voice["TachieFaceEffects"]);
            frame += generatedLength + trailingPaddingFrames;
        }
        if (root["Characters"] is JsonArray characters)
        {
            foreach (var characterNode in characters)
            {
                if (characterNode is not JsonObject character)
                {
                    continue;
                }
                SanitizeRootedPaths(character["TachieCharacterParameter"]);
                SanitizeRootedPaths(character["TachieDefaultItemParameter"]);
                SanitizeRootedPaths(character["TachieDefaultFaceParameter"]);
                SanitizeRootedPaths(character["TachieItemVideoEffects"]);
                SanitizeRootedPaths(character["TachieDefaultFaceEffects"]);
            }
        }
        timeline["Length"] = frame;
        timeline["CurrentFrame"] = 0;
        timeline["MaxLayer"] = voices.Max(voice => voice["Layer"]?.GetValue<int>() ?? 0);
        File.WriteAllText(
            path,
            root.ToJsonString(new JsonSerializerOptions { WriteIndented = false }),
            new UTF8Encoding(encoderShouldEmitUTF8Identifier: false)
        );
        return frame;
    }

    private static void SanitizeRootedPaths(JsonNode? node)
    {
        if (node is JsonObject jsonObject)
        {
            foreach (var property in jsonObject.ToList())
            {
                if (
                    property.Value is JsonValue value
                    && value.TryGetValue<string>(out var text)
                    && !string.IsNullOrWhiteSpace(text)
                    && Path.IsPathRooted(text)
                )
                {
                    var trimmed = text.TrimEnd(
                        Path.DirectorySeparatorChar,
                        Path.AltDirectorySeparatorChar);
                    jsonObject[property.Key] = Path.GetFileName(trimmed);
                }
                else
                {
                    SanitizeRootedPaths(property.Value);
                }
            }
            return;
        }
        if (node is JsonArray jsonArray)
        {
            for (var index = 0; index < jsonArray.Count; index += 1)
            {
                if (
                    jsonArray[index] is JsonValue value
                    && value.TryGetValue<string>(out var text)
                    && !string.IsNullOrWhiteSpace(text)
                    && Path.IsPathRooted(text)
                )
                {
                    var trimmed = text.TrimEnd(
                        Path.DirectorySeparatorChar,
                        Path.AltDirectorySeparatorChar);
                    jsonArray[index] = Path.GetFileName(trimmed);
                }
                else
                {
                    SanitizeRootedPaths(jsonArray[index]);
                }
            }
        }
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

    private static void OpenMenuAction(
        AutomationElement main,
        IReadOnlyList<Process> processes,
        IEnumerable<string> menuNames,
        IEnumerable<string> actionNames)
    {
        var menu = main.FindAll(TreeScope.Descendants, Condition.TrueCondition)
            .Cast<AutomationElement>()
            .FirstOrDefault(element =>
                element.Current.IsEnabled
                && element.Current.ControlType == ControlType.MenuItem
                && ContainsAny(element.Current.Name, menuNames));
        if (menu is null)
        {
            throw new InvalidOperationException("YMM4 menu was not found");
        }
        main.SetFocus();
        menu.SetFocus();
        if (!menu.TryGetCurrentPattern(ExpandCollapsePattern.Pattern, out var expand))
        {
            throw new InvalidOperationException("YMM4 menu does not expose ExpandCollapsePattern");
        }
        ((ExpandCollapsePattern)expand).Expand();

        var deadline = DateTime.UtcNow.AddSeconds(15);
        while (DateTime.UtcNow < deadline)
        {
            var processIds = processes.Where(process => !process.HasExited).Select(process => process.Id).ToHashSet();
            var action = AutomationElement.RootElement
                .FindAll(TreeScope.Descendants, Condition.TrueCondition)
                .Cast<AutomationElement>()
                .LastOrDefault(element =>
                    processIds.Contains(element.Current.ProcessId)
                    && element.Current.IsEnabled
                    && !element.Current.IsOffscreen
                    && element.Current.BoundingRectangle.Width > 0
                    && element.Current.BoundingRectangle.Height > 0
                    && ContainsAny(element.Current.Name, actionNames)
                    && (
                        element.TryGetCurrentPattern(InvokePattern.Pattern, out _)
                        || element.TryGetCurrentPattern(SelectionItemPattern.Pattern, out _)
                    )
                );
            if (action is not null)
            {
                if (action.TryGetCurrentPattern(InvokePattern.Pattern, out var invoke))
                {
                    try
                    {
                        ((InvokePattern)invoke).Invoke();
                    }
                    catch (ElementNotAvailableException)
                    {
                        // WPF removes the popup menu element synchronously when
                        // the command opens its owned window.
                    }
                    return;
                }
                if (action.TryGetCurrentPattern(SelectionItemPattern.Pattern, out var selection))
                {
                    try
                    {
                        ((SelectionItemPattern)selection).Select();
                    }
                    catch (ElementNotAvailableException)
                    {
                        // Same popup disposal behavior as InvokePattern.
                    }
                    return;
                }
                throw new InvalidOperationException(
                    $"YMM4 menu action is neither selectable nor invokable: {action.Current.Name}"
                );
            }
            Thread.Sleep(250);
        }
        throw new InvalidOperationException("YMM4 menu action was not found");
    }

    private static void CloseStaleScriptEditor(
        AutomationElement main,
        IReadOnlyList<Process> processes)
    {
        var processIds = processes.Where(process => !process.HasExited).Select(process => process.Id).ToHashSet();
        AutomationElement? FindEditorWindow()
        {
            var title = AutomationElement.RootElement
                .FindAll(TreeScope.Descendants, Condition.TrueCondition)
                .Cast<AutomationElement>()
                .FirstOrDefault(element =>
                    processIds.Contains(element.Current.ProcessId)
                    && (element.Current.Name ?? string.Empty).Contains(
                        "台本編集",
                        StringComparison.OrdinalIgnoreCase
                    )
                );
            if (title is null)
            {
                return null;
            }
            var titleRect = title.Current.BoundingRectangle;
            var titleCenter = new System.Windows.Point(
                titleRect.Left + titleRect.Width / 2,
                titleRect.Top + titleRect.Height / 2
            );
            return AutomationElement.RootElement
                .FindAll(
                    TreeScope.Descendants,
                    new PropertyCondition(
                        AutomationElement.ControlTypeProperty,
                        ControlType.Window
                    )
                )
                .Cast<AutomationElement>()
                .FirstOrDefault(window =>
                    processIds.Contains(window.Current.ProcessId)
                    && window.Current.NativeWindowHandle != main.Current.NativeWindowHandle
                    && window.Current.BoundingRectangle.Contains(titleCenter)
                );
        }

        var editor = FindEditorWindow();
        if (editor is null)
        {
            return;
        }
        TryClose(editor);

        var deadline = DateTime.UtcNow.AddSeconds(10);
        while (DateTime.UtcNow < deadline)
        {
            var prompt = AutomationElement.RootElement
                .FindAll(
                    TreeScope.Descendants,
                    new PropertyCondition(
                        AutomationElement.ControlTypeProperty,
                        ControlType.Window
                    )
                )
                .Cast<AutomationElement>()
                .FirstOrDefault(window =>
                    processIds.Contains(window.Current.ProcessId)
                    && window.Current.NativeWindowHandle != main.Current.NativeWindowHandle
                    && FindNamedAction(
                        window,
                        ["保存しない", "破棄", "いいえ", "Don't Save", "No"]
                    ) is not null
                );
            if (prompt is not null)
            {
                var discard = FindNamedAction(
                    prompt,
                    ["保存しない", "破棄", "いいえ", "Don't Save", "No"]
                )!;
                Invoke(discard);
            }
            if (FindEditorWindow() is null)
            {
                return;
            }
            Thread.Sleep(250);
        }
        throw new TimeoutException("timed out closing the stale YMM4 script editor");
    }

    private static AutomationElement WaitForNamedElement(
        IReadOnlyList<Process> processes,
        IEnumerable<string> names,
        int timeoutSeconds)
    {
        var deadline = DateTime.UtcNow.AddSeconds(timeoutSeconds);
        while (DateTime.UtcNow < deadline)
        {
            var processIds = processes
                .Where(process => !process.HasExited)
                .Select(process => process.Id)
                .ToHashSet();
            var element = AutomationElement.RootElement
                .FindAll(TreeScope.Descendants, Condition.TrueCondition)
                .Cast<AutomationElement>()
                .FirstOrDefault(candidate =>
                {
                    try
                    {
                        return processIds.Contains(candidate.Current.ProcessId)
                            && candidate.Current.IsEnabled
                            && ContainsAny(candidate.Current.Name, names);
                    }
                    catch (ElementNotAvailableException)
                    {
                        return false;
                    }
                });
            if (element is not null)
            {
                return element;
            }
            Thread.Sleep(250);
        }
        throw new TimeoutException("timed out waiting for a named YMM4 element");
    }

    private static void ConfigureOutput(
        AutomationElement outputWindow,
        IReadOnlyList<Process> processes,
        Options options)
    {
        var combos = GetOutputCombos(outputWindow);
        CurrentStage = "configure_output_video_mode";
        SelectComboIndex(combos[2], processes, 1);
        Thread.Sleep(500);
        combos = GetOutputCombos(outputWindow);

        CurrentStage = "configure_output_video_bitrate";
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
        CurrentStage = "configure_output_audio_bitrate";
        SelectComboContaining(combos[4], processes, options.AudioBitrateKbps.ToString());

        CurrentStage = "confirm_output_video_bitrate";
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

    private static void SelectComboIndex(
        AutomationElement combo,
        IReadOnlyList<Process> processes,
        int index)
    {
        var choices = ExpandComboChoices(combo, processes);
        if (index < 0 || index >= choices.Count)
        {
            throw new InvalidOperationException(
                $"YMM4 output combo has {choices.Count} choices; index {index} is unavailable"
            );
        }
        CurrentStage = $"{CurrentStage}_select";
        SelectComboChoice(combo, choices[index]);
    }

    private static void SelectComboContaining(
        AutomationElement combo,
        IReadOnlyList<Process> processes,
        string expectedFragment)
    {
        var choices = ExpandComboChoices(combo, processes);
        var choice = choices.FirstOrDefault(element =>
            ChoiceLabel(element).Contains(
                expectedFragment,
                StringComparison.OrdinalIgnoreCase
            )
        );
        if (choice is null)
        {
            var available = string.Join(", ", choices.Select(DescribeElement));
            throw new InvalidOperationException(
                $"YMM4 output combo value was not found: {expectedFragment}; available={available}"
            );
        }
        CurrentStage = $"{CurrentStage}_select";
        SelectComboChoice(combo, choice);
    }

    private static string ChoiceLabel(AutomationElement element)
    {
        try
        {
            var labels = element
                .FindAll(
                    TreeScope.Descendants,
                    new PropertyCondition(AutomationElement.ControlTypeProperty, ControlType.Text))
                .Cast<AutomationElement>()
                .Select(label => label.Current.Name)
                .Where(name => !string.IsNullOrWhiteSpace(name))
                .ToList();
            return labels.Count > 0
                ? string.Join(" ", labels)
                : element.Current.Name ?? string.Empty;
        }
        catch (ElementNotAvailableException)
        {
            return string.Empty;
        }
        catch (COMException)
        {
            return string.Empty;
        }
        catch (InvalidOperationException)
        {
            return string.Empty;
        }
    }

    private static string DescribeElement(AutomationElement element)
    {
        try
        {
            return $"{element.Current.ControlType.ProgrammaticName}:{ChoiceLabel(element)}";
        }
        catch (ElementNotAvailableException)
        {
            return "unavailable";
        }
        catch (COMException)
        {
            return "unavailable";
        }
        catch (InvalidOperationException)
        {
            return "unavailable";
        }
    }

    private static IReadOnlyList<AutomationElement> ExpandComboChoices(
        AutomationElement combo,
        IReadOnlyList<Process> processes)
    {
        var stagePrefix = CurrentStage;
        CurrentStage = $"{stagePrefix}_pattern";
        if (!combo.TryGetCurrentPattern(ExpandCollapsePattern.Pattern, out var expand))
        {
            throw new InvalidOperationException("YMM4 output combo is not expandable");
        }
        var comboRect = combo.Current.BoundingRectangle;
        CurrentStage = $"{stagePrefix}_focus";
        combo.SetFocus();
        Thread.Sleep(150);
        CurrentStage = $"{stagePrefix}_state";
        var expander = (ExpandCollapsePattern)expand;
        if (expander.Current.ExpandCollapseState == ExpandCollapseState.Collapsed)
        {
            CurrentStage = $"{stagePrefix}_expand";
            try
            {
                expander.Expand();
            }
            catch (InvalidOperationException) when (
                combo.TryGetCurrentPattern(InvokePattern.Pattern, out var invoke)
            )
            {
                ((InvokePattern)invoke).Invoke();
            }
        }
        else if (expander.Current.ExpandCollapseState == ExpandCollapseState.LeafNode)
        {
            throw new InvalidOperationException("YMM4 output combo has no expandable choices");
        }
        CurrentStage = $"{stagePrefix}_choices";
        var deadline = DateTime.UtcNow.AddSeconds(15);
        while (DateTime.UtcNow < deadline)
        {
            var processIds = processes.Where(process => !process.HasExited).Select(process => process.Id).ToHashSet();
            var choices = AutomationElement.RootElement
                .FindAll(TreeScope.Descendants, Condition.TrueCondition)
                .Cast<AutomationElement>()
                .Where(element =>
                {
                    try
                    {
                        var rect = element.Current.BoundingRectangle;
                        var horizontallyOverlaps = rect.Right > comboRect.Left
                            && rect.Left < comboRect.Right;
                        return processIds.Contains(element.Current.ProcessId)
                            && element.Current.IsEnabled
                            && !element.Current.IsOffscreen
                            && rect.Width > 0
                            && rect.Height > 0
                            && horizontallyOverlaps
                            && element.TryGetCurrentPattern(SelectionItemPattern.Pattern, out _);
                    }
                    catch (ElementNotAvailableException)
                    {
                        return false;
                    }
                    catch (COMException)
                    {
                        return false;
                    }
                    catch (InvalidOperationException)
                    {
                        return false;
                    }
                })
                .OrderBy(element => element.Current.BoundingRectangle.Top)
                .ToList();
            if (choices.Count > 0)
            {
                CurrentStage = stagePrefix;
                return choices;
            }
            Thread.Sleep(100);
        }
        throw new TimeoutException("timed out reading YMM4 output combo choices");
    }

    private static void SelectComboChoice(AutomationElement combo, AutomationElement choice)
    {
        if (!choice.TryGetCurrentPattern(SelectionItemPattern.Pattern, out var selection))
        {
            throw new InvalidOperationException("YMM4 output combo choice is not selectable");
        }
        try
        {
            ((SelectionItemPattern)selection).Select();
        }
        catch (InvalidOperationException) when (
            choice.TryGetCurrentPattern(InvokePattern.Pattern, out var invoke)
        )
        {
            ((InvokePattern)invoke).Invoke();
        }
        try
        {
            if (
                combo.TryGetCurrentPattern(ExpandCollapsePattern.Pattern, out var collapse)
                && ((ExpandCollapsePattern)collapse).Current.ExpandCollapseState
                    == ExpandCollapseState.Expanded
            )
            {
                ((ExpandCollapsePattern)collapse).Collapse();
            }
        }
        catch (ElementNotAvailableException)
        {
            // Selection can replace the WPF ComboBox peer after it commits.
        }
        catch (InvalidOperationException)
        {
            // Some WPF peers commit by selecting and immediately invalidate Collapse.
        }
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

    private static bool IsOpenDialog(AutomationElement window)
    {
        var name = window.Current.Name ?? string.Empty;
        return name.Contains("開く", StringComparison.OrdinalIgnoreCase)
            || name.Contains("Open", StringComparison.OrdinalIgnoreCase);
    }

    private static void SetSavePath(AutomationElement dialog, string path)
        => SetDialogPath(dialog, path);

    private static void SetDialogPath(AutomationElement dialog, string path)
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

    private static void CompleteScriptImportDialogs(
        AutomationElement main,
        IReadOnlyList<Process> processes)
    {
        var deadline = DateTime.UtcNow.AddSeconds(90);
        var quietSince = DateTime.MinValue;
        while (DateTime.UtcNow < deadline)
        {
            var processIds = processes.Where(process => !process.HasExited).Select(process => process.Id).ToHashSet();
            var dialogs = AutomationElement.RootElement
                .FindAll(
                    TreeScope.Descendants,
                    new PropertyCondition(AutomationElement.ControlTypeProperty, ControlType.Window))
                .Cast<AutomationElement>()
                .Where(window =>
                    processIds.Contains(window.Current.ProcessId)
                    && window.Current.NativeWindowHandle != main.Current.NativeWindowHandle)
                .ToList();
            var actionable = dialogs
                .Select(dialog => FindNamedAction(dialog, ImportConfirmNames))
                .FirstOrDefault(action => action is not null);
            if (actionable is not null)
            {
                Invoke(actionable);
                quietSince = DateTime.MinValue;
                Thread.Sleep(500);
                continue;
            }
            var blocking = dialogs.Any(dialog =>
                !string.IsNullOrWhiteSpace(dialog.Current.Name)
                && !dialog.Current.Name.Contains("ProgressViewModel", StringComparison.OrdinalIgnoreCase));
            if (!blocking)
            {
                if (quietSince == DateTime.MinValue)
                {
                    quietSince = DateTime.UtcNow;
                }
                if ((DateTime.UtcNow - quietSince).TotalSeconds >= 3)
                {
                    return;
                }
            }
            else
            {
                quietSince = DateTime.MinValue;
            }
            Thread.Sleep(250);
        }
        throw new TimeoutException("timed out waiting for YMM4 script import to complete");
    }

    private static void WaitForFileStable(
        string path,
        int timeoutSeconds,
        long minimumLengthBytes = 64 * 1024,
        int stableSeconds = 10)
    {
        var deadline = DateTime.UtcNow.AddSeconds(timeoutSeconds);
        long previousLength = -1;
        var stableSince = DateTime.MinValue;
        while (DateTime.UtcNow < deadline)
        {
            if (File.Exists(path))
            {
                var length = new FileInfo(path).Length;
                if (length >= minimumLengthBytes && length == previousLength)
                {
                    if (stableSince == DateTime.MinValue)
                    {
                        stableSince = DateTime.UtcNow;
                    }
                    if ((DateTime.UtcNow - stableSince).TotalSeconds >= stableSeconds)
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

    private static void WaitForFileModifiedStable(
        string path,
        DateTime originalWriteTime,
        long originalLength,
        int timeoutSeconds)
    {
        var deadline = DateTime.UtcNow.AddSeconds(timeoutSeconds);
        long previousLength = -1;
        var stableSince = DateTime.MinValue;
        while (DateTime.UtcNow < deadline)
        {
            if (File.Exists(path))
            {
                var file = new FileInfo(path);
                var changed = file.LastWriteTimeUtc > originalWriteTime || file.Length != originalLength;
                if (changed && file.Length > 0 && file.Length == previousLength)
                {
                    if (stableSince == DateTime.MinValue)
                    {
                        stableSince = DateTime.UtcNow;
                    }
                    if ((DateTime.UtcNow - stableSince).TotalSeconds >= 2)
                    {
                        return;
                    }
                }
                else
                {
                    previousLength = file.Length;
                    stableSince = DateTime.MinValue;
                }
            }
            Thread.Sleep(500);
        }
        throw new TimeoutException("timed out waiting for the source project save");
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
            if (element.TryGetCurrentPattern(ExpandCollapsePattern.Pattern, out var expand))
            {
                patterns.Add($"Expand:{((ExpandCollapsePattern)expand).Current.ExpandCollapseState}");
            }
            lines.Add($"{new string(' ', depth * 2)}{element.Current.ControlType.ProgrammaticName}|name={element.Current.Name}|id={element.Current.AutomationId}|enabled={element.Current.IsEnabled}|focusable={element.Current.IsKeyboardFocusable}|offscreen={element.Current.IsOffscreen}|patterns={string.Join(',', patterns)}");
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
            Csv: Get(values, "csv"),
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
        string? Csv,
        int VideoBitrateKbps,
        int AudioBitrateKbps,
        int TimeoutSeconds
    );

    private sealed record ScriptRow(string Speaker, string Text);

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
