"""Silent-by-default containment for project-owned browser/media inspection.

This module deliberately has no audible opt-in.  It launches an isolated
Chromium-family process, installs media blocking before navigation, mutes only
Core Audio sessions mapped to that owned process tree, and removes the tree and
profile when the operation ends.
"""

from __future__ import annotations

import argparse
import base64
import ctypes
from ctypes import wintypes
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import socket
import struct
import subprocess
import tempfile
import time
from typing import Any, Iterable, Mapping, Sequence
from urllib.parse import urlparse
import wave


AUDIO_POLICY_ENV = "NLMYTGEN_AUDIO_POLICY"
DEFAULT_AUDIO_POLICY = "silent"

BROWSER_EXECUTABLES = {"chrome", "chrome.exe", "msedge", "msedge.exe", "chromium", "chromium.exe"}
BLOCKED_PLAYER_EXECUTABLES = {
    "voicevox",
    "voicevox.exe",
    "softalk",
    "softalk.exe",
    "softalkw",
    "softalkw.exe",
    "yukkurimoviemaker",
    "yukkurimoviemaker.exe",
    "ffplay",
    "ffplay.exe",
    "mpv",
    "mpv.exe",
    "vlc",
    "vlc.exe",
    "wmplayer",
    "wmplayer.exe",
}
SYNTHESIS_ENGINE_EXECUTABLES = {
    "voicevox_engine",
    "voicevox_engine.exe",
    "vv-engine",
    "vv-engine.exe",
}
PYTHON_PLAYBACK_MARKERS = (
    "winsound",
    "playsound",
    "pyttsx3",
    "sounddevice",
    "pyaudio",
    "simpleaudio",
    "pygame.mixer",
)
SYSTEM_SPEECH_MARKERS = ("system.speech", "speechsynthesizer")
SYSTEM_SPEECH_PLAY_MARKERS = (".speak(", ".speakasync(", " speak ")

BROWSER_FLAGS = (
    "--headless=new",
    "--mute-audio",
    "--autoplay-policy=user-gesture-required",
    "--disable-background-mode",
    "--disable-background-networking",
    "--disable-breakpad",
    "--disable-component-update",
    "--disable-crash-reporter",
    "--disable-default-apps",
    "--disable-sync",
    "--metrics-recording-only",
    "--no-default-browser-check",
    "--no-first-run",
    "--no-pings",
    "--remote-debugging-address=127.0.0.1",
    "--remote-debugging-port=0",
    "--remote-allow-origins=http://127.0.0.1",
)

DOM_MEDIA_GUARD_SCRIPT = r"""
(() => {
  'use strict';
  const MARK = '__nlmytgenSilentMediaGuard';
  const enforce = (node) => {
    if (!(node instanceof HTMLMediaElement)) return;
    if (!node.paused) { try { node.pause(); } catch (_) {} }
    if (!node.muted) node.muted = true;
    if (!node.defaultMuted) node.defaultMuted = true;
    if (node.volume !== 0) node.volume = 0;
    if (node.autoplay) node.autoplay = false;
    if (node.hasAttribute('autoplay')) node.removeAttribute('autoplay');
  };
  const scan = (root) => {
    if (!root) return;
    if (root instanceof HTMLMediaElement) enforce(root);
    if (root.querySelectorAll) root.querySelectorAll('audio,video').forEach(enforce);
  };
  const originalPlay = HTMLMediaElement.prototype.play;
  HTMLMediaElement.prototype.play = function() {
    enforce(this);
    return Promise.resolve();
  };
  const observer = new MutationObserver((records) => {
    for (const record of records) {
      if (record.type === 'attributes') enforce(record.target);
      record.addedNodes.forEach(scan);
    }
  });
  observer.observe(document, {
    childList: true,
    subtree: true,
    attributes: true,
    attributeFilter: ['autoplay', 'muted', 'volume', 'src']
  });
  document.addEventListener('readystatechange', () => scan(document), true);
  document.addEventListener('DOMContentLoaded', () => scan(document), true);
  window[MARK] = {
    active: true,
    policy: 'silent',
    observerActive: true,
    originalPlayCaptured: typeof originalPlay === 'function'
  };
  scan(document);
})();
""".strip()

DOM_STATE_EXPRESSION = r"""
JSON.stringify((() => {
  const media = Array.from(document.querySelectorAll('audio,video'));
  const guard = window.__nlmytgenSilentMediaGuard || {};
  return {
    readyState: document.readyState,
    mediaCount: media.length,
    allMuted: media.every((node) => node.muted === true),
    allVolumeZero: media.every((node) => node.volume === 0),
    allAutoplayFalse: media.every((node) => node.autoplay === false && !node.hasAttribute('autoplay')),
    allPaused: media.every((node) => node.paused === true),
    observerActive: guard.observerActive === true,
    policy: guard.policy || null
  };
})())
""".strip()


class SilentPolicyError(RuntimeError):
    """The requested action violates the development audio policy."""


class GuardRuntimeError(RuntimeError):
    """The silent browser operation could not be proven contained."""

    def __init__(
        self,
        message: str,
        *,
        error_code: str = "silent_guard_verification_failed",
        details: Mapping[str, Any] | None = None,
    ) -> None:
        super().__init__(message)
        self.error_code = error_code
        self.details = dict(details or {})


def resolve_audio_policy(environment: Mapping[str, str] | None = None) -> str:
    env = os.environ if environment is None else environment
    value = env.get(AUDIO_POLICY_ENV, DEFAULT_AUDIO_POLICY).strip().lower()
    if value != DEFAULT_AUDIO_POLICY:
        raise SilentPolicyError(
            f"{AUDIO_POLICY_ENV} supports only 'silent' in this development slice"
        )
    return DEFAULT_AUDIO_POLICY


def _basename(value: str | os.PathLike[str]) -> str:
    return str(value).replace("\\", "/").rsplit("/", 1)[-1].lower()


def classify_command(command: Sequence[str]) -> str:
    if not command:
        return "invalid"
    executable = _basename(command[0])
    joined = " ".join(str(part) for part in command).lower()
    if executable in SYNTHESIS_ENGINE_EXECUTABLES:
        return "synthesis_engine_only"
    if executable in BLOCKED_PLAYER_EXECUTABLES:
        return "audible_frontend_or_player"
    if executable in BROWSER_EXECUTABLES:
        return "browser_media_capable"
    if any(marker in joined for marker in PYTHON_PLAYBACK_MARKERS):
        return "python_playback"
    if any(marker in joined for marker in SYSTEM_SPEECH_MARKERS) and any(
        marker in joined for marker in SYSTEM_SPEECH_PLAY_MARKERS
    ):
        return "system_speech_playback"
    if executable in {"ffprobe", "ffprobe.exe"}:
        return "static_media_metadata"
    if executable in {"ffmpeg", "ffmpeg.exe"}:
        return "media_file_generation_or_null_decode"
    return "non_playback_or_unclassified"


def assert_command_allowed(command: Sequence[str], *, guarded_browser: bool = False) -> str:
    resolve_audio_policy()
    category = classify_command(command)
    if category in {
        "invalid",
        "audible_frontend_or_player",
        "python_playback",
        "system_speech_playback",
    }:
        raise SilentPolicyError(f"silent policy rejected command category: {category}")
    if category == "browser_media_capable" and not guarded_browser:
        raise SilentPolicyError("browser media requires the silent inspection wrapper")
    return category


def build_browser_command(
    browser_path: Path,
    profile_path: Path,
    initial_url: str = "about:blank",
) -> list[str]:
    command = [str(browser_path), *BROWSER_FLAGS, f"--user-data-dir={profile_path}", initial_url]
    assert_command_allowed(command, guarded_browser=True)
    return command


def find_browser() -> Path:
    candidates: list[Path] = []
    for variable, suffixes in (
        ("PROGRAMFILES", ("Google/Chrome/Application/chrome.exe", "Microsoft/Edge/Application/msedge.exe")),
        ("PROGRAMFILES(X86)", ("Google/Chrome/Application/chrome.exe", "Microsoft/Edge/Application/msedge.exe")),
        ("LOCALAPPDATA", ("Google/Chrome/Application/chrome.exe", "Microsoft/Edge/Application/msedge.exe")),
    ):
        root = os.environ.get(variable)
        if root:
            candidates.extend(Path(root) / suffix for suffix in suffixes)
    for name in ("chrome.exe", "msedge.exe", "chromium.exe"):
        resolved = shutil.which(name)
        if resolved:
            candidates.append(Path(resolved))
    for candidate in candidates:
        if candidate.is_file():
            return candidate.resolve()
    raise GuardRuntimeError("no Chromium-family browser executable found")


def create_zero_amplitude_fixture(directory: Path, *, seconds: int = 1, rate: int = 8000) -> dict[str, Any]:
    directory.mkdir(parents=True, exist_ok=True)
    wav_path = directory / "zero_amplitude.wav"
    frame_count = seconds * rate
    frames = b"\x00\x00" * frame_count
    with wave.open(str(wav_path), "wb") as output:
        output.setnchannels(1)
        output.setsampwidth(2)
        output.setframerate(rate)
        output.writeframes(frames)
    with wave.open(str(wav_path), "rb") as source:
        readback = source.readframes(source.getnframes())
        parameters = source.getparams()
    if readback != frames or any(readback):
        raise GuardRuntimeError("zero-amplitude fixture readback failed")

    html_path = directory / "silent_media_fixture.html"
    html_path.write_text(
        "<!doctype html><meta charset=\"utf-8\"><title>Silent media guard fixture</title>\n"
        "<audio id=\"fixture\" autoplay src=\"zero_amplitude.wav\"></audio>\n"
        "<script>addEventListener('DOMContentLoaded',()=>document.querySelector('#fixture').play());</script>\n",
        encoding="utf-8",
        newline="\n",
    )
    return {
        "wav_path": wav_path,
        "html_path": html_path,
        "waveform": "zero_amplitude",
        "sample_rate": parameters.framerate,
        "sample_width": parameters.sampwidth,
        "channels": parameters.nchannels,
        "frame_count": parameters.nframes,
        "pcm_all_zero": True,
        "wav_sha256": hashlib.sha256(wav_path.read_bytes()).hexdigest(),
    }


class _PROCESSENTRY32W(ctypes.Structure):
    _fields_ = [
        ("dwSize", wintypes.DWORD),
        ("cntUsage", wintypes.DWORD),
        ("th32ProcessID", wintypes.DWORD),
        ("th32DefaultHeapID", ctypes.c_size_t),
        ("th32ModuleID", wintypes.DWORD),
        ("cntThreads", wintypes.DWORD),
        ("th32ParentProcessID", wintypes.DWORD),
        ("pcPriClassBase", wintypes.LONG),
        ("dwFlags", wintypes.DWORD),
        ("szExeFile", wintypes.WCHAR * 260),
    ]


def process_snapshot() -> dict[int, dict[str, Any]]:
    if os.name != "nt":
        return {os.getpid(): {"pid": os.getpid(), "parent_pid": os.getppid(), "executable": "python"}}
    kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
    kernel32.CreateToolhelp32Snapshot.argtypes = (wintypes.DWORD, wintypes.DWORD)
    kernel32.CreateToolhelp32Snapshot.restype = wintypes.HANDLE
    kernel32.Process32FirstW.argtypes = (wintypes.HANDLE, ctypes.POINTER(_PROCESSENTRY32W))
    kernel32.Process32FirstW.restype = wintypes.BOOL
    kernel32.Process32NextW.argtypes = (wintypes.HANDLE, ctypes.POINTER(_PROCESSENTRY32W))
    kernel32.Process32NextW.restype = wintypes.BOOL
    kernel32.CloseHandle.argtypes = (wintypes.HANDLE,)
    kernel32.CloseHandle.restype = wintypes.BOOL
    snapshot = kernel32.CreateToolhelp32Snapshot(0x00000002, 0)
    invalid_handle = ctypes.c_void_p(-1).value
    if snapshot == invalid_handle:
        raise ctypes.WinError(ctypes.get_last_error())
    entry = _PROCESSENTRY32W()
    entry.dwSize = ctypes.sizeof(entry)
    rows: dict[int, dict[str, Any]] = {}
    try:
        ok = kernel32.Process32FirstW(snapshot, ctypes.byref(entry))
        while ok:
            pid = int(entry.th32ProcessID)
            rows[pid] = {
                "pid": pid,
                "parent_pid": int(entry.th32ParentProcessID),
                "executable": entry.szExeFile,
            }
            ok = kernel32.Process32NextW(snapshot, ctypes.byref(entry))
    finally:
        kernel32.CloseHandle(snapshot)
    return rows


def descendant_pids(root_pid: int, snapshot: Mapping[int, Mapping[str, Any]]) -> set[int]:
    descendants = {root_pid}
    changed = True
    while changed:
        changed = False
        for pid, row in snapshot.items():
            if pid not in descendants and int(row.get("parent_pid", -1)) in descendants:
                descendants.add(pid)
                changed = True
    return descendants


class _JobObject:
    def __init__(self, process: subprocess.Popen[bytes]) -> None:
        self.handle: int | None = None
        if os.name != "nt":
            return

        class JOBOBJECT_BASIC_LIMIT_INFORMATION(ctypes.Structure):
            _fields_ = [
                ("PerProcessUserTimeLimit", ctypes.c_longlong),
                ("PerJobUserTimeLimit", ctypes.c_longlong),
                ("LimitFlags", wintypes.DWORD),
                ("MinimumWorkingSetSize", ctypes.c_size_t),
                ("MaximumWorkingSetSize", ctypes.c_size_t),
                ("ActiveProcessLimit", wintypes.DWORD),
                ("Affinity", ctypes.c_size_t),
                ("PriorityClass", wintypes.DWORD),
                ("SchedulingClass", wintypes.DWORD),
            ]

        class IO_COUNTERS(ctypes.Structure):
            _fields_ = [(name, ctypes.c_ulonglong) for name in (
                "ReadOperationCount", "WriteOperationCount", "OtherOperationCount",
                "ReadTransferCount", "WriteTransferCount", "OtherTransferCount",
            )]

        class JOBOBJECT_EXTENDED_LIMIT_INFORMATION(ctypes.Structure):
            _fields_ = [
                ("BasicLimitInformation", JOBOBJECT_BASIC_LIMIT_INFORMATION),
                ("IoInfo", IO_COUNTERS),
                ("ProcessMemoryLimit", ctypes.c_size_t),
                ("JobMemoryLimit", ctypes.c_size_t),
                ("PeakProcessMemoryUsed", ctypes.c_size_t),
                ("PeakJobMemoryUsed", ctypes.c_size_t),
            ]

        kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
        kernel32.CreateJobObjectW.argtypes = (ctypes.c_void_p, wintypes.LPCWSTR)
        kernel32.CreateJobObjectW.restype = wintypes.HANDLE
        kernel32.SetInformationJobObject.argtypes = (
            wintypes.HANDLE,
            ctypes.c_int,
            ctypes.c_void_p,
            wintypes.DWORD,
        )
        kernel32.SetInformationJobObject.restype = wintypes.BOOL
        kernel32.AssignProcessToJobObject.argtypes = (wintypes.HANDLE, wintypes.HANDLE)
        kernel32.AssignProcessToJobObject.restype = wintypes.BOOL
        kernel32.CloseHandle.argtypes = (wintypes.HANDLE,)
        kernel32.CloseHandle.restype = wintypes.BOOL
        handle = kernel32.CreateJobObjectW(None, None)
        if not handle:
            raise ctypes.WinError(ctypes.get_last_error())
        limits = JOBOBJECT_EXTENDED_LIMIT_INFORMATION()
        limits.BasicLimitInformation.LimitFlags = 0x00002000
        if not kernel32.SetInformationJobObject(
            handle, 9, ctypes.byref(limits), ctypes.sizeof(limits)
        ):
            error = ctypes.get_last_error()
            kernel32.CloseHandle(handle)
            raise ctypes.WinError(error)
        if not kernel32.AssignProcessToJobObject(handle, wintypes.HANDLE(process._handle)):
            error = ctypes.get_last_error()
            kernel32.CloseHandle(handle)
            raise ctypes.WinError(error)
        self.handle = handle

    def close(self) -> None:
        if self.handle is not None:
            kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
            kernel32.CloseHandle.argtypes = (wintypes.HANDLE,)
            kernel32.CloseHandle.restype = wintypes.BOOL
            kernel32.CloseHandle(self.handle)
            self.handle = None


OwnedProcessJob = _JobObject


class _WebSocket:
    def __init__(self, url: str) -> None:
        parsed = urlparse(url)
        if parsed.scheme != "ws" or parsed.hostname not in {"127.0.0.1", "localhost"}:
            raise GuardRuntimeError("CDP WebSocket must be loopback-only")
        self.socket = socket.create_connection((parsed.hostname, parsed.port or 80), timeout=15)
        key = base64.b64encode(os.urandom(16)).decode("ascii")
        request = (
            f"GET {parsed.path or '/'} HTTP/1.1\r\n"
            f"Host: {parsed.hostname}:{parsed.port or 80}\r\n"
            "Upgrade: websocket\r\nConnection: Upgrade\r\n"
            f"Sec-WebSocket-Key: {key}\r\nSec-WebSocket-Version: 13\r\n"
            "Origin: http://127.0.0.1\r\n\r\n"
        )
        self.socket.sendall(request.encode("ascii"))
        response = b""
        while b"\r\n\r\n" not in response:
            chunk = self.socket.recv(4096)
            if not chunk:
                break
            response += chunk
        if not response.startswith(b"HTTP/1.1 101"):
            self.socket.close()
            raise GuardRuntimeError("CDP WebSocket handshake failed")
        self.next_id = 1

    def _read_exact(self, count: int) -> bytes:
        result = b""
        while len(result) < count:
            chunk = self.socket.recv(count - len(result))
            if not chunk:
                raise GuardRuntimeError("CDP WebSocket closed unexpectedly")
            result += chunk
        return result

    def _send_frame(self, payload: bytes, opcode: int = 1) -> None:
        mask = os.urandom(4)
        length = len(payload)
        header = bytearray([0x80 | opcode])
        if length < 126:
            header.append(0x80 | length)
        elif length < 65536:
            header.append(0x80 | 126)
            header.extend(struct.pack("!H", length))
        else:
            header.append(0x80 | 127)
            header.extend(struct.pack("!Q", length))
        header.extend(mask)
        masked = bytes(value ^ mask[index % 4] for index, value in enumerate(payload))
        self.socket.sendall(bytes(header) + masked)

    def _receive_frame(self) -> tuple[int, bytes]:
        first, second = self._read_exact(2)
        opcode = first & 0x0F
        length = second & 0x7F
        if length == 126:
            length = struct.unpack("!H", self._read_exact(2))[0]
        elif length == 127:
            length = struct.unpack("!Q", self._read_exact(8))[0]
        mask = self._read_exact(4) if second & 0x80 else b""
        payload = self._read_exact(length)
        if mask:
            payload = bytes(value ^ mask[index % 4] for index, value in enumerate(payload))
        return opcode, payload

    def command(self, method: str, params: Mapping[str, Any] | None = None, *, session_id: str | None = None) -> dict[str, Any]:
        message_id = self.next_id
        self.next_id += 1
        payload: dict[str, Any] = {"id": message_id, "method": method}
        if params is not None:
            payload["params"] = dict(params)
        if session_id is not None:
            payload["sessionId"] = session_id
        self._send_frame(json.dumps(payload, separators=(",", ":")).encode("utf-8"))
        while True:
            opcode, raw = self._receive_frame()
            if opcode == 8:
                raise GuardRuntimeError("CDP WebSocket closed before response")
            if opcode == 9:
                self._send_frame(raw, opcode=10)
                continue
            if opcode != 1:
                continue
            response = json.loads(raw.decode("utf-8"))
            if response.get("id") == message_id:
                if "error" in response:
                    raise GuardRuntimeError(f"CDP command failed: {method}")
                return response.get("result", {})

    def close(self) -> None:
        try:
            self._send_frame(b"", opcode=8)
        except OSError:
            pass
        self.socket.close()


def _wait_for_devtools(profile_path: Path, process: subprocess.Popen[bytes], timeout: float = 15.0) -> str:
    active_port = profile_path / "DevToolsActivePort"
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        if process.poll() is not None:
            raise GuardRuntimeError("guarded browser exited before CDP became available")
        if active_port.is_file():
            lines = active_port.read_text(encoding="utf-8").splitlines()
            if len(lines) >= 2 and lines[0].isdigit() and lines[1].startswith("/"):
                return f"ws://127.0.0.1:{lines[0]}{lines[1]}"
        time.sleep(0.05)
    raise GuardRuntimeError("guarded browser CDP startup timed out")


def _powershell_executable() -> str:
    for name in ("pwsh.exe", "powershell.exe"):
        resolved = shutil.which(name)
        if resolved:
            return resolved
    raise GuardRuntimeError("PowerShell is required for built-in Core Audio inspection")


def inspect_audio_sessions(helper_path: Path, owned_pids: Iterable[int], *, mode: str) -> dict[str, Any]:
    if mode not in {"inspect", "mute"}:
        raise ValueError("invalid audio-session helper mode")
    pid_csv = ",".join(str(pid) for pid in sorted(set(owned_pids)))
    command = [
        _powershell_executable(),
        "-NoLogo",
        "-NoProfile",
        "-NonInteractive",
        "-File",
        str(helper_path),
        "-Mode",
        mode,
        "-OwnedPidCsv",
        pid_csv,
    ]
    completed = subprocess.run(command, check=False, capture_output=True, text=True, timeout=30)
    if completed.returncode != 0:
        raise GuardRuntimeError("Core Audio session helper failed")
    try:
        result = json.loads(completed.stdout)
    except json.JSONDecodeError as exc:
        raise GuardRuntimeError("Core Audio session helper returned invalid JSON") from exc
    if not result.get("supported"):
        raise GuardRuntimeError("Core Audio session inspection unavailable")
    return result


def _sanitize_command_line(value: str | None, replacements: Iterable[Path | str]) -> str:
    if not value:
        return "unavailable"
    sanitized = value
    for replacement in sorted((str(item) for item in replacements), key=len, reverse=True):
        sanitized = sanitized.replace(replacement, "<guarded-path>")
    sanitized = re.sub(r'"[A-Za-z]:\\[^\"]+"', '"<local-path>"', sanitized)
    sanitized = re.sub(r"(?i)\b[A-Z]:\\[^\s]+", "<local-path>", sanitized)
    sanitized = re.sub(r"https?://[^\s\"]+", "<remote-url>", sanitized, flags=re.IGNORECASE)
    return sanitized


def _owned_process_records(
    owned_pids: Iterable[int],
    snapshot: Mapping[int, Mapping[str, Any]],
    replacements: Iterable[Path | str],
) -> list[dict[str, Any]]:
    pids = sorted(set(owned_pids))
    process_details: dict[int, dict[str, str]] = {}
    if os.name == "nt" and pids:
        csv = ",".join(str(pid) for pid in pids)
        script = (
            f"$ids=@({csv}); Get-CimInstance Win32_Process | "
            "Where-Object { $ids -contains [int]$_.ProcessId } | "
            "Select-Object ProcessId,CommandLine,CreationDate | ConvertTo-Json -Depth 3 -Compress"
        )
        completed = subprocess.run(
            [_powershell_executable(), "-NoLogo", "-NoProfile", "-NonInteractive", "-Command", script],
            check=False,
            capture_output=True,
            text=True,
            timeout=20,
        )
        if completed.returncode == 0 and completed.stdout.strip():
            payload = json.loads(completed.stdout)
            for row in payload if isinstance(payload, list) else [payload]:
                process_details[int(row["ProcessId"])] = {
                    "command_line": row.get("CommandLine") or "",
                    "start_time": str(row.get("CreationDate") or "unavailable"),
                }
    return [
        {
            "pid": pid,
            "parent_pid": int(snapshot.get(pid, {}).get("parent_pid", -1)),
            "executable": _basename(str(snapshot.get(pid, {}).get("executable", "unknown"))),
            "command_line_sanitized": _sanitize_command_line(
                process_details.get(pid, {}).get("command_line"), replacements
            ),
            "start_time": process_details.get(pid, {}).get("start_time", "unavailable"),
            "project_owned": True,
        }
        for pid in pids
    ]


def _terminate_owned_pids(pids: Iterable[int], baseline_pids: set[int]) -> None:
    if os.name != "nt":
        return
    kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
    kernel32.OpenProcess.argtypes = (wintypes.DWORD, wintypes.BOOL, wintypes.DWORD)
    kernel32.OpenProcess.restype = wintypes.HANDLE
    kernel32.TerminateProcess.argtypes = (wintypes.HANDLE, wintypes.UINT)
    kernel32.TerminateProcess.restype = wintypes.BOOL
    kernel32.CloseHandle.argtypes = (wintypes.HANDLE,)
    kernel32.CloseHandle.restype = wintypes.BOOL
    for pid in sorted(set(pids), reverse=True):
        if pid in baseline_pids or pid == os.getpid():
            continue
        handle = kernel32.OpenProcess(0x0001, False, pid)
        if handle:
            try:
                kernel32.TerminateProcess(handle, 1)
            finally:
                kernel32.CloseHandle(handle)


def guarded_browser_inspection(
    *,
    browser_path: Path,
    target_url: str,
    diagnostics_directory: Path,
    audio_helper_path: Path,
    require_media: bool = False,
) -> dict[str, Any]:
    resolve_audio_policy()
    parsed_target = urlparse(target_url)
    if parsed_target.scheme not in {"about", "data", "file", "http", "https"}:
        raise GuardRuntimeError("unsupported inspection target scheme")
    diagnostics_directory.mkdir(parents=True, exist_ok=True)
    baseline = process_snapshot()
    baseline_pids = set(baseline)
    process: subprocess.Popen[bytes] | None = None
    job: _JobObject | None = None
    websocket: _WebSocket | None = None
    owned_seen: set[int] = set()
    audio_results: list[dict[str, Any]] = []
    dom_state: dict[str, Any] | None = None
    records: list[dict[str, Any]] = []
    cleanup_verified = False
    fail_safe_triggered = False

    with tempfile.TemporaryDirectory(prefix="isolated-browser-profile-", dir=diagnostics_directory) as profile:
        profile_path = Path(profile)
        command = build_browser_command(browser_path, profile_path)
        try:
            creationflags = subprocess.CREATE_NEW_PROCESS_GROUP if os.name == "nt" else 0
            process = subprocess.Popen(
                command,
                stdin=subprocess.DEVNULL,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                creationflags=creationflags,
            )
            job = _JobObject(process)
            websocket = _WebSocket(_wait_for_devtools(profile_path, process))
            target = websocket.command("Target.createTarget", {"url": "about:blank"})
            attached = websocket.command(
                "Target.attachToTarget", {"targetId": target["targetId"], "flatten": True}
            )
            session_id = attached["sessionId"]
            websocket.command("Page.enable", session_id=session_id)
            websocket.command("Runtime.enable", session_id=session_id)
            websocket.command(
                "Page.addScriptToEvaluateOnNewDocument",
                {"source": DOM_MEDIA_GUARD_SCRIPT},
                session_id=session_id,
            )
            current = process_snapshot()
            current_owned = descendant_pids(process.pid, current) - baseline_pids
            owned_seen.update(current_owned)
            initial_audio = inspect_audio_sessions(audio_helper_path, current_owned, mode="mute")
            audio_results.append(initial_audio)
            if initial_audio.get("unmuted_owned_session_count", 0):
                fail_safe_triggered = True
                raise GuardRuntimeError(
                    "owned Core Audio session remained unmuted",
                    error_code="unexpected_audio_output",
                    details={"owned_sessions": initial_audio.get("sessions", [])},
                )
            websocket.command("Page.navigate", {"url": target_url}, session_id=session_id)

            deadline = time.monotonic() + 15
            while time.monotonic() < deadline:
                evaluation = websocket.command(
                    "Runtime.evaluate",
                    {"expression": DOM_STATE_EXPRESSION, "returnByValue": True},
                    session_id=session_id,
                )
                value = evaluation.get("result", {}).get("value")
                if isinstance(value, str):
                    dom_state = json.loads(value)
                    media_ready = not require_media or dom_state.get("mediaCount", 0) >= 1
                    if dom_state.get("readyState") == "complete" and media_ready:
                        break
                time.sleep(0.1)
            if not dom_state or dom_state.get("readyState") != "complete":
                raise GuardRuntimeError("inspection target did not reach a verifiable DOM state")
            if require_media and dom_state.get("mediaCount", 0) < 1:
                raise GuardRuntimeError("required media element was not observed")
            required_dom = {
                "allMuted": True,
                "allVolumeZero": True,
                "allAutoplayFalse": True,
                "allPaused": True,
                "observerActive": True,
                "policy": "silent",
            }
            if any(dom_state.get(key) != expected for key, expected in required_dom.items()):
                fail_safe_triggered = True
                raise GuardRuntimeError("DOM silent-media enforcement failed")
            current = process_snapshot()
            owned_seen.update(descendant_pids(process.pid, current) - baseline_pids)
            records = _owned_process_records(
                owned_seen,
                current,
                (browser_path, profile_path, target_url),
            )
            for _ in range(2):
                final_audio = inspect_audio_sessions(audio_helper_path, owned_seen, mode="mute")
                audio_results.append(final_audio)
                if final_audio.get("unmuted_owned_session_count", 0):
                    fail_safe_triggered = True
                    raise GuardRuntimeError(
                        "final owned Core Audio session verification failed",
                        error_code="unexpected_audio_output",
                        details={
                            "owned_sessions": final_audio.get("sessions", []),
                            "owned_processes": records,
                        },
                    )
                time.sleep(0.1)
        finally:
            if websocket is not None:
                try:
                    websocket.command("Browser.close")
                except (OSError, GuardRuntimeError):
                    pass
                try:
                    websocket.close()
                except OSError:
                    pass
            if process is not None:
                try:
                    process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    pass
            if job is not None:
                job.close()
            time.sleep(0.2)
            current = process_snapshot()
            remaining = owned_seen & set(current)
            if remaining:
                _terminate_owned_pids(remaining, baseline_pids)
                time.sleep(0.2)
                current = process_snapshot()
                remaining = owned_seen & set(current)
            cleanup_verified = not remaining

    if not cleanup_verified:
        raise GuardRuntimeError("guarded browser descendants remained after cleanup")
    return {
        "schema": "nlmytgen.silent_media_runtime_result.v1",
        "status": "passed",
        "audio_policy": DEFAULT_AUDIO_POLICY,
        "target_category": "local_fixture" if parsed_target.scheme == "file" else "nonlocal_or_inline",
        "browser": {
            "executable": _basename(browser_path),
            "flags": list(BROWSER_FLAGS),
            "isolated_temporary_profile": True,
            "profile_removed": True,
            "remote_debugging_loopback_only": True,
        },
        "dom": dom_state,
        "process_ownership": {
            "baseline_process_count": len(baseline_pids),
            "owned_process_count": len(owned_seen),
            "owned_processes": records,
            "parent_child_containment_verified": bool(owned_seen),
            "cleanup_verified": cleanup_verified,
            "remaining_owned_process_count": 0,
            "pre_existing_process_operation": False,
        },
        "core_audio": {
            "supported": all(result.get("supported") for result in audio_results),
            "checks": len(audio_results),
            "owned_sessions_observed": max(
                (int(result.get("owned_session_count", 0)) for result in audio_results), default=0
            ),
            "unmuted_owned_session_count": 0,
            "sessions": audio_results[-1].get("sessions", []) if audio_results else [],
            "unowned_session_mutation": False,
            "master_volume_operation": False,
        },
        "fail_safe": {
            "triggered": fail_safe_triggered,
            "behavior": "terminate_guarded_project_owned_tree_only",
        },
        "explicit_audio_opt_in_available": False,
        "acoustic_measurement_claimed": False,
    }


def _write_json(path: Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def _cli_smoke(args: argparse.Namespace) -> int:
    diagnostics = args.diagnostics.resolve()
    fixture = create_zero_amplitude_fixture(diagnostics)
    result = guarded_browser_inspection(
        browser_path=args.browser.resolve(),
        target_url=fixture["html_path"].resolve().as_uri(),
        diagnostics_directory=diagnostics,
        audio_helper_path=args.audio_helper.resolve(),
        require_media=True,
    )
    result["fixture"] = {
        key: value for key, value in fixture.items() if key not in {"wav_path", "html_path"}
    }
    _write_json(args.result.resolve(), result)
    print(json.dumps({"status": result["status"], "result": args.result.name}, sort_keys=True))
    return 0


def _cli_inspect(args: argparse.Namespace) -> int:
    result = guarded_browser_inspection(
        browser_path=args.browser.resolve(),
        target_url=args.target,
        diagnostics_directory=args.diagnostics.resolve(),
        audio_helper_path=args.audio_helper.resolve(),
        require_media=args.require_media,
    )
    _write_json(args.result.resolve(), result)
    print(json.dumps({"status": result["status"], "result": args.result.name}, sort_keys=True))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    smoke = subparsers.add_parser("smoke", help="run an inaudible local guarded-browser smoke")
    smoke.add_argument("--browser", type=Path, default=None)
    smoke.add_argument("--diagnostics", type=Path, required=True)
    smoke.add_argument("--audio-helper", type=Path, required=True)
    smoke.add_argument("--result", type=Path, required=True)
    smoke.set_defaults(handler=_cli_smoke)
    inspect = subparsers.add_parser("inspect", help="inspect one target through the silent browser guard")
    inspect.add_argument("--browser", type=Path, default=None)
    inspect.add_argument("--target", required=True)
    inspect.add_argument("--diagnostics", type=Path, required=True)
    inspect.add_argument("--audio-helper", type=Path, required=True)
    inspect.add_argument("--result", type=Path, required=True)
    inspect.add_argument("--require-media", action="store_true")
    inspect.set_defaults(handler=_cli_inspect)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if getattr(args, "browser", None) is None:
        args.browser = find_browser()
    try:
        return int(args.handler(args))
    except (GuardRuntimeError, SilentPolicyError) as exc:
        error_code = getattr(exc, "error_code", "silent_policy_rejected")
        details = getattr(exc, "details", {})
        result_path = getattr(args, "result", None)
        if isinstance(result_path, Path):
            _write_json(
                result_path.resolve(),
                {
                    "schema": "nlmytgen.silent_media_runtime_result.v1",
                    "status": "failed",
                    "stop_condition": error_code,
                    "error": str(exc),
                    "diagnostics": details,
                    "cleanup_attempted_for_project_owned_tree_only": True,
                    "pre_existing_process_operation": False,
                    "master_volume_operation": False,
                    "explicit_audio_opt_in_available": False,
                },
            )
        raise


if __name__ == "__main__":
    raise SystemExit(main())
