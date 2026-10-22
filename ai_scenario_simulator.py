
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# ---------------- PAGE SETTINGS ----------------
st.set_page_config(
    page_title="AI Scenario Simulator",
    page_icon="📊",
    layout="wide"
)

# ---------------- NAVY + TEAL THEME ----------------
NAVY = "#0B1220"
PANEL = "#162235"
TEAL = "#14B8A6"
LIGHT_TEAL = "#5EEAD4"
WHITE = "#F1F5F9"
MUTED = "#94A3B8"

st.markdown("""
<style>
.stApp {
    background-color: #0B1220;
    color: #F1F5F9;
}
[data-testid="stHeader"] {
    background-color: #0B1220;
}
h1, h2, h3, p, label, .stMarkdown {
    color: #F1F5F9;
}
div[data-testid="stMetric"] {
    background-color: #162235;
    border: 1px solid #14B8A6;
    padding: 16px;
    border-radius: 12px;
}
div[data-testid="stMetricLabel"] {
    color: #94A3B8;
}
div[data-testid="stMetricValue"] {
    color: #5EEAD4;
}
.stSelectbox, .stSlider {
    padding-bottom: 8px;
}
</style>
""", unsafe_allow_html=True)

st.title("AI Risk vs Opportunity Platform")
st.subheader("📊 AI Scenario Simulator")
st.write(
    "Explore how hypothetical changes in exposure scores affect "
    "occupation-level results and the overall score distribution."
)

# ---------------- LOAD EXCEL DATA ----------------
# ---------------- LOAD EXCEL DATA ----------------
@st.cache_data
def load_data():
    data = pd.read_excel("ai_occupation_exposure_clean.xlsx")
    data.columns = data.columns.str.strip().str.lower()

    required_columns = [
        "soc_code",
        "occupation_title",
        "ai_exposure_score",
    ]

    missing_columns = [
        col for col in required_columns
        if col not in data.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing columns: {missing_columns}. "
            f"Available columns: {list(data.columns)}"
        )

    data = data[required_columns].copy()

    data["ai_exposure_score"] = pd.to_numeric(
        data["ai_exposure_score"], errors="coerce"
    )

    data = data.dropna(subset=required_columns).copy()

    data = data.rename(columns={
        "soc_code": "SOC_Code",
        "occupation_title": "Occupation_Title",
        "ai_exposure_score": "AI_Exposure_Score",
    })

    data["SOC_Code"] = data["SOC_Code"].astype(str)
    data["Occupation_Title"] = data["Occupation_Title"].astype(str)

    if data.empty:
        raise ValueError("No valid occupation records were found.")

    return data
try:
    df = load_data()
except Exception as error:
    st.error(f"Unable to load occupation data: {error}")
    st.info(
        "Check that ai_occupation_exposure_clean.xlsx is in "
        "the repository root and contains the required columns."
    )
    st.stop()


# Define original score series and statistics
original = df["AI_Exposure_Score"]
original_average = original.mean()
original_median = original.median()

# ---------------- DATA OVERVIEW ----------------
st.markdown("### 1. Dataset Overview")

c1, c2, c3 = st.columns(3)

c1.metric("Occupations Analysed", f"{len(df):,}")
c2.metric("Original Average Score", f"{original_average:.3f}")
c3.metric("Original Median Score", f"{original_median:.3f}")

st.divider()

# ---------------- SCENARIO CONTROLS ----------------
st.markdown("### 2. Configure Your Scenario")

scenario_presets = {
    "Baseline — no change": 0.00,
    "Small increase": 0.25,
    "Moderate increase": 0.50,
    "Large increase": 1.00,
    "Small decrease": -0.25,
    "Custom adjustment": 0.00
}

scenario = st.selectbox(
    "Select a hypothetical scenario",
    list(scenario_presets.keys())
)

adjustment = st.slider(
    "Score-point adjustment",
    min_value=-1.0,
    max_value=1.0,
    value=float(scenario_presets[scenario]),
    step=0.05,
    help=(
        "This adds or subtracts the selected number of score points "
        "from every occupation. It is an illustrative assumption."
    )
)

# Apply the same hypothetical adjustment to every occupation
simulated = (original + adjustment).rename("Simulated_Score")

results = df.copy()
results["Simulated_Score"] = simulated
results["Score_Change"] = adjustment

simulated_average = simulated.mean()
simulated_median = simulated.median()

# ---------------- SCENARIO RESULTS ----------------
st.markdown("### 3. Scenario Results")

c1, c2, c3 = st.columns(3)

c1.metric(
    "Original Average",
    f"{original_average:.3f}"
)

c2.metric(
    "Simulated Average",
    f"{simulated_average:.3f}",
    delta=f"{simulated_average - original_average:+.3f}"
)

c3.metric(
    "Score-Point Adjustment",
    f"{adjustment:+.2f}"
)

st.caption(
    "The adjustment is applied equally to all occupations. "
    "It changes score levels, not the relative ranking of occupations."
)

st.divider()

# ---------------- DISTRIBUTION CHART ----------------
st.markdown("### 4. Exposure Score Distribution")

st.write(
    "Compare the original scores with the simulated scores. "
    "The chart shows how the distribution shifts under your assumption."
)

fig1, ax1 = plt.subplots(figsize=(8, 3.5))

bins = np.linspace(
    min(original.min(), simulated.min()) - 0.1,
    max(original.max(), simulated.max()) + 0.1,
    25
)

ax1.hist(
    original,
    bins=bins,
    alpha=0.75,
    color=TEAL,
    label="Original",
    edgecolor=NAVY
)

ax1.hist(
    simulated,
    bins=bins,
    alpha=0.55,
    color=LIGHT_TEAL,
    label="Simulated",
    edgecolor=NAVY
)

ax1.axvline(
    original_average,
    color=WHITE,
    linestyle="--",
    linewidth=1.5,
    label="Original mean"
)

ax1.axvline(
    simulated_average,
    color="#F59E0B",
    linestyle=":",
    linewidth=2,
    label="Simulated mean"
)

ax1.set_xlabel("Exposure score", color=WHITE)
ax1.set_ylabel("Number of occupations", color=WHITE)
ax1.set_title(
    "Original vs Simulated Score Distribution",
    color=WHITE
)
ax1.set_facecolor(PANEL)
fig1.patch.set_facecolor(NAVY)
ax1.tick_params(colors=WHITE)
ax1.grid(axis="y", alpha=0.15)
ax1.legend(facecolor=PANEL, labelcolor=WHITE, fontsize=8)

for spine in ax1.spines.values():
    spine.set_color(MUTED)

fig1.tight_layout()
st.pyplot(fig1, use_container_width=True)
plt.close(fig1)

# ---------------- TOP 10 OCCUPATIONS ----------------
st.markdown("### 5. Top 10 Occupations: Original vs Simulated")

top10 = results.nlargest(
    10, "AI_Exposure_Score"
).sort_values(
    "AI_Exposure_Score",
    ascending=True
)

fig2, ax2 = plt.subplots(figsize=(8, 4.5))

positions = np.arange(len(top10))
bar_height = 0.36

ax2.barh(
    positions - bar_height / 2,
    top10["AI_Exposure_Score"],
    height=bar_height,
    color=TEAL,
    label="Original"
)

ax2.barh(
    positions + bar_height / 2,
    top10["Simulated_Score"],
    height=bar_height,
    color=LIGHT_TEAL,
    label="Simulated"
)

ax2.set_yticks(positions)
ax2.set_yticklabels(
    top10["Occupation_Title"],
    fontsize=8,
    color=WHITE
)
ax2.set_xlabel("Exposure score", color=WHITE)
ax2.set_title(
    "Top 10 by Original Exposure Score",
    color=WHITE
)
ax2.set_facecolor(PANEL)
fig2.patch.set_facecolor(NAVY)
ax2.tick_params(axis="x", colors=WHITE)
ax2.grid(axis="x", alpha=0.15)
ax2.legend(facecolor=PANEL, labelcolor=WHITE, fontsize=8)

for spine in ax2.spines.values():
    spine.set_color(MUTED)

fig2.tight_layout()
st.pyplot(fig2, use_container_width=True)
plt.close(fig2)

st.caption(
    "The top 10 list is selected using original scores, so the same "
    "occupations remain visible in both series for a fair comparison."
)

# ---------------- INDIVIDUAL OCCUPATION ----------------
st.divider()
st.markdown("### 6. Explore an Individual Occupation")

results["Occupation_Option"] = (
    results["Occupation_Title"] + " (" + results["SOC_Code"] + ")"
)

selected = st.selectbox(
    "Choose an occupation to compare",
    sorted(results["Occupation_Option"].unique()),
    key="scenario_occupation"
)

row = results.loc[
    results["Occupation_Option"] == selected
].iloc[0]

a, b, c = st.columns(3)

a.metric("Occupation", row["Occupation_Title"])
b.metric("Original Score", f'{row["AI_Exposure_Score"]:.3f}')
c.metric("Simulated Score", f'{row["Simulated_Score"]:.3f}')

# ---------------- SCENARIO INTERPRETATION ----------------
st.markdown("### 7. Scenario Interpretation")

if adjustment > 0:
    st.info(
        f"This scenario adds {adjustment:.2f} points to every occupation. "
        "It is an illustrative increase, not evidence that AI adoption "
        "or job losses will increase by this amount."
    )
elif adjustment < 0:
    st.info(
        f"This scenario subtracts {abs(adjustment):.2f} points from every "
        "occupation. It does not demonstrate that occupations are becoming "
        "safer or less affected by AI."
    )
else:
    st.info(
        "Baseline selected: the simulated scores equal the original scores."
    )

st.warning(
    "Important limitation: this is a user-defined mathematical scenario, "
    "not a forecast. It does not model real-world AI adoption, job losses, "
    "future hiring, or changes in task composition. Exposure scores are "
    "not probabilities of job loss."
)

# ---------------- DATA TABLE ----------------
with st.expander("View all original and simulated scores"):
    display_df = results[
        [
            "SOC_Code",
            "Occupation_Title",
            "AI_Exposure_Score",
            "Simulated_Score",
            "Score_Change"
        ]
    ].sort_values(
        "Simulated_Score",
        ascending=False
    )

    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True
    )

st.caption(
    "Source: AI Occupation Exposure Repository | "
    "Scenario adjustments are illustrative assumptions."
)
