# Acceptance Checklist

Use this checklist before treating the package as ready for a customer or paid
pilot review.

## CSV Import

- [ ] `outputs/transcript_sample_ymm4.csv` exists.
- [ ] The CSV has two columns: YMM4 character name and utterance text.
- [ ] The CSV has no header row.
- [ ] The CSV can be selected in YMM4's script import flow.
- [ ] Imported rows appear in the expected order.

## Speaker Map

- [ ] `Host1` maps to `れいむ`.
- [ ] `Host2` maps to `まりさ`.
- [ ] Unknown speakers are not silently accepted.
- [ ] The customer-provided speaker names are reflected before delivery.

## Cue Packet

- [ ] `outputs/cue_packet.md` exists.
- [ ] The cue packet separates production cues from transcript text.
- [ ] Background/support-material suggestions are usable as manual prep notes.
- [ ] Cue density matches the customer expectation for the pilot.

## Diagram Packet

- [ ] `outputs/diagram_packet.md` exists when diagram planning is included.
- [ ] It is treated as a brief, not as a finished diagram asset.
- [ ] Any required human judgement is visible before production starts.

## Readability

- [ ] Subtitle line wrapping is reasonable for a first YMM4 import pass.
- [ ] Speaker continuity is easy to follow.
- [ ] No obvious parse errors, duplicate fragments, or speaker swaps remain.
- [ ] Long customer-specific terms are checked manually.

## Human Review

- [ ] Customer or editor confirms the transcript is the intended source.
- [ ] Customer or editor confirms source rights and publication responsibility.
- [ ] YMM4 final look is accepted manually after import.
