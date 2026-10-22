
from pathlib import Path
import pandas as pd

# ============================================================
# 1. PROJECT PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

INPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "ai_exposure_language_modeling_checked.xlsx"
)

OUTPUT_FOLDER = PROJECT_ROOT / "data" / "processed"

OCCUPATION_OUTPUT = (
    OUTPUT_FOLDER / "ai_occupation_exposure_clean.xlsx"
)

INDUSTRY_OUTPUT = (
    OUTPUT_FOLDER / "ai_industry_exposure_clean.xlsx"
)

# ============================================================
# 2. CHECK INPUT FILE
# ============================================================

if not INPUT_FILE.exists():
    raise FileNotFoundError(
        f"Input file not found:\n{INPUT_FILE}"
    )

OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)

print("=" * 65)
print("AI RISK VS OPPORTUNITY INTELLIGENCE PLATFORM")
print("DATA CLEANING AND EXPORT")
print("=" * 65)

# ============================================================
# 3. LOAD THE REQUIRED COLUMNS ONLY
# ============================================================

occupations = pd.read_excel(
    INPUT_FILE,
    sheet_name="LM AIOE",
    usecols=[
        "SOC Code",
        "Occupation Title",
        "Language Modeling AIOE",
    ],
    dtype={"SOC Code": "string"},
)

industries = pd.read_excel(
    INPUT_FILE,
    sheet_name="LM AIIE",
    usecols=[
        "NAICS",
        "NAICS Description",
        "Language Modeling AIIE",
    ],
    dtype={"NAICS": "string"},
)

# ============================================================
# 4. STANDARDIZE COLUMN NAMES
# ============================================================

occupations = occupations.rename(
    columns={
        "SOC Code": "soc_code",
        "Occupation Title": "occupation_title",
        "Language Modeling AIOE": "ai_exposure_score",
    }
)

industries = industries.rename(
    columns={
        "NAICS": "industry_code",
        "NAICS Description": "industry_description",
        "Language Modeling AIIE": "ai_exposure_score",
    }
)

# ============================================================
# 5. VALIDATE REQUIRED FIELDS
# ============================================================

required_occupation_columns = [
    "soc_code",
    "occupation_title",
    "ai_exposure_score",
]

required_industry_columns = [
    "industry_code",
    "industry_description",
    "ai_exposure_score",
]

assert list(occupations.columns) == required_occupation_columns
assert list(industries.columns) == required_industry_columns

assert len(occupations) == 774, (
    f"Unexpected occupation row count: {len(occupations)}"
)

assert len(industries) == 250, (
    f"Unexpected industry row count: {len(industries)}"
)

assert not occupations[required_occupation_columns].isna().any().any()
assert not industries[required_industry_columns].isna().any().any()

assert not occupations["soc_code"].duplicated().any()
assert not industries["industry_code"].duplicated().any()

# Ensure exposure scores are numeric.
occupations["ai_exposure_score"] = pd.to_numeric(
    occupations["ai_exposure_score"],
    errors="raise",
)

industries["ai_exposure_score"] = pd.to_numeric(
    industries["ai_exposure_score"],
    errors="raise",
)

# ============================================================
# 6. EXPORT CLEAN DATASETS
# ============================================================

occupations.to_excel(
    OCCUPATION_OUTPUT,
    index=False,
)

industries.to_excel(
    INDUSTRY_OUTPUT,
    index=False,
)

# ============================================================
# 7. PRINT SUMMARY
# ============================================================

print("\nOCCUPATION DATASET")
print("-" * 65)
print(f"Records: {len(occupations)}")
print(f"Columns: {occupations.columns.tolist()}")
print(f"Output: {OCCUPATION_OUTPUT}")
print(
    "Exposure score range: "
    f"{occupations['ai_exposure_score'].min():.3f} "
    "to "
    f"{occupations['ai_exposure_score'].max():.3f}"
)

print("\nINDUSTRY DATASET")
print("-" * 65)
print(f"Records: {len(industries)}")
print(f"Columns: {industries.columns.tolist()}")
print(f"Output: {INDUSTRY_OUTPUT}")
print(
    "Exposure score range: "
    f"{industries['ai_exposure_score'].min():.3f} "
    "to "
    f"{industries['ai_exposure_score'].max():.3f}"
)

print("\n" + "=" * 65)
print("DATA CLEANING COMPLETED SUCCESSFULLY")
print("Original workbooks were not modified.")
print("Both clean datasets were exported.")
print("=" * 65)
