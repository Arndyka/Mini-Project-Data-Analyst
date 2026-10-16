import unittest
from copy import deepcopy
from retaillens.analysis import metrics, sql_metrics, clean, rfm
from retaillens.generate import generate

class MetricsTests(unittest.TestCase):
    def fixture(self):
        return [dict(order_id='O1',customer_id='A',date='2025-12-01',category='Home',channel='Web',gross=200,discount=20,refund=50,status='completed'),
                dict(order_id='O2',customer_id='A',date='2025-12-20',category='Home',channel='Web',gross=80,discount=0,refund=80,status='completed'),
                dict(order_id='O3',customer_id='B',date='2025-12-21',category='Home',channel='Web',gross=999,discount=0,refund=0,status='cancelled'),
                dict(order_id='O4',customer_id='B',date='2025-12-22',category='Tech',channel='Store',gross=120,discount=0,refund=0,status='completed')]

    def test_independent_hand_calculated_metrics(self):
        result=metrics(self.fixture())
        self.assertEqual([result[k] for k in ['gross','discount','refund','net','orders','customers']], [400,20,130,250,3,2])
        self.assertAlmostEqual(result['aov'],250/3)
        self.assertEqual(result['repeat_rate'],50)
        self.assertEqual(result,sql_metrics(self.fixture()))

    def test_empty_scope(self):
        result=metrics([])
        self.assertEqual(result['aov'],0)
        self.assertEqual(result['repeat_rate'],0)
        self.assertEqual(result,sql_metrics([]))

    def test_deterministic_generation_and_cleaning(self):
        raw=generate(42,orders=80)
        self.assertEqual(raw,generate(42,orders=80))
        tables,issues=clean(raw)
        self.assertTrue(issues)
        self.assertEqual(len(tables['orders']),80)
        self.assertEqual(metrics(tables['lines']),sql_metrics(tables['lines']))
        self.assertTrue(all(x['gross']>=x['discount']+x['refund'] for x in tables['lines']))

    def test_unknown_links_negative_amounts_and_duplicates_are_reported(self):
        raw=generate(3,orders=30)
        raw['items'].extend([deepcopy(raw['items'][0]),dict(item_id='BAD',order_id='MISSING',product_id='P001',quantity=1,unit_price=10,discount=0),dict(item_id='NEG',order_id='O00001',product_id='P001',quantity=1,unit_price=-2,discount=0)])
        tables,issues=clean(raw)
        reasons={x['reason'] for x in issues}
        self.assertIn('duplicate_id',reasons)
        self.assertIn('invalid_order_link',reasons)
        self.assertIn('invalid_amount',reasons)
        self.assertTrue(all(x['order_id']!='MISSING' for x in tables['lines']))

    def test_rfm_fixed_reference_and_cancelled_exclusion(self):
        rows=rfm(self.fixture())
        a=next(x for x in rows if x['customer_id']=='A')
        self.assertEqual(a['recency_days'],12)
        self.assertEqual(a['frequency'],2)
        self.assertEqual(a['monetary'],130)

    def test_null_and_numeric_dates_are_quarantined_without_aborting(self):
        raw=generate(42,orders=3)
        raw['orders'][0]['date']=None
        raw['orders'][1]['date']=123
        tables,issues=clean(raw)
        self.assertGreaterEqual(sum(x['reason']=='invalid_date' for x in issues),2)
        raw=generate(42,orders=3)
        raw['orders'][0]['status']='completed'
        raw['returns']=[dict(return_id='N1',item_id=raw['items'][0]['item_id'],amount=1,date=None),dict(return_id='N2',item_id=raw['items'][0]['item_id'],amount=1,date=123)]
        tables,issues=clean(raw)
        self.assertEqual(sum(x['reason']=='invalid_refund' for x in issues),2)
        self.assertEqual(tables['returns'],[])

if __name__=='__main__':unittest.main()
