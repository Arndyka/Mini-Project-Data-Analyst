"""Validated line-level model and independent Python/SQLite KPI implementations.

Money is represented as integer rupiah. Returns are attributed to original orders.
"""
from collections import Counter,defaultdict
from datetime import date
import sqlite3
from pathlib import Path

def clean(tables):
    clean_tables={};issues=[]
    def issue(table,key,reason,action='quarantined'):
        issues.append(dict(table=table,record_id=key,reason=reason,action=action))
    keys=dict(customers='customer_id',products='product_id',orders='order_id',items='item_id',returns='return_id')
    for name,key in keys.items():
        rows=[];seen=set()
        customer_ids={r['customer_id'] for r in clean_tables.get('customers',[])}
        order_index={r['order_id']:r for r in clean_tables.get('orders',[])}
        product_ids={r['product_id'] for r in clean_tables.get('products',[])}
        item_index={r['item_id']:r for r in clean_tables.get('items',[])}
        refund_totals=Counter()
        for original in tables[name]:
            row=dict(original);rid=row.get(key)
            if not rid:issue(name,'','missing_id');continue
            if rid in seen:issue(name,rid,'duplicate_id');continue
            if name=='products' and not row.get('category'):
                row['category']='Unknown';issue(name,rid,'missing_category','filled_unknown')
            if name=='orders':
                if row.get('customer_id') not in customer_ids:
                    issue(name,rid,'invalid_customer_link');continue
                try:
                    dt=date.fromisoformat(row['date'])
                    assert date(2025,1,1)<=dt<=date(2025,12,31)
                except (TypeError,ValueError,KeyError,AssertionError):issue(name,rid,'invalid_date');continue
                if row.get('status') not in ['completed','cancelled'] or row.get('channel') not in ['Web','App','Store']:
                    issue(name,rid,'invalid_status_or_channel');continue
            if name=='items':
                if row.get('order_id') not in order_index:
                    issue(name,rid,'invalid_order_link');continue
                if row.get('product_id') not in product_ids:
                    issue(name,rid,'invalid_product_link');continue
                vals=[row.get(x) for x in ['quantity','unit_price','discount']]
                if not all(type(v) is int for v in vals) or vals[0]<=0 or vals[1]<0 or not 0<=vals[2]<=vals[0]*vals[1]:
                    issue(name,rid,'invalid_amount');continue
            if name=='returns':
                item=item_index.get(row.get('item_id'))
                if item is None:issue(name,rid,'invalid_item_link');continue
                order=order_index[item['order_id']]
                prior=refund_totals[item['item_id']]
                cap=item['quantity']*item['unit_price']-item['discount']
                try:valid_date=order['date']<=date.fromisoformat(row['date']).isoformat()<='2025-12-31'
                except (TypeError,ValueError,KeyError):valid_date=False
                if order['status']!='completed' or type(row.get('amount')) is not int or not 0<row['amount']<=cap-prior or not valid_date:
                    issue(name,rid,'invalid_refund');continue
            seen.add(rid);rows.append(row)
            if name=='returns':refund_totals[row['item_id']]+=row['amount']
        clean_tables[name]=rows
    orders={x['order_id']:x for x in clean_tables['orders']};products={x['product_id']:x for x in clean_tables['products']}
    refunds=Counter()
    for x in clean_tables['returns']:refunds[x['item_id']]+=x['amount']
    lines=[]
    for x in clean_tables['items']:
        order=orders[x['order_id']]
        lines.append(dict(order_id=x['order_id'],customer_id=order['customer_id'],date=order['date'],category=products[x['product_id']]['category'],channel=order['channel'],gross=x['quantity']*x['unit_price'],discount=x['discount'],refund=refunds[x['item_id']],status=order['status']))
    clean_tables['lines']=lines
    return clean_tables,issues

def metrics(lines):
    rows=[x for x in lines if x['status']=='completed']
    gross=sum(x['gross'] for x in rows);discount=sum(x['discount'] for x in rows);refund=sum(x['refund'] for x in rows)
    orders={x['order_id'] for x in rows};by_customer=defaultdict(set)
    for x in rows:by_customer[x['customer_id']].add(x['order_id'])
    return dict(gross=gross,discount=discount,refund=refund,net=gross-discount-refund,orders=len(orders),customers=len(by_customer),aov=(gross-discount-refund)/len(orders) if orders else 0,repeat_rate=100*sum(len(v)>=2 for v in by_customer.values())/len(by_customer) if by_customer else 0)

def sql_metrics(lines):
    db=sqlite3.connect(':memory:');db.row_factory=sqlite3.Row
    db.execute('CREATE TABLE lines(order_id TEXT, customer_id TEXT, date TEXT, category TEXT, channel TEXT, gross INTEGER, discount INTEGER, refund INTEGER, status TEXT)')
    cols=['order_id','customer_id','date','category','channel','gross','discount','refund','status']
    db.executemany('INSERT INTO lines VALUES (?,?,?,?,?,?,?,?,?)',[tuple(x[k] for k in cols) for x in lines])
    result=dict(db.execute((Path(__file__).parents[1]/'sql/metrics.sql').read_text()).fetchone());db.close()
    return result

def rfm(lines):
    customers=defaultdict(list)
    for row in lines:
        if row['status']=='completed':customers[row['customer_id']].append(row)
    result=[]
    for cid,rows in sorted(customers.items()):
        recency=(date(2026,1,1)-date.fromisoformat(max(x['date'] for x in rows))).days
        frequency=len({x['order_id'] for x in rows});monetary=sum(x['gross']-x['discount']-x['refund'] for x in rows)
        # Transparent, fixed heuristic thresholds, not fitted clusters or a prediction model.
        r=3 if recency<=30 else 2 if recency<=90 else 1
        f=3 if frequency>=10 else 2 if frequency>=3 else 1
        m=3 if monetary>=10000000 else 2 if monetary>=3000000 else 1
        segment='Champions' if r==3 and f==3 and m>=2 else 'Loyal' if f==3 else 'At risk' if r==1 else 'Developing'
        result.append(dict(customer_id=cid,recency_days=recency,frequency=frequency,monetary=monetary,r=r,f=f,m=m,segment=segment))
    return result
