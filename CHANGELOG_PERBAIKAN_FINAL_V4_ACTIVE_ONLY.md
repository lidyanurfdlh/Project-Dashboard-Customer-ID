# Changelog Perbaikan Final V4 - Active Customers Only

## Keputusan metodologis final
- Segmen `No Valid Purchase` tidak lagi ditampilkan pada dashboard utama.
- Dashboard utama hanya menganalisis pelanggan yang memiliki minimal satu transaksi valid.
- Total pelanggan awal tetap 105, tetapi pelanggan yang dianalisis menjadi 87.
- Sebanyak 18 pelanggan tanpa transaksi valid dicatat pada `excluded_customers.csv` dan `preprocessing_audit.csv`.
- Label kategori `-` pada Favorite Category Distribution dihilangkan karena pelanggan tanpa kategori favorit tidak lagi dimasukkan ke `customer_rfm.csv`.

## Perbaikan Colab
1. Menambahkan pemisahan `active_customer_ids` dan `excluded_customer_ids`.
2. Mengubah `customer_rfm` agar hanya berisi pelanggan aktif.
3. Menghapus logika segmentasi `No Valid Purchase` dari output utama.
4. Menambahkan `excluded_customers.csv` sebagai audit metodologis.
5. Menyesuaikan `project_summary.json` dengan angka `raw_customers`, `analyzed_customers`, dan `excluded_customers_without_valid_orders`.

## Perbaikan Streamlit
1. Mengubah KPI card menjadi `Raw Customers`, `Analyzed Customers`, `Excluded Customers`, `Valid Orders`, dan `Relevance Rate`.
2. Menghapus warna dan filter untuk `No Valid Purchase`.
3. Mengubah narasi Executive Overview dan Data Validation agar menjelaskan active customer selection.
4. Memastikan Favorite Category Distribution tidak menampilkan label `-`.
5. Memperbaiki visual Nudge Framework menjadi horizontal bar berdasarkan jumlah customer per segmen.
6. Menambahkan tabel `excluded_customers` pada Data Explorer.

## Cara menjalankan
```bash
cd customer_id_final_fix_v2/streamlit_customer_id_final_v2
python -m pip install -r requirements.txt
python -m streamlit run app_customer_id_final_v2.py
```

## Update raw data audit sebelum preprocessing
- Menambahkan tab **Raw Data Audit** pada dashboard Streamlit.
- Menambahkan card untuk jumlah record dan jumlah field pada raw data: pelanggan, orders, detil_order, dan produk.
- Menambahkan bagan jumlah record raw data sebelum preprocessing agar jelas bahwa 182 adalah jumlah valid orders setelah filtering, bukan jumlah data mentah awal.
- Menambahkan `raw_data_summary.csv` dan `raw_field_summary.csv` pada folder outputs.
