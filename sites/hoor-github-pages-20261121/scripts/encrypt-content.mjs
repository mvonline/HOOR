import {webcrypto} from 'node:crypto';
import {readFile,writeFile,mkdir} from 'node:fs/promises';
import {gzipSync} from 'node:zlib';

const MAGIC=Buffer.from('HOORPK01','ascii');
const ITERATIONS=600000;
const SOURCE=new URL('../.snapshot/portal-data.json',import.meta.url);
const OUTPUT=new URL('../public/content.hoor',import.meta.url);
const MAX_CONTENT_BYTES=32*1024*1024;

async function readHiddenPassword(){
 if(!process.stdin.isTTY)throw new Error('Password input requires a TTY; do not pass it in arguments, environment variables or a file.');
 const previousRaw=process.stdin.isRaw;
 process.stdin.setRawMode(true);process.stdin.setEncoding('utf8');process.stdin.resume();
 console.log('Ready for hidden password input.');
 try{
  return await new Promise((resolve,reject)=>{
   let value='';
   const cleanup=()=>{process.stdin.off('data',onData);process.stdin.off('end',onEnd);};
   const onEnd=()=>{cleanup();reject(new Error('Password input ended before a line was received.'));};
   const onData=chunk=>{
    for(const character of chunk){
     if(character==='\u0003'||character==='\u0004'){cleanup();reject(new Error('Password input cancelled.'));return;}
     if(character==='\r'||character==='\n'){cleanup();resolve(value);return;}
     if(character==='\u007f'||character==='\b'){value=Array.from(value).slice(0,-1).join('');continue;}
     if(character<' '){continue;}
     value+=character;
     if(value.length>128){cleanup();reject(new Error('Password input is too long.'));return;}
    }
   };
   process.stdin.on('data',onData);process.stdin.once('end',onEnd);
  });
 }finally{process.stdin.setRawMode(Boolean(previousRaw));process.stdin.pause();process.stdout.write('\n');}
}

try{
 let password=await readHiddenPassword();
 if(!password)throw new Error('A non-empty password is required.');
 let snapshot;try{snapshot=JSON.parse(await readFile(SOURCE,'utf8'));}catch{throw new Error('The source content snapshot is not valid JSON.');}
 if(!Array.isArray(snapshot?.library?.docs)||!Array.isArray(snapshot?.library?.gallery)||!snapshot?.media||typeof snapshot.mapHtml!=='string')throw new Error('The content snapshot is incomplete.');
 snapshot.library.readerEdition=JSON.parse(await readFile(new URL('../content/reader-edition.json',import.meta.url),'utf8'));
 snapshot.library.dialogues=JSON.parse(await readFile(new URL('../content/dialogues.json',import.meta.url),'utf8'));
 if(Object.keys(snapshot.library.readerEdition).length!==18||snapshot.library.dialogues.chapters.length!==10||snapshot.library.dialogues.recordings.length!==6)throw new Error('The reader edition or dialogue collection is incomplete.');
 const plaintext=Buffer.from(JSON.stringify(snapshot),'utf8');
 if(!plaintext.length||plaintext.length>MAX_CONTENT_BYTES)throw new Error('The content snapshot is outside the supported size.');
 const salt=webcrypto.getRandomValues(new Uint8Array(16)),iv=webcrypto.getRandomValues(new Uint8Array(12));
 const header=Buffer.from(JSON.stringify({version:1,cipher:'AES-GCM',keyBits:256,kdf:'PBKDF2-SHA256',iterations:ITERATIONS,salt:Buffer.from(salt).toString('base64url'),iv:Buffer.from(iv).toString('base64url'),compression:'gzip',contentType:'application/json',plaintextBytes:plaintext.length}),'utf8');
 const passwordBytes=new TextEncoder().encode(password);password='';
 const material=await webcrypto.subtle.importKey('raw',passwordBytes,'PBKDF2',false,['deriveKey']);passwordBytes.fill(0);
 const key=await webcrypto.subtle.deriveKey({name:'PBKDF2',hash:'SHA-256',salt,iterations:ITERATIONS},material,{name:'AES-GCM',length:256},false,['encrypt']);
 const compressed=gzipSync(plaintext,{level:9});
 const ciphertext=Buffer.from(await webcrypto.subtle.encrypt({name:'AES-GCM',iv,additionalData:header,tagLength:128},key,compressed));
 const headerLength=Buffer.alloc(4);headerLength.writeUInt32BE(header.length);
 await mkdir(new URL('../public/',import.meta.url),{recursive:true});
 await writeFile(OUTPUT,Buffer.concat([MAGIC,headerLength,header,ciphertext]));
 console.log(JSON.stringify({output:'public/content.hoor',bytes:MAGIC.length+4+header.length+ciphertext.length,documents:snapshot.library.docs.length,images:snapshot.library.gallery.length,readerSummaries:Object.keys(snapshot.library.readerEdition).length,dialogueChapters:snapshot.library.dialogues.chapters.length,recordings:snapshot.library.dialogues.recordings.length}));
}catch(error){console.error(error instanceof Error?error.message:'Unable to encrypt the content snapshot.');process.exitCode=1;}
