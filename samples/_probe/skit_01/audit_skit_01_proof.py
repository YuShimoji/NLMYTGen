from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_SOURCE = REPO_ROOT / 'samples/characterAnimSample/haitatsuin_2026-04-12.ymmp'
DEFAULT_PROOF = REPO_ROOT / '_tmp/skit_01_v2_verify.ymmp'
DEFAULT_REGISTRY = REPO_ROOT / 'samples/registry_template/skit_group_registry.template.json'
RUNTIME_STATE = REPO_ROOT / 'docs/runtime-state.md'
VERIFY_DOC = REPO_ROOT / 'docs/verification/skit_01_delivery_dispute_v1_2026-04-19.md'
PROMPT_DOC = REPO_ROOT / 'docs/prompts/G24-skit01-proof-continuation.md'
PREFERRED_PROOF_PATH = '_tmp/skit_01_v2.ymmp'
SURVIVING_PROOF_PATH = '_tmp/skit_01_v2_verify.ymmp'
MANUAL_SAMPLE_PATH = REPO_ROOT / '_tmp/skit_ManualSample_01.ymmp'
GROUP_REMARK_RE = re.compile(r"motion:([^\s]+)")


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding='utf-8-sig'))


def item_type(item: dict) -> str:
    return item.get('$type', '').split(',')[0].split('.')[-1]


def load_group_remarks(path: Path) -> list[str]:
    data = load_json(path)
    items = data['Timelines'][0]['Items']
    return [item.get('Remark', '') for item in items if item_type(item) == 'GroupItem' and item.get('Layer') == 9]


def load_motion_segments(path: Path) -> list[dict]:
    data = load_json(path)
    items = data['Timelines'][0]['Items']
    segments = []
    for item in items:
        if item_type(item) != 'GroupItem' or item.get('Layer') != 9:
            continue
        remark = item.get('Remark', '')
        match = GROUP_REMARK_RE.search(remark)
        segments.append(
            {
                'frame': item.get('Frame'),
                'length': item.get('Length'),
                'remark': remark,
                'motion': match.group(1) if match else None,
            }
        )
    return segments


def load_ir_motions(path: Path) -> list[str]:
    data = load_json(path)
    motions = []
    for utterance in data.get('utterances', []):
        motion = utterance.get('motion')
        if motion and motion != 'none':
            motions.append(motion)
    return motions


def read_text(path: Path) -> str:
    if not path.exists():
        return ''
    return path.read_text(encoding='utf-8')


def main() -> int:
    parser = argparse.ArgumentParser(description='Audit skit_01 proof trust using repo-local artifacts only.')
    parser.add_argument('--source', type=Path, default=DEFAULT_SOURCE)
    parser.add_argument('--proof', type=Path, default=DEFAULT_PROOF)
    parser.add_argument('--registry', type=Path, default=DEFAULT_REGISTRY)
    parser.add_argument('--ir', type=Path, default=REPO_ROOT / 'samples/_probe/skit_01/skit_01_ir.json')
    parser.add_argument('--strict', action='store_true', help='Return non-zero when workflow breakage is detected.')
    args = parser.parse_args()

    failures: list[tuple[str, str]] = []
    trusted: list[str] = []

    runtime_text = read_text(RUNTIME_STATE)
    verify_text = read_text(VERIFY_DOC)
    prompt_text = read_text(PROMPT_DOC)

    if MANUAL_SAMPLE_PATH.exists():
        trusted.append(f'manual reference exists: {MANUAL_SAMPLE_PATH.relative_to(REPO_ROOT)}')
    elif '_tmp/skit_ManualSample_01.ymmp' in runtime_text:
        failures.append(
            (
                'REFERENCE_MASTER_MISSING',
                'Manual reference master _tmp/skit_ManualSample_01.ymmp is absent; runtime-state records this as workflow breakage.',
            )
        )

    preferred_path = REPO_ROOT / PREFERRED_PROOF_PATH
    surviving_path = REPO_ROOT / SURVIVING_PROOF_PATH
    mentions_preferred = PREFERRED_PROOF_PATH in verify_text or PREFERRED_PROOF_PATH in prompt_text
    if not preferred_path.exists() and surviving_path.exists() and mentions_preferred:
        failures.append(
            (
                'PROOF_OUTPUT_PATH_DRIFT',
                'Stale path _tmp/skit_01_v2.ymmp remains in repo docs/prompt for drift tracking, while the surviving repo artifact is _tmp/skit_01_v2_verify.ymmp.',
            )
        )

    if not args.source.exists():
        failures.append(('SOURCE_SAMPLE_MISSING', f'Missing source ymmp: {args.source.relative_to(REPO_ROOT)}'))
    else:
        trusted.append(f'source sample exists: {args.source.relative_to(REPO_ROOT)}')

    if not args.proof.exists():
        failures.append(('PROOF_YMMP_MISSING', f'Missing proof ymmp: {args.proof.relative_to(REPO_ROOT)}'))
    else:
        trusted.append(f'proof ymmp exists: {args.proof.relative_to(REPO_ROOT)}')

    if not args.registry.exists():
        failures.append(('REGISTRY_MISSING', f'Missing registry file: {args.registry.relative_to(REPO_ROOT)}'))
    else:
        trusted.append(f'registry exists: {args.registry.relative_to(REPO_ROOT)}')

    if args.ir.exists():
        ir_motions = load_ir_motions(args.ir)
        if ir_motions:
            trusted.append('IR motions: ' + ', '.join(ir_motions))
    else:
        failures.append(('IR_MISSING', f'Missing IR file: {args.ir.relative_to(REPO_ROOT)}'))

    registry = load_json(args.registry) if args.registry.exists() else None
    source_remarks = load_group_remarks(args.source) if args.source.exists() else []
    proof_segments = load_motion_segments(args.proof) if args.proof.exists() else []
    proof_remarks = [segment['remark'] for segment in proof_segments]

    if proof_segments:
        trusted.append(
            'proof group segments: ' + ', '.join(
                f"{segment['motion'] or '?'}@F{segment['frame']}+{segment['length']}" for segment in proof_segments
            )
        )

    if registry is not None:
        expected_remarks = {
            group.get('group_remark')
            for group in registry.get('canonical_groups', {}).values()
            if group.get('group_remark')
        }
        missing_remarks = sorted(
            remark for remark in expected_remarks if remark not in source_remarks and remark not in proof_remarks
        )
        if missing_remarks:
            failures.append(
                (
                    'CANONICAL_GROUP_REMARK_MISSING',
                    'Registry expects canonical group remarks that are absent from source/proof ymmp: ' + ', '.join(missing_remarks),
                )
            )

        registry_notes = registry.get('notes', '')
        if 'Not consumed by CLI yet.' in registry_notes:
            failures.append(
                (
                    'TEMPLATE_RESOLUTION_UNPROVEN',
                    'skit_group registry is still shared metadata only; current proof exercises motion remarks, not exact/fallback/manual-note template resolution.',
                )
            )

    print('Trusted repo-local artifacts')
    for line in trusted:
        print(f'- {line}')

    print('\nWorkflow breakage classes')
    if failures:
        for code, detail in failures:
            print(f'- {code}: {detail}')
    else:
        print('- none')

    print('\nAssistant-owned safer route')
    print('- Compare only source ymmp + proof ymmp + IR + registry; do not ask for a new ManualSample.')
    print('- Treat skit_01 as a mechanical motion proof until repo-resident canonical template evidence exists.')
    print('- Use this audit before promoting skit_01 claims into runtime-state or handoff docs.')

    if args.strict and failures:
        return 2
    return 0


if __name__ == '__main__':
    sys.exit(main())
