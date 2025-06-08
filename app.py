import streamlit as st
import fitz, pandas as pd, re, tempfile

def extract_resi(text):
    result = {
        'No. Resi': re.search(r"No. Resi:\s*(\S+)", text),
        'Nama Penerima': re.search(r"Penerima:\s*[\d+]*\s*(.+?)\n", text),
        'Alamat': re.search(r"Penerima:.*?\n(.+?\n.+?)\nBerat:", text, re.DOTALL),
        'Berat (gr)': re.search(r"Berat:\s*\n\s*(\d+)\s*gr", text),
        'Produk': re.search(r"# Nama Produk.*?\n(.*?)\n", text),
        'Qty': re.search(r"Qty\s+(\d+)", text),
        'No. Pesanan': re.search(r"No.Pesanan:\s*(\S+)", text),
        'Pesan': re.search(r"Pesan:\s*(.+?)\s*\(", text)
    }
    return {k: v.group(1).strip() if v else '' for k,v in result.items()}

st.title("📦 Resi PDF ➜ Excel")

pdf_file = st.file_uploader("Upload Resi PDF", type="pdf")
if pdf_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(pdf_file.read())
    doc = fitz.open(tmp.name)
    data = []
    for page in doc:
        text = page.get_text()
        for sec in re.split(r"No. Resi:", text)[1:]:
            data.append(extract_resi("No. Resi:" + sec))
    df = pd.DataFrame(data)
    st.dataframe(df)
    tmp_out = tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx")
    df.to_excel(tmp_out.name, index=False)
    with open(tmp_out.name, "rb") as f:
        st.download_button("⬇️ Download Excel", f, file_name="hasil_resi.xlsx",
                           mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
