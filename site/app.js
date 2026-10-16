import {summarize,filterRows} from './metrics.js';
const $=id=>document.getElementById(id),money=n=>new Intl.NumberFormat('id-ID',{style:'currency',currency:'IDR',maximumFractionDigits:0}).format(n),compact=n=>new Intl.NumberFormat('id-ID',{notation:'compact',maximumFractionDigits:1}).format(n),number=n=>new Intl.NumberFormat('id-ID').format(n);
const shortMoney=n=>n>=1e9?'Rp'+(n/1e9).toLocaleString('id-ID',{maximumFractionDigits:2})+' miliar':n>=1e6?'Rp'+(n/1e6).toLocaleString('id-ID',{maximumFractionDigits:2})+' juta':money(n);
const controls=['start','end','category','channel'];let data,rows=[];
const escape=s=>String(s).replace(/[&<>"']/g,x=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[x]));
function update(){
 const f=Object.fromEntries(controls.map(id=>[id,$(id).value]));
 if(f.start&&f.end&&f.start>f.end){$('status').textContent='Tanggal mulai harus sebelum atau sama dengan tanggal akhir.';return;}
 const selected=filterRows(rows,f),m=summarize(selected),completed=selected.filter(r=>r.status==='completed');
 $('net').textContent=shortMoney(m.net);$('net-exact').textContent=money(m.net);$('orders').textContent=number(m.orders);$('aov').textContent=shortMoney(m.aov);$('aov-exact').textContent=money(m.aov);$('repeat').textContent=m.repeat_rate.toFixed(1)+'%';$('refund').textContent=money(m.refund);$('customers').textContent=number(m.customers);
 $('status').textContent=m.orders?`${number(m.orders)} order selesai dalam cakupan terpilih · data sintetis 2025.`:'Tidak ada order selesai untuk filter ini. Ubah atau reset filter.';
 const months=new Map();for(let i=1;i<=12;i++){const k=`2025-${String(i).padStart(2,'0')}`;if((!f.start||k>=f.start.slice(0,7))&&(!f.end||k<=f.end.slice(0,7)))months.set(k,[]);}for(const r of completed)months.get(r.date.slice(0,7))?.push(r);
 const values=[...months].map(([month,rs])=>({month,...summarize(rs)}));
 if(!m.orders){$('trend').innerHTML='<p class="empty">Belum ada data pada cakupan ini.</p>';$('categories').innerHTML='<p class="empty">Tidak ada penjualan.</p>';$('monthly-table').innerHTML='';return;}
 const width=660,height=230,pad=45,max=Math.max(...values.map(v=>v.net),1),x=i=>pad+i*(width-pad-15)/Math.max(values.length-1,1),y=v=>height-35-v/max*(height-65);
 const points=values.map((v,i)=>`${x(i)},${y(v.net)}`).join(' ');
 $('trend').innerHTML=`<svg role="img" aria-label="Tren penjualan bersih per bulan dalam rupiah" viewBox="0 0 ${width} ${height}">${[0,.5,1].map(t=>`<line x1="${pad}" y1="${y(t*max)}" x2="650" y2="${y(t*max)}" stroke="#e2e9e3"/><text x="0" y="${y(t*max)+4}">${escape(compact(t*max))}</text>`).join('')}<polyline points="${points}" fill="none" stroke="#1b8072" stroke-width="3"/>${values.map((v,i)=>`<circle cx="${x(i)}" cy="${y(v.net)}" r="4" fill="#1b8072"><title>${v.month}: ${escape(money(v.net))}</title></circle><text text-anchor="middle" x="${x(i)}" y="220">${v.month.slice(5)}</text>`).join('')}</svg>`;
 $('monthly-table').innerHTML='<table><caption>Ringkasan bulanan sesuai filter</caption><thead><tr><th scope="col">Bulan</th><th scope="col">Order</th><th scope="col">Penjualan bersih</th></tr></thead><tbody>'+values.map(v=>`<tr><th scope="row">${v.month}</th><td>${number(v.orders)}</td><td>${money(v.net)}</td></tr>`).join('')+'</tbody></table>';
 const groups=new Map();for(const r of completed){if(!groups.has(r.category))groups.set(r.category,[]);groups.get(r.category).push(r);}const cats=[...groups].map(([label,rs])=>({label,value:summarize(rs).net})).sort((a,b)=>b.value-a.value);
 $('categories').innerHTML=cats.map(c=>`<div><div class="bar-label"><span>${escape(c.label)}</span><strong>${escape(compact(c.value))}</strong></div><div class="bar-track"><div class="bar-fill" style="width:${100*c.value/Math.max(cats[0].value,1)}%"></div></div></div>`).join('');
}
try{
 const response=await fetch('data.json');if(!response.ok)throw Error('Data tidak tersedia');data=await response.json();rows=data.rows.map(r=>Object.fromEntries(data.columns.map((k,i)=>[k,r[i]])));
 for(const id of ['category','channel'])for(const value of [...new Set(rows.map(r=>r[id]))].sort()){$(id).add(new Option(value,value));}
 $('segments').innerHTML=Object.entries(data.summary.segments).map(([label,count])=>`<div class="segment"><strong>${number(count)}</strong><span>${escape(label)}</span></div>`).join('');
 $('quality-count').textContent=number(Object.values(data.summary.quality.issues).reduce((a,b)=>a+b,0))+' temuan';
 const top=Object.entries(data.summary.categories).sort((a,b)=>b[1].net-a[1].net)[0];$('finding').textContent=`Pada cakupan setahun penuh, ${top[0]} menyumbang penjualan bersih terbesar (${money(top[1].net)}). Ringkasan tertulis menjelaskan asumsi generator dan keterbatasan interpretasinya.`;
 controls.forEach(id=>$(id).addEventListener('change',update));$('reset').addEventListener('click',()=>{$('start').value='2025-01-01';$('end').value='2025-12-31';$('category').value='';$('channel').value='';update();});update();
}catch(error){$('status').textContent='Data belum berhasil dimuat. Muat ulang halaman atau buka dataset melalui tautan GitHub.';console.error(error);}
