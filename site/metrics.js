export function filterRows(rows,{start='',end='',category='',channel=''}={}) {
 return rows.filter(r=>(!start||r.date>=start)&&(!end||r.date<=end)&&(!category||r.category===category)&&(!channel||r.channel===channel));
}
export function summarize(lines) {
 const rows=lines.filter(r=>r.status==='completed'),orders=new Set(),customers=new Map();
 let gross=0,discount=0,refund=0;
 for(const r of rows){gross+=r.gross;discount+=r.discount;refund+=r.refund;orders.add(r.order_id);if(!customers.has(r.customer_id))customers.set(r.customer_id,new Set());customers.get(r.customer_id).add(r.order_id);}
 const net=gross-discount-refund;
 return {gross,discount,refund,net,orders:orders.size,customers:customers.size,aov:orders.size?net/orders.size:0,repeat_rate:customers.size?100*[...customers.values()].filter(o=>o.size>=2).length/customers.size:0};
}
