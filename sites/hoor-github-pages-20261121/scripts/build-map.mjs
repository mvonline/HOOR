import {build} from 'esbuild';
import fs from 'node:fs/promises';
import path from 'node:path';
import {createRequire} from 'node:module';
const require=createRequire(import.meta.url);
await fs.mkdir('dist/assets',{recursive:true});
await build({entryPoints:['src/map-engine.js'],outfile:'dist/assets/map-engine.js',bundle:true,format:'esm',platform:'browser',target:'es2022',minify:true,sourcemap:false,legalComments:'eof'});
const notices=[];
for(const name of ['react','react-dom','scheduler','lucide-react','marked','d3-geo','d3-array','internmap']){
 let directory=path.dirname(require.resolve(name));let metadata;
 while(directory!==path.dirname(directory)){
  try{const entry=JSON.parse(await fs.readFile(path.join(directory,'package.json'),'utf8'));if(entry.name===name){metadata=entry;break;}}catch{}
  directory=path.dirname(directory);
 }
 if(!metadata)throw new Error('Missing package metadata: '+name);
 let license;
 for(const file of ['LICENSE','LICENSE.md','LICENSE.txt','license']){try{license=await fs.readFile(path.join(directory,file),'utf8');break;}catch{}}
 if(!license)throw new Error('Missing distribution license: '+name);
 notices.push(`${name} ${metadata.version}\n${'='.repeat(64)}\n${license.trim()}\n`);
}
await fs.writeFile('dist/THIRD_PARTY_LICENSES.txt',notices.join('\n\n'));
await fs.copyFile('dist/index.html','dist/viewer.html');
console.log('Bundled local map engine, document viewer and third-party licenses.');
