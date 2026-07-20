[CmdletBinding()]
param(
    [ValidateSet('inspect', 'mute')]
    [string]$Mode = 'inspect',

    [string]$OwnedPidCsv = ''
)

$ErrorActionPreference = 'Stop'

$source = @'
using System;
using System.Collections.Generic;
using System.Runtime.InteropServices;

public enum EDataFlow { eRender, eCapture, eAll }
public enum ERole { eConsole, eMultimedia, eCommunications }
public enum AudioSessionState { Inactive = 0, Active = 1, Expired = 2 }

[ComImport, Guid("BCDE0395-E52F-467C-8E3D-C4579291692E")]
public class MMDeviceEnumeratorComObject { }

[ComImport, Guid("A95664D2-9614-4F35-A746-DE8DB63617E6"), InterfaceType(ComInterfaceType.InterfaceIsIUnknown)]
public interface IMMDeviceEnumerator {
    int EnumAudioEndpoints(EDataFlow dataFlow, uint stateMask, out IntPtr devices);
    int GetDefaultAudioEndpoint(EDataFlow dataFlow, ERole role, out IMMDevice endpoint);
    int GetDevice([MarshalAs(UnmanagedType.LPWStr)] string id, out IMMDevice device);
    int RegisterEndpointNotificationCallback(IntPtr client);
    int UnregisterEndpointNotificationCallback(IntPtr client);
}

[ComImport, Guid("D666063F-1587-4E43-81F1-B948E807363F"), InterfaceType(ComInterfaceType.InterfaceIsIUnknown)]
public interface IMMDevice {
    int Activate(ref Guid iid, uint clsCtx, IntPtr activationParams, [MarshalAs(UnmanagedType.IUnknown)] out object instance);
    int OpenPropertyStore(uint access, out IntPtr properties);
    int GetId([MarshalAs(UnmanagedType.LPWStr)] out string id);
    int GetState(out uint state);
}

[ComImport, Guid("77AA99A0-1BD6-484F-8BC7-2C654C9A9B6F"), InterfaceType(ComInterfaceType.InterfaceIsIUnknown)]
public interface IAudioSessionManager2 {
    int GetAudioSessionControl(ref Guid sessionGuid, uint streamFlags, out IntPtr sessionControl);
    int GetSimpleAudioVolume(ref Guid sessionGuid, uint streamFlags, out IntPtr simpleVolume);
    int GetSessionEnumerator(out IAudioSessionEnumerator sessionEnum);
    int RegisterSessionNotification(IntPtr notification);
    int UnregisterSessionNotification(IntPtr notification);
    int RegisterDuckNotification([MarshalAs(UnmanagedType.LPWStr)] string sessionId, IntPtr notification);
    int UnregisterDuckNotification(IntPtr notification);
}

[ComImport, Guid("E2F5BB11-0570-40CA-ACDD-3AA01277DEE8"), InterfaceType(ComInterfaceType.InterfaceIsIUnknown)]
public interface IAudioSessionEnumerator {
    int GetCount(out int count);
    int GetSession(int index, out IAudioSessionControl control);
}

[ComImport, Guid("F4B1A599-7266-4319-A8CA-E70ACB11E8CD"), InterfaceType(ComInterfaceType.InterfaceIsIUnknown)]
public interface IAudioSessionControl {
    int GetState(out AudioSessionState state);
    int GetDisplayName([MarshalAs(UnmanagedType.LPWStr)] out string value);
    int SetDisplayName([MarshalAs(UnmanagedType.LPWStr)] string value, ref Guid context);
    int GetIconPath([MarshalAs(UnmanagedType.LPWStr)] out string value);
    int SetIconPath([MarshalAs(UnmanagedType.LPWStr)] string value, ref Guid context);
    int GetGroupingParam(out Guid value);
    int SetGroupingParam(ref Guid value, ref Guid context);
    int RegisterAudioSessionNotification(IntPtr client);
    int UnregisterAudioSessionNotification(IntPtr client);
}

[ComImport, Guid("bfb7ff88-7239-4fc9-8fa2-07c950be9c6d"), InterfaceType(ComInterfaceType.InterfaceIsIUnknown)]
public interface IAudioSessionControl2 {
    int GetState(out AudioSessionState state);
    int GetDisplayName([MarshalAs(UnmanagedType.LPWStr)] out string value);
    int SetDisplayName([MarshalAs(UnmanagedType.LPWStr)] string value, ref Guid context);
    int GetIconPath([MarshalAs(UnmanagedType.LPWStr)] out string value);
    int SetIconPath([MarshalAs(UnmanagedType.LPWStr)] string value, ref Guid context);
    int GetGroupingParam(out Guid value);
    int SetGroupingParam(ref Guid value, ref Guid context);
    int RegisterAudioSessionNotification(IntPtr client);
    int UnregisterAudioSessionNotification(IntPtr client);
    int GetSessionIdentifier([MarshalAs(UnmanagedType.LPWStr)] out string value);
    int GetSessionInstanceIdentifier([MarshalAs(UnmanagedType.LPWStr)] out string value);
    int GetProcessId(out uint processId);
    int IsSystemSoundsSession();
    int SetDuckingPreference(bool optOut);
}

[ComImport, Guid("87CE5498-68D6-44E5-9215-6DA47EF883D8"), InterfaceType(ComInterfaceType.InterfaceIsIUnknown)]
public interface ISimpleAudioVolume {
    int SetMasterVolume(float level, ref Guid context);
    int GetMasterVolume(out float level);
    int SetMute([MarshalAs(UnmanagedType.Bool)] bool mute, ref Guid context);
    int GetMute([MarshalAs(UnmanagedType.Bool)] out bool mute);
}

public class ProjectAudioSessionRow {
    public int Pid { get; set; }
    public bool Active { get; set; }
    public bool Muted { get; set; }
    public bool MutationPerformed { get; set; }
}

public static class ProjectAudioSessions {
    public static List<ProjectAudioSessionRow> Enumerate(HashSet<int> owned, bool muteOwned, out int total) {
        total = 0;
        var rows = new List<ProjectAudioSessionRow>();
        var deviceEnumerator = (IMMDeviceEnumerator)(new MMDeviceEnumeratorComObject());
        IMMDevice device = null;
        IAudioSessionManager2 manager = null;
        IAudioSessionEnumerator sessions = null;
        try {
            Marshal.ThrowExceptionForHR(deviceEnumerator.GetDefaultAudioEndpoint(EDataFlow.eRender, ERole.eMultimedia, out device));
            Guid managerIid = typeof(IAudioSessionManager2).GUID;
            object managerObject;
            Marshal.ThrowExceptionForHR(device.Activate(ref managerIid, 23, IntPtr.Zero, out managerObject));
            manager = (IAudioSessionManager2)managerObject;
            Marshal.ThrowExceptionForHR(manager.GetSessionEnumerator(out sessions));
            Marshal.ThrowExceptionForHR(sessions.GetCount(out total));
            for (int index = 0; index < total; index++) {
                IAudioSessionControl control = null;
                IAudioSessionControl2 control2 = null;
                ISimpleAudioVolume volume = null;
                try {
                    Marshal.ThrowExceptionForHR(sessions.GetSession(index, out control));
                    control2 = (IAudioSessionControl2)control;
                    uint pid;
                    Marshal.ThrowExceptionForHR(control2.GetProcessId(out pid));
                    if (!owned.Contains((int)pid)) continue;
                    volume = (ISimpleAudioVolume)control;
                    bool changed = false;
                    bool muted;
                    Marshal.ThrowExceptionForHR(volume.GetMute(out muted));
                    if (muteOwned && !muted) {
                        Guid context = Guid.NewGuid();
                        Marshal.ThrowExceptionForHR(volume.SetMute(true, ref context));
                        changed = true;
                        Marshal.ThrowExceptionForHR(volume.GetMute(out muted));
                    }
                    AudioSessionState state;
                    Marshal.ThrowExceptionForHR(control.GetState(out state));
                    rows.Add(new ProjectAudioSessionRow {
                        Pid = (int)pid,
                        Active = state == AudioSessionState.Active,
                        Muted = muted,
                        MutationPerformed = changed
                    });
                } finally {
                    if (volume != null && !Object.ReferenceEquals(volume, control)) Marshal.FinalReleaseComObject(volume);
                    if (control2 != null && !Object.ReferenceEquals(control2, control)) Marshal.FinalReleaseComObject(control2);
                    if (control != null) Marshal.FinalReleaseComObject(control);
                }
            }
            return rows;
        } finally {
            if (sessions != null) Marshal.FinalReleaseComObject(sessions);
            if (manager != null) Marshal.FinalReleaseComObject(manager);
            if (device != null) Marshal.FinalReleaseComObject(device);
            if (deviceEnumerator != null) Marshal.FinalReleaseComObject(deviceEnumerator);
        }
    }
}
'@

if (-not ('ProjectAudioSessions' -as [type])) {
    Add-Type -TypeDefinition $source -Language CSharp
}

$owned = [System.Collections.Generic.HashSet[int]]::new()
if ($OwnedPidCsv) {
    foreach ($value in $OwnedPidCsv.Split(',')) {
        $parsed = 0
        if (-not [int]::TryParse($value.Trim(), [ref]$parsed) -or $parsed -le 0) {
            throw 'OwnedPidCsv must contain positive integer process IDs.'
        }
        [void]$owned.Add($parsed)
    }
}

$total = 0
$rows = [ProjectAudioSessions]::Enumerate($owned, $Mode -eq 'mute', [ref]$total)
$sessions = @($rows | ForEach-Object {
    $processName = 'unknown'
    try {
        $processName = ([System.Diagnostics.Process]::GetProcessById($_.Pid).ProcessName + '.exe').ToLowerInvariant()
    } catch {
        $processName = 'exited.exe'
    }
    [ordered]@{
        pid = $_.Pid
        executable = $processName
        active = $_.Active
        muted = $_.Muted
        project_owned = $true
        mutation_performed = $_.MutationPerformed
    }
})

[ordered]@{
    schema = 'nlmytgen.project_audio_session_inspection.v1'
    supported = $true
    mode = $Mode
    total_session_count = $total
    owned_pid_count = $owned.Count
    owned_session_count = $sessions.Count
    muted_owned_session_count = @($sessions | Where-Object muted).Count
    unmuted_owned_session_count = @($sessions | Where-Object { -not $_.muted }).Count
    sessions = $sessions
    unowned_session_mutation = $false
    master_volume_operation = $false
} | ConvertTo-Json -Depth 5 -Compress
