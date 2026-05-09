# Real Estate DX Overlay/Card Design Review Memo

Status: reviewer-facing design memo for `overlay_only_compact_review`

This memo replaces the earlier grading-style review map. Its purpose is not to
ask the reviewer for `OK / NG` or segment-by-segment approval. Its purpose is to
make the design reasoning inspectable: what the overlay is trying to do, which
alternatives were rejected, where the assumptions are weak, and what kind of
feedback would change the next artifact.

## Current Gate

| item | current state |
|---|---|
| validator result | `status=blocked`, `errors=[]` |
| allowed_next_actions | `[overlay_only_compact_review]` |
| forbidden_next_actions | `[cast_motion_ir, ymm4_creative_acceptance, production_timing]` |
| remaining blockers | `ASSET_BLOCKED_REAL_ESTATE_CAST_TEMPLATES_MISSING`; `ASSET_BLOCKED_REAL_ESTATE_PROPS_MISSING` |
| generated preview | `samples/_probe/g24/real_estate_dx_overlay_only_compact_review.html` |
| readback proof | `status=passed`, `segments=11`, `placeholder_items_rendered=24`, `ShapeItem=24` |
| creative status | not creative acceptance |

Practical meaning: the compact review can be used to inspect overlay/card
direction, but it cannot be treated as cast motion IR, production timing, or a
YMM4 creative-quality result.

## Why This Memo Exists

| previous failure | concrete fix here | why it matters |
|---|---|---|
| The preview looked like a final answer dropped onto the table. | Each segment now shows purpose, alternatives, chosen rationale, weak assumptions, and what feedback would change. | The reviewer can challenge the decision process instead of only reacting to a rendered surface. |
| JSON/readback proof was too close to internal wiring. | Machine artifacts are listed only as proof of generation and boundaries. | The reviewer is not asked to infer product judgement from raw data. |
| The previous three-label segment scoring was too coarse. | The memo asks for discomfort, missing context, priority, and suspected wrong assumptions. | Useful critique can be natural language and does not need to fit a scoring rubric. |
| The HTML surface is scroll-heavy. | The index table gives a whole-lane scan before segment details. | The reviewer can decide where to spend attention instead of reading everything linearly. |
| Alternatives risked looking like strawmen. | Alternatives are named with their real merit and the reason they are not current. | A rejected plan can still remain useful later without becoming fake contrast. |

## How To Review

Do not review the raw JSON unless you want to audit the machine wiring. Do not
judge this as final YMM4 staging. Review the design memo first, then open the
HTML preview only where the memo raises a visual-density or placement question.

Useful feedback shapes:

- "RE-02 overuses the door metaphor; make REINS PC the main idea and demote the VIP-club visual."
- "RE-03 needs a more neutral protection/interest balance; the shadow cue may overstate bad intent."
- "RE-07A/B split is useful, but RE-07C/D feel like one AI-risk block and should be recombined."
- "The whole memo still feels like packaging after the fact; show the source-to-card compression rule more explicitly."

Not useful to ask from the reviewer:

- a single gate label as the only answer.
- forced three-label scoring for every row.
- raw readback or JSON interpretation.
- production approval while cast/prop blockers remain.

## Plan Selection Logic

| plan | real merit | why not current | when it may become useful |
|---|---|---|---|
| Dense source-audit cards | Every script claim can be traced visually. | It repeats the raw-data overload problem and makes the preview feel like a spreadsheet. | Later, if a factual/source audit is the bottleneck. |
| One headline per script block | Very fast to scan and easy to present. | It hides the actual judgement: which visual ideas deserve screen space. | Later, if an executive one-pager is needed. |
| Motion/prop-ready skit staging | Closest to the eventual YMM4 scene. | Validator forbids it while cast templates and props are missing. | After real-estate actor templates or accepted proxies exist. |
| Overlay-only compact placeholders | Shows the intended visual claims without pretending assets are ready. | It is still a temporary workbench, not the final GUI kitchen. | Current safe scope because validator allows only `overlay_only_compact_review`. |

Chosen current plan: overlay-only compact placeholders.

Reason: it is the only plan that keeps the blocked validator state honest while
still giving a reviewable design surface. The output should answer "what visual
claims are worth carrying forward?" not "is this production-ready?"

## Source-To-Card Compression Rule

| source input | compression step | overlay/card output | failure if missing |
|---|---|---|---|
| script line range and row-time map | Identify the one causal idea the viewer must retain. | 1-3 visible labels/shapes per segment. | Decorative card or arbitrary line split. |
| scene-bible block | Preserve actor/prop continuity without creating cast motion. | Placeholder role names and screen positions only. | False implication that template motion is ready. |
| script maturity note | Decide whether the beat can stand alone or needs split/reduction. | RE-07 is split into A-E subbeats; other blocks stay compact. | Long block becomes one vague card or too many micro-cards. |
| asset blockers | Mark which cards are placeholders that require future real assets. | `production_asset_required_later=true` remains visible. | Reviewer mistakes placeholder proof for production proof. |

## Lane-Level Density Check

| metric | value | interpretation |
|---|---:|---|
| total compact segments | `11` | 7 source blocks, with RE-07 split into 5 subbeats. |
| placeholder items | `24` | Enough to express causal ideas, but still high enough to watch for mini-slide-deck drift. |
| active visual coverage | `70.0%` | The lane is intentionally not wall-to-wall motion; rest windows stay possible. |
| unexplained empty duration | `0 sec` | Empty gaps are intentional rests, not missing timetable coverage. |
| visual states per min | `0.400178` | Low-tempo background layer, not a narrator reaction track. |

Reviewer concern to raise: if 24 placeholders still feels like presentation
clutter, the next assistant action is reduction, not production staging.

## Whole-Lane Decision Index

| segment | range | intended visual claim | why this granularity | known weak assumption |
|---|---:|---|---|---|
| RE-01 自力検索 | lines `1-12`, `00:00-01:53` | Search freedom plus the first hidden-gate foreshadow. | 3 cards are used because "search", "results", and "still-closed access" are different ideas. | The closed-door foreshadow may be too early or too cute. |
| RE-02 REINS-VIPクラブ | lines `13-24`, `01:53-03:21` | REINS access asymmetry: inside database vs outside portal. | 3 cards keep barrier, inside data, and public partial data separate. | VIP-club metaphor may caricature REINS or crowd the screen. |
| RE-03 保護理由 | lines `25-36`, `03:21-04:36` | Legitimate protection reasons with a shadow of interest conflict. | 2 cards avoid turning the nuance into either pure virtue or pure villainy. | Shadow cue may overstate bad intent if not balanced. |
| RE-04 囲い込み | lines `37-48`, `04:36-05:43` | Route blocking and double-agency structure. | 3 cards show relationship, blocked status, and closed route as separate causes. | May become a legal diagram unless the route is visually simple. |
| RE-05 QR透明化 | lines `49-60`, `05:43-06:48` | Transparency state change. | 2 cards are enough: status board and half-open barrier. | Half-open door may imply the system is more solved than the script says. |
| RE-06 キュレーション | lines `61-82`, `06:48-08:52` | Expert value shifts from hoarding to sorting and disclosing defects. | 3 cards preserve process, defect disclosure, and shortlist outcome. | This is the highest risk for slide-deck clutter before real props exist. |
| RE-07A Z世代/SNS信頼 | lines `83-102`, `08:52-10:54` | Lifestyle shift explains why face-visible SNS trust matters. | 2 cards keep audience condition and trust mechanism separate. | Lifestyle labels can become stereotypes if overemphasized. |
| RE-07B SNSグレーゾーン | lines `103-113`, `10:54-12:10` | SNS trust has license/ad-risk downside. | 1 warning card prevents this from becoming a scandal montage. | Needs source-safe wording; it should warn, not over-accuse. |
| RE-07C 2030年問題/DX | lines `114-129`, `12:10-14:24` | Structural risk plus AI concierge as service shift. | 2 cards bridge macro risk and DX customer experience. | May be two themes; could split if the connection is not readable. |
| RE-07D AI逆説 | lines `130-143`, `14:24-16:20` | Perfect AI match still misses invisible human/legal risk. | 2 cards set up the paradox directly. | Could become "AI bad" unless human-risk card is precise. |
| RE-07E 選び方 | lines `144-152`, `16:20-17:30` | Final criteria for the professional worth choosing. | 1 final criteria card keeps the landing focused. | Three criteria in one card may be too text-heavy. |

## Segment Design Memos

### RE-01 自力検索

| field | memo |
|---|---|
| purpose | Establish the viewer's starting belief: consumers can now search directly, but access is still not fully open. |
| current overlay idea | `スマホ=魔法の鍵`; `物件カード増殖`; `遠景の閉じた扉`. |
| alternatives considered | A single headline card would be cleaner but hides the contradiction. A dense search-UI mock would be more literal but too busy for first review. |
| chosen rationale | Three placeholders separate the three causal ideas: agency, abundance, and a still-hidden gate. |
| weak assumptions | The "magic key" metaphor may feel childish; the closed door may foreshadow REINS before the viewer needs it. |
| useful reviewer signal | Whether the gate foreshadow helps comprehension or should wait until RE-02. |
| assistant action if challenged | Remove/demote the door, or replace it with a subtle REINS sign rather than a physical gate. |

### RE-02 REINS-VIPクラブ

| field | memo |
|---|---|
| purpose | Make information asymmetry visible without turning REINS into a generic villain. |
| current overlay idea | `REINS / VIPクラブ`; `生データDB`; `一般ポータル（一部情報）`. |
| alternatives considered | A pure database UI would be more accurate but less immediately readable. A physical clubhouse visual is readable but may be too caricatured. |
| chosen rationale | The current split uses the door for access, the PC for source data, and the public portal for partial disclosure. |
| weak assumptions | Three visual pieces may crowd the segment; "VIP club" may oversimplify institutional access. |
| useful reviewer signal | Whether the metaphor clarifies access asymmetry or distracts from the REINS explanation. |
| assistant action if challenged | Make the PC/database the primary object and treat the door/VIP language as a smaller boundary marker. |

### RE-03 保護理由

| field | memo |
|---|---|
| purpose | Preserve nuance: there are legitimate reasons for controlled access, but the script also opens the interest-conflict turn. |
| current overlay idea | `プライバシー / リスク / 秩序`; `背後の利益の影`. |
| alternatives considered | A jump/surprise reaction is cheaper but turns the point into narrator reaction. A pure warning card is simpler but loses the legitimate-protection side. |
| chosen rationale | Shields carry the legitimate reasons; shadow carries the ambiguity without needing actor motion. |
| weak assumptions | Shadow may overstate bad faith; shields may look like a moral defense of the existing system if not paired carefully. |
| useful reviewer signal | Whether the balance feels fair or biased. |
| assistant action if challenged | Change shadow to a smaller "利害" tag, or add ordering so protection appears first and shadow appears only after the turn. |

### RE-04 囲い込み

| field | memo |
|---|---|
| purpose | Explain route blocking as a structure, not as an emotional reaction. |
| current overlay idea | `売主 ⇄ 業者 ⇄ 買主`; `商談中`; `他社ルート閉鎖`. |
| alternatives considered | Angry/surprised acting would be more animated but does not explain the mechanism. A legal flowchart is precise but likely too dry. |
| chosen rationale | Relationship cards plus a blocked route show how a transaction path becomes closed. |
| weak assumptions | Arrows and stamps can become a diagram instead of a scene; the seller/buyer distinction must stay readable. |
| useful reviewer signal | Whether this segment should lean scene-like or diagram-like. |
| assistant action if challenged | Collapse to one route board with a single `商談中` state, or split seller/buyer into clearer icons later. |

### RE-05 QR透明化

| field | memo |
|---|---|
| purpose | Show the system state changing from closed access to partial transparency. |
| current overlay idea | `QR / 公開ステータス`; `半分開いた扉`. |
| alternatives considered | A generic DX glow is visually quick but meaningless. A fully open door is stronger but overclaims the script. |
| chosen rationale | Status board gives the mechanism; half-open door gives the state transition. |
| weak assumptions | "Half-open" may still imply the reform is stronger than intended. QR could become a decorative tech token if status text is weak. |
| useful reviewer signal | Whether transparency should be represented as access, auditability, or user confidence. |
| assistant action if challenged | Replace the door with a status-change meter or keep only the board. |

### RE-06 キュレーション

| field | memo |
|---|---|
| purpose | Shift the professional value from gatekeeping to useful selection and defect disclosure. |
| current overlay idea | `候補を整理するテーブル`; `欠点も見せるカード`; `少ないが意味のある候補`. |
| alternatives considered | A large card pile would show abundance but not expertise. A single expert portrait would show authority but not the work performed. |
| chosen rationale | The table/process/outcome chain makes curation visible without cast motion. |
| weak assumptions | Three cards may feel like a mini-slide deck; curator value is hard to show without a real actor template. |
| useful reviewer signal | Whether the shortlist outcome is enough, or whether the sorting process is the more important visual. |
| assistant action if challenged | Reduce to `整理テーブル + 欠点カード`, or split outcome into a later beat if visual density is too high. |

### RE-07A Z世代ライフスタイルとSNS信頼

| field | memo |
|---|---|
| purpose | Explain why the trust mechanism shifts before warning about SNS risk. |
| current overlay idea | `タイパ / 推し活 / TVなし`; `SNSで顔が見える信頼`. |
| alternatives considered | A broad "Z世代" headline is concise but shallow. A detailed lifestyle montage is richer but would overload a setup beat. |
| chosen rationale | One card states the condition shift; one card states the trust mechanism. |
| weak assumptions | Labels can stereotype the audience; the segment may not need all three lifestyle markers. |
| useful reviewer signal | Which lifestyle marker is actually necessary to support the later argument. |
| assistant action if challenged | Reduce lifestyle labels to one representative marker, or move the trust card forward as the main point. |

### RE-07B SNS集客のグレーゾーン

| field | memo |
|---|---|
| purpose | Add the risk turn without making the review surface sensational. |
| current overlay idea | `無免許 / おとり広告リスク`. |
| alternatives considered | A scandal-style montage is vivid but unsafe and distracts. A footnote-style legal card is safe but may be unreadable. |
| chosen rationale | One warning card keeps the risk visible and bounded. |
| weak assumptions | Wording must remain source-safe; the card should warn about risk categories, not accuse a specific actor. |
| useful reviewer signal | Whether the warning is too strong, too weak, or needs factual qualifiers. |
| assistant action if challenged | Reword to `資格確認 / 広告表示リスク` or require a source-backed prop before carrying it forward. |

### RE-07C 2030年問題と攻めのDX

| field | memo |
|---|---|
| purpose | Connect macro property risk with the proposed DX service shift. |
| current overlay idea | `空き家 / ハザード / 相続`; `AIコンシェルジュ`. |
| alternatives considered | A demographic chart would be more analytical but may not connect to service experience. A future-city montage is attractive but vague. |
| chosen rationale | Risk cluster plus AI panel shows why experience design has to deal with complex future constraints. |
| weak assumptions | This may be two segments wearing one label; the relation between 2030 risk and AI concierge must be explicit. |
| useful reviewer signal | Whether to split macro-risk and AI-service into separate review beats. |
| assistant action if challenged | Split RE-07C into `2030 risk context` and `AI concierge response`, or demote one of the two cards. |

### RE-07D AI逆説と見えないリスク

| field | memo |
|---|---|
| purpose | Land the paradox: AI can optimize visible preference while missing human/legal risk. |
| current overlay idea | `AIの100%マッチ物件`; `境界紛争 / 相続 / 感情調整`. |
| alternatives considered | "AI is wrong" would be simple but crude. "Human expert wins" would be reassuring but under-explained. |
| chosen rationale | Pairing a perfect-match card with invisible-risk cards makes the contradiction visible. |
| weak assumptions | The human-risk list may become text-heavy; the AI card must not imply the tool itself is useless. |
| useful reviewer signal | Whether the contrast is clear without becoming anti-AI framing. |
| assistant action if challenged | Rephrase as `AIが拾いやすい条件` vs `人が確認するリスク`, or reduce the risk list. |

### RE-07E 選び方の基準と最後の問い

| field | memo |
|---|---|
| purpose | Convert the long ending into decision criteria the viewer can remember. |
| current overlay idea | `専門的キュレーター / リスク管理者 / 買ってはいけない理由`. |
| alternatives considered | A recap montage would be more cinematic but less decisive. A final question card would be cleaner but may not preserve the criteria. |
| chosen rationale | One final criteria card keeps the landing narrow and reviewable. |
| weak assumptions | Three criteria in one card can be too much; the strongest phrase may be `買ってはいけない理由`. |
| useful reviewer signal | Whether the final card should keep all three criteria or center one decisive phrase. |
| assistant action if challenged | Reduce to `買ってはいけない理由を言える専門家` and move the other criteria into supporting notes. |

## Feedback The Assistant Can Act On

| reviewer signal | assistant next |
|---|---|
| A metaphor feels misleading. | Rewrite that segment's visual claim and update placeholder labels before touching production paths. |
| A segment is too dense. | Reduce or split the overlay/card plan and regenerate only the compact-review surface. |
| An alternative seems stronger. | Add the alternative as the new candidate and explain the adoption tradeoff in this memo. |
| A card needs factual/legal grounding. | Mark it `needs source-backed prop/wording` and keep it out of production staging. |
| The review surface is still hard to judge. | Treat it as report-packaging failure and improve the memo/workbench before asking for another judgement. |
| Many concerns are about missing objects/templates. | Stop segment polishing and build an asset/proxy decision matrix first. |

## Non-Negotiable Boundaries

- This memo is not `cast_motion_ir`.
- This memo is not `ymm4_creative_acceptance`.
- This memo is not `production_timing`.
- JSON/readback files are machine proof, not manager-facing review reports.
- The HTML preview is a visual aid, not the authority for design rationale.
- If the reviewer cannot tell why a card exists from this memo, the memo is
  incomplete even if the generated preview passes readback.
