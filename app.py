
import streamlit as st
import tempfile
import os
import sys
import time
import pandas as pd
from PIL import Image
from collections import Counter

sys.path.insert(0, os.path.dirname(__file__))
from src.inference import WasteSortingSystem


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="EcoSort AI",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ============================================================
# PREMIUM ANIMATED UI
# ============================================================

st.markdown("""
<style>

/* ---------------------------------------------------------
   GLOBAL
--------------------------------------------------------- */

.stApp {
    background:
        radial-gradient(circle at 10% 10%,
            rgba(96,108,56,.20), transparent 32%),
        radial-gradient(circle at 90% 15%,
            rgba(163,177,138,.10), transparent 30%),
        radial-gradient(circle at 80% 90%,
            rgba(47,54,84,.14), transparent 35%),
        #050706;
    color: #F2F0E8;
    overflow-x: hidden;
}

.block-container {
    max-width: 1280px;
    padding-top: 1.2rem;
    padding-bottom: 4rem;
}

/* animated ambient forms */
.stApp::before,
.stApp::after {
    content: "";
    position: fixed;
    z-index: 0;
    pointer-events: none;
    filter: blur(95px);
    opacity: .24;
}

.stApp::before {
    width: 480px;
    height: 480px;
    left: -140px;
    top: 12%;
    background: #606C38;
    border-radius: 42% 58% 63% 37% / 44% 42% 58% 56%;
    animation: morphOne 18s ease-in-out infinite alternate;
}

.stApp::after {
    width: 520px;
    height: 520px;
    right: -180px;
    top: 38%;
    background: linear-gradient(
        135deg,
        #283618,
        #A3B18A,
        #303652
    );
    border-radius: 60% 40% 35% 65% / 48% 60% 40% 52%;
    animation: morphTwo 22s ease-in-out infinite alternate;
}

@keyframes morphOne {
    0% {
        transform: translate(0,0) rotate(0deg) scale(1);
        border-radius: 42% 58% 63% 37% / 44% 42% 58% 56%;
    }
    50% {
        transform: translate(130px,-40px) rotate(30deg) scale(1.15);
        border-radius: 64% 36% 45% 55% / 35% 60% 40% 65%;
    }
    100% {
        transform: translate(40px,130px) rotate(70deg) scale(.92);
        border-radius: 35% 65% 62% 38% / 58% 35% 65% 42%;
    }
}

@keyframes morphTwo {
    0% {
        transform: translate(0,0) rotate(0deg);
    }
    50% {
        transform: translate(-150px,80px) rotate(-35deg) scale(1.08);
    }
    100% {
        transform: translate(-40px,-100px) rotate(-65deg) scale(.9);
    }
}

[data-testid="stHeader"] {
    background: transparent;
}

/* ---------------------------------------------------------
   NAV
--------------------------------------------------------- */

.eco-nav {
    position: relative;
    z-index: 2;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: .8rem .2rem 1.4rem .2rem;
}

.brand {
    display: flex;
    align-items: center;
    gap: .75rem;
    font-size: 1.05rem;
    font-weight: 800;
    letter-spacing: .08em;
}

.brand-mark {
    width: 34px;
    height: 34px;
    display: grid;
    place-items: center;
    border-radius: 11px;
    background: linear-gradient(135deg,#606C38,#A3B18A);
    color: #050706;
    box-shadow: 0 0 28px rgba(163,177,138,.18);
}

.online {
    display: flex;
    align-items: center;
    gap: .55rem;
    color: #C8D2B7;
    font-size: .78rem;
    letter-spacing: .09em;
}

.online-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: #B8C89B;
    box-shadow: 0 0 12px #A3B18A;
    animation: pulseDot 2s infinite;
}

@keyframes pulseDot {
    0%,100% { opacity: .55; transform: scale(.85); }
    50% { opacity: 1; transform: scale(1.25); }
}

/* ---------------------------------------------------------
   HERO
--------------------------------------------------------- */

.hero {
    position: relative;
    z-index: 1;
    overflow: hidden;
    min-height: 420px;
    border-radius: 34px;
    padding: 4.2rem 4rem;
    display: flex;
    align-items: center;
    border: 1px solid rgba(163,177,138,.16);
    background:
        linear-gradient(
            120deg,
            rgba(10,13,11,.96),
            rgba(18,23,16,.86),
            rgba(20,24,30,.82)
        );
    box-shadow:
        0 30px 90px rgba(0,0,0,.35),
        inset 0 1px 0 rgba(255,255,255,.04);
}

.hero::after {
    content: "";
    position: absolute;
    width: 500px;
    height: 500px;
    right: -80px;
    top: -120px;
    background:
        radial-gradient(circle,
        rgba(163,177,138,.23),
        rgba(96,108,56,.09) 40%,
        transparent 68%);
    animation: heroGlow 10s ease-in-out infinite alternate;
}

@keyframes heroGlow {
    from { transform: translate(0,0) scale(.9); }
    to { transform: translate(-90px,90px) scale(1.2); }
}

.eyebrow {
    color: #A3B18A;
    font-size: .78rem;
    font-weight: 700;
    letter-spacing: .18em;
    margin-bottom: 1rem;
}

.hero h1 {
    position: relative;
    z-index: 2;
    max-width: 760px;
    margin: 0;
    font-size: clamp(3rem,6vw,5.7rem);
    line-height: .98;
    letter-spacing: -.055em;
    font-weight: 700;
    color: #F3F1EA;
    animation: fadeUp .9s ease both;
}

.hero p {
    position: relative;
    z-index: 2;
    max-width: 590px;
    margin-top: 1.5rem;
    color: #AEB4AA;
    font-size: 1.08rem;
    line-height: 1.7;
    animation: fadeUp 1.1s ease both;
}

.hero-tags {
    position: relative;
    z-index: 2;
    display: flex;
    flex-wrap: wrap;
    gap: .6rem;
    margin-top: 1.8rem;
}

.hero-tag {
    border: 1px solid rgba(163,177,138,.18);
    background: rgba(255,255,255,.035);
    backdrop-filter: blur(12px);
    border-radius: 999px;
    padding: .55rem .9rem;
    color: #C6CCBE;
    font-size: .78rem;
}

@keyframes fadeUp {
    from { opacity:0; transform:translateY(24px); }
    to { opacity:1; transform:translateY(0); }
}

/* ---------------------------------------------------------
   TYPOGRAPHY / SECTION
--------------------------------------------------------- */

.section-kicker {
    color: #87936F;
    font-size: .74rem;
    font-weight: 700;
    letter-spacing: .16em;
    margin-bottom: .45rem;
}

.section-title {
    color: #F2F0E8;
    font-size: 2rem;
    font-weight: 650;
    letter-spacing: -.035em;
    margin-bottom: .35rem;
}

.section-copy {
    color: #8E958C;
    margin-bottom: 1.4rem;
}

/* ---------------------------------------------------------
   GLASS CARDS
--------------------------------------------------------- */

.glass {
    border: 1px solid rgba(163,177,138,.14);
    background: rgba(12,15,13,.72);
    backdrop-filter: blur(18px);
    border-radius: 24px;
    padding: 1.4rem;
    box-shadow: 0 18px 55px rgba(0,0,0,.20);
}

[data-testid="stMetric"] {
    border: 1px solid rgba(163,177,138,.12);
    background: rgba(13,16,14,.75);
    border-radius: 20px;
    padding: 1.25rem 1.3rem;
    transition: transform .3s ease, border-color .3s ease;
}

[data-testid="stMetric"]:hover {
    transform: translateY(-5px);
    border-color: rgba(163,177,138,.38);
}

[data-testid="stMetricLabel"] {
    color: #858C82;
}

[data-testid="stMetricValue"] {
    color: #F2F0E8;
}

/* ---------------------------------------------------------
   FILE UPLOADER / INPUTS
--------------------------------------------------------- */

[data-testid="stFileUploader"] {
    border-radius: 22px;
    padding: .5rem;
}

[data-testid="stFileUploaderDropzone"] {
    border: 1px dashed rgba(163,177,138,.30);
    background: rgba(255,255,255,.025);
    border-radius: 20px;
    transition: all .3s ease;
}

[data-testid="stFileUploaderDropzone"]:hover {
    border-color: #A3B18A;
    background: rgba(163,177,138,.055);
}

div[data-baseweb="select"] > div {
    background: rgba(12,15,13,.82);
    border-color: rgba(163,177,138,.15);
}

/* ---------------------------------------------------------
   BUTTON
--------------------------------------------------------- */

.stButton > button {
    position: relative;
    overflow: hidden;
    width: 100%;
    min-height: 52px;
    border: 1px solid rgba(183,196,156,.28);
    border-radius: 16px;
    color: #F7F6F0;
    font-weight: 700;
    background:
        linear-gradient(
            110deg,
            #3F4826,
            #687742,
            #899A65,
            #596737
        );
    background-size: 260% 260%;
    animation: buttonFlow 8s ease infinite;
    box-shadow: 0 12px 35px rgba(96,108,56,.18);
    transition: transform .25s ease, box-shadow .25s ease;
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 16px 45px rgba(163,177,138,.22);
    border-color: rgba(203,216,176,.45);
}

@keyframes buttonFlow {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

/* ---------------------------------------------------------
   SAMPLE CARDS
--------------------------------------------------------- */

.sample-label {
    margin-top: .4rem;
    color: #AEB4AA;
    font-size: .78rem;
    text-align: center;
}

/* images */
[data-testid="stImage"] img {
    border-radius: 20px;
    transition: transform .35s ease, filter .35s ease;
}

[data-testid="stImage"] img:hover {
    transform: scale(1.015);
    filter: brightness(1.06);
}

/* ---------------------------------------------------------
   DECISION
--------------------------------------------------------- */

.decision {
    position: relative;
    overflow: hidden;
    margin: 1.2rem 0 1.8rem;
    padding: 2rem 2.2rem;
    border-radius: 24px;
    border: 1px solid rgba(163,177,138,.18);
    background:
        linear-gradient(
            135deg,
            rgba(45,53,30,.60),
            rgba(14,18,15,.90)
        );
    animation: fadeUp .7s ease both;
}

.decision::after {
    content: "";
    position: absolute;
    width: 160px;
    height: 160px;
    right: -40px;
    top: -50px;
    border-radius: 50%;
    background: rgba(163,177,138,.10);
    filter: blur(20px);
}

.decision-small {
    color: #A3B18A;
    letter-spacing: .14em;
    font-size: .72rem;
    font-weight: 700;
}

.decision-main {
    margin-top: .5rem;
    color: #F3F1EA;
    font-size: 2rem;
    font-weight: 700;
}

.decision-copy {
    margin-top: .45rem;
    color: #AAB0A7;
}

/* ---------------------------------------------------------
   QUALITY STATUS
--------------------------------------------------------- */

.status-clean,
.status-warning,
.status-danger {
    padding: 1.25rem 1.4rem;
    border-radius: 18px;
    margin: .7rem 0 1rem;
}

.status-clean {
    background: rgba(96,108,56,.14);
    border: 1px solid rgba(163,177,138,.24);
}

.status-warning {
    background: rgba(190,139,61,.10);
    border: 1px solid rgba(211,160,76,.22);
}

.status-danger {
    background: rgba(171,72,72,.10);
    border: 1px solid rgba(205,95,95,.24);
}

/* ---------------------------------------------------------
   DATAFRAME / EXPANDER
--------------------------------------------------------- */

[data-testid="stDataFrame"] {
    border: 1px solid rgba(163,177,138,.10);
    border-radius: 18px;
    overflow: hidden;
}

[data-testid="stExpander"] {
    border: 1px solid rgba(163,177,138,.12);
    background: rgba(255,255,255,.018);
    border-radius: 18px;
}

/* ---------------------------------------------------------
   SCAN FRAME
--------------------------------------------------------- */

.scan-frame {
    position: relative;
}

.scan-frame::after {
    content: "";
    position: absolute;
    left: 4%;
    right: 4%;
    height: 1px;
    top: 10%;
    background:
        linear-gradient(
            90deg,
            transparent,
            rgba(190,205,158,.75),
            transparent
        );
    box-shadow: 0 0 12px rgba(163,177,138,.45);
    animation: scan 4s ease-in-out infinite;
    pointer-events: none;
}

@keyframes scan {
    0%,100% { top: 12%; opacity:.2; }
    50% { top: 88%; opacity:.8; }
}

/* ---------------------------------------------------------
   FOOTER
--------------------------------------------------------- */

.footer {
    text-align: center;
    color: #646A63;
    padding: 3rem 0 1rem;
    font-size: .82rem;
}

/* hide Streamlit chrome */
#MainMenu {visibility:hidden;}
footer {visibility:hidden;}

</style>
""", unsafe_allow_html=True)


# ============================================================
# MODEL
# ============================================================

@st.cache_resource
def load_system():
    return WasteSortingSystem(
        detection_model="models/detection.pt",
        segmentation_model="models/segmentation.pt"
    )

system = load_system()


# ============================================================
# HELPERS
# ============================================================

DEMO_DIR = os.path.join(
    os.path.dirname(__file__),
    "demo_samples"
)

sample_names = {
    "sample_01.jpg": "Minimal waste",
    "sample_02.jpg": "Mixed material stream",
    "sample_03.jpg": "Sorting challenge",
    "sample_04.jpg": "Multi-object stream",
    "sample_05.jpg": "Sparse conveyor",
    "sample_06.jpg": "Packaging mix",
    "sample_07.jpg": "Container mix",
    "sample_08.jpg": "Low-density stream",
    "sample_09.jpg": "Mixed packaging",
    "sample_10.jpg": "Bottle & film",
    "sample_11.jpg": "Scattered packaging",
    "sample_12.jpg": "High-density stream"
}

sample_files = []

if os.path.isdir(DEMO_DIR):
    sample_files = sorted([
        f for f in os.listdir(DEMO_DIR)
        if f.lower().endswith((".jpg", ".jpeg", ".png"))
    ])


# ============================================================
# NAV
# ============================================================

st.markdown("""
<div class="eco-nav">
    <div class="brand">
        <div class="brand-mark">✦</div>
        ECOSORT / AI
    </div>
    <div class="online">
        <span class="online-dot"></span>
        AI SYSTEM READY
    </div>
</div>
""", unsafe_allow_html=True)


# ============================================================
# HERO
# ============================================================

st.markdown(
    """
<div class="hero">
<div>
<div class="eyebrow">AI RECYCLING INTELLIGENCE</div>
<h1>Waste intelligence.<br>Better decisions.</h1>
<p>EcoSort combines computer vision and recycling quality intelligence to detect waste, understand material composition and help operators make faster sorting decisions.</p>
<div class="hero-tags">
<span class="hero-tag">Object detection</span>
<span class="hero-tag">Instance segmentation</span>
<span class="hero-tag">Material intelligence</span>
<span class="hero-tag">Quality control</span>
</div>
</div>
</div>
    """,
    unsafe_allow_html=True
)

st.write("")
st.write("")


# ============================================================
# INSPECTION SETUP
# ============================================================

st.markdown(
    '<div class="section-kicker">01 / INSPECTION</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-title">Start a waste inspection</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-copy">'
    'Upload a conveyor image or choose one of the unseen '
    'PackWISE test samples.'
    '</div>',
    unsafe_allow_html=True
)

control1, control2 = st.columns([1.15, .85], gap="large")

with control1:
    uploaded_file = st.file_uploader(
        "Upload waste image",
        type=["jpg", "jpeg", "png"],
        label_visibility="collapsed"
    )

with control2:
    expected_material = st.selectbox(
        "Expected recycling stream",
        ["plastic", "paper", "metal"],
        format_func=lambda x: x.title()
    )

    confidence = st.slider(
        "Detection confidence",
        min_value=0.10,
        max_value=0.90,
        value=0.25,
        step=0.05
    )


# ============================================================
# SAMPLE GALLERY
# ============================================================

selected_sample = None

if sample_files:

    st.write("")
    st.markdown(
        '<div class="section-kicker">TRY A SAMPLE</div>',
        unsafe_allow_html=True
    )

    visible_samples = sample_files[:6]

    cols = st.columns(3, gap="medium")

    for i, filename in enumerate(visible_samples):

        path = os.path.join(DEMO_DIR, filename)

        with cols[i % 3]:

            img = Image.open(path).convert("RGB")

            st.image(
                img,
                use_container_width=True
            )

            st.markdown(
                f'<div class="sample-label">'
                f'{sample_names.get(filename, "Waste sample")}'
                f'</div>',
                unsafe_allow_html=True
            )

            if st.button(
                "Use this sample →",
                key=f"sample_{i}"
            ):
                st.session_state["chosen_sample"] = path

    if len(sample_files) > 6:

        with st.expander("Explore more samples"):

            more_cols = st.columns(3)

            for j, filename in enumerate(sample_files[6:]):

                path = os.path.join(DEMO_DIR, filename)

                with more_cols[j % 3]:

                    img = Image.open(path).convert("RGB")

                    st.image(
                        img,
                        use_container_width=True
                    )

                    st.caption(
                        sample_names.get(
                            filename,
                            "Waste sample"
                        )
                    )

                    if st.button(
                        "Use sample",
                        key=f"more_{j}"
                    ):
                        st.session_state[
                            "chosen_sample"
                        ] = path


# ============================================================
# CHOOSE IMAGE SOURCE
# ============================================================

image = None
source_path = None

if uploaded_file is not None:

    image = Image.open(
        uploaded_file
    ).convert("RGB")

elif st.session_state.get("chosen_sample"):

    source_path = st.session_state[
        "chosen_sample"
    ]

    if os.path.exists(source_path):
        image = Image.open(
            source_path
        ).convert("RGB")


# ============================================================
# ANALYSIS
# ============================================================

if image is not None:

    st.write("")
    st.write("")

    st.markdown(
        '<div class="section-kicker">02 / AI VISION</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-title">'
        'Ready for analysis'
        '</div>',
        unsafe_allow_html=True
    )

    preview_a, preview_b = st.columns(
        2,
        gap="large"
    )

    with preview_a:
        st.caption("ORIGINAL INPUT")
        st.image(
            image,
            use_container_width=True
        )

    analyze = st.button(
        "✦ Run AI inspection",
        type="primary",
        use_container_width=True
    )

    if analyze:

        with st.spinner(
            "EcoSort AI is analysing the waste stream..."
        ):

            if source_path is not None:
                analysis_path = source_path

            else:
                temp_file = (
                    tempfile.NamedTemporaryFile(
                        delete=False,
                        suffix=".jpg"
                    )
                )

                image.save(temp_file.name)
                analysis_path = temp_file.name

            result = system.analyze(
                analysis_path,
                expected_material=expected_material,
                confidence=confidence
            )

            if (
                source_path is None
                and os.path.exists(analysis_path)
            ):
                os.unlink(analysis_path)

        with preview_b:

            st.caption(
                "AI DETECTION + SEGMENTATION"
            )

            st.markdown(
                '<div class="scan-frame">',
                unsafe_allow_html=True
            )

            st.image(
                result["segmented_image"],
                use_container_width=True
            )

            st.markdown(
                '</div>',
                unsafe_allow_html=True
            )


        # ====================================================
        # QUALITY INTELLIGENCE
        # ====================================================

        object_count = result["object_count"]
        contaminant_count = len(
            result["contaminants"]
        )

        if object_count > 0:
            purity = (
                (
                    object_count
                    - contaminant_count
                )
                / object_count
            ) * 100
        else:
            purity = 0.0

        quality_score = round(purity)

        if purity >= 90:
            severity = "LOW"
            recommendation = "ACCEPT STREAM"
            recommendation_detail = (
                "Material purity is high. "
                "The stream can proceed to the "
                "next recycling stage."
            )

        elif purity >= 70:
            severity = "MODERATE"
            recommendation = "MANUAL INSPECTION"
            recommendation_detail = (
                "Some contamination is present. "
                "Secondary sorting or manual "
                "inspection is recommended."
            )

        else:
            severity = "HIGH"
            recommendation = "RE-SORT STREAM"
            recommendation_detail = (
                "Contamination is significant. "
                "Re-sorting is recommended before "
                "further processing."
            )

        st.write("")
        st.write("")

        st.markdown(
            '<div class="section-kicker">'
            '03 / QUALITY INTELLIGENCE'
            '</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="section-title">'
            'Recycling quality at a glance'
            '</div>',
            unsafe_allow_html=True
        )

        q1, q2, q3, q4 = st.columns(4)

        q1.metric(
            "Quality score",
            f"{quality_score}/100"
        )

        q2.metric(
            "Stream purity",
            f"{purity:.1f}%"
        )

        q3.metric(
            "Contamination risk",
            severity
        )

        q4.metric(
            "Objects detected",
            object_count
        )

        if severity == "LOW":
            icon = "✓"
        elif severity == "MODERATE":
            icon = "!"
        else:
            icon = "×"

        st.markdown(
            f"""
            <div class="decision">
                <div class="decision-small">
                    OPERATOR RECOMMENDATION
                </div>
                <div class="decision-main">
                    {icon} {recommendation}
                </div>
                <div class="decision-copy">
                    {recommendation_detail}
                    &nbsp; Processing time:
                    {result["processing_time"]:.2f}s.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )


        # ====================================================
        # CONTAMINATION
        # ====================================================

        if result["contaminated"]:

            st.markdown(
                f"""
                <div class="status-danger">
                    <b>CONTAMINATION DETECTED</b><br>
                    Foreign material was detected in the
                    selected <b>{expected_material.upper()}</b>
                    recycling stream.
                </div>
                """,
                unsafe_allow_html=True
            )

            contaminant_rows = []

            for item in result["contaminants"]:

                contaminant_rows.append({
                    "Waste type":
                        item["class"],

                    "Material":
                        item["material"].title(),

                    "Confidence":
                        f'{item["confidence"]*100:.1f}%'
                })

            st.dataframe(
                pd.DataFrame(
                    contaminant_rows
                ),
                use_container_width=True,
                hide_index=True
            )

        else:

            st.markdown(
                f"""
                <div class="status-clean">
                    <b>CLEAN RECYCLING STREAM</b><br>
                    All detected materials are compatible
                    with the selected
                    <b>{expected_material.upper()}</b>
                    stream.
                </div>
                """,
                unsafe_allow_html=True
            )


        # ====================================================
        # MATERIAL INTELLIGENCE
        # ====================================================

        st.write("")
        st.markdown(
            '<div class="section-kicker">'
            '04 / MATERIAL INTELLIGENCE'
            '</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="section-title">'
            'What is in this stream?'
            '</div>',
            unsafe_allow_html=True
        )

        material_counts = Counter(
            item["material"]
            for item in result["detections"]
        )

        m1, m2, m3, m4 = st.columns(4)

        m1.metric(
            "Plastic",
            material_counts.get(
                "plastic", 0
            )
        )

        m2.metric(
            "Paper",
            material_counts.get(
                "paper", 0
            )
        )

        m3.metric(
            "Metal",
            material_counts.get(
                "metal", 0
            )
        )

        m4.metric(
            "Other",
            material_counts.get(
                "other", 0
            )
        )


        # ====================================================
        # OBJECTS
        # ====================================================

        if result["detections"]:

            st.write("")
            st.markdown(
                '<div class="section-title">'
                'Detected waste objects'
                '</div>',
                unsafe_allow_html=True
            )

            table_data = []

            for i, item in enumerate(
                result["detections"],
                start=1
            ):

                material = item["material"]

                table_data.append({
                    "#": i,
                    "Waste type":
                        item["class"],
                    "Material":
                        material.title(),
                    "Confidence":
                        f'{item["confidence"]*100:.1f}%',
                    "Quality":
                        (
                            "Accepted"
                            if material
                            == expected_material
                            else "Contaminant"
                        )
                })

            st.dataframe(
                pd.DataFrame(table_data),
                use_container_width=True,
                hide_index=True
            )


        # ====================================================
        # TECHNICAL DETAILS
        # ====================================================

        st.write("")

        with st.expander(
            "Technical performance & advanced AI"
        ):

            st.caption(
                "Final detector — unseen PackWISE test set"
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

            st.markdown("""
            **Advanced experiments**

            **YOLO11** — object detection  
            **YOLO11-Seg** — instance segmentation  
            **LSTM** — experimental temporal stream monitoring  
            **VAE** — experimental rare-waste representation
            """)


# ============================================================
# FOOTER
# ============================================================

st.markdown("""
<div class="footer">
    ECOSORT / AI &nbsp; • &nbsp;
    Waste Sorting & Recycling Quality Intelligence
    <br>
    Deep Learning PBL · Circular Economy
</div>
""", unsafe_allow_html=True)
