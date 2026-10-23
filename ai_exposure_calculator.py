import streamlit as st
import pandas as pd


st.set_page_config(
    page_title="AI Exposure Calculator",
    page_icon="🤖",
    layout="wide"
)

st.markdown("""
<style>
.stApp {
    background-color: #0B1220;
    color: #F1F5F9;
}
h1, h2, h3, p, label {
    color: #F1F5F9 !important;
}
div[data-testid="stMetric"] {
    background-color: #162235;
    border: 1px solid #1E8A8A;
    padding: 18px;
    border-radius: 12px;
}
.result-card {
    background-color: #162235;
    border: 1px solid #1E8A8A;
    padding: 22px;
    border-radius: 12px;
    margin: 12px 0;
}
</style>
""", unsafe_allow_html=True)

st.title("🤖 AI Risk vs Opportunity Platform")
st.subheader("AI Occupation Exposure Calculator")

st.write(
    "Explore AI exposure scores for different occupations "
    "using the occupation exposure dataset."
)


@st.cache_data
def load_occupation_data():
    file_path = "data/processed/ai_occupation_exposure_clean.xlsx"

    df = pd.read_excel(file_path, engine="openpyxl")

    df = df.rename(columns={
        "soc_code": "SOC_Code",
        "occupation_title": "Occupation_Title",
        "ai_exposure_score": "AI_Exposure_Score"
    })

    return df
try:
    df = load_occupation_data()
    df["AI_Exposure_Score"] = pd.to_numeric(
        df["AI_Exposure_Score"], errors="coerce"
    )
    df = df.dropna(
        subset=["SOC_Code", "Occupation_Title", "AI_Exposure_Score"]
    )
    df["SOC_Code"] = df["SOC_Code"].astype(str)
    df["Occupation_Title"] = df["Occupation_Title"].astype(str)

except Exception as error:
    st.error(f"Unable to load occupation data: {error}")
    st.stop()

df["Occupation_Option"] = (
    df["Occupation_Title"] + " (" + df["SOC_Code"] + ")"
)

st.markdown("### 1. Select an Occupation")

selected_option = st.selectbox(
    "Search for an occupation",
    sorted(df["Occupation_Option"].unique())
)

selected_row = df[
    df["Occupation_Option"] == selected_option
].iloc[0]

occupation = selected_row["Occupation_Title"]
soc_code = selected_row["SOC_Code"]
score = float(selected_row["AI_Exposure_Score"])

if score > 0:
    category = "Above-zero exposure score"
    explanation = (
        "This occupation has a positive score relative to the "
        "dataset's centered exposure scale."
    )
elif score < 0:
    category = "Below-zero exposure score"
    explanation = (
        "This occupation has a negative score relative to the "
        "dataset's centered exposure scale."
    )
else:
    category = "Zero exposure score"
    explanation = (
        "This occupation's score is zero on the dataset's "
        "centered exposure scale."
    )

st.markdown("---")
st.markdown("### 2. Occupation Analysis")

st.markdown(
    f"""
    <div class="result-card">
        <p>SELECTED OCCUPATION</p>
        <h2>{occupation}</h2>
        <p>Occupation code: {soc_code}</p>
    </div>
    """,
    unsafe_allow_html=True
)

col1, col2 = st.columns(2)

with col1:
    st.metric("AI Exposure Score", f"{score:.3f}")

with col2:
    st.metric("Total Occupations", f"{len(df):,}")

st.markdown("### 3. Score Interpretation")
st.markdown(f"**Result:** {category}")
st.write(explanation)

st.info(
    "A positive score does not automatically mean high job-loss risk, "
    "and a negative score does not mean an occupation is immune to AI."
)

st.warning(
    "These are relative exposure scores, not probabilities of job loss "
    "or forecasts of future employment."
)

with st.expander("View occupation dataset"):
    st.dataframe(
        df[["SOC_Code", "Occupation_Title", "AI_Exposure_Score"]]
        .sort_values("AI_Exposure_Score", ascending=False),
        use_container_width=True,
        hide_index=True
    )

st.caption(
    "Source: AI Occupation Exposure Repository. "
    "Interpret results in the context of the dataset's methodology."
)