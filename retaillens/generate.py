"""Seeded synthetic source tables, including deliberately documented bad records."""
from datetime import date,timedelta
import random
from copy import deepcopy

CATEGORIES=['Home','Electronics','Fashion','Beauty','Sports','Books']

def generate(seed=42,orders=12000):
    rng=random.Random(seed)
    customers=[dict(customer_id=f'C{i:04}',region=rng.choice(['West','Central','East']),joined='2024-01-01') for i in range(1,1001)]
    products=[dict(product_id=f'P{i:03}',category=CATEGORIES[(i-1)%6],product_name=f'Synthetic product {i:02}',list_price=rng.randrange(3,100)*10000) for i in range(1,61)]
    out=dict(customers=customers,products=products,orders=[],items=[],returns=[])
    start=date(2025,1,1)
    for i in range(1,orders+1):
        # A fixed simulation assumption: more year-end orders, plus a repeat-buyer group.
        day=int(rng.triangular(0,365,355));day=min(day,364)
        dt=start+timedelta(days=day)
        cid=rng.randint(1,200) if rng.random()<.85 else rng.randint(201,1000)
        # A fictional dormant group stops ordering after June; this gives RFM
        # a meaningful range without pretending to discover real churn.
        if cid>=801:dt=start+timedelta(days=min(day,180))
        order=dict(order_id=f'O{i:05}',customer_id=f'C{cid:04}',date=dt.isoformat(),channel=rng.choices(['Web','App','Store'],[.3,.45,.25])[0],status='cancelled' if rng.random()<.08 else 'completed')
        out['orders'].append(order)
        for j in range(rng.randint(1,3)):
            product=rng.choice(products);qty=rng.randint(1,3);gross=qty*product['list_price']
            discount=gross*rng.choice([0,0,5,10,15] if dt.month<11 else [0,10,15,20])//100
            item=dict(item_id=f'I{i:05}-{j}',order_id=order['order_id'],product_id=product['product_id'],quantity=qty,unit_price=product['list_price'],discount=discount)
            out['items'].append(item)
            if order['status']=='completed' and rng.random()<.06:
                out['returns'].append(dict(return_id=f'R{i:05}-{j}',item_id=item['item_id'],amount=(gross-discount)*rng.choice([50,100])//100,date=min(dt+timedelta(days=rng.randint(1,20)),date(2025,12,31)).isoformat()))
    out['orders'].append(deepcopy(out['orders'][0]))
    out['orders'].append(dict(order_id='BAD-CUSTOMER',customer_id='MISSING',date='2025-05-01',channel='Web',status='completed'))
    out['orders'].append(dict(order_id='BAD-DATE',customer_id='C0001',date='2025-02-30',channel='Web',status='completed'))
    out['items'].extend([deepcopy(out['items'][0]),dict(item_id='BAD-PRICE',order_id='O00001',product_id='P001',quantity=1,unit_price=-100,discount=0)])
    out['products'][0]['category']=''
    return out
