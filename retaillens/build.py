"""Run from repository root: python -m retaillens.build."""
from pathlib import Path
from collections import Counter,defaultdict
import csv,json,sqlite3,shutil
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import nbformat
from .generate import generate
from .analysis import clean,metrics,sql_metrics,rfm

ROOT=Path(__file__).parents[1]
def save_json(path,value):
    path.write_text(json.dumps(value,ensure_ascii=False,separators=(',',':')),encoding='utf8')
def save_csv(path,rows):
    with path.open('w',encoding='utf8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)

def build():
    for folder in ['data/raw','data/clean','reports/charts','site','notebooks']:(ROOT/folder).mkdir(parents=True,exist_ok=True)
    raw=generate();tables,issues=clean(raw);lines=tables['lines'];totals=metrics(lines)
    assert totals==sql_metrics(lines),'Independent SQL reconciliation failed'
    for name,rows in raw.items():save_csv(ROOT/'data/raw'/f'{name}.csv',rows)
    for name,rows in tables.items():save_csv(ROOT/'data/clean'/f'{name}.csv',rows)
    save_csv(ROOT/'reports/data_quality.csv',issues)
    quality={'raw_rows':{k:len(v) for k,v in raw.items()},'clean_rows':{k:len(v) for k,v in tables.items()},'issues':dict(Counter(x['reason'] for x in issues)),'actions':dict(Counter(x['action'] for x in issues))}
    segments=rfm(lines);save_csv(ROOT/'reports/rfm_customers.csv',segments)
    monthly=defaultdict(list);categories=defaultdict(list);channels=defaultdict(list)
    for x in lines:
        monthly[x['date'][:7]].append(x);categories[x['category']].append(x);channels[x['channel']].append(x)
    month_results={k:metrics(v) for k,v in sorted(monthly.items())};category_results={k:metrics(v) for k,v in sorted(categories.items())}
    summary=dict(synthetic=True,seed=42,window=['2025-01-01','2025-12-31'],rfm_reference='2026-01-01',metrics=totals,monthly=month_results,categories=category_results,channels={k:metrics(v) for k,v in channels.items()},quality=quality,segments=dict(Counter(x['segment'] for x in segments)))
    save_json(ROOT/'reports/summary.json',summary)
    cols=list(lines[0]);save_json(ROOT/'site/data.json',dict(columns=cols,rows=[[r[k] for k in cols] for r in lines],summary=summary))
    db=sqlite3.connect(ROOT/'data/retail.sqlite')
    for name,rows in tables.items():
        db.execute(f'DROP TABLE IF EXISTS "{name}"')
        definitions=','.join(f'"{k}" '+('INTEGER' if type(v) is int else 'TEXT') for k,v in rows[0].items())
        db.execute(f'CREATE TABLE "{name}" ({definitions})')
        db.executemany(f'INSERT INTO "{name}" VALUES ({",".join("?" for k in rows[0])})',[tuple(row.values()) for row in rows])
    db.commit();db.close()
    plt.rcParams.update({'font.family':'DejaVu Sans','axes.spines.top':False,'axes.spines.right':False,'axes.titleweight':'bold'})
    for filename,title,values in [
        ('monthly_sales','Monthly net sales · synthetic 2025',{k[5:]:v['net']/1e9 for k,v in month_results.items()}),
        ('category_sales','Net sales by category · synthetic 2025',{k:v['net']/1e9 for k,v in category_results.items()}),
        ('rfm_segments','RFM segments · fixed reference 1 Jan 2026',summary['segments'])]:
        fig,ax=plt.subplots(figsize=(9,4.5),layout='constrained');ax.bar(list(values),list(values.values()),color='#1b8c83');ax.set_title(title,loc='left',pad=18);ax.set_ylabel('IDR billion' if filename!='rfm_segments' else 'Customers');ax.grid(axis='y',alpha=.15);ax.set_axisbelow(True);fig.savefig(ROOT/'reports/charts'/f'{filename}.png',dpi=160);plt.close(fig)
    top=max(category_results,key=lambda k:category_results[k]['net']);peak=max(month_results,key=lambda k:month_results[k]['net'])
    q1=sum(v['net'] for k,v in month_results.items() if k[5:] in ['01','02','03']);q4=sum(v['net'] for k,v in month_results.items() if k[5:] in ['10','11','12'])
    money=lambda n:f'Rp{n:,.0f}'.replace(',','.')
    report=f'''# RetailLens — ringkasan analisis

Seluruh data adalah simulasi, bukan transaksi perusahaan atau bukti dampak bisnis.

## Hasil yang dihitung

- Penjualan bersih: **{money(totals['net'])}**, dari **{totals['orders']:,}** order selesai dan **{totals['customers']:,}** pelanggan pembeli.
- Nilai rata-rata order: **{money(totals['aov'])}**. Persentase pembeli dengan sedikitnya dua order selesai: **{totals['repeat_rate']:.2f}%**.
- Kategori dengan penjualan bersih terbesar: **{top}**, sebesar **{money(category_results[top]['net'])}**.
- Puncak penjualan bulanan: **{peak}**, sebesar **{money(month_results[peak]['net'])}**.
- Perbandingan penjualan Q4 terhadap Q1: **{(q4/q1-1)*100:.2f}%**. Kenaikan bukan temuan pasar: generator sengaja memberi bobot lebih besar pada order akhir tahun.
- Refund valid: **{money(totals['refund'])}**. Baris cancelled tidak dihitung sebagai penjualan. Order selesai yang direfund penuh tetap masuk denominator AOV.

## Kualitas dan interpretasi

Pipeline mencatat **{len(issues)}** masalah: {json.dumps(quality['issues'])}. Baris invalid/duplikat dikarantina; kategori kosong diberi Unknown, bukan ditebak. Detail dapat diaudit melalui data_quality.csv dan raw CSV. SQL dan Python menghasilkan KPI yang sama.

RFM memakai data setahun penuh dengan tanggal acuan 1 Januari 2026. Ambang R: ≤30 / ≤90 / >90 hari; F: ≥10 / ≥3 / <3 order; M: ≥Rp10 juta / ≥Rp3 juta / <Rp3 juta. Champions memerlukan R=3, F=3 dan M≥2; Loyal: F=3; At risk: R=1; sisanya Developing. Ini aturan deskriptif, bukan model prediksi.

## Hipotesis tindak lanjut

1. Uji perubahan merchandising pada kategori penjualan terbesar, menggunakan margin yang benar-benar tersedia sebelum menilai profitabilitas.
2. Bandingkan penawaran retensi antar segmen dengan eksperimen terkontrol; data simulasi tidak membuktikan kenaikan retensi.
3. Tinjau nilai refund beserta alasan retur sebelum mengubah kebijakan. Simulasi belum memuat alasan retur atau biaya layanan.

## Batasan

Generator memasukkan kelompok pembeli berulang, kelompok dorman yang berhenti setelah Juni, preferensi channel, kenaikan volume akhir tahun, dan diskon musiman. Karena itu, hasil ini mendemonstrasikan metode, bukan generalisasi perilaku retail. Refund diatribusikan ke tanggal order; tanggal refund tidak melampaui 31 Desember dalam simulasi ini. Tidak tersedia biaya produk, profit, atribusi pemasaran, atau klaim kausal. RFM tidak mengikuti filter dashboard; label panel menjelaskan cakupan tetapnya.
'''
    (ROOT/'reports/insights.md').write_text(report,encoding='utf8')
    shutil.copyfile(ROOT/'reports/insights.md',ROOT/'site/insights.md')
    shutil.copyfile(ROOT/'reports/data_quality.csv',ROOT/'site/quality.csv')
    nb=nbformat.v4.new_notebook(cells=[nbformat.v4.new_markdown_cell('# RetailLens\nSynthetic retail analysis. Run `python -m retaillens.build` first. No real customer data.'),nbformat.v4.new_code_cell("from pathlib import Path\nimport sys, json\nroot=Path.cwd()\nif root.name=='notebooks': root=root.parent\nsys.path.insert(0,str(root))\nimport pandas as pd\nfrom retaillens.analysis import metrics, sql_metrics\nlines=pd.read_csv(root/'data/clean/lines.csv')\nrecords=lines.to_dict('records')\nresult=metrics(records)\nassert result==sql_metrics(records)\nresult"),nbformat.v4.new_code_cell("completed=lines[lines.status=='completed'].copy()\ncompleted['net']=completed.gross-completed.discount-completed.refund\nassert int(completed.net.sum())==result['net']\ncompleted.groupby('category').net.sum().sort_values(ascending=False)"),nbformat.v4.new_code_cell("quality=pd.read_csv(root/'reports/data_quality.csv')\nquality.groupby(['reason','action']).size()"),nbformat.v4.new_code_cell("from IPython.display import Image, display\ndisplay(Image(filename=str(root/'reports/charts/monthly_sales.png')))"),nbformat.v4.new_markdown_cell('## Interpretation\nRead reports/insights.md. The generated seasonal pattern and repeat-buyer bias are assumptions, not discoveries about a real business. RFM uses the fixed full-year window.')])
    nb.metadata['kernelspec']={'display_name':'Python 3','language':'python','name':'python3'}
    nbformat.write(nb,ROOT/'notebooks/retail_analysis.ipynb')
    print(json.dumps(dict(metrics=totals,quality=quality),indent=2))

if __name__=='__main__':build()
