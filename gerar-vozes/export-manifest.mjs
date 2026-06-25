// Exporta TODAS as falas do jogo para audio-manifest.json
// O "id" de cada fala = impressao digital (FNV-1a) de who+texto.
// ESSA funcao fnv1a precisa ser IDENTICA a do motor (no HTML),
// senao o nome do arquivo de audio nao bate com a fala.
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.dirname(HERE);
const htmlPath = path.join(ROOT, 'THE-LONG-RUN.html');

const html = fs.readFileSync(htmlPath, 'utf8');
let storySrc = html.match(/const STORY = \{[\s\S]*?\n\};/)[0].replace('const STORY =', 'globalThis.STORY =');
eval(storySrc);

function fnv1a(str){
  let h = 0x811c9dc5;
  for (let i = 0; i < str.length; i++){
    h ^= str.charCodeAt(i);
    h = Math.imul(h, 0x01000193) >>> 0;
  }
  return ('0000000' + h.toString(16)).slice(-8);
}
function audioId(who, text){
  return who + '_' + fnv1a(who + '|' + text.replace(/<[^>]+>/g, ''));
}

const manifest = [];
const seen = new Set();
for (const nodeId in STORY){
  const msgs = STORY[nodeId].messages || [];
  msgs.forEach((m, i) => {
    const id = audioId(m.who, m.text);
    // evita gerar 2x a mesma fala identica (mesmo who+texto)
    if (seen.has(id)) return;
    seen.add(id);
    manifest.push({ id, who: m.who, node: nodeId, idx: i, text: m.text.replace(/<[^>]+>/g, '') });
  });
}

const out = path.join(HERE, 'audio-manifest.json');
fs.writeFileSync(out, JSON.stringify(manifest, null, 2), 'utf8');

const byWho = {};
manifest.forEach(m => byWho[m.who] = (byWho[m.who] || 0) + 1);
console.log('Manifesto gerado:', manifest.length, 'falas unicas');
console.log('Por personagem:', JSON.stringify(byWho));
console.log('->', out);
