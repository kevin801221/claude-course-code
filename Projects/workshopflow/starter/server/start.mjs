import express from 'express';
import {fileURLToPath} from 'node:url';
import {api} from './routes.mjs';
const app=express(), dist=fileURLToPath(new URL('../dist/',import.meta.url));
app.use(express.json({limit:'16kb'}));app.use('/api',api);app.use(express.static(dist));
app.use((err,_q,r,_n)=>{const status=err.status || 500;if(status>=500) console.error(err);r.status(status).json({error:status>=500?'服務執行失敗':err.message});});
const srv=app.listen(Number(process.env.PORT||4100),'127.0.0.1',()=>console.log('READY http://127.0.0.1:'+srv.address().port));
