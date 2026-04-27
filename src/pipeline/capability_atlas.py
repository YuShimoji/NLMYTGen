from __future__ import annotations

import json
from pathlib import Path
from typing import Any

SCHEMA_VERSION = "1.0"
SUPPORT_LEVELS = frozenset({
    "direct_proven",
    "template_catalog_only",
    "probe_only",
    "unsupported",
})

DEFAULT_EFFECT_CATALOG_PATH = Path("samples/effect_catalog.json")
DEFAULT_TIMELINE_CONTRACT_PATH = Path("samples/timeline_route_contract.json")
DEFAULT_MOTION_LIBRARY_PATH = Path("samples/tachie_motion_map_library.json")
DEFAULT_SKIT_REGISTRY_PATH = Path("samples/registry_template/skit_group_registry.template.json")
DEFAULT_OUTPUT_PATH = Path("samples/_generated/capability_atlas.json")
EXPORTED_SKIT_TEMPLATE_INTENTS = frozenset({
    "deny_oneshot",
    "enter_from_left",
    "exit_left",
    "nod",
    "surprise_oneshot",
})


def _read_json(path: Path) -> dict[str, Any]:
    with open(path, encoding="utf-8-sig") as f:
        data = json.load(f)
    if not isinstance(data, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return data


def load_default_artifacts(project_root: Path | None = None) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]:
    root = project_root or Path.cwd()
    return (
        _read_json(root / DEFAULT_EFFECT_CATALOG_PATH),
        _read_json(root / DEFAULT_TIMELINE_CONTRACT_PATH),
        _read_json(root / DEFAULT_MOTION_LIBRARY_PATH),
        _read_json(root / DEFAULT_SKIT_REGISTRY_PATH),
    )


def build_default_capability_atlas(project_root: Path | None = None) -> dict[str, Any]:
    return build_capability_atlas(*load_default_artifacts(project_root))


def build_capability_atlas(
    effect_catalog: dict[str, Any],
    timeline_contract: dict[str, Any],
    motion_library: dict[str, Any],
    skit_registry: dict[str, Any],
) -> dict[str, Any]:
    entries = []
    entries.extend(_static_entries())
    entries.extend(_skit_template_entries(skit_registry))
    entries.extend(_raw_effect_entries(effect_catalog, timeline_contract, motion_library))
    atlas = {
        "schema_version": SCHEMA_VERSION,
        "entries": sorted(entries, key=lambda entry: entry["expression_id"]),
    }
    _validate_atlas(atlas)
    return atlas


def write_capability_atlas(atlas: dict[str, Any], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(atlas, f, ensure_ascii=False, indent=2)
        f.write("\n")


def _evidence(path: str, reason: str) -> dict[str, str]:
    return {"path": path, "reason": reason}


def _entry(
    expression_id: str,
    scope: str,
    preferred_route: str,
    support_level: str,
    evidence: list[dict[str, str]],
    manual_checks: list[str],
    limitations: list[str],
) -> dict[str, Any]:
    return {
        "expression_id": expression_id,
        "scope": scope,
        "preferred_route": preferred_route,
        "support_level": support_level,
        "evidence": evidence,
        "manual_checks": manual_checks,
        "limitations": limitations,
    }


def _static_entries() -> list[dict[str, Any]]:
    return [
        _entry(
            "bg_layer.bg",
            "bg_layer",
            "IR bg -> bg_map -> patch-ymmp",
            "direct_proven",
            [
                _evidence("docs/PRODUCTION_IR_CAPABILITY_MATRIX.md", "bg is a patch-time route in the capability matrix"),
                _evidence("docs/verification/G15-micro-bg-patch.md", "micro bg patch is the proof packet for Layer 0 background writes"),
            ],
            [
                "Confirm the chosen background still matches the narrative beat in YMM4",
            ],
            [
                "Background asset choice remains a registry/operator judgement",
            ],
        ),
        _entry(
            "bg_layer.bg_anim",
            "bg_layer",
            "IR bg_anim -> timeline contract route -> patch-ymmp",
            "direct_proven",
            [
                _evidence("samples/timeline_route_contract.json", "ImageItem X/Y/Zoom and ImageItem.VideoEffects routes are measured in repo-local contract profiles"),
                _evidence("docs/verification/G12-timeline-route-measurement.md", "bg_anim route measurement packet fixes the repo-local write routes"),
                _evidence("docs/PRODUCTION_IR_CAPABILITY_MATRIX.md", "bg_anim has two approved patch paths: keyframes and VideoEffects"),
            ],
            [
                "Check whether the pan/zoom strength is visually comfortable in the target scene",
            ],
            [
                "VideoEffects route depends on a measured profile; do not assume every ymmp corpus has the same background route",
            ],
        ),
        _entry(
            "overlay_se.overlay",
            "overlay_se",
            "IR overlay -> overlay_map -> timing anchor -> patch-ymmp",
            "direct_proven",
            [
                _evidence("docs/verification/G13-overlay-se-insertion-packet.md", "overlay insertion packet fixes deterministic label/timing insertion"),
                _evidence("docs/PRODUCTION_IR_CAPABILITY_MATRIX.md", "overlay is listed as a yes/write path in patch_ymmp"),
            ],
            [
                "Confirm density, overlap, and final screen readability in YMM4",
            ],
            [
                "Overlay remains registry and timing-anchor dependent",
            ],
        ),
        _entry(
            "overlay_se.se",
            "overlay_se",
            "IR se -> se_map -> timing anchor -> patch-ymmp",
            "direct_proven",
            [
                _evidence("docs/verification/G18-se-audioitem-implementation.md", "SE AudioItem insertion is implemented and documented"),
                _evidence("docs/PRODUCTION_IR_CAPABILITY_MATRIX.md", "se is a conditional write path with mechanical failure classes"),
            ],
            [
                "Check timing, loudness, and whether the SE is worth keeping in the final edit",
            ],
            [
                "SE still requires registry resolution and timing-anchor coverage",
            ],
        ),
        _entry(
            "skit_group.canonical_anchor",
            "skit_group",
            "canonical ymmp -> audit-skit-group",
            "direct_proven",
            [
                _evidence("samples/canonical.ymmp", "Canonical skit_group artifact contains GroupItem remark 'haitatsuin_delivery_main' on Layer 9 with ImageItem-only children"),
                _evidence("docs/verification/G24-canonical-anchor-adoption-2026-04-20.md", "Canonical adoption packet records audit-skit-group success against the canonical corpus"),
            ],
            [
                "Confirm the left-facing base pose and center-relative composition still match the intended default actor stance",
            ],
            [
                "Derived native template assets are still pending; this proves the anchor, not the full template set",
            ],
        ),
        _entry(
            "skit_group.group_motion",
            "skit_group",
            "IR group_motion + group_target -> group_motion_map -> GroupItem.X/Y/Zoom",
            "direct_proven",
            [
                _evidence("samples/timeline_route_contract.json", "group_motion_only profile fixes GroupItem.X/Y/Zoom as the measured route"),
                _evidence("docs/verification/G20-group-and-asset-automation-comprehensive-review-2026-04.md", "G-20 review fixes group_motion as geometry helper, not the acting mainline"),
                _evidence("docs/PRODUCTION_IR_CAPABILITY_MATRIX.md", "group_motion is documented as a yes/write path with failure classes"),
            ],
            [
                "Check whether the geometry nudge preserves scene composition and relative alignment",
            ],
            [
                "Use only as a geometry helper; do not replace canonical skit templates with repeated group_motion tweaks",
            ],
        ),
        _entry(
            "skit_group.motion_target",
            "skit_group",
            "IR motion + motion_target -> tachie_motion_map_library -> layer-specific VideoEffects",
            "direct_proven",
            [
                _evidence("docs/verification/B2-haitatsuin-motion-groupitem-2026-04-19.md", "motion_target layer:9 proof shows GroupItem-level VideoEffects writes in repo-local corpus"),
                _evidence("docs/MOTION_PRESET_LIBRARY_SPEC.md", "motion library v2 documents why animation params are needed for ImageItem/GroupItem targets"),
                _evidence("docs/PRODUCTION_IR_CAPABILITY_MATRIX.md", "motion_target is documented as a direct write path to ImageItem/GroupItem"),
            ],
            [
                "Confirm the whole actor still moves as intended and does not break face/body alignment",
            ],
            [
                "Supplementary route only; skit_group acting should start from template intent, not from raw motion_target edits",
            ],
        ),
        _entry(
            "speaker_tachie.face",
            "speaker_tachie",
            "IR face -> face_map/palette -> patch-ymmp",
            "direct_proven",
            [
                _evidence("docs/FEATURE_REGISTRY.md", "G-06 records face patch as done and production proven"),
                _evidence("docs/verification/CHABANGEKI-E2E-PROOF-2026-04-13.md", "face changes are included in the tea-time E2E proof"),
            ],
            [
                "Confirm the chosen label still reads correctly as a human expression in YMM4",
            ],
            [
                "Label naming remains human-authored; patch only resolves existing registry labels",
            ],
        ),
        _entry(
            "speaker_tachie.idle_face",
            "speaker_tachie",
            "IR idle_face -> face_map/palette -> patch-ymmp",
            "direct_proven",
            [
                _evidence("docs/FEATURE_REGISTRY.md", "G-07 records idle_face as done"),
                _evidence("docs/verification/CHABANGEKI-E2E-PROOF-2026-04-13.md", "idle_face insertion is part of the tea-time E2E proof"),
            ],
            [
                "Check that non-speaker idle faces do not feel distracting in context",
            ],
            [
                "Idle face coverage still depends on palette completeness",
            ],
        ),
        _entry(
            "speaker_tachie.motion",
            "speaker_tachie",
            "IR motion -> tachie_motion_map_library or motion_map -> patch-ymmp",
            "direct_proven",
            [
                _evidence("samples/timeline_route_contract.json", "motion routes are measured for TachieItem.VideoEffects in the repo-local contract"),
                _evidence("docs/MOTION_PRESET_LIBRARY_SPEC.md", "motion library is the approved label-to-effect path for motion"),
                _evidence("docs/verification/G17-motion-adapter-packet.md", "motion write adapter is already proved for measured routes"),
            ],
            [
                "Check intensity, repetition, and whether the motion steals focus from the line itself",
            ],
            [
                "This route is for speaker_tachie; do not widen it into the skit_group mainline",
            ],
        ),
        _entry(
            "speaker_tachie.slot",
            "speaker_tachie",
            "IR slot -> slot_map -> patch-ymmp",
            "direct_proven",
            [
                _evidence("docs/FEATURE_REGISTRY.md", "G-11 records slot patch as completed"),
                _evidence("docs/verification/CHABANGEKI-E2E-PROOF-2026-04-13.md", "slot changes are included in the tea-time E2E proof"),
            ],
            [
                "Check final left/right staging and whether the scene stays readable",
            ],
            [
                "Slot positions remain registry-driven, not freeform creative layout synthesis",
            ],
        ),
        _entry(
            "transition.fade",
            "transition",
            "IR transition=fade -> measured fade-family route -> patch-ymmp",
            "direct_proven",
            [
                _evidence("samples/timeline_route_contract.json", "fade-family transition keys are part of the measured contract"),
                _evidence("docs/verification/G12-timeline-route-measurement.md", "fade-family transition is the confirmed route family in repo-local corpus"),
                _evidence("docs/PRODUCTION_IR_CAPABILITY_MATRIX.md", "transition is patchable only for none/fade in the current adapter"),
            ],
            [
                "Check whether the fade timing feels natural for the scene cut",
            ],
            [
                "Only fade is a production route today; other transition families remain outside the supported path",
            ],
        ),
        _entry(
            "transition.non_fade",
            "transition",
            "Do not write directly from IR; redesign with fade or manual YMM4 authoring",
            "unsupported",
            [
                _evidence("docs/verification/G12-timeline-route-measurement.md", "non-fade/template-backed transition families remain unmeasured in repo-local corpus"),
                _evidence("docs/PRODUCTION_IR_CAPABILITY_MATRIX.md", "validate-ir treats non-fade transition labels as unknown for patch-time application"),
            ],
            [
                "If a non-fade transition is still desired, re-measure the route and document it before implementation",
            ],
            [
                "Unsupported in the current production adapter",
            ],
        ),
        _entry(
            "ymmp.direct_effect_from_atom",
            "ir_junction",
            "Do not derive IR directly from raw effect names; choose a higher-level route first",
            "unsupported",
            [
                _evidence("docs/TIMELINE_EFFECT_CAPABILITY_ATLAS.md", "Capability Atlas explicitly treats effect atoms as a dictionary, not as a primary IR contract"),
                _evidence("samples/EFFECT_CATALOG_USAGE.md", "effect_catalog is described as a pick-up source for registries, not a production IR schema"),
            ],
            [
                "Translate the intent into motion/template/bg_anim/overlay/se before patching",
            ],
            [
                "Raw effect names are not a recommended production entrypoint",
            ],
        ),
    ]


def _skit_template_entries(skit_registry: dict[str, Any]) -> list[dict[str, Any]]:
    templates = skit_registry.get("templates", {})
    entries = []
    for template_name, template in templates.items():
        if not isinstance(template, dict):
            continue
        if template.get("target_type") != "skit_group":
            continue
        intent = template.get("intent") or template_name
        manual_checks = [str(value) for value in template.get("manual_checks", [])]
        support_level = "template_catalog_only"
        evidence = [
            _evidence("samples/registry_template/skit_group_registry.template.json", f"Registry template defines skit intent '{intent}'"),
            _evidence("docs/SKIT_GROUP_TEMPLATE_SPEC.md", "Skit group spec fixes template-first as the mainline"),
        ]
        limitations = []
        if intent in EXPORTED_SKIT_TEMPLATE_INTENTS:
            support_level = "direct_proven"
            evidence.extend([
                _evidence("docs/verification/P02-production-adoption-proof.md", "Manual acceptance, production adoption proof, and standalone export sync are recorded here"),
                _evidence("samples/canonical.ymmp", "Canonical anchor plus skit registry resolves the v1 template set as exact in audit-skit-group"),
                _evidence("samples/haitatsuin_2026-04-12_g24_proof.ymmp", "Repo-tracked proof sample stores exported native GroupItem snippets for completed v1 intents"),
            ])
            limitations.extend([
                "Promotion is limited to exported skit intents only; future skit intents stay template_catalog_only until their own export/proof is synced",
                "Target ymmp still needs a compatible skit_group actor setup and preflight should be run before production use",
            ])
        else:
            evidence.append(
                _evidence("docs/verification/G24-canonical-anchor-adoption-2026-04-20.md", "Canonical anchor is repo-resident, but this intent is still awaiting standalone native template asset proof"),
            )
            limitations.extend([
                "Current repo evidence proves canonical anchor existence plus preflight classification, but not a full repo-resident derived native template asset set for this intent",
                "Run audit-skit-group before treating this intent as production-ready template resolution",
            ])
        fallback = template.get("fallback")
        if fallback:
            limitations.append(f"Per-template fallback note exists ({fallback}), but preflight resolution uses top-level intent_fallbacks first")
        entries.append(
            _entry(
                f"skit_group.intent.{intent}",
                "skit_group",
                "template intent -> skit_group_registry -> audit-skit-group",
                support_level,
                evidence,
                manual_checks,
                limitations,
            )
        )
    return entries


def _raw_effect_entries(
    effect_catalog: dict[str, Any],
    timeline_contract: dict[str, Any],
    motion_library: dict[str, Any],
) -> list[dict[str, Any]]:
    motion_names = set(motion_library.get("motions", {}).keys())
    transition_routes = set()
    for profile in timeline_contract.get("profiles", {}).values():
        if not isinstance(profile, dict):
            continue
        for route_name in ("required_routes", "optional_routes"):
            routes = profile.get(route_name, {})
            if isinstance(routes, dict):
                transition_routes.update(routes.get("transition", []))

    entries = []
    for effect_name, effect in effect_catalog.get("effects", {}).items():
        if not isinstance(effect, dict):
            continue
        limitations = [
            "Raw effect atom only; choose a higher-level IR route before production use",
        ]
        if effect.get("is_community"):
            limitations.append("Requires YukkuriMovieMaker.Plugin.Community in the target environment")
        if effect_name in motion_names:
            limitations.append("A similarly named motion exists in tachie_motion_map_library, but the atom itself is still not the IR entrypoint")
        if effect.get("$type") in transition_routes:
            limitations.append("Route measurement alone does not promote this atom into a supported transition contract")
        entries.append(
            _entry(
                f"effect_atom.{effect_name}",
                "effect_catalog",
                "Use as a registry pick-up source only after choosing motion/template/bg_anim/overlay/se",
                "probe_only",
                [
                    _evidence("samples/effect_catalog.json", f"Effect catalog contains raw effect atom '{effect_name}'"),
                    _evidence("samples/EFFECT_CATALOG_USAGE.md", "effect_catalog usage note treats effect names as registry/source material"),
                ],
                [
                    "Promote to a higher-level route before relying on it in a production script",
                ],
                limitations,
            )
        )
    return entries


def _validate_atlas(atlas: dict[str, Any]) -> None:
    if atlas.get("schema_version") != SCHEMA_VERSION:
        raise ValueError("Unexpected atlas schema version")
    entries = atlas.get("entries")
    if not isinstance(entries, list):
        raise ValueError("Atlas entries must be a list")
    seen: set[str] = set()
    for entry in entries:
        expression_id = entry.get("expression_id")
        if not isinstance(expression_id, str) or not expression_id:
            raise ValueError("Each atlas entry must have a non-empty expression_id")
        if expression_id in seen:
            raise ValueError(f"Duplicate atlas expression_id: {expression_id}")
        seen.add(expression_id)
        support_level = entry.get("support_level")
        if support_level not in SUPPORT_LEVELS:
            raise ValueError(f"Unexpected support_level: {support_level}")
        for field in ("scope", "preferred_route"):
            if not isinstance(entry.get(field), str) or not entry[field]:
                raise ValueError(f"Atlas entry {expression_id} has invalid {field}")
        for field in ("manual_checks", "limitations", "evidence"):
            if not isinstance(entry.get(field), list):
                raise ValueError(f"Atlas entry {expression_id} must have list field {field}")
        for ev in entry["evidence"]:
            if not isinstance(ev, dict) or set(ev.keys()) != {"path", "reason"}:
                raise ValueError(f"Atlas entry {expression_id} has invalid evidence payload")
