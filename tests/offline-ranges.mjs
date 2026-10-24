import {readFileSync} from 'node:fs';
import vm from 'node:vm';
import assert from 'node:assert/strict';
const context=vm.createContext({Response,self:{addEventListener(){}}});
vm.runInContext(readFileSync(new URL('../sw.js',import.meta.url),'utf8'),context);
for(const [range,status,body,header]of [
 ['bytes=2-5',206,'2345','bytes 2-5/10'],
 ['bytes=7-',206,'789','bytes 7-9/10'],
 ['bytes=-3',206,'789','bytes 7-9/10'],
 ['bytes=10-',416,'','bytes */10'],
 ['bytes=7-3',416,'','bytes */10'],
]){
 const result=await context.ranged(new Response('0123456789'),range);
 assert.equal(result.status,status);assert.equal(await result.text(),body);assert.equal(result.headers.get('Content-Range'),header);
}
console.log('Five offline MP3 range cases passed.');
