# RetailLens — ringkasan analisis

Seluruh data adalah simulasi, bukan transaksi perusahaan atau bukti dampak bisnis.

## Hasil yang dihitung

- Penjualan bersih: **Rp20.864.988.750**, dari **11,112** order selesai dan **912** pelanggan pembeli.
- Nilai rata-rata order: **Rp1.877.699**. Persentase pembeli dengan sedikitnya dua order selesai: **79.28%**.
- Kategori dengan penjualan bersih terbesar: **Home**, sebesar **Rp3.799.208.250**.
- Puncak penjualan bulanan: **2025-11**, sebesar **Rp2.923.945.750**.
- Perbandingan penjualan Q4 terhadap Q1: **523.08%**. Kenaikan bukan temuan pasar: generator sengaja memberi bobot lebih besar pada order akhir tahun.
- Refund valid: **Rp981.008.250**. Baris cancelled tidak dihitung sebagai penjualan. Order selesai yang direfund penuh tetap masuk denominator AOV.

## Kualitas dan interpretasi

Pipeline mencatat **6** masalah: {"missing_category": 1, "duplicate_id": 2, "invalid_customer_link": 1, "invalid_date": 1, "invalid_amount": 1}. Baris invalid/duplikat dikarantina; kategori kosong diberi Unknown, bukan ditebak. Detail dapat diaudit melalui data_quality.csv dan raw CSV. SQL dan Python menghasilkan KPI yang sama.

RFM memakai data setahun penuh dengan tanggal acuan 1 Januari 2026. Ambang R: ≤30 / ≤90 / >90 hari; F: ≥10 / ≥3 / <3 order; M: ≥Rp10 juta / ≥Rp3 juta / <Rp3 juta. Champions memerlukan R=3, F=3 dan M≥2; Loyal: F=3; At risk: R=1; sisanya Developing. Ini aturan deskriptif, bukan model prediksi.

## Hipotesis tindak lanjut

1. Uji perubahan merchandising pada kategori penjualan terbesar, menggunakan margin yang benar-benar tersedia sebelum menilai profitabilitas.
2. Bandingkan penawaran retensi antar segmen dengan eksperimen terkontrol; data simulasi tidak membuktikan kenaikan retensi.
3. Tinjau nilai refund beserta alasan retur sebelum mengubah kebijakan. Simulasi belum memuat alasan retur atau biaya layanan.

## Batasan

Generator memasukkan kelompok pembeli berulang, kelompok dorman yang berhenti setelah Juni, preferensi channel, kenaikan volume akhir tahun, dan diskon musiman. Karena itu, hasil ini mendemonstrasikan metode, bukan generalisasi perilaku retail. Refund diatribusikan ke tanggal order; tanggal refund tidak melampaui 31 Desember dalam simulasi ini. Tidak tersedia biaya produk, profit, atribusi pemasaran, atau klaim kausal. RFM tidak mengikuti filter dashboard; label panel menjelaskan cakupan tetapnya.
