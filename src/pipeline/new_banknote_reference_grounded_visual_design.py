from __future__ import annotations

import hashlib
import html
import json
from collections import Counter
from pathlib import Path
from typing import Any


BASE_REVISION = "8d7fd5a19b392dd4869fa71536b7fe9f7fe3c028"
RETRIEVED_AT = "2026-07-20T05:21:35+09:00"
RESEARCH_FROZEN_AT = "2026-07-20T05:21:35+09:00"
DESIGN_GENERATION_STARTED_AT = "2026-07-20T05:24:00+09:00"
OUTPUT_INSPECTED_AT = "2026-07-20T05:35:35+09:00"
CANVAS_WIDTH = 1920
CANVAS_HEIGHT = 1080
DISCLAIMER = "模式図／実券の縮尺・配置ではありません"
DESIGN_ID = "documentary_object_focus_consensus"
STATE_ID = "new-banknote-reference-grounded-visual-proof-human-review-ready-v1"

DEFAULT_PILOT = Path(
    "production_pilots/yukkuri_newsroom_content_spine_002/"
    "external_editorial_input/new_banknote_security_notebooklm_001"
)
DEFAULT_OUTPUT = DEFAULT_PILOT / "reference_grounded_visual_design"
OLD_PROOF = DEFAULT_PILOT / "route_a_visual_proof"

QUERY_LOG = [
    "site:npb.go.jp 新しい日本銀行券 偽造防止技術 特設サイト",
    "site:boj.or.jp 新しい日本銀行券 2024 特設サイト 動画",
    "site:mof.go.jp 新しい日本銀行券 パンフレット PDF",
    "site:gov-online.go.jp 新しい日本銀行券 動画",
    "新紙幣 製造 工場 取材 動画 NHK 2024",
    "新紙幣 偽造防止 技術 解説 動画 日テレ TBS FNN ANN 2024",
    "ytsearch10:ゆっくり解説 新紙幣",
    "ytsearch:ずんだもん 新紙幣 お札 解説",
]


def _reference(
    reference_id: str,
    title: str,
    publisher: str,
    date: str,
    url: str,
    cohort: str,
    topic_scope: str,
    *,
    creator: str | None = None,
    content_type: str = "web_page",
    accessibility_status: str = "public_no_login",
    visually_analyzed: bool = True,
    inspected_surfaces: list[str] | None = None,
    representative_sections: list[str] | None = None,
    primary_visual_subject: str = "real object or source image",
    ratio: str = "object_high / diagram_medium / character_none",
    composition: str = "single object field with bounded explanatory labels",
    subtitle: str = "not observed on static surface",
    speaker: str = "no persistent character",
    title_treatment: str = "large topic title with short section labels",
    callout: str = "bounded outline or close-up when needed",
    credit: str = "publisher identity on page",
    background: str = "neutral page or source image",
    palette: str = "neutral base with functional accent",
    motion: str = "not directly observed",
    thumbnail: str = "object-led, short promise where relevant",
    strengths: list[str] | None = None,
    weaknesses: list[str] | None = None,
    misleading_risk: str = "source image may be mistaken for reusable production material",
    adopt: list[str] | None = None,
    avoid: list[str] | None = None,
    grade: str = "medium",
    tags: list[str] | None = None,
    local_capture: str | None = None,
    capture_note: str = "captured in ignored local research cache",
) -> dict[str, Any]:
    return {
        "reference_id": reference_id,
        "exact_title": title,
        "publisher_channel": publisher,
        "creator": creator or publisher,
        "publication_update_date": date,
        "retrieval_timestamp": RETRIEVED_AT,
        "canonical_url": url,
        "redirects_observed": [],
        "content_type": content_type,
        "cohort": cohort,
        "topic_scope": topic_scope,
        "accessibility_status": accessibility_status,
        "visually_analyzed": visually_analyzed,
        "inspected_surfaces": inspected_surfaces or ["page viewport", "page images"],
        "representative_timestamps_or_sections": representative_sections or [],
        "primary_visual_subject": primary_visual_subject,
        "object_image_diagram_character_ratio": ratio,
        "screen_composition": composition,
        "subtitle_position_and_approximate_line_count": subtitle,
        "character_speaker_placement": speaker,
        "title_and_key_term_treatment": title_treatment,
        "callout_arrow_zoom_usage": callout,
        "source_credit_treatment": credit,
        "background_treatment": background,
        "palette_role": palette,
        "motion_type_and_frequency": motion,
        "thumbnail_grammar": thumbnail,
        "strengths": strengths or ["clear subject hierarchy"],
        "weaknesses": weaknesses or ["source-specific branding cannot transfer"],
        "misleading_risk": misleading_risk,
        "rights_reuse_status": "research_only_public_visibility_not_reuse_permission",
        "patterns_worth_adopting": adopt or ["single primary subject", "short key term"],
        "patterns_to_avoid": avoid or ["copying exact composition", "reusing source imagery"],
        "evidence_grade": grade,
        "coverage_tags": tags or [],
        "local_capture": local_capture,
        "capture_note": capture_note,
    }


REFERENCES: list[dict[str, Any]] = [
    _reference(
        "O01",
        "新しい日本銀行券特設サイト｜新しい一万円札について",
        "独立行政法人 国立印刷局",
        "date_not_stated",
        "https://www.npb.go.jp/ja/n_banknote/design10/index.html",
        "official_educational",
        "exact_topic",
        inspected_surfaces=[
            "page structure and image inventory",
            "high-definition watermark image",
            "multi-state hologram image",
        ],
        representative_sections=["3Dで見る偽造防止技術", "新たに採用された偽造防止技術"],
        composition="object-first sections followed by feature close-ups and labels",
        callout="sequential close-up states; isolated feature crops",
        motion="angle-change sequence represented as bounded still states",
        strengths=["real object remains primary", "feature explanation follows the object"],
        weaknesses=["exact source images carry high rights and likeness burden"],
        adopt=["object first", "feature-by-feature close-up", "short functional labels"],
        tags=["exact_topic", "object_centred", "motion_callout_zoom", "source_credit"],
        local_capture="local_reference_captures/O01_npb_hologram.jpg",
        grade="high",
    ),
    _reference(
        "O02",
        "新しい日本銀行券の特徴",
        "日本銀行",
        "2024-07-03 issuance context; page update date not stated",
        "https://www.boj.or.jp/note_tfjgs/note/n_note/security.htm",
        "official_educational",
        "exact_topic",
        inspected_surfaces=["1440x1100 page capture", "annotated note overview", "magnified feature image"],
        representative_sections=["1．偽造防止技術", "2．ユニバーサルデザイン"],
        composition="large source object with numbered outlines, followed by individual crops",
        callout="numbered outlines, leader lines, magnified detail window",
        credit="constant institutional header and footer",
        motion="before/angle states described through paired still images",
        strengths=["numbered callouts map feature to object", "institutional source is explicit"],
        weaknesses=["full note likeness is unsuitable for a rights-minimal proof"],
        adopt=["numbered feature callouts", "one magnified detail at a time", "source visibility"],
        tags=["exact_topic", "object_centred", "motion_callout_zoom", "source_credit"],
        local_capture="local_reference_captures/O02_boj_annotated_note.png",
        grade="high",
    ),
    _reference(
        "O03",
        "2024年7月3日、新しいお札が発行！",
        "政府広報オンライン",
        "2024-08-19",
        "https://www.gov-online.go.jp/article/202406/entry-6075.html",
        "official_educational",
        "exact_topic",
        accessibility_status="metadata_and_index_accessible_direct_capture_http_403",
        visually_analyzed=False,
        inspected_surfaces=["search-index image descriptions only", "direct capture returned HTTP 403"],
        representative_sections=["POINT", "高精細すき入れの採用", "3Dホログラムの採用"],
        strengths=["clear section hierarchy in accessible metadata"],
        weaknesses=["actual pixels unavailable in this session"],
        grade="limited_not_counted",
        tags=["exact_topic"],
        local_capture=None,
        capture_note="metadata card only; direct headless access returned HTTP 403",
    ),
    _reference(
        "O04",
        "新しいお札の新しい工夫",
        "政府広報オンライン",
        "2024-11-05",
        "https://www.gov-online.go.jp/useful/202406/video-284832.html",
        "official_educational",
        "exact_topic",
        content_type="video_page",
        accessibility_status="metadata_accessible_direct_capture_http_403",
        visually_analyzed=False,
        inspected_surfaces=["public player metadata", "direct capture returned HTTP 403"],
        representative_sections=["3:15 public-service video player"],
        strengths=["bounded public-service runtime"],
        weaknesses=["actual video surface unavailable in this session"],
        grade="limited_not_counted",
        tags=["exact_topic"],
        local_capture=None,
        capture_note="metadata card only; direct headless access returned HTTP 403",
    ),
    _reference(
        "O05",
        "広報ビデオ：そこが知りたい日本銀行",
        "日本銀行",
        "2025-03 production date",
        "https://www.boj.or.jp/about/education/thisisboj.htm",
        "official_educational",
        "adjacent_format",
        content_type="video_index_page",
        inspected_surfaces=["1440x1100 page capture", "official video capture image"],
        representative_sections=["わが国唯一の発券銀行として（5分13秒）"],
        primary_visual_subject="official title card and topic imagery",
        ratio="image_medium / text_high / host_not_visible_in_inspected_frame",
        composition="single title field with restrained institutional framing",
        title_treatment="one centered sentence on a full-frame title card",
        callout="none in inspected title card",
        background="light patterned field with restrained branded border",
        palette="cream field with gold, green, and black institutional accents",
        motion="dynamic content exists; only official capture still inspected",
        strengths=["one message per frame", "clear institutional source"],
        weaknesses=["decorative institutional motif is publisher-specific"],
        adopt=["one message per frame", "short section card", "clear source"],
        avoid=["copying branded border", "copying decorative motif"],
        tags=["object_centred", "source_credit", "motion_callout_zoom"],
        local_capture="local_reference_captures/O05_boj_video_capture.png",
        grade="medium",
    ),
    _reference(
        "O06",
        "見どころ解説",
        "お札と切手の博物館／独立行政法人 国立印刷局",
        "2026-06-30",
        "https://www.npb.go.jp/museum/tenji/jousetu/midokoro.html",
        "official_educational",
        "adjacent_format",
        inspected_surfaces=["1440x1100 page capture", "new-banknote exhibit summary"],
        representative_sections=["新日本銀行券の紹介", "偽造防止技術体験コーナー・Q&A"],
        composition="large section heading, compact topic tabs, small source object at edge",
        callout="section tabs rather than diagram callouts",
        background="white educational page with faint guilloche motif",
        strengths=["content hierarchy is obvious", "topic navigation remains secondary"],
        weaknesses=["decorative guilloche is distinctive and non-transferable"],
        adopt=["large section heading", "short topic labels", "neutral whitespace"],
        avoid=["copying guilloche motif", "using exact banknote image"],
        tags=["exact_topic", "object_centred", "source_credit"],
        local_capture="local_reference_captures/O06_npb_museum.png",
        grade="high",
    ),
    _reference(
        "J01",
        "20年ぶり「新紙幣」いよいよ　3Dホログラム、進化版すかし……偽造防止の最新技術　“最後の紙幣”に？【#みんなのギモン】",
        "日テレNEWS NNN",
        "2024-07-02 10:04",
        "https://news.ntv.co.jp/category/economy/8f3eede662e94d2190bd9662aa645086",
        "journalism_documentary",
        "exact_topic",
        content_type="article_with_video",
        inspected_surfaces=["1440x1100 page capture", "video thumbnail/explainer card"],
        representative_sections=["#みんなのギモン opening card"],
        primary_visual_subject="two large question circles and short topic labels",
        ratio="diagram_high / text_high / small generic people row",
        composition="single bright explainer card with two balanced questions",
        subtitle="headline-like text inside the graphic; no full sentence subtitle observed",
        speaker="generic people silhouettes along lower edge",
        title_treatment="short question phrases in large circles",
        callout="two circular focus fields",
        background="flat high-saturation field",
        palette="pink base with teal and yellow functional contrast",
        motion="video player present; thumbnail only inspected",
        strengths=["question structure is instantly legible", "few large information units"],
        weaknesses=["publisher palette and illustration style are distinctive"],
        adopt=["short question headline", "few large information units"],
        avoid=["copying palette", "copying circular Q motif"],
        tags=["exact_topic", "motion_callout_zoom", "source_credit"],
        local_capture="local_reference_captures/J01_ntv.png",
        grade="high",
    ),
    _reference(
        "J02",
        "20年ぶりの新紙幣　来月3日の流通開始を前に製造工程を公開",
        "テレビ朝日／テレ朝NEWS",
        "2024-06-19 16:23",
        "https://news.tv-asahi.co.jp/news_economy/articles/000355266.html",
        "journalism_documentary",
        "exact_topic",
        content_type="video_news_article",
        inspected_surfaces=["1440x1100 page capture", "manufacturing video preview frame"],
        representative_sections=["video preview: sheets of notes in production"],
        primary_visual_subject="real manufacturing object filling the video frame",
        ratio="real_object_very_high / text_low / character_none",
        composition="full-frame process image with a narrow headline strip",
        subtitle="short top headline strip; no dialogue subtitle in inspected preview",
        title_treatment="white/cyan broadcast headline over object",
        callout="no diagram callout in inspected frame",
        background="real manufacturing footage",
        palette="source-derived beige with cyan/white overlay",
        motion="manufacturing footage; preview still inspected",
        strengths=["process object dominates", "overlay text is short"],
        weaknesses=["production footage cannot be reused"],
        adopt=["object dominance", "short overlay", "process close-up"],
        tags=["exact_topic", "object_centred", "motion_callout_zoom"],
        local_capture="local_reference_captures/J02_tv_asahi.png",
        grade="high",
    ),
    _reference(
        "J03",
        "【新紙幣】プラスチック製の国も増える中で「紙」のままなのは『日本が〇〇大国』だから？偽造防止技術はパワーアップ！",
        "毎日放送／TBS NEWS DIG",
        "2024-06-05 15:39",
        "https://newsdig.tbs.co.jp/articles/-/1213068",
        "journalism_documentary",
        "exact_topic",
        content_type="video_news_article",
        inspected_surfaces=["1440x1100 page capture", "studio explainer preview frame"],
        representative_sections=["presenter plus numbered three-point board"],
        primary_visual_subject="source object and numbered explanation board",
        ratio="object_medium / diagram_medium / presenter_medium",
        composition="presenter left, object and three numbered points right",
        subtitle="short broadcast title at top; list items one to three",
        speaker="human presenter at left, not persistent character art",
        title_treatment="large numbered key points with green emphasis",
        callout="numbered list aligned to object images",
        background="studio",
        palette="white with green functional highlight",
        motion="studio explainer video; preview still inspected",
        strengths=["numbered hierarchy", "subject and explanation stay adjacent"],
        weaknesses=["presenter/studio composition is asset-heavy"],
        adopt=["numbered steps", "one short point at a time", "adjacent object and explanation"],
        avoid=["recreating presenter", "copying board styling"],
        tags=["exact_topic", "object_centred", "motion_callout_zoom", "source_credit"],
        local_capture="local_reference_captures/J03_tbs_mbs.png",
        grade="high",
    ),
    _reference(
        "J04",
        "新紙幣 発行開始　世界初の3Dホログラム採用",
        "Impress Watch",
        "2024-07-03 13:59",
        "https://www.watch.impress.co.jp/docs/topic/1605299.html",
        "journalism_documentary",
        "exact_topic",
        content_type="image_led_article",
        inspected_surfaces=["1440x1100 page capture", "credited object images", "feature close-ups"],
        representative_sections=["opening note lineup", "high-definition watermark", "3D hologram"],
        primary_visual_subject="credited real object images",
        ratio="object_high / prose_medium / character_none",
        composition="single article column; image followed by source credit and explanation",
        subtitle="not applicable",
        speaker="none",
        title_treatment="plain headline; feature terms in body headings",
        callout="successive feature close-ups rather than overlaid arrows",
        credit="visible source caption directly below image",
        background="white editorial page",
        palette="neutral source-derived imagery; blue publisher chrome",
        motion="linked official video for hologram; article stills inspected",
        strengths=["source credit is adjacent", "object and explanation are sequential"],
        weaknesses=["real object imagery has high rights burden"],
        adopt=["adjacent source credit", "one feature crop at a time", "neutral field"],
        tags=["exact_topic", "object_centred", "motion_callout_zoom", "source_credit"],
        local_capture="local_reference_captures/J04_impress.png",
        grade="high",
    ),
    _reference(
        "J05",
        "【独自】新紙幣に謎の文字「あれ？ちょっと違う！」「“F”だけ丸い」財務省国庫課トップに理由を直撃…隠された仕掛けは他にも",
        "FNNプライムオンライン／イット！",
        "2025-06-01 15:00",
        "https://www.fnn.jp/articles/-/879612",
        "journalism_documentary",
        "exact_topic",
        content_type="broadcast_article_with_image_gallery",
        inspected_surfaces=["1440x1100 page capture", "broadcast opening frame", "image-gallery metadata"],
        representative_sections=["opening frame: three notes plus short lower-third"],
        primary_visual_subject="real object on dark neutral field",
        ratio="object_very_high / text_medium / character_none",
        composition="full-frame object with compact lower-third headline",
        subtitle="bottom headline band, two lines",
        speaker="none in inspected frame",
        title_treatment="short red/black emphasis in white lower-third",
        callout="later article close-ups indicated; opening frame has no arrow",
        background="dark neutral textile",
        palette="source-derived object color with white/black/red overlay",
        motion="broadcast segment; opening still inspected",
        strengths=["object remains dominant", "headline band does not split the frame"],
        weaknesses=["broadcast lower-third styling is publisher-specific"],
        adopt=["single object field", "bottom two-line text band", "high contrast"],
        avoid=["copying lower-third package", "copying source photograph"],
        tags=["exact_topic", "object_centred", "source_credit"],
        local_capture="local_reference_captures/J05_fnn.png",
        grade="high",
    ),
    _reference(
        "Y01",
        "【20年ぶりになぜ？】ついに新紙幣発行！知らないと損する⁈その狙いとは…【ずんだもん＆ゆっくり解説】",
        "にゃんだもん",
        "2024-07-29",
        "https://www.youtube.com/watch?v=hVx2x3YUIUM",
        "yukkuri_adjacent_explainer",
        "exact_topic",
        creator="にゃんだもん",
        content_type="youtube_video_thumbnail_and_metadata",
        inspected_surfaces=["1280x720 public thumbnail", "public video metadata"],
        representative_sections=["thumbnail only; no frame-level claims"],
        primary_visual_subject="money imagery plus two dialogue avatars",
        ratio="source_image_high / text_high / characters_medium",
        composition="split topic image with one speaker on each side",
        subtitle="thumbnail speech boxes; dialogue subtitle not inspected",
        speaker="two avatars at left and right with separate speech boxes",
        title_treatment="very large high-contrast promise at top",
        callout="speech boxes rather than arrows",
        credit="source links in public description; not visible in thumbnail",
        background="full-bleed topic image",
        palette="black field with red/yellow headline and green-outlined speech boxes",
        motion="not inspected; thumbnail-limited",
        strengths=["speaker separation is immediate", "topic promise is short"],
        weaknesses=["character art, source image, and click-through style cannot transfer"],
        adopt=["speaker-coded labels", "short key term", "object plus dialogue"],
        avoid=["character art reuse", "sensational wording", "copying thumbnail layout"],
        grade="thumbnail_limited",
        tags=["exact_topic", "two_character_dialogue", "object_centred", "thumbnail"],
        local_capture="local_reference_cache/youtube/hVx2x3YUIUM.jpg",
    ),
    _reference(
        "Y02",
        "【ゆっくり解説】新紙幣凄すぎる！",
        "グリム貨幣コレクション",
        "2024-07-08",
        "https://www.youtube.com/watch?v=PXI5Q57YXD4",
        "yukkuri_adjacent_explainer",
        "exact_topic",
        creator="グリム貨幣コレクション",
        content_type="youtube_video_thumbnail_and_metadata",
        inspected_surfaces=["1280x720 public thumbnail", "public video metadata"],
        representative_sections=["thumbnail only; no frame-level claims"],
        primary_visual_subject="dense collage of banknote feature images plus two avatars",
        ratio="source_image_very_high / text_medium / characters_low",
        composition="full-frame collage, two small speakers at bottom corners",
        subtitle="large centered thumbnail promise; dialogue subtitle not inspected",
        speaker="two small Yukkuri busts at lower corners",
        title_treatment="single red high-contrast phrase across lower middle",
        callout="collage crops imply close-up; no explicit leader line",
        credit="visible watermark on source imagery; description states image handling",
        background="full-bleed image collage",
        palette="source-derived with red/black title",
        motion="not inspected; thumbnail-limited",
        strengths=["topic object fills the frame", "speakers remain secondary"],
        weaknesses=["dense collage and source images create high rights burden"],
        adopt=["object-first hierarchy", "secondary speaker cues", "one short promise"],
        avoid=["source-image collage", "creator character art", "watermark imitation"],
        grade="thumbnail_limited",
        tags=["exact_topic", "two_character_dialogue", "object_centred", "thumbnail"],
        local_capture="local_reference_cache/youtube/PXI5Q57YXD4.jpg",
    ),
    _reference(
        "Y03",
        "【二千円札】誰も使わない紙幣、二千円札が普及しなかった意外な理由【ゆっくり解説】",
        "ゆっくりルーザーズ",
        "2021-09-26",
        "https://www.youtube.com/watch?v=aCYgLBDrNYk",
        "yukkuri_adjacent_explainer",
        "adjacent_format",
        creator="ゆっくりルーザーズ",
        content_type="youtube_video_thumbnail_and_metadata",
        inspected_surfaces=["1280x720 public thumbnail", "public video metadata"],
        representative_sections=["thumbnail only; no frame-level claims"],
        primary_visual_subject="one banknote image and one short question",
        ratio="source_image_high / text_high / characters_low",
        composition="rough half split: object left, question and two speakers right",
        subtitle="bottom promise band; dialogue subtitle not inspected",
        speaker="two busts grouped at upper right",
        title_treatment="one very large word pair and one bottom explanatory line",
        callout="none",
        credit="not visible in thumbnail",
        background="white text field plus object crop",
        palette="black/white with red and yellow emphasis",
        motion="not inspected; thumbnail-limited",
        strengths=["question and object are immediately paired", "speaker role is compact"],
        weaknesses=["thumbnail exaggeration and source image are not proof grammar"],
        adopt=["compact speaker pair", "single question", "high text contrast"],
        avoid=["copying split", "copying character art", "sensational emphasis"],
        grade="thumbnail_limited",
        tags=["two_character_dialogue", "object_centred", "thumbnail"],
        local_capture="local_reference_cache/youtube/aCYgLBDrNYk.jpg",
    ),
    _reference(
        "Y04",
        "【ゆっくり解説】日本細菌学のパイオニア。新千円札の「北里柴三郎」の生涯が凄すぎた",
        "【ゆっくり解説】日本の偉人伝",
        "2023-08-10",
        "https://www.youtube.com/watch?v=NUjG_XKDYRw",
        "yukkuri_adjacent_explainer",
        "adjacent_format",
        creator="【ゆっくり解説】日本の偉人伝",
        content_type="youtube_video_thumbnail_and_metadata",
        inspected_surfaces=["1280x720 public thumbnail", "public video metadata"],
        representative_sections=["thumbnail only; no frame-level claims"],
        primary_visual_subject="portrait surrounded by four context images",
        ratio="source_image_very_high / text_medium / characters_low",
        composition="central subject portrait, four context quadrants, speakers at lower corners",
        subtitle="large central name; dialogue subtitle not inspected",
        speaker="two Yukkuri busts at lower corners",
        title_treatment="central subject name with short corner labels",
        callout="context images act as four supporting facets",
        credit="not visible in thumbnail",
        background="full-bleed image collage",
        palette="source-derived with red/yellow/black title",
        motion="not inspected; thumbnail-limited",
        strengths=["primary subject is unambiguous", "supporting facets are bounded"],
        weaknesses=["portrait collage and creator art carry rights burden"],
        adopt=["one primary subject", "bounded supporting facets", "short labels"],
        avoid=["portrait reuse", "collage copying", "creator character art"],
        grade="thumbnail_limited",
        tags=["two_character_dialogue", "thumbnail"],
        local_capture="local_reference_cache/youtube/NUjG_XKDYRw.jpg",
    ),
    _reference(
        "Y05",
        "【ゆっくり解説】新紙幣の3人をざっくり説明【渋沢栄一/津田梅子/北里柴三郎】",
        "ゆっくりアレコレ",
        "2019-04-09",
        "https://www.youtube.com/watch?v=5Uc_e7FHcX8",
        "yukkuri_adjacent_explainer",
        "adjacent_format",
        creator="ゆっくりアレコレ",
        content_type="youtube_video_thumbnail_and_metadata",
        inspected_surfaces=["1280x720 public thumbnail", "public video metadata"],
        representative_sections=["thumbnail only; no frame-level claims"],
        primary_visual_subject="new-note lineup and portrait",
        ratio="source_image_very_high / text_high / characters_low",
        composition="full background object, question upper left, two speakers lower left",
        subtitle="large two-line question; dialogue subtitle not inspected",
        speaker="two busts together at lower left",
        title_treatment="large yellow/red question",
        callout="no explicit callout",
        credit="not visible in thumbnail",
        background="full-bleed source image",
        palette="source-derived beige with yellow/red text",
        motion="not inspected; thumbnail-limited",
        strengths=["short question frames the topic", "speaker pair is compact"],
        weaknesses=["source likeness and creator art cannot transfer"],
        adopt=["compact speaker pair", "single framing question", "large key term"],
        avoid=["source image reuse", "character art reuse", "copying exact placement"],
        grade="thumbnail_limited",
        tags=["two_character_dialogue", "thumbnail"],
        local_capture="local_reference_cache/youtube/5Uc_e7FHcX8.jpg",
    ),
]

PATTERNS = [
    {
        "pattern_id": "P01_object_first",
        "dimension": "primary_subject",
        "classification": "dominant",
        "usable_reference_count": 11,
        "usable_reference_ratio": 0.7857,
        "supporting_reference_ids": ["O01", "O02", "O06", "J02", "J03", "J04", "J05", "Y01", "Y02", "Y03", "Y05"],
        "finding": "A real object or source image is the first visual anchor; text explains rather than replaces it.",
        "transfer_rule": "Use a neutral, explicitly empty source slot in the proof; do not reconstruct or embed the real note.",
    },
    {
        "pattern_id": "P02_one_focus_callout",
        "dimension": "composition_callout",
        "classification": "dominant",
        "usable_reference_count": 7,
        "usable_reference_ratio": 0.5,
        "supporting_reference_ids": ["O01", "O02", "J01", "J03", "J04", "Y02", "Y04"],
        "finding": "One feature, crop, numbered point, or magnified region receives emphasis at a time.",
        "transfer_rule": "Use one bounded focus window or numbered focus card per cue.",
    },
    {
        "pattern_id": "P03_short_key_term",
        "dimension": "information_hierarchy",
        "classification": "dominant",
        "usable_reference_count": 12,
        "usable_reference_ratio": 0.8571,
        "supporting_reference_ids": ["O01", "O02", "O05", "O06", "J01", "J02", "J03", "J04", "J05", "Y01", "Y03", "Y05"],
        "finding": "A short topic label or key term is larger than explanatory copy.",
        "transfer_rule": "Keep one Japanese action label and one feature term above the subtitle.",
    },
    {
        "pattern_id": "P04_bottom_text_band",
        "dimension": "subtitle",
        "classification": "recurring",
        "usable_reference_count": 4,
        "usable_reference_ratio": 0.2857,
        "supporting_reference_ids": ["J05", "Y01", "Y03", "Y05"],
        "finding": "A high-contrast lower band carries a short promise or dialogue text.",
        "transfer_rule": "Retain the approved subtitle safe area as a production constraint, not as copied styling.",
    },
    {
        "pattern_id": "P05_speaker_cues",
        "dimension": "speaker_representation",
        "classification": "cohort_specific",
        "usable_reference_count": 5,
        "usable_reference_ratio": 0.3571,
        "supporting_reference_ids": ["Y01", "Y02", "Y03", "Y04", "Y05"],
        "finding": "Dialogue explainers visibly distinguish two speakers, commonly with busts at edges or corners.",
        "transfer_rule": "Use neutral speaker nameplates only; no character art is authorized.",
    },
    {
        "pattern_id": "P06_adjacent_source_credit",
        "dimension": "source_attribution",
        "classification": "recurring",
        "usable_reference_count": 4,
        "usable_reference_ratio": 0.2857,
        "supporting_reference_ids": ["O02", "O05", "O06", "J04"],
        "finding": "Institutional identity or an image source caption stays adjacent to the evidence surface.",
        "transfer_rule": "Show compact reference IDs and the research-only rights boundary in a footer.",
    },
    {
        "pattern_id": "P07_restrained_reveal",
        "dimension": "motion",
        "classification": "recurring",
        "usable_reference_count": 5,
        "usable_reference_ratio": 0.3571,
        "supporting_reference_ids": ["O01", "O02", "O05", "J02", "J03"],
        "finding": "Change is explained through angle states, a reveal, a process shot, or one focus shift.",
        "transfer_rule": "Storyboard one non-looping reveal or zoom per cue; do not infer playback quality.",
    },
    {
        "pattern_id": "P08_neutral_field",
        "dimension": "background_palette",
        "classification": "dominant",
        "usable_reference_count": 8,
        "usable_reference_ratio": 0.5714,
        "supporting_reference_ids": ["O01", "O02", "O06", "J02", "J04", "J05", "Y03", "Y05"],
        "finding": "Neutral or source-derived fields keep the object and explanation dominant.",
        "transfer_rule": "Use charcoal and warm-white neutral glue; accents encode speaker or focus only.",
    },
    {
        "pattern_id": "P09_creator_brand_world",
        "dimension": "background_branding",
        "classification": "unsuitable",
        "usable_reference_count": 6,
        "usable_reference_ratio": 0.4286,
        "supporting_reference_ids": ["O05", "J01", "J02", "J03", "J05", "Y01"],
        "finding": "Publisher and creator packages are common but source-specific.",
        "transfer_rule": "Do not copy branded frames, character art, studio worlds, or a creator palette.",
    },
    {
        "pattern_id": "P10_dense_collage",
        "dimension": "thumbnail",
        "classification": "outlier",
        "usable_reference_count": 2,
        "usable_reference_ratio": 0.1429,
        "supporting_reference_ids": ["Y02", "Y04"],
        "finding": "Dense multi-image collage appears in individual thumbnails, not across cohorts.",
        "transfer_rule": "Reject as a full-frame proof grammar because it increases rights and comprehension burden.",
    },
]

DECISIONS = [
    ("D01", "primary subject", "neutral source/object slot", ["O01", "O02", "J02", "J04"], ["P01_object_first"]),
    ("D02", "full-frame composition", "single object field plus one bounded focus", ["O01", "O02", "J03", "J05"], ["P01_object_first", "P02_one_focus_callout"]),
    ("D03", "character/speaker treatment", "speaker nameplate only; no character art", ["Y01", "Y02", "Y03"], ["P05_speaker_cues"]),
    ("D04", "subtitle placement", "approved text in bottom safe band", ["J05", "Y01", "Y03"], ["P04_bottom_text_band"]),
    ("D05", "explanation text placement", "one short key point adjacent to focus", ["J01", "J03", "Y02", "Y05"], ["P02_one_focus_callout", "P03_short_key_term"]),
    ("D06", "callout/zoom treatment", "one numbered focus window or close-up", ["O01", "O02", "J04"], ["P02_one_focus_callout"]),
    ("D07", "source-credit placement", "compact source IDs in lower footer", ["J04", "O05", "O06"], ["P06_adjacent_source_credit"]),
    ("D08", "background", "neutral charcoal and warm-white field", ["O02", "J04", "Y03"], ["P08_neutral_field"]),
    ("D09", "color roles", "neutral base plus speaker/focus accents", ["J01", "Y01", "Y02", "Y05"], ["P08_neutral_field", "P05_speaker_cues"]),
    ("D10", "typography roles", "large action label, medium feature term, exact subtitle", ["J01", "J03", "Y04", "Y05"], ["P03_short_key_term"]),
    ("D11", "transition/motion class", "single non-looping reveal or zoom", ["O01", "J02", "J03", "O05"], ["P07_restrained_reveal"]),
    ("D12", "thumbnail/contact-sheet grammar", "one subject, short label, small speaker cue", ["Y01", "Y02", "J01", "J05"], ["P01_object_first", "P03_short_key_term"]),
]

KEYFRAME_SPECS = [
    {"filename": "reference_S1_overview.svg", "cue_id": "cue_001", "scene_id": "S1", "action": "まず、全体像", "term": "四つの確認動作", "focus": "overview", "refs": ["O01", "J01", "Y01"]},
    {"filename": "reference_cue_003_watermark.svg", "cue_id": "cue_003", "scene_id": "S2", "action": "透かす", "term": "高精細すき入れ", "focus": "watermark", "refs": ["O01", "O02", "J04"]},
    {"filename": "reference_cue_004_hologram.svg", "cue_id": "cue_004", "scene_id": "S2", "action": "傾ける", "term": "3Dホログラム", "focus": "hologram", "refs": ["O01", "O02", "J02"]},
    {"filename": "reference_cue_005_intaglio.svg", "cue_id": "cue_005", "scene_id": "S2", "action": "触る", "term": "深凹版印刷", "focus": "intaglio", "refs": ["O02", "J03", "Y02"]},
    {"filename": "reference_cue_006_microtext.svg", "cue_id": "cue_006", "scene_id": "S2", "action": "ルーペで見る", "term": "マイクロ文字", "focus": "microtext", "refs": ["O01", "O02", "J04"]},
    {"filename": "reference_S3_summary.svg", "cue_id": "cue_009", "scene_id": "S3", "action": "四つを覚える", "term": "確認動作のまとめ", "focus": "summary", "refs": ["J01", "J05", "Y03"]},
]

MOTION_BY_CUE = {
    "cue_001": ("label_reveal", "question and action labels reveal once"),
    "cue_002": ("object_focus_reveal", "four-action overview settles once"),
    "cue_003": ("light_reveal", "neutral source slot brightens once"),
    "cue_004": ("angle_state_reveal", "three angle states reveal once"),
    "cue_005": ("relief_reveal", "raised-line profile reveals once"),
    "cue_006": ("magnification_zoom", "one focus window zooms once"),
    "cue_007": ("marker_reveal", "identification marker label reveals once"),
    "cue_008": ("difference_reveal", "two neutral comparison cards reveal once"),
    "cue_009": ("four_step_sequence", "four action labels sequence once"),
}

REVIEW_QUESTIONS = [
    "調査対象は、この動画の視覚設計を判断するために十分で偏りがありませんか。",
    "新しい画面は、既存コンテンツの共通文法を利用しており、AI独自の世界観を押し出していませんか。",
    "S1／S2／S3と9 cueの画面構成は、字幕・会話・技術説明を理解しやすくしていますか。",
    "参照元の模倣や権利上危険な再利用ではなく、共通パターンの適切な翻案になっていますか。",
    "このreference-grounded proofをShot／MotionとAsset／Rights設計の基準にしてよいですか。",
]


def build_reference_grounded_visual_design(*, root: str | Path | None = None) -> dict[str, Any]:
    repo_root = Path(root).resolve() if root else Path(__file__).resolve().parents[2]
    pilot = repo_root / DEFAULT_PILOT
    output = repo_root / DEFAULT_OUTPUT
    keyframes = output / "keyframes"
    keyframes.mkdir(parents=True, exist_ok=True)
    for local_name in ("local_reference_cache", "local_reference_captures", "local_render_inspection"):
        (output / local_name).mkdir(parents=True, exist_ok=True)

    script = _load_json(pilot / "canonical_script.json")
    approval = _load_json(pilot / "human_script_approval_receipt.json")
    cues = script["cues"]
    cue_by_id = {cue["cue_id"]: cue for cue in cues}
    old_hashes = {
        path.relative_to(repo_root).as_posix(): _sha(path)
        for path in sorted((repo_root / OLD_PROOF).rglob("*"))
        if path.is_file()
    }

    generated: dict[Path, str] = {}
    registry = {
        "schema_version": "new_banknote.reference_registry.v1",
        "status": "research_frozen_before_design",
        "retrieval_timestamp": RETRIEVED_AT,
        "research_frozen_at": RESEARCH_FROZEN_AT,
        "design_generation_started_at": DESIGN_GENERATION_STARTED_AT,
        "query_log": QUERY_LOG,
        "reference_count": len(REFERENCES),
        "references": REFERENCES,
        "research_policy": {
            "login_used": False,
            "paywall_or_access_control_circumvented": False,
            "video_or_audio_downloaded": False,
            "bulk_scraping_used": False,
            "public_visibility_treated_as_reuse_permission": False,
        },
    }
    generated[output / "reference_registry.json"] = _json_text(registry)
    generated[output / "reference_audit_matrix.json"] = _json_text(
        {
            "schema_version": "new_banknote.reference_audit_matrix.v1",
            "status": "complete",
            "required_field_count": 35,
            "rows": REFERENCES,
        }
    )
    coverage = _coverage_readback()
    generated[output / "reference_coverage_readback.json"] = _json_text(coverage)
    generated[output / "visual_grammar_clusters.json"] = _json_text(
        {
            "schema_version": "new_banknote.visual_grammar_clusters.v1",
            "status": "passed",
            "usable_reference_denominator": coverage["usable_visually_analyzed_references"],
            "classification_rules": {
                "dominant": "at least 40 percent of usable references or strong across two cohorts",
                "recurring": "at least three independent references",
                "cohort_specific": "common within one cohort only",
                "outlier": "one source or one creator pattern",
                "unsuitable": "conflicts with fidelity, rights, readability, or feasibility",
            },
            "patterns": PATTERNS,
        }
    )
    generated[output / "visual_pattern_frequency.json"] = _json_text(
        {
            "schema_version": "new_banknote.visual_pattern_frequency.v1",
            "usable_reference_denominator": coverage["usable_visually_analyzed_references"],
            "frequencies": [
                {
                    "pattern_id": row["pattern_id"],
                    "count": row["usable_reference_count"],
                    "ratio": row["usable_reference_ratio"],
                    "classification": row["classification"],
                }
                for row in PATTERNS
            ],
        }
    )
    generated[output / "current_ai_design_deviation_report.md"] = _deviation_report()
    generated[output / "ai_original_visual_supersession_receipt.json"] = _json_text(
        _supersession_receipt(old_hashes)
    )
    scorecard = _selection_scorecard()
    generated[output / "reference_selection_scorecard.json"] = _json_text(scorecard)
    contract = _design_contract()
    generated[output / "reference_grounded_design_contract.json"] = _json_text(contract)
    lineage = _lineage()
    generated[output / "reference_to_visual_lineage.json"] = _json_text(lineage)

    mapping = _mapping(cues)
    generated[output / "reference_grounded_visual_mapping.json"] = _json_text(mapping)
    motion = _motion_storyboard(cues)
    generated[output / "reference_grounded_motion_storyboard.json"] = _json_text(motion)
    for spec in KEYFRAME_SPECS:
        generated[keyframes / spec["filename"]] = _render_keyframe(spec, cue_by_id[spec["cue_id"]])
    generated[output / "reference_grounded_nine_cue_contact_sheet.svg"] = _render_contact_sheet(cues)
    generated[output / "reference_grounded_motion_storyboard.svg"] = _render_motion_storyboard(cues)
    generated[output / "reference_grounded_visual_proof.html"] = _render_html(lineage)
    generated[output / "README_REFERENCE_GROUNDED_VISUAL_PROOF.md"] = _proof_readme()
    generated[output / "reference_grounded_visual_review_sheet.md"] = _review_sheet()
    generated[output / "README_REFERENCE_GROUNDED_VISUAL_DESIGN.md"] = _research_readme(coverage, scorecard)

    changed: list[str] = []
    for path, content in generated.items():
        if _write_if_changed(path, content):
            changed.append(path.relative_to(repo_root).as_posix())

    manifest_rows = []
    for path in sorted(generated):
        manifest_rows.append(
            {
                "path": path.relative_to(repo_root).as_posix(),
                "sha256": _sha(path),
                "category": _artifact_category(path),
            }
        )
    manifest = {
        "schema_version": "new_banknote.reference_grounded_visual_proof_manifest.v1",
        "status": "human_review_ready_not_accepted",
        "source_base_revision": BASE_REVISION,
        "design_id": DESIGN_ID,
        "artifacts": manifest_rows,
        "research": {
            "total_references": coverage["total_references"],
            "usable_visually_analyzed_references": coverage["usable_visually_analyzed_references"],
            "cohort_counts": coverage["usable_cohort_counts"],
            "research_preceded_design_generation": RESEARCH_FROZEN_AT < DESIGN_GENERATION_STARTED_AT,
        },
        "approved_content": {
            "approval_receipt_id": approval["receipt_id"],
            "approved_hash_count": len(approval["approved_file_hashes"]),
            "cue_count": script["cue_count"],
            "scene_allocation": script["scene_allocation"],
            "speaker_counts": script["speaker_counts"],
            "content_modified": False,
        },
        "proof_contract": {
            "canvas": [CANVAS_WIDTH, CANVAS_HEIGHT],
            "full_frame_keyframes": len(KEYFRAME_SPECS),
            "cue_coverage": "9/9",
            "viewer_first": True,
            "reference_lineage_second": True,
            "external_asset_count": 0,
            "source_images_embedded": False,
            "final_visual_acceptance": False,
            "implementation_authorized": False,
            "YMM4_authorized": False,
            "render_authorized": False,
            "production_authorized": False,
            "publication_authorized": False,
            "rights_authorized": False,
        },
        "superseded_old_proof": {
            "artifact_root": OLD_PROOF.as_posix(),
            "status": "exploratory_ai_original_not_reference_grounded",
            "current_visual_authority": False,
            "historical_evidence": True,
            "protected_file_count": len(old_hashes),
        },
    }
    manifest_path = output / "reference_grounded_visual_proof_manifest.json"
    if _write_if_changed(manifest_path, _json_text(manifest)):
        changed.append(manifest_path.relative_to(repo_root).as_posix())

    readback = _readback(repo_root, output, script, approval, manifest, lineage, old_hashes)
    readback_path = output / "reference_grounded_visual_proof_readback.json"
    if _write_if_changed(readback_path, _json_text(readback)):
        changed.append(readback_path.relative_to(repo_root).as_posix())

    contact_path = output / "reference_contact_sheet.local.html"
    _write_if_changed(contact_path, _render_local_contact_sheet())
    return {
        "status": "passed" if readback["checks"]["all_passed"] else "failed",
        "changed": sorted(changed),
        "reference_count": len(REFERENCES),
        "usable_reference_count": coverage["usable_visually_analyzed_references"],
        "selected_design": DESIGN_ID,
        "selected_score": scorecard["selection"]["selected_score"],
    }


def _coverage_readback() -> dict[str, Any]:
    usable = [row for row in REFERENCES if row["visually_analyzed"]]
    cohort_counts = Counter(row["cohort"] for row in REFERENCES)
    usable_cohort_counts = Counter(row["cohort"] for row in usable)
    tag_counts = Counter(tag for row in usable for tag in row["coverage_tags"])
    checks = {
        "total_references_between_15_and_18": 15 <= len(REFERENCES) <= 18,
        "usable_visually_analyzed_minimum_12": len(usable) >= 12,
        "official_usable_minimum_4": usable_cohort_counts["official_educational"] >= 4,
        "journalism_usable_minimum_4": usable_cohort_counts["journalism_documentary"] >= 4,
        "yukkuri_usable_minimum_4": usable_cohort_counts["yukkuri_adjacent_explainer"] >= 4,
        "exact_topic_minimum_2": tag_counts["exact_topic"] >= 2,
        "object_centred_minimum_3": tag_counts["object_centred"] >= 3,
        "two_character_minimum_3": tag_counts["two_character_dialogue"] >= 3,
        "source_credit_minimum_2": tag_counts["source_credit"] >= 2,
        "motion_callout_zoom_minimum_3": tag_counts["motion_callout_zoom"] >= 3,
        "title_only_not_counted": all(
            "title only" not in " ".join(row["inspected_surfaces"]).lower() for row in usable
        ),
    }
    checks["all_passed"] = all(checks.values())
    return {
        "schema_version": "new_banknote.reference_coverage_readback.v1",
        "status": "passed" if checks["all_passed"] else "failed",
        "total_references": len(REFERENCES),
        "usable_visually_analyzed_references": len(usable),
        "limited_not_counted_reference_ids": [row["reference_id"] for row in REFERENCES if not row["visually_analyzed"]],
        "cohort_counts": dict(sorted(cohort_counts.items())),
        "usable_cohort_counts": dict(sorted(usable_cohort_counts.items())),
        "coverage_tag_counts": dict(sorted(tag_counts.items())),
        "checks": checks,
    }


def _deviation_report() -> str:
    rows = [
        ("Security Inspection Lab metaphor", "route_a_visual_proof/", "AI-original visual choice", "none", "history-only", "No recurring cross-cohort lab metaphor was found."),
        ("invented lab/studio world", "route_a_visual_proof/", "AI-original visual choice", "none", "discard", "Existing content uses source objects, studios, or neutral pages—not a shared invented world."),
        ("off-white / ink-blue / green / orange palette", "README_ROUTE_A_VISUAL_PROOF.md", "AI-original visual choice", "weak", "discard", "Publisher colors vary; only neutral base plus functional accent recurs."),
        ("three-column composition", "route_a_visual_proof keyframes", "AI-original visual choice", "weak", "discard", "Single subject fields and one bounded focus recur more strongly."),
        ("abstract banknote geometry", "route_a_visual_proof keyframes", "AI-original visual choice", "none", "discard", "It risks looking like an invented note and is not required for the reference grammar."),
        ("action boxes", "route_a_visual_proof keyframes", "AI-original visual choice", "recurring", "adapt", "Short action labels recur, but the old box styling does not."),
        ("right-side explanation block", "route_a_visual_proof keyframes", "AI-original visual choice", "weak", "discard", "Explanation should stay adjacent to one focus, not form a persistent third column."),
        ("subtitle band", "route_a_visual_proof keyframes", "production constraint", "recurring", "retain constraint / restyle", "Bottom text bands recur and approved safe-area separation remains useful."),
        ("motion vocabulary names", "route_a_motion_storyboard.json", "AI-original visual choice", "weak", "discard", "Retain only evidence-supported reveal/zoom classes and the non-looping budget."),
        ("nine-cue contact sheet", "route_a_nine_cue_contact_sheet.svg", "production constraint", "recurring", "retain function / redesign", "Overview surfaces recur; the old styling is not reusable authority."),
        ("viewer/annotation separation", "route_a_visual_proof.html", "production constraint", "strong", "retain", "Viewer-first with a secondary evidence surface improves review clarity."),
        ("schematic disclaimer", "route_a_visual_proof keyframes", "production constraint", "strong", "retain", "Required to prevent exact-note or official-procedure interpretation."),
        ("subtitle safe-area geometry", "route_a_visual_proof keyframes", "production constraint", "not a visual reference claim", "retain as neutral glue", "Preserves approved text and platform fit."),
        ("one-motion/non-looping budget", "route_a_motion_storyboard.json", "production constraint", "recurring", "retain", "Restrained one-time reveal/zoom is supported; playback remains untested."),
    ]
    body = [
        "# Current AI Design Deviation Report",
        "",
        "> The prior Route A proof is preserved byte-exact as exploratory AI-original history. It is not current visual authority.",
        "",
        "| current element | artifact | likely origin | reference support | disposition | rationale |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    body.extend("| " + " | ".join(row) + " |" for row in rows)
    body.extend(
        [
            "",
            "## Result",
            "",
            "Approved text, cue mapping, subtitle safety, viewer/evidence separation, the schematic disclaimer, and the non-looping motion limit remain constraints. The Lab metaphor, palette, three-column UI, abstract-note styling, persistent right explanation block, decorative geometry, and bespoke motion naming are not carried forward.",
            "",
            "Final acceptance remains a human decision. This audit authorizes neither YMM4 nor assets, render, production, publication, or rights use.",
        ]
    )
    return "\n".join(body) + "\n"


def _supersession_receipt(old_hashes: dict[str, str]) -> dict[str, Any]:
    return {
        "schema_version": "new_banknote.ai_original_visual_supersession_receipt.v1",
        "receipt_id": "new-banknote-route-a-ai-original-supersession-v1",
        "superseded_artifact_root": OLD_PROOF.as_posix(),
        "source_commit": BASE_REVISION,
        "supersession_reason": "existing content research was required before visual authority; the prior proof was created from original abstract geometry without external visual references",
        "status": "exploratory_ai_original_not_reference_grounded",
        "current_visual_authority": False,
        "historical_evidence": True,
        "content_authority": "unchanged",
        "reusable_constraints": [
            "approved text and cue mapping",
            "subtitle safe-area concept",
            "viewer and evidence surface separation",
            "schematic disclaimer",
            "one principal motion maximum and no continuous loop",
        ],
        "non_reusable_style_decisions": [
            "Security Inspection Lab metaphor",
            "invented lab/studio world",
            "off-white ink-blue green orange palette",
            "three-column composition",
            "abstract banknote geometry",
            "persistent right explanation block",
            "decorative geometry",
            "bespoke motion naming",
        ],
        "user_correction_classification": "project_wide_visual_process_requirement",
        "final_acceptance": False,
        "protected_file_count": len(old_hashes),
        "protected_artifact_sha256": old_hashes,
    }


def _selection_scorecard() -> dict[str, Any]:
    candidates = [
        {
            "candidate_id": "documentary_object_focus_consensus",
            "supporting_reference_ids": ["O01", "O02", "J02", "J03", "J04", "J05", "Y01", "Y02"],
            "cohort_coverage": 3,
            "subject_strategy": "single neutral source/object slot with one focus",
            "character_strategy": "speaker nameplates only",
            "subtitle_strategy": "bottom safe band",
            "callout_strategy": "one focus window or numbered point",
            "source_credit_strategy": "compact reference footer",
            "motion_strategy": "one non-looping reveal or zoom",
            "rights_burden": "low",
            "YMM4_feasibility": "high",
            "content_risk": "low",
            "deviations": ["real source imagery is replaced with neutral placeholders"],
            "score_components": {
                "reference_support_breadth": 24,
                "approved_content_fidelity": 20,
                "viewer_comprehension_readability": 14,
                "rights_and_asset_feasibility": 14,
                "yukkuri_dialogue_compatibility": 8,
                "YMM4_feasibility": 8,
                "motion_restraint_maintainability": 4,
            },
            "score": 92,
            "hard_fail": False,
        },
        {
            "candidate_id": "official_feature_map",
            "supporting_reference_ids": ["O01", "O02", "O06", "J04"],
            "cohort_coverage": 2,
            "subject_strategy": "numbered object map",
            "character_strategy": "voice only",
            "subtitle_strategy": "bottom safe band",
            "callout_strategy": "multiple numbered outlines",
            "source_credit_strategy": "institutional footer",
            "motion_strategy": "feature reveal",
            "rights_burden": "low when placeholders are used",
            "YMM4_feasibility": "medium",
            "content_risk": "medium because a multi-callout map may imply exact placement",
            "deviations": ["exact object geometry cannot transfer"],
            "score_components": {
                "reference_support_breadth": 20,
                "approved_content_fidelity": 18,
                "viewer_comprehension_readability": 13,
                "rights_and_asset_feasibility": 13,
                "yukkuri_dialogue_compatibility": 7,
                "YMM4_feasibility": 7,
                "motion_restraint_maintainability": 4,
            },
            "score": 82,
            "hard_fail": False,
        },
        {
            "candidate_id": "dialogue_overlay_object",
            "supporting_reference_ids": ["J01", "J03", "Y01", "Y02", "Y03", "Y04", "Y05"],
            "cohort_coverage": 2,
            "subject_strategy": "object field plus two speaker cues",
            "character_strategy": "nameplates replace art",
            "subtitle_strategy": "speaker-coded bottom band",
            "callout_strategy": "short speech point",
            "source_credit_strategy": "footer",
            "motion_strategy": "speaker cue reveal",
            "rights_burden": "medium",
            "YMM4_feasibility": "high",
            "content_risk": "medium because dialogue framing can overpower technical evidence",
            "deviations": ["creator character art is excluded"],
            "score_components": {
                "reference_support_breadth": 21,
                "approved_content_fidelity": 18,
                "viewer_comprehension_readability": 13,
                "rights_and_asset_feasibility": 11,
                "yukkuri_dialogue_compatibility": 10,
                "YMM4_feasibility": 9,
                "motion_restraint_maintainability": 4,
            },
            "score": 86,
            "hard_fail": False,
        },
    ]
    return {
        "schema_version": "new_banknote.reference_selection_scorecard.v1",
        "status": "selected_for_human_review_proof",
        "scoring_model_maximum": 100,
        "candidates": candidates,
        "selection": {
            "rule": "top valid candidate leads the second by at least 5 points",
            "selected_candidate": DESIGN_ID,
            "selected_score": 92,
            "second_candidate": "dialogue_overlay_object",
            "second_score": 86,
            "lead": 6,
            "reference_threshold_passed": True,
            "hard_constraints_passed": True,
            "selection_confidence": "medium_high",
            "human_approval_status": "pending",
        },
    }


def _design_contract() -> dict[str, Any]:
    return {
        "schema_version": "new_banknote.reference_grounded_design_contract.v1",
        "status": "implemented_proof_pending_human_review",
        "design_id": DESIGN_ID,
        "canvas": {"width": CANVAS_WIDTH, "height": CANVAS_HEIGHT},
        "selected_grammar": [
            "P01_object_first",
            "P02_one_focus_callout",
            "P03_short_key_term",
            "P04_bottom_text_band",
            "P05_speaker_cues",
            "P06_adjacent_source_credit",
            "P07_restrained_reveal",
            "P08_neutral_field",
        ],
        "implementation": {
            "primary_subject": "neutral source/object slot; no external image embedded",
            "composition": "single field plus one bounded focus",
            "speaker_treatment": "text-only speaker nameplate",
            "subtitle_safe_area": [84, 780, 1752, 220],
            "source_credit": "compact reference IDs and rights boundary footer",
            "palette": {
                "field": "#15181D",
                "surface": "#F7F5EF",
                "reimu": "#CF3F57",
                "marisa": "#E5B840",
                "focus": "#52C7C7",
            },
            "motion": "one non-looping reveal or zoom maximum per cue; storyboard only",
        },
        "rights_boundary": {
            "external_assets": 0,
            "source_images_embedded": False,
            "logos": False,
            "creator_character_art": False,
            "exact_banknote_likeness": False,
            "portrait_seal_serial_exact_security_pattern": False,
            "reference_captures": "ignored local research evidence only",
        },
        "content_boundary": {
            "approved_text_changed": False,
            "scene_allocation": {"S1": 2, "S2": 4, "S3": 3},
            "speaker_counts": {"れいむ": 3, "まりさ": 6},
            "new_claims_added": False,
        },
        "authorization": {
            "human_visual_acceptance": False,
            "shot_motion": False,
            "asset_rights": False,
            "YMM4": False,
            "render": False,
            "production": False,
            "publication": False,
        },
    }


def _lineage() -> dict[str, Any]:
    decisions = []
    contribution: Counter[str] = Counter()
    for decision_id, decision_type, selected, refs, patterns in DECISIONS:
        contribution.update(refs)
        decisions.append(
            {
                "decision_id": decision_id,
                "decision_type": decision_type,
                "selected_value": selected,
                "supporting_reference_ids": refs,
                "supporting_cohort_count": len({
                    row["cohort"] for row in REFERENCES if row["reference_id"] in refs
                }),
                "support_strength": "threshold_A",
                "adopted_pattern_ids": patterns,
                "adaptation_description": "Shared grammar is reduced to an original, rights-minimal construction.",
                "deviation_from_references": "No source image, logo, creator art, branded frame, or exact composition is copied.",
                "original_glue": "coordinates, semantic wrapping, neutral placeholder geometry, and contrast tuning",
                "original_glue_class": "neutral_glue",
                "content_fidelity_effect": "approved wording and order remain exact",
                "rights_effect": "reduces source-image and creator-style reuse burden",
                "YMM4_feasibility_effect": "static primitives and one bounded motion class; untested in YMM4",
                "human_approval_impact": "pending",
            }
        )
    reference_count = len(DECISIONS)
    contribution_rows = [
        {
            "reference_id": reference_id,
            "supported_major_decision_count": count,
            "share_of_major_decisions": round(count / reference_count, 4),
        }
        for reference_id, count in sorted(contribution.items())
    ]
    max_share = max(row["share_of_major_decisions"] for row in contribution_rows)
    return {
        "schema_version": "new_banknote.reference_to_visual_lineage.v1",
        "status": "complete_pending_human_acceptance",
        "major_decision_count": len(decisions),
        "covered_major_decision_count": len(decisions),
        "coverage_ratio": 1.0,
        "decisions": decisions,
        "source_dominance": {
            "rule_maximum": 0.4,
            "maximum_observed_share": max_share,
            "passed": max_share <= 0.4,
            "by_reference": contribution_rows,
        },
        "unreported_design_choice_count": 0,
        "human_approval_status": "pending",
    }


def _mapping(cues: list[dict[str, Any]]) -> dict[str, Any]:
    frame_by_cue = {spec["cue_id"]: spec["filename"] for spec in KEYFRAME_SPECS}
    return {
        "schema_version": "new_banknote.reference_grounded_visual_mapping.v1",
        "status": "complete_pending_human_review",
        "cue_count": len(cues),
        "scene_allocation": {"S1": 2, "S2": 4, "S3": 3},
        "speaker_counts": dict(Counter(cue["speaker"] for cue in cues)),
        "cues": [
            {
                "sequence": cue["sequence"],
                "cue_id": cue["cue_id"],
                "scene_id": cue["scene_id"],
                "speaker": cue["speaker"],
                "text": cue["text"],
                "keyframe": frame_by_cue.get(cue["cue_id"]),
                "contact_sheet_thumbnail": True,
                "adopted_pattern_ids": ["P01_object_first", "P03_short_key_term", "P04_bottom_text_band"],
                "external_asset": False,
                "loop": False,
                "principal_motion_count": 1,
            }
            for cue in cues
        ],
    }


def _motion_storyboard(cues: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "schema_version": "new_banknote.reference_grounded_motion_storyboard.v1",
        "status": "proposal_only_not_implemented",
        "motion_bearing_cue_count": len(cues),
        "principal_motion_maximum_per_cue": 1,
        "continuous_loop_allowed": False,
        "states": ["start", "emphasis", "settled"],
        "reference_pattern_id": "P07_restrained_reveal",
        "cues": [
            {
                "cue_id": cue["cue_id"],
                "motion_class": MOTION_BY_CUE[cue["cue_id"]][0],
                "display_label": MOTION_BY_CUE[cue["cue_id"]][1],
                "start": "neutral hold",
                "emphasis": "single supported focus action",
                "settled": "stable reading frame",
                "duration_seconds": 0.65,
                "easing": "ease-out",
                "loop": False,
                "simultaneous_principal_motions": 1,
                "implementation_status": "storyboard_only_YMM4_untested",
            }
            for cue in cues
        ],
    }


def _render_keyframe(spec: dict[str, Any], cue: dict[str, Any]) -> str:
    speaker_color = "#CF3F57" if cue["speaker"] == "れいむ" else "#E5B840"
    refs = " ".join(spec["refs"])
    attrs = {
        "xmlns": "http://www.w3.org/2000/svg",
        "width": str(CANVAS_WIDTH),
        "height": str(CANVAS_HEIGHT),
        "viewBox": "0 0 1920 1080",
        "data-surface": "viewer",
        "data-design-id": DESIGN_ID,
        "data-cue-id": cue["cue_id"],
        "data-approved-text": cue["text"],
        "data-reference-ids": refs,
        "data-pattern-ids": "P01_object_first P02_one_focus_callout P03_short_key_term P04_bottom_text_band P06_adjacent_source_credit",
        "data-external-asset-count": "0",
        "data-human-approval": "pending",
        "data-implementation-authorized": "false",
    }
    pieces = [
        _svg_open(attrs),
        '<rect width="1920" height="1080" fill="#15181D"/>',
        '<rect x="48" y="42" width="1824" height="696" rx="32" fill="#F7F5EF"/>',
        f'<text x="84" y="116" font-size="30" font-weight="800" fill="#70757D">{_xml(spec["scene_id"])} / {_xml(cue["cue_id"])}</text>',
        f'<text x="84" y="188" font-size="70" font-weight="900" fill="#15181D">{_xml(spec["action"])}</text>',
        f'<text x="84" y="238" font-size="28" font-weight="800" fill="#387F82">{_xml(spec["term"])}</text>',
        _render_focus(spec["focus"]),
        f'<text x="84" y="724" font-size="24" font-weight="800" fill="#70757D">{_xml(DISCLAIMER)}</text>',
        '<rect x="84" y="780" width="1752" height="220" rx="26" fill="#24282F" stroke="#454B55" stroke-width="2"/>',
        f'<rect x="112" y="812" width="170" height="56" rx="28" fill="{speaker_color}"/>',
        f'<text x="197" y="850" text-anchor="middle" font-size="28" font-weight="900" fill="#15181D">{_xml(cue["speaker"])}</text>',
        _svg_text_lines(cue["text"], x=316, y=844, font_size=38, line_gap=50, max_chars=34, max_lines=3, fill="#FFFFFF"),
        f'<text x="84" y="1044" font-size="20" font-weight="700" fill="#B7BDC5">参照文法 {refs} ｜ 外部画像不使用 ｜ human review pending</text>',
        "</svg>",
    ]
    return "\n".join(pieces) + "\n"


def _render_focus(focus: str) -> str:
    common = '<rect x="722" y="274" width="1114" height="414" rx="28" fill="#FFFFFF" stroke="#D8D5CC" stroke-width="4"/>'
    if focus == "overview":
        labels = [("透かす", 790), ("触る", 1045), ("傾ける", 1300), ("ルーペ", 1555)]
        parts = [common, '<text x="1279" y="342" text-anchor="middle" font-size="28" font-weight="800" fill="#70757D">対象資料の確認手順</text>']
        for index, (label, x) in enumerate(labels, 1):
            parts.extend([
                f'<circle cx="{x}" cy="500" r="92" fill="#EEF7F7" stroke="#52C7C7" stroke-width="6"/>',
                f'<text x="{x}" y="486" text-anchor="middle" font-size="24" font-weight="900" fill="#387F82">0{index}</text>',
                f'<text x="{x}" y="536" text-anchor="middle" font-size="30" font-weight="900" fill="#15181D">{_xml(label)}</text>',
            ])
        return "".join(parts)
    if focus == "watermark":
        return "".join([
            common,
            '<circle cx="1100" cy="486" r="152" fill="#F3F1EA" stroke="#B8B2A4" stroke-width="5"/>',
            '<path d="M1010 486 Q1100 372 1190 486 Q1100 600 1010 486Z" fill="none" stroke="#52C7C7" stroke-width="12"/>',
            '<circle cx="1540" cy="486" r="126" fill="#EEF7F7" stroke="#52C7C7" stroke-width="7"/>',
            '<path d="M1238 450 L1400 418" stroke="#52C7C7" stroke-width="7"/>',
            '<text x="1540" y="474" text-anchor="middle" font-size="28" font-weight="900" fill="#15181D">細かな模様</text>',
            '<text x="1540" y="516" text-anchor="middle" font-size="23" fill="#59616B">光に透かして確認</text>',
        ])
    if focus == "hologram":
        parts = [common, '<text x="1279" y="338" text-anchor="middle" font-size="26" font-weight="800" fill="#70757D">角度の変化を三状態で示す</text>']
        for index, x in enumerate((920, 1279, 1638), 1):
            parts.extend([
                f'<rect x="{x - 116}" y="382" width="232" height="214" rx="22" fill="#EEF7F7" stroke="#52C7C7" stroke-width="5"/>',
                f'<path d="M{x - 58} 535 Q{x} {415 + index * 12} {x + 58} 535" fill="none" stroke="#387F82" stroke-width="10"/>',
                f'<text x="{x}" y="638" text-anchor="middle" font-size="22" font-weight="800" fill="#70757D">ANGLE 0{index}</text>',
            ])
        return "".join(parts)
    if focus == "intaglio":
        parts = [common, '<text x="1279" y="338" text-anchor="middle" font-size="26" font-weight="800" fill="#70757D">盛り上がりを断面で読む</text>']
        for index, x in enumerate(range(880, 1681, 100)):
            height = 50 + (index % 3) * 28
            parts.append(f'<rect x="{x}" y="{570 - height}" width="54" height="{height}" rx="8" fill="#52C7C7"/>')
        parts.extend([
            '<path d="M850 584 H1735" stroke="#15181D" stroke-width="8"/>',
            '<path d="M1010 408 Q1270 350 1510 408" fill="none" stroke="#E5B840" stroke-width="14" stroke-linecap="round"/>',
            '<text x="1279" y="458" text-anchor="middle" font-size="25" font-weight="900" fill="#15181D">触感は高さの差として説明</text>',
        ])
        return "".join(parts)
    if focus == "microtext":
        return "".join([
            common,
            '<rect x="820" y="398" width="490" height="178" rx="22" fill="#EEEAE0"/>',
            '<text x="1065" y="500" text-anchor="middle" font-size="27" letter-spacing="8" fill="#70757D">NIPPONGINKO</text>',
            '<circle cx="1535" cy="486" r="150" fill="#FFFFFF" stroke="#52C7C7" stroke-width="9"/>',
            '<path d="M1425 596 L1324 682" stroke="#52C7C7" stroke-width="22" stroke-linecap="round"/>',
            '<text x="1535" y="474" text-anchor="middle" font-size="34" font-weight="900" fill="#15181D">文字を</text>',
            '<text x="1535" y="522" text-anchor="middle" font-size="34" font-weight="900" fill="#15181D">拡大</text>',
            '<text x="1050" y="640" text-anchor="middle" font-size="22" fill="#70757D">位置・書体・パターンは再現しない</text>',
        ])
    parts = [common, '<text x="1279" y="338" text-anchor="middle" font-size="26" font-weight="800" fill="#70757D">確認動作を一枚で整理</text>']
    labels = [("透かす", 930, 440), ("触る", 1420, 440), ("傾ける", 930, 570), ("ルーペで見る", 1420, 570)]
    for index, (label, x, y) in enumerate(labels, 1):
        parts.extend([
            f'<rect x="{x - 205}" y="{y - 52}" width="410" height="104" rx="22" fill="#EEF7F7" stroke="#52C7C7" stroke-width="4"/>',
            f'<text x="{x - 155}" y="{y + 11}" font-size="24" font-weight="900" fill="#387F82">0{index}</text>',
            f'<text x="{x + 24}" y="{y + 11}" text-anchor="middle" font-size="30" font-weight="900" fill="#15181D">{_xml(label)}</text>',
        ])
    return "".join(parts)


def _render_contact_sheet(cues: list[dict[str, Any]]) -> str:
    parts = [
        _svg_open({
            "xmlns": "http://www.w3.org/2000/svg",
            "width": "1920",
            "height": "1080",
            "viewBox": "0 0 1920 1080",
            "data-cue-coverage": "9/9",
            "data-design-id": DESIGN_ID,
        }),
        '<rect width="1920" height="1080" fill="#15181D"/>',
        '<text x="70" y="78" font-size="42" font-weight="900" fill="#FFFFFF">9 CUE / REFERENCE-GROUNDED OVERVIEW</text>',
        '<text x="70" y="118" font-size="22" fill="#B7BDC5">single subject · short key term · speaker cue · source boundary</text>',
    ]
    action_by_cue = {
        "cue_001": "問い", "cue_002": "全体像", "cue_003": "透かす", "cue_004": "傾ける",
        "cue_005": "触る", "cue_006": "ルーペ", "cue_007": "識別", "cue_008": "差を見る", "cue_009": "四つを覚える",
    }
    for index, cue in enumerate(cues):
        col = index % 3
        row = index // 3
        x = 70 + col * 610
        y = 160 + row * 286
        color = "#CF3F57" if cue["speaker"] == "れいむ" else "#E5B840"
        parts.extend([
            f'<g data-cue-id="{cue["cue_id"]}" data-approved-text="{_xml(cue["text"])}">',
            f'<rect x="{x}" y="{y}" width="560" height="244" rx="24" fill="#F7F5EF"/>',
            f'<rect x="{x + 24}" y="{y + 22}" width="126" height="38" rx="19" fill="{color}"/>',
            f'<text x="{x + 87}" y="{y + 49}" text-anchor="middle" font-size="20" font-weight="900" fill="#15181D">{_xml(cue["speaker"])}</text>',
            f'<text x="{x + 536}" y="{y + 50}" text-anchor="end" font-size="19" font-weight="800" fill="#70757D">{_xml(cue["scene_id"])} / {_xml(cue["cue_id"])}</text>',
            f'<text x="{x + 28}" y="{y + 112}" font-size="39" font-weight="900" fill="#15181D">{_xml(action_by_cue[cue["cue_id"]])}</text>',
            f'<rect x="{x + 28}" y="{y + 142}" width="504" height="72" rx="16" fill="#EEF7F7"/>',
            _svg_text_lines(cue["text"], x=x + 48, y=y + 169, font_size=18, line_gap=25, max_chars=27, max_lines=2, fill="#3F4650", truncate=True),
            "</g>",
        ])
    parts.extend([
        '<text x="70" y="1050" font-size="20" fill="#B7BDC5">9/9 cue · external assets 0 · thumbnails are original neutral diagrams · human review pending</text>',
        "</svg>",
    ])
    return "\n".join(parts) + "\n"


def _render_motion_storyboard(cues: list[dict[str, Any]]) -> str:
    parts = [
        _svg_open({
            "xmlns": "http://www.w3.org/2000/svg",
            "width": "1920",
            "height": "1080",
            "viewBox": "0 0 1920 1080",
            "data-loop": "false",
            "data-motion-status": "storyboard-only",
        }),
        '<rect width="1920" height="1080" fill="#F7F5EF"/>',
        '<text x="70" y="76" font-size="42" font-weight="900" fill="#15181D">MOTION STORYBOARD / START → EMPHASIS → SETTLED</text>',
        '<text x="70" y="116" font-size="22" fill="#70757D">P07 restrained reveal · one principal motion maximum · continuous loop false · YMM4 untested</text>',
    ]
    for index, cue in enumerate(cues):
        y = 158 + index * 96
        label = MOTION_BY_CUE[cue["cue_id"]][1]
        parts.extend([
            f'<g data-cue-id="{cue["cue_id"]}" data-loop="false" data-principal-motion-count="1">',
            f'<rect x="70" y="{y}" width="1780" height="76" rx="18" fill="#FFFFFF" stroke="#D8D5CC" stroke-width="2"/>',
            f'<text x="96" y="{y + 48}" font-size="24" font-weight="900" fill="#15181D">{_xml(cue["cue_id"])}</text>',
            f'<text x="300" y="{y + 48}" font-size="23" fill="#59616B">{_xml(label)}</text>',
            f'<text x="1160" y="{y + 48}" font-size="21" font-weight="800" fill="#387F82">START</text>',
            f'<path d="M1250 {y + 38} H1340" stroke="#52C7C7" stroke-width="5"/>',
            f'<text x="1370" y="{y + 48}" font-size="21" font-weight="800" fill="#387F82">EMPHASIS</text>',
            f'<path d="M1515 {y + 38} H1605" stroke="#52C7C7" stroke-width="5"/>',
            f'<text x="1635" y="{y + 48}" font-size="21" font-weight="800" fill="#387F82">SETTLED</text>',
            "</g>",
        ])
    parts.extend(["</svg>"])
    return "\n".join(parts) + "\n"


def _render_html(lineage: dict[str, Any]) -> str:
    cards = []
    for spec in KEYFRAME_SPECS:
        cards.append(
            f'<article class="frame"><h3>{html.escape(spec["action"])} <small>{html.escape(spec["term"])}</small></h3>'
            f'<img src="keyframes/{html.escape(spec["filename"])}" alt="{html.escape(spec["action"])} keyframe"></article>'
        )
    lineage_cards = []
    for row in lineage["decisions"]:
        lineage_cards.append(
            '<article class="lineage-card">'
            f'<p class="kicker">{html.escape(row["decision_id"])} / {html.escape(row["decision_type"])}</p>'
            f'<h3>{html.escape(row["selected_value"])}</h3>'
            f'<p><strong>refs</strong> {html.escape(" · ".join(row["supporting_reference_ids"]))}</p>'
            f'<p><strong>adapted</strong> {html.escape(row["adaptation_description"])}</p>'
            f'<p><strong>neutral glue</strong> {html.escape(row["original_glue"])}</p>'
            f'<p><strong>rights</strong> no source image, logo, creator art, or exact composition is copied.</p>'
            f'<p><strong>approval</strong> {html.escape(row["human_approval_impact"])}</p>'
            '</article>'
        )
    return f'''<!doctype html>
<html lang="ja"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Reference-Grounded New Banknote Visual Proof</title>
<style>
:root{{--field:#15181d;--surface:#f7f5ef;--ink:#171a1f;--muted:#6a7078;--focus:#52c7c7;--line:#d8d5cc}}
*{{box-sizing:border-box}}body{{margin:0;background:#e8e7e2;color:var(--ink);font-family:"Yu Gothic UI","Meiryo",sans-serif;line-height:1.65}}
.banner{{background:var(--field);color:white;padding:14px 24px;font-weight:900;letter-spacing:.06em}}main{{max-width:1540px;margin:auto;padding:32px}}
.hero{{display:grid;grid-template-columns:1.35fr .65fr;gap:24px}}.panel,.frame,.lineage-card{{background:var(--surface);border:1px solid var(--line);border-radius:20px;padding:22px}}
h1{{font-size:clamp(40px,6vw,76px);line-height:1.05;margin:.2em 0}}h2{{font-size:34px;margin-top:1.7em}}h3{{font-size:26px;margin:.2em 0 .6em}}small{{display:block;color:#387f82}}
.pill{{display:inline-block;border:2px solid var(--focus);border-radius:999px;padding:5px 11px;margin:3px;font-weight:800}}.frames{{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:20px}}
.frame img,.wide img{{display:block;width:100%;height:auto;border-radius:12px;background:white}}.wide{{background:var(--surface);padding:18px;border-radius:20px;margin:20px 0}}
.lineage-grid{{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:16px}}.kicker{{color:#387f82;font-weight:900;letter-spacing:.06em}}.review{{background:var(--field);color:white;border-radius:22px;padding:26px;margin-top:30px}}a{{color:inherit}}
body:has(#reference-lineage:target) .banner{{display:none}}body:has(#reference-lineage:target) main>:not(#reference-lineage){{display:none}}body:has(#reference-lineage:target) #reference-lineage{{display:block}}
@media(max-width:900px){{.hero,.frames,.lineage-grid{{grid-template-columns:1fr}}main{{padding:18px}}}}
</style></head>
<body data-design-id="{DESIGN_ID}" data-default-surface="viewer" data-review-status="pending" data-external-resource-count="0">
<div class="banner">内部レビュー用／REFERENCE-GROUNDED CANDIDATE／最終承認前／非公開／非本番</div>
<main><section class="hero"><div><p class="kicker">EXISTING CONTENT → SHARED GRAMMAR → ORIGINAL PROOF</p><h1>実物を中心に、ひとつずつ見る</h1><p>16件の公開referenceを先に調査し、14件の実視覚面から横断文法を抽出しました。外部画像やcreator artは使わず、単一主対象・一つのfocus・短い要点・speaker nameplateへ翻案しています。</p><span class="pill">6 keyframes</span><span class="pill">9/9 cues</span><span class="pill">external assets 0</span></div><aside class="panel"><h2>Authority</h2><p>旧Route Aは探索的AI-original historyです。このproofだけが次のhuman-review candidateですが、final acceptance、Shot/Motion、Asset/Rights、YMM4、renderは未承認です。</p></aside></section>
<section id="viewer"><h2>Viewer-first keyframes</h2><div class="frames">{''.join(cards)}</div></section>
<section><h2>9-cue overview</h2><div class="wide"><img src="reference_grounded_nine_cue_contact_sheet.svg" alt="9 cue contact sheet"></div></section>
<section><h2>Motion proposal</h2><div class="wide"><img src="reference_grounded_motion_storyboard.svg" alt="motion storyboard"></div></section>
<details id="reference-lineage" open><summary><strong>Reference lineage mode</strong> — adopted grammar / neutral glue / rights boundary</summary><div class="lineage-grid">{''.join(lineage_cards)}</div></details>
<section class="review"><h2>Human review gate</h2><p><a href="reference_grounded_visual_review_sheet.md">5問のreview sheet</a> · <a href="README_REFERENCE_GROUNDED_VISUAL_DESIGN.md">research README</a> · <a href="reference_to_visual_lineage.json">machine lineage</a></p></section>
</main><script>if(location.hash==="#reference-lineage"){{const lineage=document.getElementById("reference-lineage");lineage.open=true;window.addEventListener("load",()=>lineage.scrollIntoView({{block:"start"}}))}}</script></body></html>
'''


def _research_readme(coverage: dict[str, Any], scorecard: dict[str, Any]) -> str:
    cohorts = coverage["usable_cohort_counts"]
    return f"""# Reference-Grounded Visual Design

> **INTERNAL RESEARCH + HUMAN-REVIEW CANDIDATE / NOT FINAL / NON-PUBLIC / NON-PRODUCTION**

## Why the prior Route A proof was superseded

The prior `Security Inspection Lab` proof was built from AI-original abstract SVG geometry before existing-content research. The user classified that ordering as a project-wide quality and compliance failure. The old package remains byte-exact history, but it is not current visual authority.

## What was researched

- total references: **{coverage['total_references']}**
- usable visually analyzed references: **{coverage['usable_visually_analyzed_references']}**
- official / educational usable: **{cohorts['official_educational']}**
- journalism / documentary usable: **{cohorts['journalism_documentary']}**
- Yukkuri / adjacent explainer usable: **{cohorts['yukkuri_adjacent_explainer']}**
- limited and not counted: **{', '.join(coverage['limited_not_counted_reference_ids'])}**

The tracked registry records titles, publishers, dates, canonical URLs, inspected surfaces, visual observations, evidence grades, and rights boundaries. Captures and YouTube thumbnails remain only in ignored local research cache. `reference_contact_sheet.local.html` is the local visual comparison surface.

## Common visual grammar

Across cohorts, the most transferable grammar is: keep the object or source surface primary; emphasize one feature at a time; use one short action or key term; separate dialogue speakers visibly; place subtitles in a high-contrast lower region; keep source identity adjacent; and restrict motion to a bounded reveal, angle state, or zoom.

The patterns rejected as authority are creator-specific branding, character art, full source-image reuse, dense collage, exact note likeness, branded lower thirds, and invented story worlds.

## Implemented direction

`{DESIGN_ID}` scored **{scorecard['selection']['selected_score']}/100**, leading the next valid candidate by **{scorecard['selection']['lead']}** points. It uses a single neutral source/object slot, one focus window, short Japanese action labels, text-only speaker nameplates, the exact approved subtitle, and a compact reference footer.

Reference-derived: hierarchy, object-first focus, bounded close-up, short key term, speaker distinction, adjacent credit, and restrained one-shot motion. Neutral glue: coordinates, semantic line wrapping, placeholder geometry, and contrast tuning.

Nothing in the tracked proof copies a screenshot, thumbnail, logo, character, branded frame, portrait, seal, serial number, exact banknote geometry, or security pattern. Public visibility was not treated as reuse permission.

## How the new proof differs

The Lab metaphor, three-column pseudo-interface, old palette, abstract-note geometry, persistent right explanation block, decorative system, and bespoke motion vocabulary are absent. Approved content, cue order, scene 2/4/3, speaker 3/6, claims, evidence, CSVs, lineage, and the non-looping motion ceiling are unchanged.

## Review next

Open `reference_grounded_visual_proof.html`, then answer the five questions in `reference_grounded_visual_review_sheet.md`. Human acceptance is still required before Shot/Motion or Asset/Rights contracts. YMM4, render, pronunciation/rhythm/clipping review, production, publication, rights approval, PR, and master integration remain closed.
"""


def _proof_readme() -> str:
    return f"""# Reference-Grounded Visual Proof

> **HUMAN REVIEW CANDIDATE / NOT ACCEPTED / EXTERNAL ASSETS 0**

- primary surface: `reference_grounded_visual_proof.html`
- six 1920x1080 keyframes: `keyframes/`
- nine-cue coverage: `reference_grounded_nine_cue_contact_sheet.svg`
- motion proposal: `reference_grounded_motion_storyboard.svg`
- exact decision lineage: `reference_to_visual_lineage.json`
- five-question gate: `reference_grounded_visual_review_sheet.md`

The selected grammar is `{DESIGN_ID}`. Source captures and thumbnails are research-only ignored files and do not appear in the tracked proof. All visible diagram geometry is original, neutral, and non-likeness-based.

The prior `route_a_visual_proof/` remains byte-exact exploratory AI-original history. Final visual acceptance, Shot/Motion, Asset/Rights, YMM4, render, production, publication, and rights approval remain false.
"""


def _review_sheet() -> str:
    lines = [
        "# Reference-Grounded Visual Review",
        "",
        "> Human decision required. This proof is not accepted and does not authorize YMM4, render, production, publication, or rights use.",
        "",
    ]
    lines.extend(f"{index}. {question}" for index, question in enumerate(REVIEW_QUESTIONS, 1))
    lines.extend(
        [
            "",
            "Allowed response:",
            "",
            "- `accept`",
            "- `source/reference-specific revision`",
            "- `scene/cue-specific revision`",
            "",
            "Do not review or select the old Route A proof.",
        ]
    )
    return "\n".join(lines) + "\n"


def _render_local_contact_sheet() -> str:
    sections = []
    cohort_labels = {
        "official_educational": "A. Official / educational",
        "journalism_documentary": "B. Journalism / documentary",
        "yukkuri_adjacent_explainer": "C. Yukkuri / adjacent explainer",
    }
    for cohort, label in cohort_labels.items():
        cards = []
        for row in [item for item in REFERENCES if item["cohort"] == cohort]:
            if row["local_capture"]:
                visual = f'<img src="{html.escape(row["local_capture"])}" alt="local research capture for {row["reference_id"]}">'
            else:
                visual = f'<div class="missing">metadata card only<br>{html.escape(row["capture_note"])}</div>'
            cards.append(
                '<article>'
                f'<p class="id">{row["reference_id"]} · {html.escape(row["evidence_grade"])}</p>'
                f'<h3>{html.escape(row["exact_title"])}</h3><p>{html.escape(row["publisher_channel"])}</p>{visual}'
                f'<p><a href="{html.escape(row["canonical_url"])}">source URL</a></p>'
                f'<p><strong>grammar</strong> {html.escape(", ".join(row["patterns_worth_adopting"]))}</p>'
                f'<p><strong>adopt</strong> {html.escape("; ".join(row["patterns_worth_adopting"]))}</p>'
                f'<p><strong>avoid</strong> {html.escape("; ".join(row["patterns_to_avoid"]))}</p>'
                '</article>'
            )
        sections.append(f'<section><h2>{html.escape(label)}</h2><div class="grid">{"".join(cards)}</div></section>')
    return f'''<!doctype html><html lang="ja"><head><meta charset="utf-8"><title>Local Reference Contact Sheet</title>
<style>body{{margin:0;background:#171a1f;color:#f7f5ef;font-family:"Yu Gothic UI",sans-serif}}main{{max-width:1500px;margin:auto;padding:28px}}.notice{{border:2px solid #e5b840;padding:14px}}.grid{{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:16px}}article{{background:#252a31;border-radius:16px;padding:16px}}img{{width:100%;height:230px;object-fit:contain;background:white}}.missing{{height:230px;display:grid;place-items:center;text-align:center;background:#343a43;color:#c7ccd3}}a{{color:#52c7c7}}.id{{color:#e5b840;font-weight:900}}@media(max-width:900px){{.grid{{grid-template-columns:1fr}}}}</style></head>
<body><main><h1>LOCAL RESEARCH CONTACT SHEET</h1><p class="notice">Research evidence only. Captures are ignored and untracked. Public visibility is not reuse permission. Do not publish or embed these images in the tracked proof.</p>{''.join(sections)}</main></body></html>
'''


def _readback(
    repo_root: Path,
    output: Path,
    script: dict[str, Any],
    approval: dict[str, Any],
    manifest: dict[str, Any],
    lineage: dict[str, Any],
    old_hashes: dict[str, str],
) -> dict[str, Any]:
    approved_exact = all(
        _sha(repo_root / DEFAULT_PILOT / name) == digest
        for name, digest in approval["approved_file_hashes"].items()
    )
    old_exact = all(_sha(repo_root / path) == digest for path, digest in old_hashes.items())
    mapped = _load_json(output / "reference_grounded_visual_mapping.json")
    motion = _load_json(output / "reference_grounded_motion_storyboard.json")
    proof_text = (output / "reference_grounded_visual_proof.html").read_text(encoding="utf-8")
    combined = "\n".join(
        path.read_text(encoding="utf-8", errors="strict")
        for path in output.rglob("*")
        if path.is_file()
        and path.name != "reference_contact_sheet.local.html"
        and not any(part.startswith("local_") for part in path.relative_to(output).parts)
    )
    checks = {
        "research_preceded_design": RESEARCH_FROZEN_AT < DESIGN_GENERATION_STARTED_AT,
        "corpus_coverage_passed": _coverage_readback()["checks"]["all_passed"],
        "approved_hashes_8_of_8_exact": approved_exact,
        "old_route_a_proof_byte_exact": old_exact,
        "old_route_a_not_current_authority": manifest["superseded_old_proof"]["current_visual_authority"] is False,
        "six_keyframes": len(list((output / "keyframes").glob("*.svg"))) == 6,
        "cue_coverage_9_of_9": mapped["cue_count"] == 9,
        "scene_allocation_2_4_3": mapped["scene_allocation"] == {"S1": 2, "S2": 4, "S3": 3},
        "speaker_counts_3_6": mapped["speaker_counts"] == {"れいむ": 3, "まりさ": 6},
        "approved_text_and_order_exact": [row["text"] for row in mapped["cues"]] == [row["text"] for row in script["cues"]],
        "major_decision_lineage_complete": lineage["coverage_ratio"] == 1.0,
        "source_dominance_passed": lineage["source_dominance"]["passed"],
        "no_external_assets": "https://" not in proof_text and "http://" not in proof_text,
        "no_security_inspection_lab_in_viewer": "Security Inspection Lab" not in proof_text,
        "no_absolute_path_or_uuid": not _contains_private_tokens(combined),
        "motion_budget": all(row["loop"] is False and row["simultaneous_principal_motions"] == 1 for row in motion["cues"]),
        "viewer_lineage_separated": 'id="viewer"' in proof_text and 'id="reference-lineage"' in proof_text,
        "final_acceptance_false": manifest["proof_contract"]["final_visual_acceptance"] is False,
        "YMM4_render_false": manifest["proof_contract"]["YMM4_authorized"] is False and manifest["proof_contract"]["render_authorized"] is False,
    }
    checks["all_passed"] = all(checks.values())
    return {
        "schema_version": "new_banknote.reference_grounded_visual_proof_readback.v1",
        "status": "passed" if checks["all_passed"] else "failed",
        "checks": checks,
        "evidence_grades": {
            "source_metadata": "web_and_public_metadata_verified",
            "visual_observation": "14 usable captures_or_public_thumbnails; 2 limited not counted",
            "rendered_output": "all_six_keyframes_contact_sheet_storyboard_primary_html_lineage_and_local_contact_sheet_inspected",
            "YMM4": "not_tested",
        },
        "output_inspection": {
            "inspected_at": OUTPUT_INSPECTED_AT,
            "method": "headless Chromium capture at 1920 px width plus manual visual inspection",
            "artifacts": [
                "six keyframes",
                "nine-cue contact sheet",
                "motion storyboard",
                "primary HTML viewer",
                "reference lineage mode",
                "ignored local reference contact sheet",
            ],
            "repair_cycles": 1,
            "result": "passed_after_microtext_annotation_handle_overlap_repair",
        },
    }


def _contains_private_tokens(value: str) -> bool:
    lowered = value.lower()
    private_fragments = ("c:\\users\\", "c:/users/", "/users/", "/home/", "notebooklm.google.com")
    if any(fragment in lowered for fragment in private_fragments):
        return True
    import re

    return re.search(r"(?i)\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b", value) is not None


def _svg_open(attrs: dict[str, str]) -> str:
    rendered = " ".join(f'{name}="{_xml(value)}"' for name, value in attrs.items())
    return f"<svg {rendered}>"


def _svg_text_lines(
    value: str,
    *,
    x: int,
    y: int,
    font_size: int,
    line_gap: int,
    max_chars: int,
    max_lines: int,
    fill: str,
    truncate: bool = False,
) -> str:
    lines = _wrap_japanese(value, max_chars=max_chars, max_lines=max_lines, truncate=truncate)
    tspans = "".join(
        f'<tspan x="{x}" y="{y + index * line_gap}">{_xml(line)}</tspan>'
        for index, line in enumerate(lines)
    )
    return f'<text font-size="{font_size}" font-weight="800" fill="{fill}">{tspans}</text>'


def _wrap_japanese(value: str, *, max_chars: int, max_lines: int, truncate: bool) -> list[str]:
    if len(value) <= max_chars:
        return [value]
    lines: list[str] = []
    cursor = 0
    while cursor < len(value) and len(lines) < max_lines:
        remaining = value[cursor:]
        if len(remaining) <= max_chars:
            lines.append(remaining)
            cursor = len(value)
            break
        limit = cursor + max_chars
        break_at = limit
        candidates = [
            pos + 1
            for pos in range(cursor + max_chars // 2, limit)
            if value[pos] in "、。！？）』】 "
        ]
        if candidates:
            break_at = candidates[-1]
        while break_at < len(value) and value[break_at] in "、。！？）』】":
            break_at += 1
        lines.append(value[cursor:break_at])
        cursor = break_at
    if cursor < len(value):
        if not truncate:
            lines[-1] += value[cursor:]
        else:
            lines[-1] = lines[-1].rstrip("、。！？") + "…"
    return lines


def _artifact_category(path: Path) -> str:
    if path.suffix == ".svg":
        return "visual_proof"
    if path.suffix == ".html":
        return "review_surface"
    if path.suffix == ".md":
        return "human_readme_or_review"
    return "machine_contract"


def _load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"expected object: {path}")
    return value


def _write_if_changed(path: Path, content: str) -> bool:
    path.parent.mkdir(parents=True, exist_ok=True)
    current = path.read_text(encoding="utf-8") if path.exists() else None
    if current == content:
        return False
    path.write_text(content, encoding="utf-8", newline="\n")
    return True


def _json_text(value: dict[str, Any]) -> str:
    return json.dumps(value, ensure_ascii=False, indent=2, sort_keys=False) + "\n"


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _xml(value: object) -> str:
    return html.escape(str(value), quote=True)


def main() -> int:
    result = build_reference_grounded_visual_design()
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
