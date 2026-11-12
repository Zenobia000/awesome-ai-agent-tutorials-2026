// 投影片健康檢查（在 deck/ 執行）：node check_slides.mjs slides [--min-label 22]
// 抓四類問題：①同一檔出現兩份頁面（編輯時整段被重複貼上）②行內 <script> 語法錯（圖會整片消失）
// ③ CSS font-size 低於下限（.code 與 <sub> 例外，請人工確認）④仍引用外部 CDN（離線會壞）。重疊、溢出、構圖仍要看截圖
import fs from 'node:fs'; import path from 'node:path';
const dir = process.argv[2] || 'slides';
const opt = k => { const i = process.argv.indexOf(k); return i > 0 ? +process.argv[i + 1] : null; };
const minLabel = opt('--min-label') ?? 22;
let bad = 0;
for (const f of fs.readdirSync(dir).filter(x => x.endsWith('.html')).sort()) {
  const s = fs.readFileSync(path.join(dir, f), 'utf8'), out = [];
  const n = (s.match(/class="(?:[^"]*\s)?slide(?:\s[^"]*)?"/g) || []).length;
  if (n !== 1) out.push(`slide 容器 ${n} 個（應為 1，檔案可能被重複貼上）`);
  for (const m of s.matchAll(/<script>([\s\S]*?)<\/script>/g)) { try { new Function(m[1]); } catch (e) { out.push(`script 語法錯：${e.message}`); } }
  if (!s.trim().endsWith('</html>')) out.push('檔尾不是 </html>');
  for (const m of s.matchAll(/font-size:\s*(\d+)px/g)) if (+m[1] < minLabel && !/<sub/.test(s.slice(Math.max(0, m.index - 40), m.index))) out.push(`font-size ${m[1]}px < ${minLabel}`);
  if (/(unpkg\.com|fonts\.googleapis\.com|fonts\.gstatic\.com|cdn\.jsdelivr|cdnjs\.cloudflare)/.test(s)) out.push('引用外部 CDN');
  if (out.length) { bad++; console.log(`${f}\n  - ${[...new Set(out)].join('\n  - ')}`); }
}
console.log(bad ? `\n${bad} 個檔案有問題` : 'OK：全部通過'); process.exit(bad ? 1 : 0);
