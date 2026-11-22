import {createHash} from 'node:crypto';
import {readFileSync} from 'node:fs';

let contentVersion='dev';
try{
 contentVersion=createHash('sha256').update(readFileSync(new URL('./public/content.hoor',import.meta.url))).digest('hex').slice(0,12);
}catch{}

export default {
 base:'./',
 define:{__CONTENT_VERSION__:JSON.stringify(contentVersion)},
 build:{sourcemap:false,target:'es2022',emptyOutDir:false},
 server:{host:'127.0.0.1',port:5174,strictPort:true},
 preview:{host:'127.0.0.1',port:5174,strictPort:true},
};
