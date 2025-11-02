import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="InsightBoard - Analisis Penjualan", layout="wide", initial_sidebar_state="expanded")

CSV_PATH = "CSV_PATH = uts/Copy of finalProj_df - df.csv"
"
df = pd.read_csv(CSV_PATH)

date_cols = [c for c in df.columns if "date" in c.lower() or "time" in c.lower()]
num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
cat_cols = df.select_dtypes(exclude=[np.number]).columns.tolist()

st.markdown("""
<style>
body {
    background-color: #0f172a;
    color: #e2e8f0;
}
[data-testid="stSidebar"] {
    background: rgba(15, 23, 42, 0.7);
    backdrop-filter: blur(12px);
}
h1, h2, h3 {
    color: #38bdf8;
}
.card {
    background: rgba(255,255,255,0.05);
    padding: 1rem;
    border-radius: 15px;
    box-shadow: inset 1px 1px 4px rgba(255,255,255,0.05),
                inset -1px -1px 4px rgba(0,0,0,0.2);
}
</style>
""", unsafe_allow_html=True)

st.sidebar.title("Navigasi InsightBoard")
menu = st.sidebar.radio("Pilih Halaman:", [
    "Ringkasan Data",
    "Pola Waktu & Tren",
    "Profit & Margin",
    "Kontribusi Kategori",
    "Segmentasi Pelanggan",
])

if menu == "Ringkasan Data":
    st.title("InsightBoard — Analisis Pola Penjualan")
    st.markdown("Dashboard ini menampilkan **pola performa penjualan dan perilaku pelanggan** berdasarkan dataset transaksi.")

    col1, col2, col3, col4 = st.columns(4)
    main_num = num_cols[0] if num_cols else None
    if main_num:
        col1.metric("Total Nilai", f"{df[main_num].sum():,.0f}")
        col2.metric("Rata-rata", f"{df[main_num].mean():,.2f}")
        col3.metric("Median", f"{df[main_num].median():,.2f}")
        col4.metric("Jumlah Data", f"{len(df)}")

    st.markdown("### Contoh Data")
    st.dataframe(df.head(10), use_container_width=True)

elif menu == "Pola Waktu & Tren":
    st.title("Pola Waktu dan Tren Penjualan")

    if date_cols:
        date_col = st.selectbox("Pilih kolom waktu:", date_cols)
        df[date_col] = pd.to_datetime(df[date_col], errors="coerce")
        numeric = st.selectbox("Pilih kolom numerik:", num_cols)
        df_time = df.groupby(df[date_col].dt.to_period("M"))[numeric].sum().reset_index()
        df_time[date_col] = df_time[date_col].dt.to_timestamp()

        fig = px.area(df_time, x=date_col, y=numeric, color_discrete_sequence=["#22d3ee"],
                      title="Pola Penjualan Bulanan", template="plotly_dark")
        fig.update_traces(fill='tozeroy')
        st.plotly_chart(fig, use_container_width=True)

        df_time["MovingAvg"] = df_time[numeric].rolling(3).mean()
        fig2 = px.line(df_time, x=date_col, y="MovingAvg", color_discrete_sequence=["#38bdf8"],
                       title="Tren Rata-rata Bergerak (3 Bulan)", template="plotly_dark")
        st.plotly_chart(fig2, use_container_width=True)
    else:
        st.warning("Tidak ditemukan kolom tanggal untuk analisis pola waktu.")

elif menu == "Profit & Margin":
    st.title("Distribusi Profit dan Margin")

    if "profit" in df.columns:
        col = "profit"
    elif len(num_cols) >= 2:
        col = st.selectbox("Pilih kolom keuntungan / nilai:", num_cols)
    else:
        st.error("Tidak ada kolom numerik yang dapat digunakan.")
        st.stop()

    df["margin_percent"] = (df[col] / (df[col].max() + 1)) * 100
    fig = px.violin(df, y="margin_percent", box=True, points="all",
                    color_discrete_sequence=["#22c55e"], template="plotly_dark",
                    title="Distribusi Margin (%)")
    st.plotly_chart(fig, use_container_width=True)

    avg_margin = df["margin_percent"].mean()
    st.info(f"Rata-rata margin profit: **{avg_margin:.2f}%**")

elif menu == "Kontribusi Kategori":
    st.title("Kontribusi Kategori terhadap Total Penjualan")

    if cat_cols and num_cols:
        cat = st.selectbox("Pilih kolom kategori:", cat_cols)
        num = st.selectbox("Pilih kolom nilai:", num_cols)
        df_cat = df.groupby(cat)[num].sum().sort_values(ascending=False).reset_index()

        fig = px.pie(df_cat, values=num, names=cat, hole=0.5, color_discrete_sequence=px.colors.sequential.Teal)
        fig.update_traces(textposition='inside', textinfo='percent+label')
        fig.update_layout(title="Proporsi Kontribusi Kategori", showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

        st.dataframe(df_cat.head(10))
    else:
        st.warning("Tidak ditemukan data kategorikal untuk kontribusi.")

elif menu == "Segmentasi Pelanggan":
    st.title("Segmentasi Pelanggan Berdasarkan Perilaku Pembelian")

    if "customer_id" in df.columns and len(num_cols) > 0:
        val = num_cols[0]
        df_seg = df.groupby("customer_id")[val].sum().reset_index()
        q1, q2 = df_seg[val].quantile([0.33, 0.66])
        def segment(v):
            if v <= q1: return "Low"
            elif v <= q2: return "Medium"
            else: return "High"
        df_seg["Segment"] = df_seg[val].apply(segment)

        seg_count = df_seg["Segment"].value_counts()
        fig = px.bar(x=seg_count.index, y=seg_count.values,
                     color=seg_count.index, color_discrete_sequence=px.colors.qualitative.Bold,
                     title="Jumlah Pelanggan per Segmen")
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("### Distribusi Pelanggan Berdasarkan Total Pembelian")
        st.dataframe(df_seg.head(15))
    else:
        st.warning("Kolom customer_id tidak ditemukan dalam dataset.")


