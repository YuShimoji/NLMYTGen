# INT-02e Real URL Operator Smoke Gate

Status: `baseline / in_progress`

INT-02e is not `done`. It stays `baseline / in_progress` until a real URL
operator smoke leaves evidence for every gate below.

## Done Gate

INT-02e can be considered `done` only after all of the following evidence exists:

- actual real URL fetch was performed after rights / terms review was supplied
- `source.wav` readback passed with Python `wave`
- receipt, sidecar, and `material_ledger` readback passed
- `audit-material-ledger` passed
- boundary grep passed
- URL, command summary, stderr digest / tail, and receipt output were scrubbed for
  secrets, tokens, and query parameters

Dry-run, local placeholder input, mocked source data, or a successful plan is not
enough for `done`.

## Pre-Smoke Preconditions

Before the real URL smoke begins, confirm and record:

- target commit hash
- `git status --short` is clean
- `git rev-list --left-right --count HEAD...origin/main` returns `0 0`
- URL and rights / terms review information were provided by the user

If `origin/main` is unavailable or the count is not `0 0`, do not substitute a
different branch silently. Report the mismatch and stop before real fetch.

## Operator Smoke Order

After URL and rights / terms review information are received, run only this
sequence:

1. `fetch-source-audio --mode yt-dlp-audio --dry-run`
2. actual fetch
3. Python `wave` readback for `source.wav`
4. receipt / sidecar / `material_ledger` readback
5. `audit-material-ledger`
6. boundary grep
7. SH-05 preview pack / GUI read-only ingest, if available

## Scrub Rule

Any reported URL, command summary, stderr digest / tail, and receipt data must
scrub:

- secrets
- tokens
- query parameters
- auth headers
- cookies
- local credentials

Prefer host / path-level evidence over full raw URLs when possible.

## Boundary

Passing INT-02e does not authorize expansion into:

- `fetch-source-video`
- GUI fetch button
- STT URL fetch
- cut / concat
- subtitle burn-in
- render / encode
- Publishing / OAuth

Those remain separate gates.
