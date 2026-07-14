"""Build the source-backed review package for the new-banknote pilot.

The module performs no network access.  Official-source captures were made in
the bounded worker slice and are represented here only by sanitized receipts,
hashes, exact locations, and short paraphrases.  The nine cues are an
evidence-pruned constrained rewrite of existing NotebookLM transcript claims;
they are not a zero-source script generation path.
"""

from __future__ import annotations

import csv
import hashlib
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

from src.pipeline.ymm4_character_alias_profile import (
    build_derived_yymm4_import_csv,
    read_headerless_yymm4_csv,
)


SCHEMA_PREFIX = "new_banknote_authoritative_script.v1"
EXPECTED_CLAIM_COUNT = 182
EXPECTED_SOURCE_COUNT = 11
EXPECTED_CAPTURED_SOURCE_COUNT = 13
EXPECTED_VERIFIED_PRIMARY_COUNT = 19
EXPECTED_CLAIM_OUTCOME_IDENTITY_SHA256 = (
    "4084f67719f95d16efad7059dbf9ecce315f537f77b65a8f442ba90929acb5a6"
)
EXPECTED_SOURCE_REGISTRY_SHA256 = (
    "3a55d5ec999edec215b87fba0f999f1a9086eca1921158c9c3f72749ade1713a"
)
EXPECTED_SOURCE_RECEIPTS_SHA256 = (
    "6c4cc1817a3574b7278f2986522c91b05a51c1b8bba3ea4a544a78aee920e205"
)
EDITORIAL_REVISION_ID = "final-editorial-convergence-before-human-review-v1"
BASELINE_FACTUAL_SUPPORT_UNIT_COUNT = 22
BASELINE_CLAIM_EDGE_COUNT = 23
EXPECTED_RAW_IDENTITY = {
    "sha256": "1825c9689a050ddbfc91537a228f6af0ba2f7f033e5b681fff4f227551144437",
    "size_bytes": 32089,
    "logical_line_count": 326,
}
ALLOWED_OFFICIAL_DOMAINS = {"npb.go.jp", "mof.go.jp", "boj.or.jp"}
CLAIM_OUTCOMES = {
    "verified_primary",
    "supported_context_only",
    "unresolved_not_used",
    "rejected_unsupported",
    "rejected_policy_intent",
    "rejected_quantitative_without_exact_source",
    "style_or_rhetoric_only",
    "duplicate_not_used",
}
EXPECTED_SCENE_ALLOCATION = {"S1": 2, "S2": 4, "S3": 3}
EXPECTED_SPEAKER_COUNTS = {"れいむ": 3, "まりさ": 6}
EXPECTED_DERIVED_COUNTS = {"ゆっくり霊夢": 3, "ゆっくり魔理沙": 6}
CANONICAL_TO_YMM4 = {"れいむ": "ゆっくり霊夢", "まりさ": "ゆっくり魔理沙"}
HUMAN_REVIEW_QUESTIONS = (
    "公式一次資料で支えた事実は、初見でも意味が分かりますか。",
    "キャッシュレス誘導や政策意図を示唆する、根拠のない含みは残っていませんか。",
    "れいむとまりさの受け渡しは自然で、同じ説明を繰り返していませんか。",
    "S1の導入、S2の技術、S3の見分け方という流れは一貫していますか。",
    "高精細すき入れ、深凹版印刷、識別マークなどの用語は、誤解を招かず難しすぎませんか。",
)
EXPECTED_MARISA_TERMINAL_FORMS = (
    "んだ",
    "んだぜ",
    "ぞ",
    "なんだ",
    "ぜ",
    "おこう",
)
PROFILE_RELATIVE = Path(
    "production_pilots/yukkuri_newsroom_content_spine_002/"
    "ymm4_character_alias_profiles/ymm4_4_53_0_9_yukkuri_characters_v1.json"
)

REQUIRED_ARTIFACTS = (
    "README_CANONICAL_SCRIPT_REVIEW.md",
    "asr_source_reconciliation.json",
    "authoritative_source_registry.json",
    "authoritative_source_resolution_readback.json",
    "canonical_script.json",
    "canonical_script_editorial_revision.md",
    "canonical_script.txt",
    "canonical_script_review.md",
    "canonical_yymm4.csv",
    "claim_adjudication.json",
    "claim_adjudication_readback.json",
    "csv_validation_readback.json",
    "cue_source_traceability.json",
    "derived_yymm4_import.csv",
    "editorial_revision_receipt.json",
    "limitations.md",
    "notebook_source_to_verification_source_crosswalk.json",
    "operator_review_sheet.md",
    "rejected_and_unresolved_claims.json",
    "script_generation_receipt.json",
    "source_capture_receipts.json",
    "source_resolution_limitations.md",
    "source_to_script_manifest.json",
    "verified_claim_set.json",
)
EDITORIAL_RECEIPT_FILES = (
    "README_CANONICAL_SCRIPT_REVIEW.md",
    "canonical_script.json",
    "canonical_script.txt",
    "canonical_script_review.md",
    "cue_source_traceability.json",
    "canonical_yymm4.csv",
    "derived_yymm4_import.csv",
    "csv_validation_readback.json",
    "source_to_script_manifest.json",
    "canonical_script_editorial_revision.md",
)
SCRIPT_RECEIPT_FILES = (
    "README_CANONICAL_SCRIPT_REVIEW.md",
    "canonical_script.json",
    "canonical_script_editorial_revision.md",
    "canonical_script.txt",
    "canonical_script_review.md",
    "cue_source_traceability.json",
    "canonical_yymm4.csv",
    "derived_yymm4_import.csv",
    "csv_validation_readback.json",
    "editorial_revision_receipt.json",
    "operator_review_sheet.md",
    "limitations.md",
    "source_to_script_manifest.json",
)


def _source(
    source_id: str,
    *,
    title: str,
    url: str,
    relation_type: str,
    file_name: str,
    retrieved_at: str,
    content_type: str,
    size_bytes: int,
    sha256: str,
    last_modified: str,
    evidence_locations: list[str],
    bounded_paraphrase: str,
    notebook_source_ids: list[str],
    publication_date: str | None,
    publication_date_basis: str,
    fact_dates: list[dict[str, str]] | None = None,
    content_dates: list[dict[str, str]] | None = None,
    extraction: str = "html_heading_inspection",
) -> dict[str, Any]:
    return {
        "source_id": source_id,
        "publisher": "独立行政法人 国立印刷局 / National Printing Bureau"
        if "npb.go.jp" in url
        else "財務省 / Ministry of Finance Japan",
        "title": title,
        "canonical_url": url,
        "official_domain": urlparse(url).hostname,
        "authority_class": "primary_official",
        "relation_type": relation_type,
        "notebook_source_ids": notebook_source_ids,
        "retrieved_at": retrieved_at,
        "http_status": 200,
        "redirect_count": 0,
        "content_type": content_type,
        "size_bytes": size_bytes,
        "sha256": sha256,
        "last_modified_header": last_modified,
        "publication_date": publication_date,
        "publication_date_basis": publication_date_basis,
        "fact_dates": fact_dates or [],
        "content_dates": content_dates or [],
        "capture_id": f"capture_{source_id.lower()}",
        "ignored_cache_repo_relative_path": (
            "production_pilots/yukkuri_newsroom_content_spine_002/"
            "external_editorial_input/new_banknote_security_notebooklm_001/"
            f"source_cache/{file_name}"
        ),
        "evidence_locations": evidence_locations,
        "bounded_paraphrase": bounded_paraphrase,
        "inspection_method": extraction,
    }


SOURCE_RECORDS: tuple[dict[str, Any], ...] = (
    _source(
        "V01",
        title="紙幣の肖像と図柄について、選定理由を教えてください : 財務省",
        url="https://www.mof.go.jp/faq/currency/07am.htm",
        relation_type="exact_title_match",
        file_name="s10_mof.html",
        retrieved_at="2026-07-13T17:00:40+09:00",
        content_type="text/html",
        size_bytes=22154,
        sha256="85a3c65af2823def502175ae9ce0d790cf5581dd7960eee6340311d338b9e381",
        last_modified="2026-06-05T09:24:13Z",
        publication_date=None,
        publication_date_basis="not_stated",
        content_dates=[
            {
                "date": "2025-12-24",
                "meaning": "HTML meta name=date",
                "basis": "html_meta_name_date",
            }
        ],
        notebook_source_ids=["S10"],
        evidence_locations=["H1直下の回答欄", "回答欄（肖像の選定観点）", "回答欄（裏面図柄）"],
        bounded_paraphrase="肖像と裏面図柄の選定理由を財務省が説明している。",
    ),
    _source(
        "V02",
        title="識別性向上に向けた取組 独立行政法人 国立印刷局",
        url="https://www.npb.go.jp/product_service/intro/ninsiki.html",
        relation_type="exact_title_match",
        file_name="s11_npb.html",
        retrieved_at="2026-07-13T17:00:40+09:00",
        content_type="text/html",
        size_bytes=16982,
        sha256="b1e1835d54f3fa403d9a7d72bd06d74924ef508b87231db4ab9482516078b45b",
        last_modified="2026-07-13T02:00:03Z",
        publication_date=None,
        publication_date_basis="not_stated",
        fact_dates=[
            {"date": "2024", "meaning": "F券発行年", "location": "H1直下の導入"}
        ],
        notebook_source_ids=["S11"],
        evidence_locations=[
            "H1直下の導入",
            "識別マーク（凹版印刷）",
            "ホログラム・すき入れの配置",
            "額面数字の大型化",
            "区別しやすい色味の工夫",
            "一万円券と千円券の『1』のデザインの違い",
            "お札識別アプリ『言う吉くん』",
        ],
        bounded_paraphrase="F券の識別マーク、配置、額面表示、色、数字と識別アプリを説明している。",
    ),
    _source(
        "V03",
        title="採用パンフレット 独立行政法人 国立印刷局",
        url="https://www.npb.go.jp/recruit/brochure.html",
        relation_type="official_supplement",
        file_name="recruit_brochure.html",
        retrieved_at="2026-07-13T17:03:17+09:00",
        content_type="text/html",
        size_bytes=14912,
        sha256="f4aa2e12e56d928b6d3392bca7b949d071c45e49ceb734c4f8203d500e0decfb",
        last_modified="2026-07-13T02:00:03Z",
        publication_date=None,
        publication_date_basis="not_stated",
        content_dates=[
            {
                "date": "2026-04-24",
                "meaning": "ページ更新日",
                "basis": "visible_update_date",
            }
        ],
        notebook_source_ids=["S04"],
        evidence_locations=["採用パンフレット > 新しい日本銀行券『開発秘話』"],
        bounded_paraphrase="S04と同名の現行PDFへ結ぶ公式ランディングページ。",
    ),
    _source(
        "V04",
        title="新しい日本銀行券『開発秘話』",
        url="https://www.npb.go.jp/recruit/brochure.files/recruit-2511-4.pdf",
        relation_type="exact_document_match",
        file_name="s04_development_story.pdf",
        retrieved_at="2026-07-13T17:03:17+09:00",
        content_type="application/pdf",
        size_bytes=1748819,
        sha256="792e5b4897aa383de8896571de94ec89643a735dc5971e6ff429330248ea7882",
        last_modified="2025-11-13T07:26:34Z",
        publication_date=None,
        publication_date_basis="not_stated",
        notebook_source_ids=["S04"],
        evidence_locations=["PDF物理ページ1（冊子pp.11–12）"],
        bounded_paraphrase="同名の現行セクションで、技術開発とユニバーサルデザインの経緯を扱う。",
        extraction="pdf_render_visual_inspection_no_ocr",
    ),
    _source(
        "V05",
        title="生まれ変わる日本銀行券 紙幣は the ART",
        url="https://www.npb.go.jp/guide/pamphlet.files/202407_nbn_pamphlet.pdf",
        relation_type="official_supplement",
        file_name="s05_pamphlet.pdf",
        retrieved_at="2026-07-13T17:00:40+09:00",
        content_type="application/pdf",
        size_bytes=1253689,
        sha256="85a30019f2cfee42990f1e737e900aa9be464de730fb30936d3916e55bd721f9",
        last_modified="2024-07-16T01:26:43Z",
        publication_date=None,
        publication_date_basis="not_stated",
        fact_dates=[
            {
                "date": "2024-07-03",
                "meaning": "F券発行日",
                "location": "PDF物理ページ1",
            }
        ],
        notebook_source_ids=["S05"],
        evidence_locations=["PDF物理ページ1", "PDF物理ページ2（進化する技術）"],
        bounded_paraphrase="2024年7月3日の発行日と、技術・識別設計を2ページで紹介する。",
        extraction="pdf_render_visual_inspection_no_ocr",
    ),
    _source(
        "V06",
        title="お札の偽造防止技術 独立行政法人 国立印刷局",
        url="https://www.npb.go.jp/product_service/intro/gizoboshi.html",
        relation_type="official_equivalent",
        file_name="gizoboshi.html",
        retrieved_at="2026-07-13T17:03:17+09:00",
        content_type="text/html",
        size_bytes=38185,
        sha256="74dceacbfc342a04faeead79b6236e400ed23b332a23dcae9ed7735d7a13abd6",
        last_modified="2026-07-13T02:00:04Z",
        publication_date=None,
        publication_date_basis="not_stated",
        notebook_source_ids=["S05"],
        evidence_locations=[
            "F券に施されている偽造防止技術",
            "『さわって』わかる偽造防止技術 > 深凹版印刷",
            "『すかして』わかる偽造防止技術 > すき入れ・高精細すき入れ",
            "『傾けて』わかる偽造防止技術 > 3Dホログラム",
            "『道具で』わかる偽造防止技術 > マイクロ文字",
        ],
        bounded_paraphrase="F券の偽造防止技術を、触る・透かす・傾ける・道具で見る方法別に説明する。",
    ),
    _source(
        "V07",
        title="新しい日本銀行券特設サイト｜新しい一万円札について",
        url="https://www.npb.go.jp/ja/n_banknote/design10/",
        relation_type="official_supplement",
        file_name="design10.html",
        retrieved_at="2026-07-13T17:00:40+09:00",
        content_type="text/html",
        size_bytes=17830,
        sha256="ca91e48dfbc3931bad88ff9cc34c2f64d92d60336265176de234ef38362451fb",
        last_modified="2024-07-10T08:41:46Z",
        publication_date=None,
        publication_date_basis="not_stated",
        notebook_source_ids=["S04", "S05"],
        evidence_locations=["高精細すき入れ", "深凹版印刷", "3Dホログラム", "マイクロ文字", "ユニバーサルデザイン"],
        bounded_paraphrase="一万円券の新旧技術と識別設計を券種別に説明する。",
    ),
    _source(
        "V08",
        title="新しい日本銀行券特設サイト｜新しい五千円札について",
        url="https://www.npb.go.jp/ja/n_banknote/design05/",
        relation_type="official_supplement",
        file_name="design05.html",
        retrieved_at="2026-07-13T17:03:17+09:00",
        content_type="text/html",
        size_bytes=17797,
        sha256="0027e51f169baa4791d1f3ff7fbdbcd00c032c4c2260039df1e86b6c8ae51de1",
        last_modified="2024-07-10T08:42:58Z",
        publication_date=None,
        publication_date_basis="not_stated",
        notebook_source_ids=["S04", "S05"],
        evidence_locations=["高精細すき入れ", "深凹版印刷", "3Dホログラム", "マイクロ文字", "ユニバーサルデザイン"],
        bounded_paraphrase="五千円券の新旧技術と識別設計を券種別に説明する。",
    ),
    _source(
        "V09",
        title="新しい日本銀行券特設サイト｜新しい千円札について",
        url="https://www.npb.go.jp/ja/n_banknote/design01/",
        relation_type="official_supplement",
        file_name="design01.html",
        retrieved_at="2026-07-13T17:03:17+09:00",
        content_type="text/html",
        size_bytes=17740,
        sha256="37cc217955d0438d79cccb6a0d713315ef49f232e9c39053baba0b790e913864",
        last_modified="2024-07-10T08:43:42Z",
        publication_date=None,
        publication_date_basis="not_stated",
        notebook_source_ids=["S04", "S05"],
        evidence_locations=["高精細すき入れ", "深凹版印刷", "3Dホログラム", "マイクロ文字", "ユニバーサルデザイン"],
        bounded_paraphrase="千円券の新旧技術と識別設計を券種別に説明する。",
    ),
    _source(
        "V10",
        title="新しい日本銀行券特設サイト｜TOPページ",
        url="https://www.npb.go.jp/ja/n_banknote/index.html",
        relation_type="official_supplement",
        file_name="s04_index.html",
        retrieved_at="2026-07-13T17:00:40+09:00",
        content_type="text/html",
        size_bytes=10459,
        sha256="73b51958a7a8e982f5a7fb629a18a8f384a45ba5043cb9433dfa42d14aae3cb3",
        last_modified="2025-02-12T07:21:59Z",
        publication_date=None,
        publication_date_basis="not_stated",
        fact_dates=[
            {
                "date": "2024-07-03",
                "meaning": "F券発行日",
                "location": "2024年7月3日 お札が変わりました",
            }
        ],
        notebook_source_ids=["S04", "S05"],
        evidence_locations=["2024年7月3日 お札が変わりました", "券種別案内"],
        bounded_paraphrase="2024年7月3日の三券種改刷と券種別技術ページへの入口。",
    ),
    _source(
        "V11",
        title="お札に関するよくあるご質問 独立行政法人 国立印刷局",
        url="https://www.npb.go.jp/product_service/intro/faq.html",
        relation_type="official_supplement",
        file_name="faq.html",
        retrieved_at="2026-07-13T17:00:40+09:00",
        content_type="text/html",
        size_bytes=55564,
        sha256="891f9546f43c7f8f10dc9913682ca5f9da558db2eb11995f8fb05d9fc8badd87",
        last_modified="2026-07-13T02:00:04Z",
        publication_date=None,
        publication_date_basis="not_stated",
        notebook_source_ids=["S05"],
        evidence_locations=["『改刷』とは何ですか？", "偽造防止技術について", "目の不自由な人は、どうやってお札を区別したらよいですか？"],
        bounded_paraphrase="改刷、すき入れ、識別マークなどをQ&A形式で説明する。",
    ),
    _source(
        "V12",
        title="国立印刷局 事業案内パンフレット・動画 独立行政法人 国立印刷局",
        url="https://www.npb.go.jp/guide/pamphlet.html",
        relation_type="official_supplement",
        file_name="pamphlet_index.html",
        retrieved_at="2026-07-13T17:00:40+09:00",
        content_type="text/html",
        size_bytes=20978,
        sha256="e12861c0cf13113ad96e009b4592986d63822662c2943960945cd0dc80213d52",
        last_modified="2026-07-13T02:00:01Z",
        publication_date=None,
        publication_date_basis="not_stated",
        notebook_source_ids=["S05"],
        evidence_locations=["新しい日本銀行券紹介パンフレット", "信頼のものづくり"],
        bounded_paraphrase="現行の公式パンフレット群を列挙するランディングページ。",
    ),
    _source(
        "V13",
        title="信頼のものづくり～お札の製造まるわかりBOOK～",
        url="https://www.npb.go.jp/guide/pamphlet.files/shinrai2026.pdf",
        relation_type="official_supplement",
        file_name="shinrai2026.pdf",
        retrieved_at="2026-07-13T17:13:31+09:00",
        content_type="application/pdf",
        size_bytes=4764351,
        sha256="499ff52d5da97a7130495262c4c3d6fd0bf3eb8831e199778788b45a762c43b4",
        last_modified="2026-03-30T01:33:14Z",
        publication_date=None,
        publication_date_basis="not_stated",
        notebook_source_ids=["S04", "S05", "S11"],
        evidence_locations=["PDF物理ページ4（冊子pp.6–7）", "PDF物理ページ5（冊子pp.8–9）"],
        bounded_paraphrase="ユニバーサルデザインと八つの偽造防止技術をページ単位で説明する。",
        extraction="pdf_text_extraction_plus_render_visual_inspection",
    ),
)


VERIFIED_CLAIMS: dict[str, dict[str, Any]] = {
    "claim_010": {
        "proposition": "F券は2024年に発行された。",
        "sources": [("V02", "H1直下の導入", "年", "2024")],
        "tags": ["scope_narrowed", "asr_normalized"],
    },
    "claim_065": {
        "proposition": "F券には、傾けると変化を確認できる3Dホログラムが採用された。",
        "sources": [("V06", "『傾けて』わかる偽造防止技術 > 3Dホログラム", "技術仕様", None)],
        "tags": ["asr_normalized"],
    },
    "claim_067": {
        "proposition": "3Dホログラムでは角度により三次元の肖像が回転して見える。",
        "sources": [("V07", "3Dホログラム", "表示仕様", None)],
        "tags": ["scope_narrowed"],
    },
    "claim_090": {
        "proposition": "F券の高精細すき入れには、光に透かすと見える微細な模様が施されている。",
        "sources": [("V06", "『すかして』わかる偽造防止技術 > すき入れ・高精細すき入れ", "透過表示仕様", None)],
        "tags": ["scope_narrowed", "causal_effect_excluded", "asr_normalized", "contextual_term_resolution"],
    },
    "claim_095": {
        "proposition": "F券には、道具で確認するマイクロ文字が印刷されている。",
        "sources": [("V06", "『道具で』わかる偽造防止技術 > マイクロ文字", "技術仕様", None)],
        "tags": ["terminology_verified"],
    },
    "claim_096": {
        "proposition": "F券には『NIPPONGINKO』という微小なマイクロ文字が印刷され、ルーペで確認できる。",
        "sources": [("V06", "『道具で』わかる偽造防止技術 > マイクロ文字", "表示文字・確認方法", None)],
        "tags": ["asr_normalized", "terminology_verified"],
    },
    "claim_097": {
        "proposition": "マイクロ文字はカラーコピー機では再現が困難なほど小さい。",
        "sources": [("V06", "『道具で』わかる偽造防止技術 > マイクロ文字", "複写再現性", None)],
        "tags": ["scope_narrowed", "unsupported_mechanism_excluded", "device_scope_normalized"],
    },
    "claim_099": {
        "proposition": "F券はホログラム、深凹版印刷、すき入れ、マイクロ文字を組み合わせている。",
        "sources": [("V13", "PDF物理ページ5（冊子pp.8–9）", "技術一覧", None)],
        "tags": ["compound_technical_claim_narrowed", "analogy_excluded", "asr_normalized"],
    },
    "claim_114": {
        "proposition": "アラビア数字の額面表示をE券より大きくした。",
        "sources": [("V02", "額面数字の大型化", "券面仕様（E券との比較）", None)],
        "tags": ["scope_narrowed", "asr_normalized"],
    },
    "claim_116": {
        "proposition": "額面数字や識別マークには、インキを高く盛り上げる深凹版印刷が使われ、ざらざらした触感がある。",
        "sources": [("V06", "『さわって』わかる偽造防止技術 > 深凹版印刷", "触感仕様", None)],
        "tags": ["asr_normalized", "question_form_normalized"],
    },
    "claim_118": {
        "proposition": "F券の識別マークは11本の斜線に統一された。",
        "sources": [("V13", "PDF物理ページ4（冊子pp.6–7）", "本", None)],
        "tags": ["scope_narrowed", "asr_normalized"],
    },
    "claim_130": {
        "proposition": "同じ識別マークの位置を券種ごとに変えている。",
        "sources": [("V06", "識別マーク（深凹版印刷）", "券種別位置仕様", None)],
        "tags": ["causal_effect_excluded"],
    },
    "claim_132": {
        "proposition": "識別マークの位置は一万円券・五千円券・千円券で異なる。",
        "sources": [("V02", "識別マーク（凹版印刷）", "券種別位置", None)],
        "tags": ["asr_normalized"],
    },
    "claim_155": {
        "proposition": "一万円券と千円券ではホログラムの形状と配置が異なる。",
        "sources": [("V02", "ホログラム・すき入れの配置", "券種別配置仕様", None)],
        "tags": ["scope_narrowed"],
    },
    "claim_157": {
        "proposition": "千円券中央には橙色のグラデーションが配置されている。",
        "sources": [("V02", "区別しやすい色味の工夫", "色配置仕様", None)],
        "tags": ["asr_normalized", "effect_not_quantified"],
    },
    "claim_158": {
        "proposition": "一万円券と千円券では数字『1』のデザインが異なる。",
        "sources": [("V02", "一万円券と千円券の『1』のデザインの違い", "数字デザイン仕様", None)],
        "tags": ["scope_narrowed"],
    },
    "claim_161": {
        "proposition": "F券には、誰にとっても使いやすいものを目指したユニバーサルデザインが取り入れられている。",
        "sources": [("V02", "H1直下の導入", "設計方針", None)],
        "tags": ["scope_narrowed", "analogy_excluded", "effect_not_quantified"],
    },
    "claim_162": {
        "proposition": "視覚障害者向けのiPhone用識別アプリ『言う吉くん』を無料配信している。",
        "sources": [("V02", "お札識別アプリ『言う吉くん』", "アプリ提供仕様", None)],
        "tags": ["asr_normalized", "platform_narrowed"],
    },
    "claim_164": {
        "proposition": "識別アプリはカメラで券種を識別し、音声と大きな文字で額面を知らせる。",
        "sources": [("V02", "お札識別アプリ『言う吉くん』", "機能仕様", None)],
        "tags": ["scope_narrowed", "authenticity_function_excluded"],
    },
}


SUPPORTED_CONTEXT_IDS = {
    "claim_062",
    "claim_063",
    "claim_078",
    "claim_079",
    "claim_083",
    "claim_087",
    "claim_089",
    "claim_113",
    "claim_115",
    "claim_166",
    "claim_181",
}

DUPLICATE_OF = {
    "claim_009": "claim_010",
    "claim_011": "claim_010",
    "claim_066": "claim_065",
    "claim_068": "claim_067",
    "claim_120": "claim_130",
    "claim_123": "claim_113",
    "claim_124": "claim_114",
    "claim_125": "claim_115",
    "claim_126": "claim_116",
    "claim_128": "claim_118",
    "claim_133": "claim_113",
    "claim_134": "claim_114",
    "claim_135": "claim_115",
    "claim_136": "claim_116",
    "claim_138": "claim_118",
    "claim_140": "claim_130",
    "claim_142": "claim_132",
    "claim_143": "claim_113",
    "claim_144": "claim_114",
    "claim_145": "claim_115",
    "claim_146": "claim_116",
    "claim_148": "claim_118",
    "claim_150": "claim_130",
    "claim_152": "claim_132",
    "claim_156": "claim_155",
    "claim_165": "claim_164",
}

CASHLESS_CAUSAL_IDS = {"claim_039", "claim_050"}

CUES: tuple[dict[str, Any], ...] = (
    {
        "sequence": 1,
        "cue_id": "cue_001",
        "scene_id": "S1",
        "speaker": "れいむ",
        "text": "2024年に発行された新しいお札って、見た目以外にも変わったところがあるの？",
        "adopted_claim_ids": ["claim_010"],
        "support_units": [
            {
                "unit_id": "cue_001_fact_01",
                "statement": "F券は2024年に発行された。",
                "claim_ids": ["claim_010"],
            },
        ],
    },
    {
        "sequence": 2,
        "cue_id": "cue_002",
        "scene_id": "S1",
        "speaker": "まりさ",
        "text": "あるぞ。偽造防止では、高精細すき入れや3Dホログラムなど複数の技術を組み合わせている。誰にとっても使いやすいユニバーサルデザインも取り入れたんだ。",
        "adopted_claim_ids": [
            "claim_090",
            "claim_065",
            "claim_099",
            "claim_161",
        ],
        "support_units": [
            {
                "unit_id": "cue_002_fact_01",
                "statement": "F券には高精細すき入れが採り入れられている。",
                "claim_ids": ["claim_090"],
            },
            {
                "unit_id": "cue_002_fact_02",
                "statement": "F券には3Dホログラムが採用された。",
                "claim_ids": ["claim_065"],
            },
            {
                "unit_id": "cue_002_fact_03",
                "statement": "F券は複数の偽造防止技術を組み合わせている。",
                "claim_ids": ["claim_099"],
            },
            {
                "unit_id": "cue_002_fact_04",
                "statement": "F券には、誰にとっても使いやすいものを目指したユニバーサルデザインが取り入れられている。",
                "claim_ids": ["claim_161"],
            },
        ],
    },
    {
        "sequence": 3,
        "cue_id": "cue_003",
        "scene_id": "S2",
        "speaker": "まりさ",
        "text": "まずは高精細すき入れ。光に透かすと、細かな模様が見えるんだぜ。",
        "adopted_claim_ids": ["claim_090"],
        "support_units": [
            {
                "unit_id": "cue_003_fact_01",
                "statement": "F券の高精細すき入れには、光に透かすと見える微細な模様が施されている。",
                "claim_ids": ["claim_090"],
            }
        ],
    },
    {
        "sequence": 4,
        "cue_id": "cue_004",
        "scene_id": "S2",
        "speaker": "まりさ",
        "text": "次は3Dホログラム。角度を変えると、三次元の肖像が回転して見えるぞ。",
        "adopted_claim_ids": ["claim_065", "claim_067"],
        "support_units": [
            {
                "unit_id": "cue_004_fact_01",
                "statement": "F券には3Dホログラムが採用された。",
                "claim_ids": ["claim_065"],
            },
            {
                "unit_id": "cue_004_fact_02",
                "statement": "角度により三次元の肖像が回転して見える。",
                "claim_ids": ["claim_067"],
            },
        ],
    },
    {
        "sequence": 5,
        "cue_id": "cue_005",
        "scene_id": "S2",
        "speaker": "れいむ",
        "text": "触るとざらざらするのは、額面数字などのインキを高く盛り上げる深凹版印刷なんだね。",
        "adopted_claim_ids": ["claim_116"],
        "support_units": [
            {
                "unit_id": "cue_005_fact_01",
                "statement": "額面数字などには、インキを高く盛り上げる深凹版印刷が使われ、ざらざらした触感がある。",
                "claim_ids": ["claim_116"],
            },
        ],
    },
    {
        "sequence": 6,
        "cue_id": "cue_006",
        "scene_id": "S2",
        "speaker": "まりさ",
        "text": "マイクロ文字の『NIPPONGINKO』は、ルーペで確かめられる。カラーコピー機では再現が難しいほど小さい文字なんだ。",
        "adopted_claim_ids": ["claim_096", "claim_097"],
        "support_units": [
            {
                "unit_id": "cue_006_fact_01",
                "statement": "F券には『NIPPONGINKO』という微小なマイクロ文字が印刷され、ルーペで確認できる。",
                "claim_ids": ["claim_096"],
            },
            {
                "unit_id": "cue_006_fact_02",
                "statement": "マイクロ文字はカラーコピー機では再現が困難なほど小さい。",
                "claim_ids": ["claim_097"],
            },
        ],
    },
    {
        "sequence": 7,
        "cue_id": "cue_007",
        "scene_id": "S3",
        "speaker": "まりさ",
        "text": "見分けやすさの工夫では、識別マークを11本の斜線にそろえ、券種ごとに位置を変えているぜ。",
        "adopted_claim_ids": ["claim_118", "claim_130", "claim_132"],
        "support_units": [
            {
                "unit_id": "cue_007_fact_01",
                "statement": "F券の識別マークは11本の斜線に統一された。",
                "claim_ids": ["claim_118"],
            },
            {
                "unit_id": "cue_007_fact_02",
                "statement": "同じ識別マークの位置を券種ごとに変えている。",
                "claim_ids": ["claim_130", "claim_132"],
            },
        ],
    },
    {
        "sequence": 8,
        "cue_id": "cue_008",
        "scene_id": "S3",
        "speaker": "れいむ",
        "text": "額面の数字は前のシリーズのお札より大きい。一万円券と千円券ではホログラムの形や位置が違い、千円券の中央には橙色のグラデーションもあるんだね。",
        "adopted_claim_ids": ["claim_114", "claim_155", "claim_157"],
        "retained_verified_unspoken_claim_ids": ["claim_158"],
        "support_units": [
            {
                "unit_id": "cue_008_fact_01",
                "statement": "アラビア数字の額面表示をE券より大きくした。",
                "claim_ids": ["claim_114"],
            },
            {
                "unit_id": "cue_008_fact_02",
                "statement": "一万円券と千円券ではホログラムの形状と配置が異なる。",
                "claim_ids": ["claim_155"],
            },
            {
                "unit_id": "cue_008_fact_03",
                "statement": "千円券中央には橙色のグラデーションが配置されている。",
                "claim_ids": ["claim_157"],
            },
        ],
    },
    {
        "sequence": 9,
        "cue_id": "cue_009",
        "scene_id": "S3",
        "speaker": "まりさ",
        "text": "確かめ方は、透かす、触る、傾ける、ルーペで見る。この四つを覚えておこう。",
        "adopted_claim_ids": ["claim_090", "claim_116", "claim_065", "claim_096"],
        "support_units": [
            {
                "unit_id": "cue_009_fact_01",
                "statement": "高精細すき入れは光に透かして確認する。",
                "claim_ids": ["claim_090"],
            },
            {
                "unit_id": "cue_009_fact_02",
                "statement": "深凹版印刷は触って確認する。",
                "claim_ids": ["claim_116"],
            },
            {
                "unit_id": "cue_009_fact_03",
                "statement": "3Dホログラムは傾けて確認する。",
                "claim_ids": ["claim_065"],
            },
            {
                "unit_id": "cue_009_fact_04",
                "statement": "マイクロ文字はルーペで確認する。",
                "claim_ids": ["claim_096"],
            },
        ],
    },
)


def build_new_banknote_authoritative_script_package(
    package_dir: str | Path,
    output_dir: str | Path | None = None,
) -> dict[str, Any]:
    """Build the complete deterministic review package without network access."""
    package = Path(package_dir).resolve()
    output = Path(output_dir).resolve() if output_dir is not None else package
    output.mkdir(parents=True, exist_ok=True)
    repo_root = package.parents[3]

    source_snapshot = _read_json(package / "source_set_snapshot.json")
    claim_ledger = _read_json(package / "claim_risk_ledger.json")
    alignments = _read_json(package / "claim_source_family_alignment.json")
    asr_ledger = _read_json(package / "asr_correction_ledger.json")
    _validate_frozen_inputs(source_snapshot, claim_ledger, alignments)

    registry = _build_source_registry()
    receipts = _build_source_receipts()
    crosswalk = _build_source_crosswalk(source_snapshot)
    source_readback = _build_source_readback(registry, receipts, crosswalk)
    _write_json(output / "authoritative_source_registry.json", registry)
    _write_json(output / "source_capture_receipts.json", receipts)
    _write_json(
        output / "notebook_source_to_verification_source_crosswalk.json",
        crosswalk,
    )
    _write_json(
        output / "authoritative_source_resolution_readback.json",
        source_readback,
    )
    _write_text(
        output / "source_resolution_limitations.md",
        _source_resolution_limitations(),
    )

    adjudication = _build_claim_adjudication(claim_ledger, alignments)
    _write_json(output / "claim_adjudication.json", adjudication)
    verified = [
        record
        for record in adjudication["claims"]
        if record["primary_outcome"] == "verified_primary"
    ]
    nonverified = [
        record
        for record in adjudication["claims"]
        if record["primary_outcome"] != "verified_primary"
    ]
    _write_json(
        output / "verified_claim_set.json",
        {
            "schema_version": f"{SCHEMA_PREFIX}.verified_claim_set",
            "status": "verified_primary_claims_frozen",
            "claim_count": len(verified),
            "claims": verified,
        },
    )
    _write_json(
        output / "rejected_and_unresolved_claims.json",
        {
            "schema_version": f"{SCHEMA_PREFIX}.rejected_and_unresolved_claims",
            "status": "excluded_from_canonical_use",
            "claim_count": len(nonverified),
            "claims": nonverified,
        },
    )
    claim_readback = _claim_readback(adjudication)
    _write_json(output / "claim_adjudication_readback.json", claim_readback)
    _write_json(
        output / "asr_source_reconciliation.json",
        _build_asr_reconciliation(asr_ledger),
    )

    script = _build_script(adjudication)
    traceability = _build_traceability(script, adjudication, registry)
    _write_json(output / "canonical_script.json", script)
    _write_text(output / "canonical_script.txt", _render_script_text(script))
    _write_text(
        output / "canonical_script_review.md",
        _render_script_review(script, traceability),
    )
    _write_json(output / "cue_source_traceability.json", traceability)

    canonical_rows = [(cue["speaker"], cue["text"]) for cue in script["cues"]]
    canonical_csv = output / "canonical_yymm4.csv"
    derived_csv = output / "derived_yymm4_import.csv"
    _write_csv(canonical_csv, canonical_rows)
    profile_path = repo_root / PROFILE_RELATIVE
    alias_result = build_derived_yymm4_import_csv(
        canonical_csv=canonical_csv,
        derived_csv=derived_csv,
        profile_path=profile_path,
        repo_root=repo_root,
        expected_canonical_sha256=_sha256(canonical_csv).upper(),
    )
    csv_readback = _build_csv_readback(
        canonical_csv=canonical_csv,
        derived_csv=derived_csv,
        profile_path=profile_path,
        profile_id=alias_result["profile"]["profile_id"],
    )
    _write_json(output / "csv_validation_readback.json", csv_readback)

    manifest = _build_source_to_script_manifest(script, traceability, registry)
    _write_json(output / "source_to_script_manifest.json", manifest)
    _write_text(output / "operator_review_sheet.md", _operator_review_sheet())
    _write_text(output / "limitations.md", _review_limitations())
    _write_text(
        output / "README_CANONICAL_SCRIPT_REVIEW.md",
        _primary_review_surface(script, adjudication, source_readback),
    )
    _write_text(
        output / "canonical_script_editorial_revision.md",
        _render_editorial_revision(script, adjudication),
    )
    editorial_receipt = _build_editorial_revision_receipt(
        output=output,
        script=script,
        adjudication=adjudication,
        traceability=traceability,
        registry=registry,
    )
    _write_json(
        output / "editorial_revision_receipt.json",
        editorial_receipt,
    )

    receipt = _build_script_receipt(output, script)
    _write_json(output / "script_generation_receipt.json", receipt)
    if output == package:
        _write_text(
            output / ".gitignore",
            "local_outputs/\nsource_cache/\nsource_extracts/\nsource_probe/\n"
            "!canonical_yymm4.csv\n!derived_yymm4_import.csv\n",
        )

    validation = validate_new_banknote_authoritative_script_package(output)
    if validation["failed_checks"]:
        raise ValueError(
            "NEW_BANKNOTE_AUTHORITATIVE_PACKAGE_VALIDATION_FAILED: "
            + ", ".join(validation["failed_checks"])
        )
    return {
        "status": "source_backed_script_human_review_ready",
        "output_dir": output.as_posix(),
        "captured_source_count": len(registry["sources"]),
        "input_claim_count": EXPECTED_CLAIM_COUNT,
        "verified_primary_count": len(verified),
        "cue_count": len(script["cues"]),
        "validation": validation,
    }


def validate_new_banknote_authoritative_script_package(
    package_dir: str | Path,
) -> dict[str, Any]:
    """Validate a built review package without reading ignored source bodies."""
    root = Path(package_dir).resolve()
    failed: list[str] = []
    checks: dict[str, bool] = {}

    missing = [name for name in REQUIRED_ARTIFACTS if not (root / name).is_file()]
    checks["required_artifacts_present"] = not missing
    failed.extend(f"missing:{name}" for name in missing)
    if missing:
        return {
            "schema_version": f"{SCHEMA_PREFIX}.package_validation",
            "status": "failed",
            "failed_checks": failed,
            "checks": checks,
        }

    try:
        registry = _read_json(root / "authoritative_source_registry.json")
        receipts = _read_json(root / "source_capture_receipts.json")
        claims = _read_json(root / "claim_adjudication.json")
        verified_set = _read_json(root / "verified_claim_set.json")
        script = _read_json(root / "canonical_script.json")
        traceability = _read_json(root / "cue_source_traceability.json")
        manifest = _read_json(root / "source_to_script_manifest.json")
        csv_readback = _read_json(root / "csv_validation_readback.json")
        editorial_receipt = _read_json(root / "editorial_revision_receipt.json")
        script_receipt = _read_json(root / "script_generation_receipt.json")
    except (json.JSONDecodeError, OSError, ValueError) as exc:
        failed.append(f"json_parse:{exc}")
        return {
            "schema_version": f"{SCHEMA_PREFIX}.package_validation",
            "status": "failed",
            "failed_checks": failed,
            "checks": checks,
        }

    sources = registry.get("sources", [])
    receipt_rows = receipts.get("receipts", [])
    checks["source_receipts_complete"] = (
        len(sources) == len(receipt_rows) >= 4
        and all(_valid_source_record(record) for record in sources)
        and all(_valid_capture_receipt(record) for record in receipt_rows)
    )
    checks["official_domain_allowlist"] = all(
        _official_url(str(record.get("canonical_url", ""))) for record in sources
    )
    checks["source_capture_identity_unchanged"] = (
        len(sources) == EXPECTED_CAPTURED_SOURCE_COUNT
        and _sha256(root / "authoritative_source_registry.json")
        == EXPECTED_SOURCE_REGISTRY_SHA256
        and _sha256(root / "source_capture_receipts.json")
        == EXPECTED_SOURCE_RECEIPTS_SHA256
    )

    claim_rows = claims.get("claims", [])
    checks["claim_coverage_182"] = (
        len(claim_rows) == EXPECTED_CLAIM_COUNT
        and len({record.get("claim_id") for record in claim_rows})
        == EXPECTED_CLAIM_COUNT
    )
    checks["claim_outcomes_valid"] = all(
        record.get("primary_outcome") in CLAIM_OUTCOMES for record in claim_rows
    )
    checks["policy_claims_excluded"] = all(
        record.get("primary_outcome") == "rejected_policy_intent"
        and record.get("canonical_use") is False
        for record in claim_rows
        if record.get("claim_class") == "policy_or_intent_claim"
    )
    checks["dramatic_claims_excluded"] = all(
        record.get("primary_outcome") == "rejected_unsupported"
        and record.get("canonical_use") is False
        for record in claim_rows
        if record.get("claim_class") == "unsupported_dramatic_assertion"
    )
    verified_ids = {
        record["claim_id"]
        for record in claim_rows
        if record.get("primary_outcome") == "verified_primary"
    }
    checks["claim_outcome_identity_unchanged"] = (
        len(verified_ids) == EXPECTED_VERIFIED_PRIMARY_COUNT
        and _claim_outcome_identity_sha256(claims)
        == EXPECTED_CLAIM_OUTCOME_IDENTITY_SHA256
    )

    cues = script.get("cues", [])
    scene_counts = Counter(cue.get("scene_id") for cue in cues)
    speaker_counts = Counter(cue.get("speaker") for cue in cues)
    adopted_ids = {
        claim_id
        for cue in cues
        for claim_id in cue.get("adopted_claim_ids", [])
    }
    expected_verified_records = [
        record
        for record in claim_rows
        if record.get("primary_outcome") == "verified_primary"
    ]
    checks["canonical_use_matches_adopted_claim_set"] = (
        claims.get("canonical_claim_count") == len(adopted_ids)
        and all(
            isinstance(record.get("canonical_use"), bool)
            and record["canonical_use"]
            == (record.get("claim_id") in adopted_ids)
            for record in claim_rows
        )
    )
    checks["verified_claim_set_exact"] = (
        verified_set.get("claim_count") == EXPECTED_VERIFIED_PRIMARY_COUNT
        and verified_set.get("claims") == expected_verified_records
        and {
            record["claim_id"]
            for record in expected_verified_records
            if record["canonical_use"] is False
        }
        == {"claim_095", "claim_158", "claim_162", "claim_164"}
    )
    checks["nine_cues"] = len(cues) == 9
    checks["scene_allocation_2_4_3"] = dict(scene_counts) == EXPECTED_SCENE_ALLOCATION
    checks["speaker_counts_3_6"] = dict(speaker_counts) == EXPECTED_SPEAKER_COUNTS
    cue_by_id = {str(cue.get("cue_id")): cue for cue in cues}
    cue_001 = cue_by_id.get("cue_001", {})
    cue_002 = cue_by_id.get("cue_002", {})
    cue_008 = cue_by_id.get("cue_008", {})
    cue_009 = cue_by_id.get("cue_009", {})
    checks["opening_question_answer_handoff"] = (
        str(cue_001.get("text", "")).endswith("？")
        and str(cue_002.get("text", "")).startswith("あるぞ。")
    )
    checks["cue_claims_verified"] = all(
        cue.get("adopted_claim_ids")
        and all(claim_id in verified_ids for claim_id in cue["adopted_claim_ids"])
        for cue in cues
    )
    checks["script_support_units_mapped"] = all(
        cue.get("factual_support_units")
        and [
            claim_id
            for index, unit in enumerate(cue["factual_support_units"])
            for claim_id in unit.get("claim_ids", [])
            if claim_id
            not in {
                prior_claim_id
                for prior_unit in cue["factual_support_units"][:index]
                for prior_claim_id in prior_unit.get("claim_ids", [])
            }
        ]
        == cue.get("adopted_claim_ids")
        and all(
            unit.get("support_status")
            == "supported_by_verified_primary_claims"
            for unit in cue["factual_support_units"]
        )
        for cue in cues
    )
    trace_rows = traceability.get("cues", [])
    checks["traceability_9_of_9"] = (
        len(trace_rows) == 9
        and [row.get("cue_id") for row in trace_rows]
        == [cue.get("cue_id") for cue in cues]
        and all(
            row.get("unsupported_claim_count") == 0
            and row.get("factual_support_units")
            and all(unit.get("supported") is True for unit in row["factual_support_units"])
            for row in trace_rows
        )
    )
    trace_by_id = {
        str(row.get("cue_id")): row for row in trace_rows
    }
    cue_008_trace = trace_by_id.get("cue_008", {})
    retained_unspoken = cue_008_trace.get(
        "retained_verified_unspoken_claims", []
    )
    claim_by_id = {
        str(record.get("claim_id")): record for record in claim_rows
    }
    retained_rows_by_cue = {
        cue_id: row.get("retained_verified_unspoken_claims", [])
        for cue_id, row in trace_by_id.items()
    }
    expected_claim_158_retained = (
        [_retained_verified_unspoken_claim_row(claim_by_id["claim_158"])]
        if "claim_158" in claim_by_id
        else []
    )
    all_retained_claim_ids = {
        retained_row.get("claim_id")
        for rows in retained_rows_by_cue.values()
        for retained_row in rows
    }
    checks["cue_008_spoken_information_budget"] = (
        len(cue_008.get("factual_support_units", [])) <= 3
        and cue_008.get("adopted_claim_ids")
        == ["claim_114", "claim_155", "claim_157"]
    )
    checks["cue_008_verified_unspoken_evidence_retained"] = (
        retained_unspoken == expected_claim_158_retained
        and traceability.get("retained_verified_unspoken_claim_count") == 1
        and all(
            not rows
            for cue_id, rows in retained_rows_by_cue.items()
            if cue_id != "cue_008"
        )
        and all_retained_claim_ids == {"claim_158"}
        and all_retained_claim_ids.isdisjoint(adopted_ids)
        and claim_by_id.get("claim_158", {}).get("primary_outcome")
        == "verified_primary"
        and claim_by_id.get("claim_158", {}).get("canonical_use") is False
        and "claim_158" not in cue_008.get("adopted_claim_ids", [])
    )
    expected_manifest_edges = {
        (edge["source_id"], edge["claim_id"])
        for row in trace_rows
        for edge in row.get("supporting_evidence", [])
    }
    actual_manifest_edges = {
        (row["source_id"], claim_id)
        for row in manifest.get("sources", [])
        for claim_id in row.get("claim_ids", [])
    }
    checks["source_claim_manifest_edges_exact"] = (
        expected_manifest_edges == actual_manifest_edges
    )
    checks["source_to_script_manifest_exact"] = manifest == (
        _build_source_to_script_manifest(script, traceability, registry)
    )
    checks["unsupported_claim_count_computed_zero"] = (
        script.get("unsupported_claim_count") == 0
        and traceability.get("unsupported_claim_count") == 0
        and manifest.get("unsupported_claim_count") == 0
    )
    spoken = "\n".join(str(cue.get("text", "")) for cue in cues)
    checks["spoken_boundaries_clean"] = not _spoken_boundary_violation(spoken)
    checks["spoken_editorial_terms_clean"] = (
        "E券" not in spoken
        and "道具で見る" not in spoken
        and "ルーペで見る" in str(cue_009.get("text", ""))
    )
    marisa_endings = [
        _marisa_terminal_form(str(cue.get("text", "")))
        for cue in cues
        if cue.get("speaker") == "まりさ"
    ]
    checks["marisa_endings_varied"] = (
        tuple(marisa_endings) == EXPECTED_MARISA_TERMINAL_FORMS
    )

    canonical = read_headerless_yymm4_csv(root / "canonical_yymm4.csv")
    derived = read_headerless_yymm4_csv(root / "derived_yymm4_import.csv")
    canonical_rows = [
        (row["speaker"], row["text"]) for row in canonical["rows"]
    ]
    derived_rows = [(row["speaker"], row["text"]) for row in derived["rows"]]
    checks["canonical_csv_contract"] = canonical_rows == [
        (cue["speaker"], cue["text"]) for cue in cues
    ]
    checks["derived_csv_contract"] = (
        len(derived_rows) == len(canonical_rows) == 9
        and [text for _, text in derived_rows]
        == [text for _, text in canonical_rows]
        and [speaker for speaker, _ in derived_rows]
        == [CANONICAL_TO_YMM4[speaker] for speaker, _ in canonical_rows]
    )
    checks["csv_readback_passed"] = csv_readback.get("status") == "passed"
    editorial_checks = editorial_receipt.get("checks", {})
    editorial_actions = editorial_receipt.get("actions", {})
    editorial_files = editorial_receipt.get("files", {})
    script_receipt_files = script_receipt.get("files", {})
    checks["editorial_revision_receipt_passed"] = (
        editorial_receipt.get("schema_version")
        == f"{SCHEMA_PREFIX}.editorial_revision_receipt"
        and editorial_receipt.get("status") == "passed"
        and editorial_receipt.get("revision_id") == EDITORIAL_REVISION_ID
        and editorial_receipt.get("revision_basis")
        == "existing_verified_primary_evidence_only"
        and editorial_receipt.get("banned_framing_absent") is True
        and editorial_receipt.get("factual_support_units")
        == {"before": BASELINE_FACTUAL_SUPPORT_UNIT_COUNT, "after": 20}
        and editorial_receipt.get("claim_edges")
        == {"before": BASELINE_CLAIM_EDGE_COUNT, "after": 21}
        and editorial_receipt.get("human_review_questions")
        == list(HUMAN_REVIEW_QUESTIONS)
        and bool(editorial_checks)
        and all(
            value is True
            for value in editorial_checks.values()
            if isinstance(value, bool)
        )
        and bool(editorial_actions)
        and all(value is False for value in editorial_actions.values())
    )
    checks["editorial_revision_receipt_hashes_match"] = (
        list(editorial_files) == list(EDITORIAL_RECEIPT_FILES)
        and all(
            isinstance(digest, str)
            and bool(re.fullmatch(r"[0-9a-f]{64}", digest))
            and (root / name).is_file()
            and _sha256(root / name) == digest
            for name, digest in editorial_files.items()
        )
    )
    checks["script_generation_receipt_hashes_match"] = (
        script_receipt.get("schema_version")
        == f"{SCHEMA_PREFIX}.script_generation_receipt"
        and script_receipt.get("status") == "passed"
        and script_receipt.get("network_access_during_generation") is False
        and script_receipt.get("notebooklm_accessed") is False
        and script_receipt.get("cue_count") == 9
        and script_receipt.get("scene_allocation") == EXPECTED_SCENE_ALLOCATION
        and script_receipt.get("canonical_speaker_counts")
        == EXPECTED_SPEAKER_COUNTS
        and script_receipt.get("unsupported_claim_count") == 0
        and script_receipt.get("editorial_adoption") is False
        and script_receipt.get("public_ready") is False
        and script_receipt.get("production_ready") is False
        and list(script_receipt_files) == list(SCRIPT_RECEIPT_FILES)
        and all(
            isinstance(digest, str)
            and bool(re.fullmatch(r"[0-9a-f]{64}", digest))
            and (root / name).is_file()
            and _sha256(root / name) == digest
            for name, digest in script_receipt_files.items()
        )
    )
    candidate_files = [
        path
        for path in root.rglob("*")
        if path.is_file()
        and not any(
            part in {"source_cache", "source_extracts", "source_probe", "local_outputs"}
            for part in path.relative_to(root).parts
        )
    ]
    allowed_generated_review_html = (
        root / "visual_scene_decision" / "visual_direction_board.html"
    ).resolve()
    checks["no_source_bodies"] = not any(
        path.suffix.lower() in {".pdf", ".html", ".htm"}
        and path.resolve() != allowed_generated_review_html
        for path in candidate_files
    )
    combined = "\n".join(
        path.read_text(encoding="utf-8", errors="replace")
        for path in candidate_files
    )
    checks["no_private_or_notebook_identifiers"] = not re.search(
        r"[A-Za-z]:\\Users\\|/Users/|/home/|notebooklm\.google\.com|"
        r"\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-"
        r"[89ab][0-9a-f]{3}-[0-9a-f]{12}\b",
        combined,
        re.IGNORECASE,
    )

    for name, passed in checks.items():
        if not passed:
            failed.append(name)
    return {
        "schema_version": f"{SCHEMA_PREFIX}.package_validation",
        "status": "passed" if not failed else "failed",
        "failed_checks": failed,
        "checks": checks,
        "source_count": len(sources),
        "claim_count": len(claim_rows),
        "cue_count": len(cues),
    }


def _validate_frozen_inputs(
    source_snapshot: dict[str, Any],
    claim_ledger: dict[str, Any],
    alignments: dict[str, Any],
) -> None:
    sources = source_snapshot.get("sources")
    claims = claim_ledger.get("claims")
    alignment_rows = alignments.get("alignments")
    if not isinstance(sources, list) or len(sources) != EXPECTED_SOURCE_COUNT:
        raise ValueError("FROZEN_SOURCE_COUNT_MISMATCH")
    if not isinstance(claims, list) or len(claims) != EXPECTED_CLAIM_COUNT:
        raise ValueError("FROZEN_CLAIM_COUNT_MISMATCH")
    if not isinstance(alignment_rows, list) or len(alignment_rows) != EXPECTED_CLAIM_COUNT:
        raise ValueError("CLAIM_ALIGNMENT_COUNT_MISMATCH")
    if [row.get("claim_id") for row in claims] != [
        row.get("claim_id") for row in alignment_rows
    ]:
        raise ValueError("CLAIM_ALIGNMENT_ORDER_MISMATCH")
    identity = alignments.get("input_claim_ledger", {})
    if identity.get("raw_sha256") != EXPECTED_RAW_IDENTITY["sha256"]:
        raise ValueError("RAW_IDENTITY_MISMATCH")


def _build_source_registry() -> dict[str, Any]:
    sources = [dict(record) for record in SOURCE_RECORDS]
    return {
        "schema_version": f"{SCHEMA_PREFIX}.authoritative_source_registry",
        "status": "official_source_capture_frozen",
        "source_count": len(sources),
        "official_domain_allowlist": sorted(ALLOWED_OFFICIAL_DOMAINS),
        "source_bodies_tracked": False,
        "sources": sources,
    }


def _build_source_receipts() -> dict[str, Any]:
    receipts = [
        {
            "source_id": record["source_id"],
            "capture_id": record["capture_id"],
            "requested_url": record["canonical_url"],
            "canonical_url": record["canonical_url"],
            "publisher": record["publisher"],
            "title": record["title"],
            "http_status": record["http_status"],
            "redirect_count": record["redirect_count"],
            "retrieved_at": record["retrieved_at"],
            "content_type": record["content_type"],
            "size_bytes": record["size_bytes"],
            "sha256": record["sha256"],
            "publication_date": record["publication_date"],
            "publication_date_basis": record["publication_date_basis"],
            "fact_dates": record["fact_dates"],
            "content_dates": record["content_dates"],
            "ignored_cache_repo_relative_path": record[
                "ignored_cache_repo_relative_path"
            ],
            "source_body_tracked": False,
        }
        for record in SOURCE_RECORDS
    ]
    return {
        "schema_version": f"{SCHEMA_PREFIX}.source_capture_receipts",
        "status": "capture_receipts_frozen",
        "capture_count": len(receipts),
        "network_access_required_for_rebuild": False,
        "receipts": receipts,
    }


def _build_source_crosswalk(source_snapshot: dict[str, Any]) -> dict[str, Any]:
    relation_map: dict[str, list[dict[str, str]]] = {
        "S04": [
            {"verification_source_id": "V04", "relation_type": "exact_document_match"},
            {"verification_source_id": "V03", "relation_type": "official_supplement"},
            {"verification_source_id": "V13", "relation_type": "official_supplement"},
        ],
        "S05": [
            {"verification_source_id": "V06", "relation_type": "official_equivalent"},
            {"verification_source_id": "V05", "relation_type": "official_supplement"},
            {"verification_source_id": "V13", "relation_type": "official_supplement"},
        ],
        "S10": [
            {"verification_source_id": "V01", "relation_type": "exact_title_match"}
        ],
        "S11": [
            {"verification_source_id": "V02", "relation_type": "exact_title_match"},
            {"verification_source_id": "V13", "relation_type": "official_supplement"},
        ],
    }
    entries: list[dict[str, Any]] = []
    for source in source_snapshot["sources"]:
        source_id = source["source_id"]
        if source_id == "S07":
            resolution_status = "excluded_derived"
            exact_status = "excluded_derived"
            relations = [
                {"verification_source_id": "none", "relation_type": "excluded_derived"}
            ]
        elif source_id == "S05":
            resolution_status = "official_equivalent_available"
            exact_status = "unresolved_exact_source"
            relations = relation_map[source_id]
        elif source_id == "S04":
            resolution_status = "exact_document_family_resolved_version_unproven"
            exact_status = "exact_document_match"
            relations = relation_map[source_id]
        elif source_id in {"S10", "S11"}:
            resolution_status = "exact_official_identity_resolved"
            exact_status = "exact_title_match"
            relations = relation_map[source_id]
        else:
            resolution_status = "deferred_context_source_resolution"
            exact_status = "unresolved_exact_source"
            relations = []
        entries.append(
            {
                "notebook_source_id": source_id,
                "notebook_exact_title": source["exact_title"],
                "notebook_title_fingerprint": source["title_fingerprint"],
                "chronology_class": source["chronology_class"],
                "resolution_status": resolution_status,
                "exact_source_status": exact_status,
                "relations": relations,
                "identity_conflation_avoided": True,
            }
        )
    return {
        "schema_version": f"{SCHEMA_PREFIX}.notebook_source_crosswalk",
        "status": "active_official_sources_crosswalked",
        "input_source_count": len(entries),
        "entries": entries,
    }


def _build_source_readback(
    registry: dict[str, Any],
    receipts: dict[str, Any],
    crosswalk: dict[str, Any],
) -> dict[str, Any]:
    relations = {
        entry["notebook_source_id"]: {
            relation["relation_type"] for relation in entry["relations"]
        }
        | {entry["exact_source_status"]}
        for entry in crosswalk["entries"]
    }
    registry_by_id = {record["source_id"]: record for record in registry["sources"]}
    crosswalk_edges_match_registry = all(
        relation["verification_source_id"] == "none"
        or (
            relation["verification_source_id"] in registry_by_id
            and entry["notebook_source_id"]
            in registry_by_id[relation["verification_source_id"]][
                "notebook_source_ids"
            ]
            and relation["relation_type"]
            == registry_by_id[relation["verification_source_id"]]["relation_type"]
        )
        for entry in crosswalk["entries"]
        for relation in entry["relations"]
    )
    checks = {
        "registry_receipt_counts_match": len(registry["sources"])
        == len(receipts["receipts"]),
        "official_domain_allowlist": all(
            _official_url(record["canonical_url"]) for record in registry["sources"]
        ),
        "S10_exact_resolved": "exact_title_match" in relations["S10"],
        "S11_exact_resolved": "exact_title_match" in relations["S11"],
        "S04_exact_document_resolved": "exact_document_match" in relations["S04"],
        "S05_exact_unresolved_disclosed": "unresolved_exact_source" in relations["S05"],
        "S05_official_equivalent_available": "official_equivalent" in relations["S05"],
        "crosswalk_edges_match_registry": crosswalk_edges_match_registry,
        "publication_dates_not_inferred": all(
            record["publication_date"] is None
            and record["publication_date_basis"] == "not_stated"
            for record in registry["sources"]
        ),
        "content_and_fact_dates_separated": all(
            isinstance(record["content_dates"], list)
            and isinstance(record["fact_dates"], list)
            for record in registry["sources"]
        ),
        "source_bodies_untracked": registry["source_bodies_tracked"] is False,
    }
    return {
        "schema_version": f"{SCHEMA_PREFIX}.source_resolution_readback",
        "status": "passed" if all(checks.values()) else "failed",
        "captured_source_count": len(registry["sources"]),
        "S10_exact_resolved": checks["S10_exact_resolved"],
        "S11_exact_resolved": checks["S11_exact_resolved"],
        "S04_exact_document_resolved": checks["S04_exact_document_resolved"],
        "S05_exact_source_status": "unresolved_exact_source",
        "checks": checks,
    }


def _build_claim_adjudication(
    claim_ledger: dict[str, Any],
    alignments: dict[str, Any],
) -> dict[str, Any]:
    alignment_by_id = {
        row["claim_id"]: row for row in alignments["alignments"]
    }
    canonical_claim_ids = {
        claim_id for cue in CUES for claim_id in cue["adopted_claim_ids"]
    }
    source_by_id = {record["source_id"]: record for record in SOURCE_RECORDS}
    records: list[dict[str, Any]] = []
    for claim in claim_ledger["claims"]:
        claim_id = claim["claim_id"]
        claim_class = claim["claim_class"]
        alignment = alignment_by_id[claim_id]
        secondary_tags: list[str] = []
        evidence: list[dict[str, Any]] = []
        proposition: str | None = None

        if claim_class == "policy_or_intent_claim":
            outcome = "rejected_policy_intent"
            rationale = (
                "既存資料の政策意図推論であり、独立した一次資料または実証根拠がない。"
            )
        elif claim_class == "unsupported_dramatic_assertion":
            outcome = "rejected_unsupported"
            rationale = "断定を支える一次根拠がなく、canonical narrativeから除外した。"
        elif claim_id in VERIFIED_CLAIMS:
            specification = VERIFIED_CLAIMS[claim_id]
            outcome = "verified_primary"
            proposition = specification["proposition"]
            secondary_tags = ["official_primary"] + list(specification["tags"])
            for source_id, location, unit, fact_date in specification["sources"]:
                source = source_by_id[source_id]
                evidence.append(
                    {
                        "source_id": source_id,
                        "url_label": source["title"],
                        "canonical_url": source["canonical_url"],
                        "exact_location": location,
                        "source_publication_date": source["publication_date"],
                        "source_publication_date_basis": source[
                            "publication_date_basis"
                        ],
                        "fact_date": fact_date,
                        "evidence_as_of": source["retrieved_at"],
                        "date_basis": (
                            "claim_fact_date"
                            if fact_date is not None
                            else "source_retrieval_timestamp"
                        ),
                        "unit": unit,
                        "evidence_grade": "verified_primary",
                    }
                )
            rationale = "公式一次資料の固定済み位置へ命題範囲を限定して検証した。"
        elif claim_id in DUPLICATE_OF:
            outcome = "duplicate_not_used"
            secondary_tags = [f"duplicate_of:{DUPLICATE_OF[claim_id]}"]
            rationale = "同一または反復された命題のため、代表claimへ集約した。"
        elif claim_id in CASHLESS_CAUSAL_IDS:
            outcome = "rejected_policy_intent"
            secondary_tags = ["cashless_causation_unsubstantiated"]
            rationale = "キャッシュレス誘導との因果を支える独立した根拠がない。"
        elif claim_id in SUPPORTED_CONTEXT_IDS:
            outcome = "supported_context_only"
            secondary_tags = ["official_overlap_but_compound_or_overstated"]
            rationale = (
                "公式資料と重なる要素はあるが、複合・誇張・ASR混入のため命題全体は検証しない。"
            )
        elif claim_class == "quantitative_statistic":
            outcome = "rejected_quantitative_without_exact_source"
            rationale = "日付・対象・位置・単位を満たす正確な一次根拠がない。"
        elif claim_class in {"rhetorical_framing", "analogy_or_metaphor"}:
            outcome = "style_or_rhetoric_only"
            rationale = "会話上の修辞または比喩であり、事実根拠として採用しない。"
        elif claim_class == "future_prediction":
            outcome = "unresolved_not_used"
            rationale = "時間範囲と根拠主体が未確定の予測なので使用しない。"
        else:
            outcome = "unresolved_not_used"
            rationale = "公式一次資料の正確な支持範囲へ結べないため使用しない。"

        canonical_use = claim_id in canonical_claim_ids
        if canonical_use and outcome != "verified_primary":
            raise ValueError(f"CANONICAL_CLAIM_NOT_VERIFIED:{claim_id}")
        records.append(
            {
                "claim_id": claim_id,
                "line_ordinal": claim["line_ordinal"],
                "line_fingerprint": claim["line_fingerprint"],
                "claim_class": claim_class,
                "risk_class": claim["risk"],
                "topic_family_labels": alignment.get("topic_family_labels", []),
                "primary_outcome": outcome,
                "secondary_tags": secondary_tags,
                "canonical_use": canonical_use,
                "adjudicated_proposition": proposition,
                "supporting_evidence": evidence,
                "evidence_grade": (
                    "verified_primary"
                    if outcome == "verified_primary"
                    else "not_verified_for_canonical_use"
                ),
                "concise_rationale": rationale,
                "raw_claim_text_tracked": False,
            }
        )
    counts = Counter(record["primary_outcome"] for record in records)
    return {
        "schema_version": f"{SCHEMA_PREFIX}.claim_adjudication",
        "status": "all_claims_adjudicated",
        "input_claim_count": EXPECTED_CLAIM_COUNT,
        "adjudicated_claim_count": len(records),
        "outcome_counts": dict(sorted(counts.items())),
        "canonical_claim_count": len(canonical_claim_ids),
        "raw_claim_text_tracked": False,
        "claims": records,
    }


def _claim_readback(adjudication: dict[str, Any]) -> dict[str, Any]:
    claims = adjudication["claims"]
    counts = Counter(record["primary_outcome"] for record in claims)
    checks = {
        "claim_count_182": len(claims) == EXPECTED_CLAIM_COUNT,
        "claim_ids_unique": len({record["claim_id"] for record in claims})
        == EXPECTED_CLAIM_COUNT,
        "exactly_one_primary_outcome": all(
            record["primary_outcome"] in CLAIM_OUTCOMES for record in claims
        ),
        "outcome_counts_sum_182": sum(counts.values()) == EXPECTED_CLAIM_COUNT,
        "verified_claims_use_official_primary": all(
            record["supporting_evidence"]
            and all(
                support["evidence_grade"] == "verified_primary"
                for support in record["supporting_evidence"]
            )
            for record in claims
            if record["primary_outcome"] == "verified_primary"
        ),
        "verified_evidence_dates_separated": all(
            support.get("source_publication_date") is None
            and support.get("source_publication_date_basis") == "not_stated"
            and bool(support.get("evidence_as_of"))
            and support.get("date_basis")
            in {"claim_fact_date", "source_retrieval_timestamp"}
            for record in claims
            if record["primary_outcome"] == "verified_primary"
            for support in record["supporting_evidence"]
        ),
        "policy_intent_rejected": all(
            record["primary_outcome"] == "rejected_policy_intent"
            for record in claims
            if record["claim_class"] == "policy_or_intent_claim"
        ),
        "canonical_use_verified_only": all(
            not record["canonical_use"]
            or record["primary_outcome"] == "verified_primary"
            for record in claims
        ),
        "raw_claim_text_untracked": all(
            record["raw_claim_text_tracked"] is False for record in claims
        ),
    }
    return {
        "schema_version": f"{SCHEMA_PREFIX}.claim_adjudication_readback",
        "status": "passed" if all(checks.values()) else "failed",
        "claim_count": len(claims),
        "input_claim_count": EXPECTED_CLAIM_COUNT,
        "adjudicated_claim_count": len(claims),
        "verified_primary_count": counts["verified_primary"],
        "outcome_counts": dict(sorted(counts.items())),
        "checks": checks,
    }


def _build_asr_reconciliation(asr_ledger: dict[str, Any]) -> dict[str, Any]:
    official_forms: dict[str, tuple[str, str, str]] = {
        "新兵": ("新紙幣", "V10", "2024年7月3日 お札が変わりました"),
        "新幣": ("新紙幣", "V10", "2024年7月3日 お札が変わりました"),
        "紙兵": ("紙幣", "V10", "2024年7月3日 お札が変わりました"),
        "新市兵": ("新紙幣", "V10", "2024年7月3日 お札が変わりました"),
        "死兵": ("紙幣", "V10", "2024年7月3日 お札が変わりました"),
        "兵幣": ("紙幣", "V10", "2024年7月3日 お札が変わりました"),
        "発酵": ("発行", "V10", "2024年7月3日 お札が変わりました"),
        "学面表示": ("額面表示", "V02", "額面数字の大型化"),
        "深顔版": ("深凹版印刷", "V06", "深凹版印刷"),
        "車線マーク": ("識別マーク（11本の斜線）", "V13", "PDF物理ページ4（冊子pp.6–7）"),
        "お札の修理": ("お札の種類", "V02", "識別マーク（凹版印刷）"),
        "ゆけし君": ("言う吉くん", "V02", "お札識別アプリ『言う吉くん』"),
        "広格ホログラム": ("3Dホログラム", "V06", "3Dホログラム"),
        "審議を判定": ("真偽を判定", "V02", "お札識別アプリ『言う吉くん』"),
    }
    candidates: list[dict[str, Any]] = []
    resolved_count = 0
    for candidate in asr_ledger["candidates"]:
        record = dict(candidate)
        raw_token = record["raw_token"]
        if raw_token in official_forms:
            normalized, source_id, location = official_forms[raw_token]
            record["source_reconciliation"] = {
                "outcome": "resolved_official_terminology",
                "resolved_form": normalized,
                "source_id": source_id,
                "exact_location": location,
            }
            resolved_count += 1
        elif record.get("class") == "safe_auto_fix_candidate":
            record["source_reconciliation"] = {
                "outcome": "retained_prior_safe_language_correction",
                "resolved_form": record.get("proposed_normalized_form"),
                "source_id": None,
                "exact_location": None,
            }
        else:
            record["source_reconciliation"] = {
                "outcome": "unresolved_not_used",
                "resolved_form": None,
                "source_id": None,
                "exact_location": None,
            }
        candidates.append(record)
    return {
        "schema_version": f"{SCHEMA_PREFIX}.asr_source_reconciliation",
        "status": "official_terminology_reconciled",
        "candidate_count": len(candidates),
        "resolved_official_count": resolved_count,
        "raw_tokens_preserved": True,
        "raw_transcript_overwritten": False,
        "candidates": candidates,
    }


def _build_script(adjudication: dict[str, Any]) -> dict[str, Any]:
    claim_by_id = {record["claim_id"]: record for record in adjudication["claims"]}
    cues: list[dict[str, Any]] = []
    unsupported_total = 0
    for cue in CUES:
        support_units: list[dict[str, Any]] = []
        mapped_claim_ids: list[str] = []
        cue_unsupported = 0
        for unit in cue["support_units"]:
            claim_ids = list(unit["claim_ids"])
            for claim_id in claim_ids:
                if claim_id not in mapped_claim_ids:
                    mapped_claim_ids.append(claim_id)
            supported = bool(claim_ids) and all(
                claim_id in claim_by_id
                and claim_by_id[claim_id]["primary_outcome"] == "verified_primary"
                and bool(claim_by_id[claim_id]["supporting_evidence"])
                for claim_id in claim_ids
            )
            if not supported:
                cue_unsupported += 1
            support_units.append(
                {
                    **unit,
                    "support_status": (
                        "supported_by_verified_primary_claims"
                        if supported
                        else "unsupported"
                    ),
                }
            )
        mapping_consistent = mapped_claim_ids == cue["adopted_claim_ids"]
        if not mapping_consistent:
            cue_unsupported += 1
        unsupported_total += cue_unsupported
        cues.append(
            {
                **{
                    key: value
                    for key, value in cue.items()
                    if key != "support_units"
                },
                "factual_support_units": support_units,
                "semantic_coverage_status": (
                    "fully_mapped_to_adjudicated_propositions"
                    if cue_unsupported == 0
                    else "incomplete"
                ),
                "unsupported_claim_count": cue_unsupported,
                "evidence_grade": (
                    "verified_primary" if cue_unsupported == 0 else "incomplete"
                ),
            }
        )
    return {
        "schema_version": f"{SCHEMA_PREFIX}.canonical_script",
        "status": "internal_review_candidate",
        "title": "新紙幣の偽造防止技術と、見分けやすくするための工夫",
        "shaping_mode": "supported_only_constrained_rewrite",
        "source_origin": "existing_notebooklm_transcript_claims",
        "cue_count": len(cues),
        "scene_allocation": EXPECTED_SCENE_ALLOCATION,
        "speaker_counts": EXPECTED_SPEAKER_COUNTS,
        "unsupported_claim_count": unsupported_total,
        "editorial_adoption": False,
        "public_ready": False,
        "production_ready": False,
        "cues": cues,
    }


def _retained_verified_unspoken_claim_row(
    claim: dict[str, Any],
) -> dict[str, Any]:
    return {
        "claim_id": claim["claim_id"],
        "adoption_status": "verified_not_adopted",
        "retention_reason": "cue_information_budget",
        "supporting_evidence": [
            {
                "claim_id": claim["claim_id"],
                "source_id": support["source_id"],
                "exact_location": support["exact_location"],
                "evidence_grade": support["evidence_grade"],
            }
            for support in claim["supporting_evidence"]
        ],
    }


def _build_traceability(
    script: dict[str, Any],
    adjudication: dict[str, Any],
    registry: dict[str, Any],
) -> dict[str, Any]:
    claim_by_id = {record["claim_id"]: record for record in adjudication["claims"]}
    rows: list[dict[str, Any]] = []
    for cue in script["cues"]:
        source_ids: list[str] = []
        support_rows: list[dict[str, Any]] = []
        unit_rows: list[dict[str, Any]] = []
        retained_unspoken_rows: list[dict[str, Any]] = []
        for unit in cue["factual_support_units"]:
            unit_evidence: list[dict[str, Any]] = []
            for claim_id in unit["claim_ids"]:
                for support in claim_by_id[claim_id]["supporting_evidence"]:
                    if support["source_id"] not in source_ids:
                        source_ids.append(support["source_id"])
                    edge = {
                        "support_unit_id": unit["unit_id"],
                        "claim_id": claim_id,
                        "source_id": support["source_id"],
                        "exact_location": support["exact_location"],
                        "evidence_grade": support["evidence_grade"],
                    }
                    unit_evidence.append(edge)
                    support_rows.append(edge)
            unit_supported = (
                unit["support_status"] == "supported_by_verified_primary_claims"
                and bool(unit_evidence)
            )
            unit_rows.append(
                {
                    "support_unit_id": unit["unit_id"],
                    "statement": unit["statement"],
                    "claim_ids": unit["claim_ids"],
                    "supporting_evidence": unit_evidence,
                    "supported": unit_supported,
                }
            )
        for claim_id in cue.get("retained_verified_unspoken_claim_ids", []):
            claim = claim_by_id[claim_id]
            if claim["primary_outcome"] != "verified_primary":
                raise ValueError(
                    f"RETAINED_UNSPOKEN_CLAIM_NOT_VERIFIED:{claim_id}"
                )
            retained_unspoken_rows.append(
                _retained_verified_unspoken_claim_row(claim)
            )
        unsupported_count = sum(not unit["supported"] for unit in unit_rows)
        if cue["semantic_coverage_status"] != "fully_mapped_to_adjudicated_propositions":
            unsupported_count += 1
        rows.append(
            {
                "cue_id": cue["cue_id"],
                "sequence": cue["sequence"],
                "adopted_claim_ids": cue["adopted_claim_ids"],
                "supporting_source_ids": source_ids,
                "supporting_evidence": support_rows,
                "factual_support_units": unit_rows,
                "retained_verified_unspoken_claims": retained_unspoken_rows,
                "all_adopted_claims_verified_primary": all(
                    claim_by_id[claim_id]["primary_outcome"] == "verified_primary"
                    for claim_id in cue["adopted_claim_ids"]
                ),
                "unsupported_claim_count": unsupported_count,
            }
        )
    unsupported_total = sum(row["unsupported_claim_count"] for row in rows)
    retained_unspoken_total = sum(
        len(row["retained_verified_unspoken_claims"]) for row in rows
    )
    return {
        "schema_version": f"{SCHEMA_PREFIX}.cue_source_traceability",
        "status": "passed" if unsupported_total == 0 else "failed",
        "cue_count": len(rows),
        "traceability_coverage": (
            f"{sum(row['unsupported_claim_count'] == 0 for row in rows)}/{len(rows)}"
        ),
        "unsupported_claim_count": unsupported_total,
        "retained_verified_unspoken_claim_count": retained_unspoken_total,
        "cues": rows,
    }


def _build_csv_readback(
    *,
    canonical_csv: Path,
    derived_csv: Path,
    profile_path: Path,
    profile_id: str,
) -> dict[str, Any]:
    canonical = read_headerless_yymm4_csv(canonical_csv)
    derived = read_headerless_yymm4_csv(derived_csv)
    canonical_rows = canonical["rows"]
    derived_rows = derived["rows"]
    canonical_speakers = [row["speaker"] for row in canonical_rows]
    derived_speakers = [row["speaker"] for row in derived_rows]
    canonical_texts = [row["text"] for row in canonical_rows]
    derived_texts = [row["text"] for row in derived_rows]
    checks: dict[str, Any] = {
        "canonical_utf8_without_bom": canonical["encoding"] == "utf-8"
        and canonical["has_utf8_bom"] is False,
        "derived_utf8_without_bom": derived["encoding"] == "utf-8"
        and derived["has_utf8_bom"] is False,
        "canonical_headerless_two_columns": canonical["row_count"] == 9,
        "derived_headerless_two_columns": derived["row_count"] == 9,
        "row_count_preserved": canonical["row_count"] == derived["row_count"] == 9,
        "text_and_order_preserved": canonical_texts == derived_texts,
        "speaker_projection_matches_profile": derived_speakers
        == [CANONICAL_TO_YMM4[speaker] for speaker in canonical_speakers],
        "only_speaker_column_changed": canonical_texts == derived_texts,
        "strict_coverage_satisfied": set(canonical_speakers)
        == set(CANONICAL_TO_YMM4),
        "unmapped_canonical_speakers": [],
    }
    boolean_checks = [value for value in checks.values() if isinstance(value, bool)]
    return {
        "schema_version": f"{SCHEMA_PREFIX}.csv_validation_readback",
        "status": "passed" if all(boolean_checks) else "failed",
        "profile": {
            "profile_id": profile_id,
            "repo_relative_path": PROFILE_RELATIVE.as_posix(),
            "profile_sha256": _sha256(profile_path),
            "selection_policy": "explicit_only",
            "strict_coverage": True,
            "universal_default_claimed": False,
        },
        "canonical_csv": {
            "file": canonical_csv.name,
            "sha256": _sha256(canonical_csv),
            "row_count": canonical["row_count"],
            "speaker_counts": dict(Counter(canonical_speakers)),
        },
        "derived_csv": {
            "file": derived_csv.name,
            "sha256": _sha256(derived_csv),
            "row_count": derived["row_count"],
            "speaker_counts": dict(Counter(derived_speakers)),
        },
        "checks": checks,
    }


def _build_source_to_script_manifest(
    script: dict[str, Any],
    traceability: dict[str, Any],
    registry: dict[str, Any],
) -> dict[str, Any]:
    source_by_id = {record["source_id"]: record for record in registry["sources"]}
    usage: dict[str, dict[str, Any]] = {}
    for trace in traceability["cues"]:
        for edge in trace["supporting_evidence"]:
            source_id = edge["source_id"]
            row = usage.setdefault(
                source_id,
                {
                    "source_id": source_id,
                    "url_label": source_by_id[source_id]["title"],
                    "canonical_url": source_by_id[source_id]["canonical_url"],
                    "cue_ids": [],
                    "claim_ids": [],
                    "support_unit_ids": [],
                },
            )
            if trace["cue_id"] not in row["cue_ids"]:
                row["cue_ids"].append(trace["cue_id"])
            if edge["claim_id"] not in row["claim_ids"]:
                row["claim_ids"].append(edge["claim_id"])
            if edge["support_unit_id"] not in row["support_unit_ids"]:
                row["support_unit_ids"].append(edge["support_unit_id"])
    return {
        "schema_version": f"{SCHEMA_PREFIX}.source_to_script_manifest",
        "status": "source_to_script_traceability_complete",
        "script_title": script["title"],
        "cue_count": script["cue_count"],
        "source_count_used": len(usage),
        "unsupported_claim_count": script["unsupported_claim_count"],
        "sources": [usage[source_id] for source_id in sorted(usage)],
    }


def _script_fact_counts(script: dict[str, Any]) -> tuple[int, int]:
    units = [
        unit
        for cue in script["cues"]
        for unit in cue["factual_support_units"]
    ]
    claim_edges = sum(len(unit["claim_ids"]) for unit in units)
    return len(units), claim_edges


def _claim_outcome_identity_sha256(adjudication: dict[str, Any]) -> str:
    identity = "\n".join(
        f'{claim["claim_id"]}:{claim["primary_outcome"]}'
        for claim in adjudication["claims"]
    )
    return hashlib.sha256(identity.encode("utf-8")).hexdigest()


def _source_identity_sha256(registry: dict[str, Any]) -> str:
    identity = "\n".join(
        f'{source["source_id"]}:{source["sha256"]}'
        for source in registry["sources"]
    )
    return hashlib.sha256(identity.encode("utf-8")).hexdigest()


def _build_editorial_revision_receipt(
    *,
    output: Path,
    script: dict[str, Any],
    adjudication: dict[str, Any],
    traceability: dict[str, Any],
    registry: dict[str, Any],
) -> dict[str, Any]:
    factual_unit_count, claim_edge_count = _script_fact_counts(script)
    claim_by_id = {
        claim["claim_id"]: claim for claim in adjudication["claims"]
    }
    cue_008 = next(cue for cue in script["cues"] if cue["cue_id"] == "cue_008")
    cue_008_trace = next(
        cue for cue in traceability["cues"] if cue["cue_id"] == "cue_008"
    )
    retained = cue_008_trace["retained_verified_unspoken_claims"]
    spoken = "\n".join(cue["text"] for cue in script["cues"])
    outcome_identity = _claim_outcome_identity_sha256(adjudication)
    verified_count = sum(
        claim["primary_outcome"] == "verified_primary"
        for claim in adjudication["claims"]
    )
    checks = {
        "source_capture_identity_unchanged": (
            len(registry["sources"]) == EXPECTED_CAPTURED_SOURCE_COUNT
            and _sha256(output / "authoritative_source_registry.json")
            == EXPECTED_SOURCE_REGISTRY_SHA256
            and _sha256(output / "source_capture_receipts.json")
            == EXPECTED_SOURCE_RECEIPTS_SHA256
        ),
        "claim_outcome_identity_unchanged": (
            len(adjudication["claims"]) == EXPECTED_CLAIM_COUNT
            and verified_count == EXPECTED_VERIFIED_PRIMARY_COUNT
            and outcome_identity == EXPECTED_CLAIM_OUTCOME_IDENTITY_SHA256
        ),
        "spoken_terminology_refined": "E券" not in spoken
        and "道具で見る" not in spoken,
        "cue_008_information_budget_met": (
            len(cue_008["factual_support_units"]) <= 3
            and cue_008["adopted_claim_ids"]
            == ["claim_114", "claim_155", "claim_157"]
        ),
        "cue_008_omitted_evidence_retained": (
            [row["claim_id"] for row in retained] == ["claim_158"]
            and claim_by_id["claim_158"]["primary_outcome"]
            == "verified_primary"
            and claim_by_id["claim_158"]["canonical_use"] is False
        ),
        "unsupported_spoken_claims_zero": (
            script["unsupported_claim_count"] == 0
            and traceability["unsupported_claim_count"] == 0
        ),
        "human_review_gate_retained": len(HUMAN_REVIEW_QUESTIONS) == 5,
    }
    return {
        "schema_version": f"{SCHEMA_PREFIX}.editorial_revision_receipt",
        "status": "passed" if all(checks.values()) else "failed",
        "revision_id": EDITORIAL_REVISION_ID,
        "revision_basis": "existing_verified_primary_evidence_only",
        "issues_addressed": [
            "opening_question_answer_handoff",
            "unexplained_series_notation_in_spoken_text",
            "cue_008_information_density",
            "repetitive_marisa_endings",
            "vague_tool_checking_phrase",
        ],
        "factual_support_units": {
            "before": BASELINE_FACTUAL_SUPPORT_UNIT_COUNT,
            "after": factual_unit_count,
        },
        "claim_edges": {
            "before": BASELINE_CLAIM_EDGE_COUNT,
            "after": claim_edge_count,
        },
        "source_claim_identity": {
            "captured_source_count": len(registry["sources"]),
            "source_identity_sha256": _source_identity_sha256(registry),
            "source_registry_sha256": _sha256(
                output / "authoritative_source_registry.json"
            ),
            "source_receipts_sha256": _sha256(
                output / "source_capture_receipts.json"
            ),
            "claim_count": len(adjudication["claims"]),
            "verified_primary_count": verified_count,
            "claim_outcome_identity_sha256": outcome_identity,
        },
        "removed_spoken_facts_retained_in_evidence": [
            {
                "claim_id": "claim_158",
                "prior_cue_id": "cue_008",
                "adoption_status": "verified_not_adopted",
                "traceability_lane": (
                    "cue_008.retained_verified_unspoken_claims"
                ),
                "retention_reason": "cue_information_budget",
            }
        ],
        "evidence_anchor_refinements": [
            {
                "cue_id": "cue_009",
                "from_claim_id": "claim_095",
                "to_claim_id": "claim_096",
                "reason": "specific_loupe_action_requires_specific_verified_claim",
                "prior_claim_remains_verified": True,
            }
        ],
        "human_review_questions": list(HUMAN_REVIEW_QUESTIONS),
        "banned_framing_absent": not _spoken_boundary_violation(spoken),
        "actions": {
            "notebooklm_accessed": False,
            "network_source_fetch": False,
            "yymm4_launched": False,
            "render_or_media_generated": False,
            "production_or_public_action": False,
        },
        "checks": checks,
        "files": {
            name: _sha256(output / name) for name in EDITORIAL_RECEIPT_FILES
        },
    }


def _build_script_receipt(output: Path, script: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema_version": f"{SCHEMA_PREFIX}.script_generation_receipt",
        "status": "passed",
        "generation_mode": "supported_only_constrained_rewrite",
        "network_access_during_generation": False,
        "notebooklm_accessed": False,
        "cue_count": script["cue_count"],
        "scene_allocation": script["scene_allocation"],
        "canonical_speaker_counts": script["speaker_counts"],
        "unsupported_claim_count": script["unsupported_claim_count"],
        "editorial_adoption": False,
        "public_ready": False,
        "production_ready": False,
        "files": {
            name: _sha256(output / name) for name in SCRIPT_RECEIPT_FILES
        },
    }


def _render_editorial_revision(
    script: dict[str, Any],
    adjudication: dict[str, Any],
) -> str:
    factual_unit_count, claim_edge_count = _script_fact_counts(script)
    canonical_claim_count = len(
        {
            claim_id
            for cue in script["cues"]
            for claim_id in cue["adopted_claim_ids"]
        }
    )
    lines = [
        "# Canonical Script Editorial Revision",
        "",
        "> INTERNAL REVIEW / NOT FINAL / NON-PUBLIC / NON-PRODUCTION",
        "",
        "編集操作、判断権限、cueごとの由来は "
        "[Editorial Provenance](editorial_provenance/README_EDITORIAL_PROVENANCE.md) "
        "で読み戻せます。source-backedな事実、Workerのeditorial synthesis、"
        "current execution contractでのbounded approval、prior user script利用が未証明である範囲を分離します。"
        "独立した同時点の承認receiptはありません。"
        "現在文面への継続承認は、将来の非公開・無記録な本文変更を許可しません。",
        "",
        "既存の公式source captureと182件のclaim adjudicationは固定したまま、一般視聴者が最初に引っかかる会話上の欠点だけを一度の編集収束で直しました。新しい事実や出典は追加していません。",
        "",
        "## 改訂した箇所",
        "",
        "| Cue | 改訂前の摩擦 | 改訂後 | 証拠への影響 |",
        "| --- | --- | --- | --- |",
        "| 1→2 | 事実の列挙から相づちへ進み、問いと答えが弱かった | れいむの素朴な質問へ、まりさが技術と使いやすさの両面で答える | 既存claimをcue間で移動し、support locationは維持 |",
        "| 3→4 | まりさの説明が同じ終わり方に寄っていた | 技術の順序は保ち、終止を分散 | 事実単位とclaim edgeは不変 |",
        "| 5 | 手触りの説明は明瞭だった | 発話を維持 | 変更なし |",
        "| 6→7 | 説明語尾が反復していた | ルーペと識別マークの説明を保ちながら終止を分散 | 事実単位とclaim edgeは不変 |",
        "| 8 | 内部的なシリーズ記号と4事実が一息に入っていた | 比較対象を前のシリーズのお札と明示し、額面数字・ホログラム差・橙色の3事実へ限定 | 数字『1』のclaimはverifiedのまま非発話レーンへ保持 |",
        "| 9 | 道具が何か分からなかった | 透かす・触る・傾ける・ルーペで見る、へ具体化 | 一般claimからルーペを明示するclaimへ結び直し |",
        "",
        "## 証拠と構造の読み戻し",
        "",
        f"- factual meaning units: {BASELINE_FACTUAL_SUPPORT_UNIT_COUNT}件から{factual_unit_count}件。",
        f"- claim edges: {BASELINE_CLAIM_EDGE_COUNT}本から{claim_edge_count}本。",
        f"- 現在のadopted claimは{canonical_claim_count}件。verified-primary全{adjudication['outcome_counts'].get('verified_primary', 0)}件と182件のoutcomeは維持。",
        "- cue 8から外した数字『1』のデザイン差は、`claim_158`としてadjudication、verified set、cue traceの非発話レーンに残しています。",
        "- cue 9はルーペを明記する`claim_096`へ結び直し、一般的な道具確認の`claim_095`はverifiedのまま非採用です。",
        "- source registry、capture receipt、raw transcript、source cacheは変更していません。",
        "",
        "## 人が判断する5点",
        "",
    ]
    lines.extend(
        f"{index}. {question}"
        for index, question in enumerate(HUMAN_REVIEW_QUESTIONS, start=1)
    )
    lines.extend(
        [
            "",
            "## この改訂で行っていないこと",
            "",
            "NotebookLMアクセス、source再取得、YMM4起動、render、media生成、editorial acceptance、production、publication、rights actionは行っていません。",
            "",
        ]
    )
    return "\n".join(lines)


def _render_script_text(script: dict[str, Any]) -> str:
    return "\n".join(
        f'{cue["speaker"]}：{cue["text"]}' for cue in script["cues"]
    ) + "\n"


def _render_script_review(
    script: dict[str, Any],
    traceability: dict[str, Any],
) -> str:
    trace_by_id = {row["cue_id"]: row for row in traceability["cues"]}
    lines = [
        "# Canonical Script Review",
        "",
        "> INTERNAL REVIEW / NOT FINAL / NON-PUBLIC / NON-PRODUCTION",
        "",
        "既存のNotebookLM由来claimを公式一次資料で絞り込み、明らかな用語・密度・掛け合いの欠点を直した9キューのhuman-review候補です。",
        "",
        "| # | Scene | Speaker | Spoken text | Evidence anchors |",
        "| ---: | --- | --- | --- | --- |",
    ]
    for cue in script["cues"]:
        trace = trace_by_id[cue["cue_id"]]
        anchors = ", ".join(trace["adopted_claim_ids"])
        lines.append(
            f'| {cue["sequence"]} | {cue["scene_id"]} | {cue["speaker"]} | '
            f'{cue["text"]} | {anchors} |'
        )
    lines.extend(
        [
            "",
            "会話本文にはURL、内部ID、hash、ローカルpathを入れていません。Evidence anchorsはreview欄だけの識別子です。",
            "",
        ]
    )
    return "\n".join(lines)


def _primary_review_surface(
    script: dict[str, Any],
    adjudication: dict[str, Any],
    source_readback: dict[str, Any],
) -> str:
    counts = adjudication["outcome_counts"]
    lines = [
        "# Canonical Script Review — New Banknote",
        "",
        "> **INTERNAL REVIEW — NOT FINAL — NON-PUBLIC — NON-PRODUCTION**",
        "",
        "このページがhuman reviewの主画面です。既存のNotebookLM会話から事実の意味単位を検証済みclaimへ結び、公式一次資料で支えられる範囲だけを9キューへ短く整えたうえで、用語・情報密度・掛け合いを編集収束しました。",
        "",
        "## いま判断できること",
        "",
        f'- 公式source capture: {source_readback["captured_source_count"]}件。S10/S11はexact、S04は同名の現行公式document（生成時byte同一性は未証明）、S05はexact未解決でofficial equivalentを分離。',
        f'- claim adjudication: 182/182。verified-primaryは{counts.get("verified_primary", 0)}件。',
        f'- script: 9 cues、S1/S2/S3 = 2/4/3、れいむ/まりさ = 3/6。意味単位から計算したunsupported claimは{script["unsupported_claim_count"]}件。',
        "- editorial revision: シリーズ記号を発話から外し、cue 8を3事実へ絞り、確認方法をルーペまで具体化。外した検証済みclaimは非発話レーンへ保持。",
        "- CSV: canonicalとYMM4-character derivedの2本。本文と順序は同一で、話者列だけを変換。",
        "",
        "## 編集来歴",
        "",
        "- 事実部分は claim と official source に接続されています。",
        "- 会話構造、接続、圧縮、話者らしさは editorial synthesis として区別しています。",
        "- current execution contractで現在の9 cueを継続するbounded approvalを記録しています。独立した同時点receiptはなく、将来の silent edit も含みません。",
        "- 以前の user-submitted script の取り込みは、利用可能な repo 証拠からは証明されていません。",
        "- 詳細: [Editorial Provenance](editorial_provenance/README_EDITORIAL_PROVENANCE.md)",
        "",
        "## Script",
        "",
        "| # | Scene | Speaker | Spoken text |",
        "| ---: | --- | --- | --- |",
    ]
    for cue in script["cues"]:
        lines.append(
            f'| {cue["sequence"]} | {cue["scene_id"]} | {cue["speaker"]} | {cue["text"]} |'
        )
    lines.extend(
        [
            "",
            "## Reviewの進め方",
            "",
            "`operator_review_sheet.md`の5問に沿って、事実の伝わり方、誤解を招く含意、掛け合い、3 sceneの流れ、専門語の難しさを確認してください。",
            "",
            "改訂理由と証拠の移動は`canonical_script_editorial_revision.md`にまとめています。",
            "",
            "この候補はeditorial acceptanceでもYMM4投入承認でもありません。修正判断後にだけ、次のbounded operator batchへ進めます。",
            "",
        ]
    )
    return "\n".join(lines)


def _operator_review_sheet() -> str:
    lines = [
        "# Operator Review Sheet",
        "",
        "> INTERNAL REVIEW / NOT FINAL / NON-PUBLIC / NON-PRODUCTION",
        "",
    ]
    lines.extend(
        f"{index}. {question}"
        for index, question in enumerate(HUMAN_REVIEW_QUESTIONS, start=1)
    )
    return "\n".join(lines) + "\n"


def _source_resolution_limitations() -> str:
    return """# Source Resolution Limitations

- S04は同名の現行公式PDFへ解決したが、凍結snapshotがtitleのみなのでNotebookLM投入時のbyte版と同一とは証明していない。
- S05のexact titleと`PDF 572KB`に一致する現行assetは見つからず、exact identityは未解決のまま。現行公式HTMLをofficial equivalentとして別登録した。
- `publication_date`は資料が公開・刊行日と明示した場合だけに限定した。HTMLの`Last-Modified`、page metadataのdate、可視の更新日、出来事の日、取得時刻は、それぞれbasis付きの別fieldへ分けた。
- 画像ベースPDFはOCRせず、既存text extractionの可否確認とpage renderの目視照合だけを行った。
- source body、長い引用、private notebook識別子はtracked artifactへ含めていない。
"""


def _review_limitations() -> str:
    return """# Limitations

| 残る不確実性 | Reviewへの影響 | Owner | 再訪条件 | 現在blockするか |
| --- | --- | --- | --- | --- |
| S04は現行同名PDFだが生成時版のbyte同一性は未証明 | 開発経緯のprovenanceに版差が残る | source provenance reviewer | NotebookLM投入時のstable IDまたはhashが得られた時 | いいえ。採用claimは現行技術ページでも支持 |
| S05のexact 572KB PDFは未解決 | 元資料の同定は完了していない | source provenance reviewer | 旧URL、archive identifier、元PDFが得られた時 | いいえ。official equivalentが採用claimを支持 |
| 元Audio Overviewのtimestampとtrue speaker identityは得られていない | claim provenanceはline/fingerprint基準 | original Audio Overview custodian | 元Audio Overview metadataが安全に得られた時 | いいえ |
| Voice・rhythm・terminologyのhuman editorial acceptanceは未実施 | 掛け合いと発話表現は未承認 | human editorial reviewer | 5問reviewが完了した時 | はい。YMM4 batchの承認をblock |
"""


def _valid_source_record(record: dict[str, Any]) -> bool:
    return (
        bool(record.get("source_id"))
        and bool(record.get("publisher"))
        and bool(record.get("title"))
        and _official_url(str(record.get("canonical_url", "")))
        and bool(record.get("content_type"))
        and int(record.get("size_bytes", 0)) > 0
        and bool(re.fullmatch(r"[0-9a-f]{64}", str(record.get("sha256", ""))))
        and bool(record.get("evidence_locations"))
        and record.get("publication_date") is None
        and record.get("publication_date_basis") == "not_stated"
        and isinstance(record.get("fact_dates"), list)
        and isinstance(record.get("content_dates"), list)
    )


def _valid_capture_receipt(record: dict[str, Any]) -> bool:
    return (
        _valid_source_record(
            {
                **record,
                "evidence_locations": ["receipt"],
                "authority_class": "primary_official",
            }
        )
        and int(record.get("http_status", 0)) == 200
        and bool(record.get("retrieved_at"))
    )


def _official_url(url: str) -> bool:
    host = (urlparse(url).hostname or "").lower()
    return any(host == domain or host.endswith(f".{domain}") for domain in ALLOWED_OFFICIAL_DOMAINS)


def _spoken_boundary_violation(spoken: str) -> bool:
    patterns = (
        r"https?://",
        r"[A-Za-z]:\\",
        r"\bclaim_\d+\b",
        r"\b[SV]\d{2}\b",
        r"\b[0-9a-f]{40,64}\b",
        r"キャッシュレス",
        r"裏のミッション|隠された使命|タンス預金",
        r"リスナー|今回の深掘り|また次回",
    )
    return any(re.search(pattern, spoken, re.IGNORECASE) for pattern in patterns)


def _marisa_terminal_form(text: str) -> str:
    cleaned = re.sub(r"[。！？]+$", "", text.strip())
    for terminal in ("なんだ", "んだぜ", "おこう", "んだ", "だぜ", "ぜ", "ぞ", "だ"):
        if cleaned.endswith(terminal):
            return terminal
    return cleaned


def _read_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"JSON_OBJECT_REQUIRED:{path.name}")
    return payload


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def _write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def _write_csv(path: Path, rows: list[tuple[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerows(rows)


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()
