// Render an HTML/SVG visualization of the layout instruction proof readback.
// Visualization-only. Not a render, not creative acceptance.

const fs = require('fs');
const path = require('path');

const root = path.resolve(__dirname, '..');
const readbackPath = 'samples/_probe/g24/layout_instruction_proof_readback.json';
const outHtmlPath = 'samples/_probe/g24/layout_instruction_proof.html';

function abs(rel) { return path.join(root, rel); }
function readJson(rel) { return JSON.parse(fs.readFileSync(abs(rel), 'utf8').replace(/^﻿/, '')); }
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
function ymmpToSvg(cx, cy) { return { sx: 960 + cx, sy: 540 + cy }; }
function escapeXml(s) {
  return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}

function renderItem(item) {
  if (item.is_hidden) return `      <!-- hidden: ${item.display_name} -->`;
  if (item.item_type === 'ShapeItem') {
    // ShapeItem: YMM4 X/Y is geometry center.
    const { sx, sy } = ymmpToSvg(item.x ?? 0, item.y ?? 0);
    const fill = argbCss(item.fill_color);
    const alpha = argbAlpha(item.fill_color);
    const opacity = ((item.opacity ?? 100) / 100) * alpha;
    const left = sx - (item.width ?? 0) / 2;
    const top = sy - (item.height ?? 0) / 2;
    const rx = Math.min(item.round ?? 0, (item.width ?? 0) / 2, (item.height ?? 0) / 2);
    return `      <rect data-name="${escapeXml(item.display_name)}" data-role="${escapeXml(item.role || '')}" x="${left}" y="${top}" width="${item.width}" height="${item.height}" rx="${rx}" ry="${rx}" fill="${fill}" fill-opacity="${opacity.toFixed(3)}" />`;
  }
  if (item.item_type === 'TextItem') {
    // TextItem: YMM4 X/Y is the top-left of the text bbox (no built-in center alignment).
    // Mirror that anchor in SVG so the HTML proof and YMM4 GUI agree on visual positioning.
    const { sx, sy } = ymmpToSvg(item.x ?? 0, item.y ?? 0);
    const fill = argbCss(item.text_color);
    const alpha = argbAlpha(item.text_color);
    const opacity = ((item.opacity ?? 100) / 100) * alpha;
    return `      <text data-name="${escapeXml(item.display_name)}" data-role="${escapeXml(item.role || '')}" x="${sx}" y="${sy}" font-size="${item.font_size}" fill="${fill}" fill-opacity="${opacity.toFixed(3)}" text-anchor="start" dominant-baseline="hanging" font-family="'Yu Gothic UI','Hiragino Sans','Noto Sans CJK JP',sans-serif" font-weight="600">${escapeXml(item.text)}</text>`;
  }
  return '';
}

function guidesOverlay(stroke) {
  // outer safe band (5%), title band, grid bbox, character regions, caption safe area
  return [
    `      <rect data-guide="outer_safe_band" x="96" y="54" width="1728" height="972" fill="none" stroke="${stroke}" stroke-dasharray="6 6" stroke-width="2" />`,
    `      <rect data-guide="caption_safe_area" x="0" y="864" width="1920" height="216" fill="rgba(255,80,80,0.04)" stroke="${stroke}" stroke-dasharray="3 3" stroke-width="1" />`,
    `      <rect data-guide="title_band" x="96" y="97" width="1728" height="86" fill="none" stroke="${stroke}" stroke-dasharray="3 3" stroke-width="1" />`,
  ].join('\n');
}

function main() {
  const readback = readJson(readbackPath);
  const items = readback.items.slice().sort((a, b) => (a.layer ?? 0) - (b.layer ?? 0));
  const svgItems = items.map(renderItem).join('\n');
  const c = readback.layout_compliance;
  const checksLine = Object.entries(c.instruction_compliance).map(([k, v]) => `${k}=${v}`).join(' / ');
  const violations = (c.violations || []).map((v) => `${v.rule}(${v.severity})`).join(', ') || 'none';

  const html = `<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8" />
  <title>G-27 Layout Instruction Compliance Proof</title>
  <style>
    html, body { margin: 0; padding: 0; background: #1f2933; color: #e6edf3; font-family: 'Yu Gothic UI', sans-serif; }
    .meta { padding: 12px 24px; font-size: 13px; line-height: 1.55; background: #0b1217; border-bottom: 1px solid #2b3640; }
    .meta strong { color: #f0b429; }
    .frame-wrap { width: 1920px; height: 1080px; position: relative; }
    .frame-wrap svg { display: block; }
  </style>
  <script>
    window.addEventListener('DOMContentLoaded', () => {
      const params = new URLSearchParams(location.search);
      if (params.get('no_meta') === '1') {
        const meta = document.querySelector('.meta'); if (meta) meta.style.display = 'none';
      }
      if (params.get('guides') === '0') {
        document.querySelectorAll('[data-guide]').forEach((el) => el.remove());
      }
    });
  </script>
</head>
<body>
  <div class="meta">
    <div>Layout Instruction Compliance Proof — diagnostic-only layout/slot proof, not a scene composition.</div>
    <div><strong>status</strong>: ${readback.status} / <strong>items</strong>: ${readback.totals.item_count} (Shape=${readback.totals.shape_item_count}, Text=${readback.totals.text_item_count}) / <strong>hard_fail</strong>: ${readback.totals.hard_failure_count}</div>
    <div><strong>checks</strong>: ${escapeXml(checksLine)}</div>
    <div><strong>violations</strong>: ${escapeXml(violations)}</div>
    <div>query: <code>?no_meta=1</code> hide this strip; <code>?guides=0</code> hide grid guides.</div>
  </div>
  <div class="frame-wrap">
    <svg viewBox="0 0 1920 1080" width="1920" height="1080" xmlns="http://www.w3.org/2000/svg">
${svgItems}
${guidesOverlay('rgba(255, 240, 200, 0.35)')}
    </svg>
  </div>
</body>
</html>`;

  writeText(outHtmlPath, html);
  console.log(`HTML proof written: ${outHtmlPath}`);
  console.log(`status=${readback.status}, items=${readback.totals.item_count}, hard_fail=${readback.totals.hard_failure_count}`);
}

main();
