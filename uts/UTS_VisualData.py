import streamlit as st
import pandas as pd
import plotly.express as px
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
import io

st.set_page_config(page_title="Cafe Sekolah", layout="wide")

st.markdown("""
<style>
.sidebar .sidebar-content {
    background-color: #2f5d9b;
    color: white;
}
[data-testid="stSidebar"] {
    background-color: #2f5d9b;
}
.menu-title {
    font-size: 20px;
    font-weight: bold;
    color: white;
}
.card {
    background-color: #f5f7fa;
    padding: 15px;
    border-radius: 10px;
    margin-bottom: 10px;
}
.highlight {
    background-color: #f4a300;
    padding: 10px;
    border-radius: 8px;
    color: white;
}
</style>
""", unsafe_allow_html=True)

st.sidebar.markdown('<div class="menu-title">☕ Cafe Sekolah</div>', unsafe_allow_html=True)

menu = st.sidebar.radio(
    "",
    ["Dashboard", "POS", "Pre Order", "Stok", "Laporan"]
)

if menu == "Laporan":
    st.sidebar.markdown('<div class="highlight">📁 Laporan</div>', unsafe_allow_html=True)

st.title("Laporan Cafe Sekolah")

tab1, tab2, tab3, tab4 = st.tabs(
    ["Laba Rugi", "Arus Kas", "Menu Terlaris", "Kinerja Siswa"]
)

pendapatan = 5000000
beban_operasional = 1500000
beban_lainnya = 500000
hpp = 1000000
laba_kotor = pendapatan - hpp
laba_bersih = laba_kotor - (beban_operasional + beban_lainnya)

def generate_pdf():
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer)
    styles = getSampleStyleSheet()

    elements = []

    elements.append(Paragraph("Laporan Laba Rugi Cafe Sekolah", styles["Title"]))
    elements.append(Spacer(1, 10))

    data = [
        ["Keterangan", "Nominal"],
        ["Pendapatan", f"Rp {pendapatan:,}"],
        ["HPP", f"Rp {hpp:,}"],
        ["Laba Kotor", f"Rp {laba_kotor:,}"],
        ["Beban Operasional", f"Rp {beban_operasional:,}"],
        ["Beban Lainnya", f"Rp {beban_lainnya:,}"],
        ["Laba Bersih", f"Rp {laba_bersih:,}"],
    ]

    table = Table(data)
    table.setStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.grey),
        ('GRID', (0,0), (-1,-1), 1, colors.black),
    ])

    elements.append(table)
    doc.build(elements)

    buffer.seek(0)
    return buffer

with tab1:
    st.subheader("Laporan Laba Rugi")

    col1, col2, col3, col4 = st.columns(4)

    col1.markdown(f'<div class="card">Pendapatan<br><b>Rp {pendapatan:,}</b></div>', unsafe_allow_html=True)
    col2.markdown(f'<div class="card">Operasional<br><b>Rp {beban_operasional:,}</b></div>', unsafe_allow_html=True)
    col3.markdown(f'<div class="card">Lainnya<br><b>Rp {beban_lainnya:,}</b></div>', unsafe_allow_html=True)
    col4.markdown(f'<div class="card">Laba Bersih<br><b>Rp {laba_bersih:,}</b></div>', unsafe_allow_html=True)

    chart_data = pd.DataFrame({
        "Kategori": ["Pendapatan", "Operasional", "Lainnya", "Laba"],
        "Nilai": [pendapatan, beban_operasional, beban_lainnya, laba_bersih]
    })

    fig = px.bar(chart_data, x="Kategori", y="Nilai")
    st.plotly_chart(fig, use_container_width=True)

    df = pd.DataFrame({
        "Keterangan": [
            "Pendapatan Total",
            "HPP",
            "Laba Kotor",
            "Pengeluaran Operasional",
            "Laba Bersih"
        ],
        "Nominal": [
            pendapatan,
            hpp,
            laba_kotor,
            beban_operasional,
            laba_bersih
        ]
    })

    st.dataframe(df, use_container_width=True)

    pdf = generate_pdf()
    st.download_button(
        label="📄 Export PDF",
        data=pdf,
        file_name="laporan_laba_rugi.pdf",
        mime="application/pdf"
    )

with tab2:
    st.subheader("Arus Kas")
    st.info("Belum tersedia")

with tab3:
    st.subheader("Menu Terlaris")
    st.info("Belum tersedia")

with tab4:
    st.subheader("Kinerja Siswa")
    st.info("Belum tersedia")
