type Progress=(message:string)=>void;
type ErrorCode='password'|'network'|'format'|'decompression'|'content'|'unsupported'|'cancelled';
type Package={library:any;media:Record<string,{type:string;data:string}>;mapHtml:string};
type Header={version:number;cipher:string;keyBits:number;kdf:string;iterations:number;salt:string;iv:string;compression:string;contentType:string;plaintextBytes:number};

export class PortalError extends Error{
 constructor(public readonly code:ErrorCode,message:string){super(message);this.name='PortalError';}
}

const MAGIC='HOORPK01',MAX_DOWNLOAD=32*1024*1024,MAX_PLAINTEXT=32*1024*1024,MAX_ITERATIONS=1000000;
const encoder=new TextEncoder();
let ciphertext:Uint8Array|null=null,pendingDownload:Promise<Uint8Array>|null=null;
let decrypted:Package|null=null,epoch=0,mapObjectUrl:string|null=null;
const imageObjectUrls=new Map<string,string>();

const failure=(code:ErrorCode)=>new PortalError(code,{
 password:'رمز درست نیست. دوباره بررسی کنید.',
 network:'دریافت کتاب طراحی انجام نشد. اتصال اینترنت را بررسی کنید و دوباره تلاش کنید.',
 format:'بستهٔ کتاب طراحی معتبر نیست. صفحه را تازه کنید یا به مسئول سایت اطلاع دهید.',
 decompression:'رمزگشایی انجام شد، اما بازکردن بستهٔ محتوا ممکن نشد. بستهٔ منتشرشده نیاز به بررسی دارد.',
 content:'محتوای کتاب طراحی ناقص یا نامعتبر است. بستهٔ منتشرشده نیاز به بررسی دارد.',
 unsupported:'مرورگر از بازکردن امن این بسته پشتیبانی نمی‌کند. از مرورگر به‌روز و نشانی HTTPS استفاده کنید.',
 cancelled:'ورود لغو شد.',
}[code]);

function baseUrl(){
 const configured=(import.meta as ImportMeta&{env?:{BASE_URL?:string}}).env?.BASE_URL||'./';
 return new URL(configured,document.baseURI);
}

async function readBounded(stream:ReadableStream<Uint8Array>,limit:number,errorCode:ErrorCode){
 const reader=stream.getReader(),chunks:Uint8Array[]=[];let total=0;
 try{
  for(;;){const part=await reader.read();if(part.done)break;total+=part.value.byteLength;if(total>limit){await reader.cancel();throw failure(errorCode);}chunks.push(part.value);}
 }finally{reader.releaseLock();}
 const result=new Uint8Array(total);let offset=0;for(const chunk of chunks){result.set(chunk,offset);offset+=chunk.byteLength;}return result;
}

async function download(progress?:Progress){
 if(ciphertext)return ciphertext;
 if(pendingDownload)return pendingDownload;
 progress?.('در حال دریافت بستهٔ کتاب طراحی…');
 pendingDownload=(async()=>{
  try{
   const response=await fetch(new URL('content.hoor',baseUrl()),{cache:'no-store',credentials:'omit'});
   if(!response.ok)throw failure('network');
   const declared=Number(response.headers.get('content-length'));
   if(declared>MAX_DOWNLOAD)throw failure('format');
   const bytes=response.body?await readBounded(response.body,MAX_DOWNLOAD,'format'):new Uint8Array(await response.arrayBuffer());
   if(!bytes.length||bytes.length>MAX_DOWNLOAD)throw failure('format');
   ciphertext=bytes;return bytes;
  }catch(error){if(error instanceof PortalError)throw error;throw failure('network');}
 })();
 try{return await pendingDownload;}finally{pendingDownload=null;}
}

function decodeBase64Url(value:string,length:number){
 if(typeof value!=='string'||!/^[A-Za-z0-9_-]+$/.test(value))throw failure('format');
 let binary:string;try{binary=atob(value.replace(/-/g,'+').replace(/_/g,'/'));}catch{throw failure('format');}
 if(binary.length!==length)throw failure('format');
 return Uint8Array.from(binary,c=>c.charCodeAt(0));
}

function envelope(bytes:Uint8Array){
 if(bytes.length<29||new TextDecoder().decode(bytes.subarray(0,8))!==MAGIC)throw failure('format');
 const length=new DataView(bytes.buffer,bytes.byteOffset,bytes.byteLength).getUint32(8,false);
 if(length<2||length>4096||bytes.length<=12+length+16)throw failure('format');
 const headerBytes=bytes.slice(12,12+length);let header:Header;
 try{header=JSON.parse(new TextDecoder('utf-8',{fatal:true}).decode(headerBytes));}catch{throw failure('format');}
 if(!header||header.version!==1||header.cipher!=='AES-GCM'||header.keyBits!==256||header.kdf!=='PBKDF2-SHA256'||header.compression!=='gzip'||header.contentType!=='application/json'||!Number.isInteger(header.iterations)||header.iterations<100000||header.iterations>MAX_ITERATIONS||!Number.isInteger(header.plaintextBytes)||header.plaintextBytes<1||header.plaintextBytes>MAX_PLAINTEXT)throw failure('format');
 const salt=decodeBase64Url(header.salt,16),iv=decodeBase64Url(header.iv,12);
 return {header,headerBytes,salt,iv,cipher:bytes.slice(12+length)};
}

function validateContent(value:any):value is Package{
 const l=value?.library,m=value?.media;
 if(!l||!Array.isArray(l.docs)||!l.docs.length||l.docs.length>1000||!Array.isArray(l.gallery)||!l.gallery.length||l.gallery.length>1000||!Array.isArray(l.chapters)||!Array.isArray(l.sideStories)||!Array.isArray(l.people)||!Array.isArray(l.chapterSummaries)||!Array.isArray(l.budget?.main_missions)||!l.copy||!m||typeof m!=='object'||Array.isArray(m)||typeof value.mapHtml!=='string'||value.mapHtml.length>3*1024*1024)return false;
 if(l.docs.some((d:any)=>typeof d?.id!=='string'||typeof d.markdown!=='string'||typeof d.title!=='string'))return false;
 if(l.gallery.some((g:any)=>typeof g?.id!=='string'||!Object.prototype.hasOwnProperty.call(m,g.id)))return false;
 const entries=Object.values(m) as any[];
 return entries.length<=1000&&entries.every(image=>image&&['image/webp','image/png','image/jpeg'].includes(image.type)&&typeof image.data==='string'&&image.data.length<=8*1024*1024&&/^[A-Za-z0-9+/]*={0,2}$/.test(image.data));
}

function clearPlaintext(){
 for(const url of imageObjectUrls.values())URL.revokeObjectURL(url);imageObjectUrls.clear();
 if(mapObjectUrl)URL.revokeObjectURL(mapObjectUrl);mapObjectUrl=null;decrypted=null;
}

export function lock(){epoch++;clearPlaintext();}
export function getLibrary(){return decrypted?.library??null;}

export async function unlock(password:string,onProgress?:Progress){
 if(!globalThis.crypto?.subtle||typeof DecompressionStream==='undefined')throw failure('unsupported');
 if(typeof password!=='string'||!password.length||password.length>128)throw failure('password');
 const attempt=++epoch;clearPlaintext();
 const current=()=>{if(attempt!==epoch)throw failure('cancelled');};
 const bytes=await download(onProgress);current();
 const parsed=envelope(bytes);onProgress?.('در حال بررسی رمز و بازکردن بسته…');
 const passwordBytes=encoder.encode(password);password='';
 const material=await crypto.subtle.importKey('raw',passwordBytes,'PBKDF2',false,['deriveKey']);passwordBytes.fill(0);current();
 const key=await crypto.subtle.deriveKey({name:'PBKDF2',hash:'SHA-256',salt:parsed.salt,iterations:parsed.header.iterations},material,{name:'AES-GCM',length:256},false,['decrypt']);current();
 let compressed:ArrayBuffer;
 try{compressed=await crypto.subtle.decrypt({name:'AES-GCM',iv:parsed.iv,additionalData:parsed.headerBytes,tagLength:128},key,parsed.cipher);}catch{current();throw failure('password');}
 current();onProgress?.('در حال آماده‌کردن متن‌ها، تصاویر و نقشه‌ها…');
 let plaintext:Uint8Array;
 try{const stream=new Blob([compressed]).stream().pipeThrough(new DecompressionStream('gzip'));plaintext=await readBounded(stream,Math.min(parsed.header.plaintextBytes,MAX_PLAINTEXT),'decompression');}catch(error){if(error instanceof PortalError)throw error;throw failure('decompression');}
 current();if(plaintext.byteLength!==parsed.header.plaintextBytes)throw failure('content');
 let content:any;try{content=JSON.parse(new TextDecoder('utf-8',{fatal:true}).decode(plaintext));}catch{throw failure('content');}finally{plaintext.fill(0);}
 current();if(!validateContent(content))throw failure('content');
 decrypted=content;return content.library;
}

export function mediaUrl(id:string):string{
 if(imageObjectUrls.has(id))return imageObjectUrls.get(id)!;
 if(!decrypted||!Object.prototype.hasOwnProperty.call(decrypted.media,id))return '';
 const item=decrypted.media[id];let binary:string;try{binary=atob(item.data);}catch{throw failure('content');}
 const bytes=Uint8Array.from(binary,c=>c.charCodeAt(0));
 const url=URL.createObjectURL(new Blob([bytes],{type:item.type}));imageObjectUrls.set(id,url);return url;
}

export function mapUrl():string{
 if(mapObjectUrl)return mapObjectUrl;if(!decrypted)return '';
 const engineUrl=new URL('assets/map-engine.js',baseUrl()).href;
 const html=decrypted.mapHtml.replaceAll('https://esm.sh/d3-geo@3.1.1',engineUrl);
 mapObjectUrl=URL.createObjectURL(new Blob([html],{type:'text/html; charset=utf-8'}));return mapObjectUrl;
}
