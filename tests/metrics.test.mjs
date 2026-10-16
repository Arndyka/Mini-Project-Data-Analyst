import test from 'node:test';
import assert from 'node:assert/strict';
import { summarize, filterRows } from '../site/metrics.js';
const rows=[{order_id:'1',customer_id:'A',date:'2025-01-01',category:'Home',channel:'App',gross:200,discount:20,refund:50,status:'completed'},{order_id:'2',customer_id:'A',date:'2025-02-01',category:'Home',channel:'App',gross:80,discount:0,refund:80,status:'completed'},{order_id:'3',customer_id:'B',date:'2025-02-01',category:'Tech',channel:'Web',gross:120,discount:0,refund:0,status:'completed'},{order_id:'4',customer_id:'B',date:'2025-02-01',category:'Tech',channel:'Web',gross:999,discount:0,refund:0,status:'cancelled'}];
test('same hand-calculated metrics as Python/SQL',()=>{assert.deepEqual(summarize(rows),{gross:400,discount:20,refund:130,net:250,orders:3,customers:2,aov:250/3,repeat_rate:50});});
test('date category and channel combine, zero denominators remain finite',()=>{
 assert.equal(summarize(filterRows(rows,{start:'2025-02-01',end:'2025-02-28',category:'Home',channel:'App'})).net,0);
 assert.equal(filterRows(rows,{category:'Missing'}).length,0);
 assert.equal(summarize([]).aov,0);assert.equal(summarize([]).repeat_rate,0);
});
