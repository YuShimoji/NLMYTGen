// Render an HTML/SVG visualization of the diagnostic carrier from its readback JSON.
// This is a visualization-only proof. It is not a render, not creative acceptance,
// not production timing, and does not replace YMM4-side composition judgement.
// Hidden items (G27PBD_Arrow) are emitted as HTML comments so layout is preserved.

const fs = require('fs');
const path = require('path');

const root = path.resolve(__dirname, '..');
const readbackPath = 'samples/_probe/g24/real_estate_dx_diagnostic_carrier_readback.json';
const outHtmlPath = 'samples/_probe/g24/real_estate_dx_diagnostic_carrier_proof.html';

function abs(rel) {
  return path.join(root, rel);
}

function readJson(rel) {
  return JSON.parse(fs.readFileSync(abs(rel), 'utf8').replace(/^﻿/, ''));
}

function writeText(rel, text) {
  fs.mkdirSync(path.dirname(abs(rel)), { recursive: true });
  fs.writeFileSync(abs(rel), text, 'utf8');
}

function argbCss(argb) {
  if (!/^#[0-9A-Fa-f]{8}$/.test(argb || '')) return '#000000';
  return '#' + argb.slice(3);
}

function argbAlpha(argb) {
  if (!/^#[0-9A-Fa-f]{8}$/.test(argb || '')) return 1;
  return parseInt(argb.slice(1, 3), 16) / 255;
}

function ymmpToSvg(cx, cy) {
  return { sx: 960 + cx, sy: 540 + cy };
}

function escapeXml(s) {
  return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}

function renderItem(item) {
  if (item.is_hidden) return `      <!-- hidden: ${item.item_name} (role=${item.role}) -->`;
  const { sx, sy } = ymmpToSvg(item.x ?? 0, item.y ?? 0);
  if (item.item_type === 'ShapeItem') {
    const fill = argbCss(item.fill_color);
    const alpha = argbAlpha(item.fill_color);
    const opacity = ((item.opacity ?? 100) / 100) * alpha;
    const left = sx - (item.width ?? 0) / 2;
    const top = sy - (item.height ?? 0) / 2;
    return `      <rect data-name="${escapeXml(item.item_name)}" data-role="${escapeXml(item.role || '')}" x="${left}" y="${top}" width="${item.width}" height="${item.height}" fill="${fill}" fill-opacity="${opacity.toFixed(3)}" />`;
  }
  if (item.item_type === 'TextItem') {
    const fill = argbCss(item.text_color);
    const alpha = argbAlpha(item.text_color);
    const opacity = ((item.opacity ?? 100) / 100) * alpha;
    return `      <text data-name="${escapeXml(item.item_name)}" data-role="${escapeXml(item.role || '')}" x="${sx}" y="${sy}" font-size="${item.font_size}" fill="${fill}" fill-opacity="${opacity.toFixed(3)}" text-anchor="middle" dominant-baseline="middle" font-family="'Yu Gothic UI','Hiragino Sans','Noto Sans CJK JP',sans-serif" font-weight="600">${escapeXml(item.text)}</text>`;
  }
  return '';
}

function safeAreaOutline(stroke) {
  // SCS §1 outer safe band: top/bottom 54px, left/right 96px
  // caption safe area: bottom 184px (cy 302..486 = svg_y 842..1026)
  return [
    `      <rect data-guide="outer_safe_band" x="96" y="54" width="1728" height="972" fill="none" stroke="${stroke}" stroke-dasharray="6 6" stroke-width="2" />`,
    `      <rect data-guide="caption_safe_area" x="0" y="842" width="1920" height="184" fill="rgba(255,80,80,0.05)" stroke="${stroke}" stroke-dasharray="3 3" stroke-width="1" />`,
    `      <rect data-guide="title_band" x="96" y="54" width="1728" height="86" fill="none" stroke="${stroke}" stroke-dasharray="3 3" stroke-width="1" />`,
  ].join('\n');
}

function main() {
  const readback = readJson(readbackPath);
  const items = readback.items.slice().sort((a, b) => (a.layer ?? 0) - (b.layer ?? 0));
  const svgItems = items.map(renderItem).join('\n');

  const compliance = readback.scs_compliance;
  const violations = (compliance.composition_violations || []).map((v) => `${v.rule} (${v.severity})`).join(', ') || 'none';

  const html = `<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8" />
  <title>G-27 Diagnostic Carrier Proof (SCS §2.1 split)</title>
  <style>
    html, body { margin: 0; padding: 0; background: #1f2933; color: #e6edf3; font-family: 'Yu Gothic UI', sans-serif; }
    .meta { padding: 12px 24px; font-size: 14px; line-height: 1.6; background: #0b1217; border-bottom: 1px solid #2b3640; }
    .meta strong { color: #f0b429; }
    .frame-wrap { width: 1920px; height: 1080px; margin: 0; position: relative; }
    .frame-wrap svg { display: block; }
    /* When opening this HTML in Electron with BrowserWindow size = 1920x1080,
       use ?no_meta=1 to hide the top meta strip. */
  </style>
  <script>
    window.addEventListener('DOMContentLoaded', () => {
      const params = new URLSearchParams(location.search);
      if (params.get('no_meta') === '1') {
        const meta = document.querySelector('.meta');
        if (meta) meta.style.display = 'none';
      }
      if (params.get('guides') === '0') {
        document.querySelectorAll('[data-guide]').forEach((el) => el.remove());
      }
    });
  </script>
</head>
<body>
  <div class="meta">
    <div>diagnostic carrier visualization (SCS §2.1 split). not a render, not creative acceptance.</div>
    <div><strong>composition_type</strong>: ${compliance.composition_type} / <strong>element_count</strong>: ${compliance.element_count} / <strong>reading_order</strong>: ${(compliance.reading_order || []).join(' → ')}</div>
    <div><strong>safe_area</strong>: ${compliance.safe_area_check} / <strong>subtitle_clearance</strong>: ${compliance.subtitle_clearance_check} / <strong>shape_size_mode</strong>: ${compliance.shape_size_mode_check} / <strong>color_format</strong>: ${compliance.color_format_check}</div>
    <div><strong>violations</strong>: ${escapeXml(violations)}</div>
    <div>query: <code>?no_meta=1</code> to hide this strip; <code>?guides=0</code> to hide SCS grid guides.</div>
  </div>
  <div class="frame-wrap">
    <svg viewBox="0 0 1920 1080" width="1920" height="1080" xmlns="http://www.w3.org/2000/svg">
${svgItems}
${safeAreaOutline('rgba(255, 240, 200, 0.35)')}
    </svg>
  </div>
</body>
</html>`;

  writeText(outHtmlPath, html);
  console.log(`HTML proof written: ${outHtmlPath}`);
  console.log(`Open in a browser or load via Electron BrowserWindow.loadFile().`);
  console.log(`composition_type=${compliance.composition_type}, violations=${(compliance.composition_violations || []).length}`);
}

main();
