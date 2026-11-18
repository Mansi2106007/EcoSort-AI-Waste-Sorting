
import streamlit as st
import tempfile
import os
import sys
import pandas as pd
from PIL import Image
from collections import Counter

sys.path.insert(0, os.path.dirname(__file__))
from src.inference import WasteSortingSystem


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="EcoSort AI",
    page_icon="♻️",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

/* Main page */
.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1400px;
}

/* Hero */
.hero {
    padding: 2.2rem 2.4rem;
    border-radius: 22px;
    background: linear-gradient(135deg, #063b2c 0%, #0d684d 55%, #12805d 100%);
    margin-bottom: 1.6rem;
}

.hero-title {
    color: white;
    font-size: 2.7rem;
    font-weight: 800;
    margin-bottom: 0.4rem;
}

.hero-subtitle {
    color: #d8f3e8;
    font-size: 1.08rem;
    margin-bottom: 1.1rem;
}

/* Badges */
.badge {
    display: inline-block;
    padding: 7px 13px;
    margin-right: 7px;
    margin-bottom: 6px;
    border-radius: 999px;
    background: rgba(255,255,255,0.14);
    color: white;
    font-size: 0.85rem;
    font-weight: 600;
}

/* Section title */
.section-title {
    font-size: 1.35rem;
    font-weight: 750;
    margin-top: 0.7rem;
    margin-bottom: 0.8rem;
}

/* Status cards */
.clean-card {
    padding: 18px 20px;
    border-radius: 16px;
    background: rgba(22, 163, 74, 0.12);
    border: 1px solid rgba(22, 163, 74, 0.35);
    margin-top: 8px;
    margin-bottom: 16px;
}

.alert-card {
    padding: 18px 20px;
    border-radius: 16px;
    background: rgba(220, 38, 38, 0.10);
    border: 1px solid rgba(220, 38, 38, 0.35);
    margin-top: 8px;
    margin-bottom: 16px;
}

/* Footer */
.footer {
    text-align: center;
    opacity: 0.65;
    padding-top: 30px;
    font-size: 0.9rem;
}

/* Upload widget */
[data-testid="stFileUploader"] {
    border-radius: 16px;
}

/* Metric cards */
[data-testid="stMetric"] {
    border: 1px solid rgba(128,128,128,0.18);
    padding: 15px;
    border-radius: 15px;
    background: rgba(128,128,128,0.04);
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# LOAD AI SYSTEM
# =========================================================

@st.cache_resource
def load_system():
    return WasteSortingSystem(
        detection_model="models/detection.pt",
        segmentation_model="models/segmentation.pt"
    )


system = load_system()


# =========================================================
# HERO
# =========================================================

st.markdown("""
<div class="hero">
    <div class="hero-title">♻️ EcoSort AI</div>
    <div class="hero-subtitle">
        Waste Sorting & Recycling Quality Controller powered by Deep Learning
    </div>
    <div>
        <span class="badge">🎯 Object Detection</span>
        <span class="badge">🎨 Instance Segmentation</span>
        <span class="badge">♻️ Material Classification</span>
        <span class="badge">⚠️ Contamination Control</span>
    </div>
</div>
""", unsafe_allow_html=True)


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.title("⚙️ Control Panel")

st.sidebar.write(
    "Configure the recycling stream and AI detection threshold."
)

expected_material = st.sidebar.selectbox(
    "Expected Recycling Stream",
    ["plastic", "paper", "metal"],
    format_func=lambda x: x.title()
)

confidence = st.sidebar.slider(
    "Detection Confidence",
    min_value=0.10,
    max_value=0.90,
    value=0.25,
    step=0.05
)

st.sidebar.divider()

st.sidebar.markdown("### 🧠 AI Pipeline")
st.sidebar.write("YOLO11 — Object Detection")
st.sidebar.write("YOLO11-Seg — Instance Segmentation")
st.sidebar.write("LSTM — Stream Monitoring")
st.sidebar.write("VAE — Rare Waste Analysis")

st.sidebar.divider()

st.sidebar.caption(
    "Circular Economy • Deep Learning PBL"
)


# =========================================================
# UPLOAD SECTION
# =========================================================

st.markdown(
    '<div class="section-title">📤 Waste Inspection</div>',
    unsafe_allow_html=True
)

st.write(
    "Upload a conveyor-belt waste image and let the AI inspect "
    "its material composition and recycling quality."
)

uploaded_file = st.file_uploader(
    "Upload waste image",
    type=["jpg", "jpeg", "png"],
    label_visibility="collapsed"
)


# =========================================================
# IMAGE + ANALYSIS
# =========================================================

if uploaded_file is not None:

    image = Image.open(uploaded_file).convert("RGB")

    st.markdown(
        '<div class="section-title">🖼️ Inspection Preview</div>',
        unsafe_allow_html=True
    )

    preview1, preview2 = st.columns(2, gap="large")

    with preview1:
        st.markdown("#### Original Image")
        st.image(image, use_container_width=True)

    analyze = st.button(
        "🔍 Run AI Waste Inspection",
        type="primary",
        use_container_width=True
    )

    if analyze:

        with st.spinner(
            "AI models are analysing the waste stream..."
        ):

            with tempfile.NamedTemporaryFile(
                delete=False,
                suffix=".jpg"
            ) as temp:

                image.save(temp.name)

                result = system.analyze(
                    temp.name,
                    expected_material=expected_material,
                    confidence=confidence
                )

            os.unlink(temp.name)


        # =============================================
        # AI IMAGE
        # =============================================

        with preview2:

            st.markdown("#### AI Segmentation & Detection")

            st.image(
                result["segmented_image"],
                use_container_width=True
            )


        # =============================================
        # CALCULATE DASHBOARD VALUES
        # =============================================

        object_count = result["object_count"]
        contaminant_count = len(result["contaminants"])

        if object_count > 0:
            purity = (
                (object_count - contaminant_count)
                / object_count
            ) * 100
        else:
            purity = 0.0

        status = (
            "CONTAMINATED"
            if result["contaminated"]
            else "CLEAN"
        )


        # =============================================
        # KPI DASHBOARD
        # =============================================

        st.divider()

        st.markdown(
            '<div class="section-title">📊 Inspection Summary</div>',
            unsafe_allow_html=True
        )

        k1, k2, k3, k4 = st.columns(4)

        k1.metric(
            "Detected Objects",
            object_count
        )

        k2.metric(
            "Estimated Purity",
            f"{purity:.1f}%"
        )

        k3.metric(
            "Processing Time",
            f'{result["processing_time"]:.2f}s'
        )

        k4.metric(
            "Quality Status",
            status
        )


        # =============================================
        # QUALITY CONTROL
        # =============================================

        st.markdown(
            '<div class="section-title">♻️ Recycling Quality Control</div>',
            unsafe_allow_html=True
        )

        if result["contaminated"]:

            st.markdown(
                f"""
                <div class="alert-card">
                    <b>⚠️ CONTAMINATION DETECTED</b><br><br>
                    The selected stream is
                    <b>{expected_material.upper()}</b>,
                    but foreign material was detected.
                </div>
                """,
                unsafe_allow_html=True
            )

            contaminant_rows = []

            for item in result["contaminants"]:

                contaminant_rows.append({
                    "Waste Type": item["class"],
                    "Detected Material":
                        item["material"].title(),
                    "Confidence":
                        f'{item["confidence"] * 100:.1f}%'
                })

            st.dataframe(
                pd.DataFrame(contaminant_rows),
                use_container_width=True,
                hide_index=True
            )

        else:

            st.markdown(
                f"""
                <div class="clean-card">
                    <b>✅ CLEAN RECYCLING STREAM</b><br><br>
                    All detected objects are compatible with
                    the selected
                    <b>{expected_material.upper()}</b>
                    recycling stream.
                </div>
                """,
                unsafe_allow_html=True
            )


        # =============================================
        # MATERIAL DISTRIBUTION
        # =============================================

        st.markdown(
            '<div class="section-title">🧱 Material Composition</div>',
            unsafe_allow_html=True
        )

        material_counts = Counter(
            item["material"]
            for item in result["detections"]
        )

        material_df = pd.DataFrame({
            "Material": [
                "Plastic",
                "Paper",
                "Metal",
                "Other"
            ],
            "Objects": [
                material_counts.get("plastic", 0),
                material_counts.get("paper", 0),
                material_counts.get("metal", 0),
                material_counts.get("other", 0)
            ]
        })

        chart_col, info_col = st.columns(
            [2, 1],
            gap="large"
        )

        with chart_col:

            st.bar_chart(
                material_df.set_index("Material")
            )

        with info_col:

            st.markdown("#### Material Counts")

            for _, row in material_df.iterrows():

                st.write(
                    f'**{row["Material"]}:** '
                    f'{row["Objects"]}'
                )


        # =============================================
        # DETECTION TABLE
        # =============================================

        st.markdown(
            '<div class="section-title">🔎 Detected Waste Objects</div>',
            unsafe_allow_html=True
        )

        if result["detections"]:

            table_data = []

            for i, item in enumerate(
                result["detections"],
                start=1
            ):

                material = item["material"]

                quality = (
                    "Accepted"
                    if material == expected_material
                    else "Contaminant"
                )

                table_data.append({
                    "#": i,
                    "Waste Type": item["class"],
                    "Material": material.title(),
                    "Confidence":
                        f'{item["confidence"] * 100:.1f}%',
                    "Quality": quality
                })

            st.dataframe(
                pd.DataFrame(table_data),
                use_container_width=True,
                hide_index=True
            )

        else:

            st.warning(
                "No waste objects were detected "
                "at the selected confidence threshold."
            )


        # =============================================
        # MODEL PERFORMANCE
        # =============================================

        st.divider()

        st.markdown(
            '<div class="section-title">🧠 Model Performance</div>',
            unsafe_allow_html=True
        )

        st.caption(
            "Final YOLO detector — unseen PackWISE test set"
        )

        p1, p2, p3, p4 = st.columns(4)

        p1.metric(
            "Precision",
            "38.93%"
        )

        p2.metric(
            "Recall",
            "36.47%"
        )

        p3.metric(
            "mAP@50",
            "31.32%"
        )

        p4.metric(
            "mAP@50–95",
            "26.40%"
        )


        # =============================================
        # HOW IT WORKS
        # =============================================

        with st.expander(
            "ℹ️ How does EcoSort AI work?"
        ):

            st.markdown("""
            **1. Object Detection**  
            YOLO detects individual waste objects and predicts
            their waste categories.

            **2. Instance Segmentation**  
            YOLO segmentation estimates the pixel-level region
            occupied by each detected waste object.

            **3. Material Mapping**  
            Waste categories are mapped into plastic, paper,
            metal and other material groups.

            **4. Recycling Quality Control**  
            Detected materials are compared with the expected
            recycling stream to identify contamination.

            **5. Advanced Deep Learning Experiments**  
            An LSTM stream-monitoring experiment analyses
            sequential material composition, while a VAE
            explores representations of rare waste categories.
            """)


# =========================================================
# FOOTER
# =========================================================

st.markdown("""
<div class="footer">
    ♻️ EcoSort AI — Waste Sorting & Recycling Quality Controller<br>
    Deep Learning PBL • Circular Economy
</div>
""", unsafe_allow_html=True)
