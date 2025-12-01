import streamlit as st
from transformers import pipeline

@st.cache_resource
def load_model():
    return pipeline(
        "text-classification",
        model="Yakobbabis/sarkasmeter-indonesia-v1",  # ← pastikan ini nama model kamu di HF
        return_all_scores=True
    )

classifier = load_model()

st.set_page_config(page_title="Sarkasmeter Indonesia", page_icon="🇮🇩")
st.title("🇮🇩 Sarkasmeter Indonesia")
st.markdown("### Deteksi sarkasme, humor, atau netral dalam 1 detik")

teks = st.text_area("Masukkan kalimat:", placeholder="selamat berangkat haji tuan menir", height=130)

if st.button("🔍 Cek Sarkasme!", type="primary"):
    if not teks.strip():
        st.warning("Tulis kalimat dulu dong!")
    else:
        with st.spinner("Sedang mikir..."):
            hasil = classifier(teks)[0]
        st.success("Selesai!")
        sorted_hasil = sorted(hasil, key=lambda x: x['score'], reverse=True)
        for item in sorted_hasil:
            label = {"LABEL_0": "😐 Netral", "LABEL_1": "😂 Lucu", "LABEL_2": "😏 Sarkasme"}[item['label']]
            skor = item['score'] * 100
            st.write(f"**{label} → {skor:.1f}%**")
            st.progress(skor / 100)
