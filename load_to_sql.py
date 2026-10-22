
from pathlib import Path

import pandas as pd
import pyodbc

# ============================================================
# 1. PROJECT PATHS AND SQL SERVER SETTINGS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_FOLDER = PROJECT_ROOT / "data" / "processed"

OCCUPATION_FILE = DATA_FOLDER / "ai_occupation_exposure_clean.xlsx"
INDUSTRY_FILE = DATA_FOLDER / "ai_industry_exposure_clean.xlsx"

SERVER = r"localhost\SQLEXPRESS"
DATABASE = "AIRiskOpportunityDB"
DRIVER = "ODBC Driver 18 for SQL Server"

EXPECTED_OCCUPATION_ROWS = 774
EXPECTED_INDUSTRY_ROWS = 250

# ============================================================
# 2. CHECK THE INPUT FILES
# ============================================================

for file_path in [OCCUPATION_FILE, INDUSTRY_FILE]:
    if not file_path.exists():
        raise FileNotFoundError(
            f"Required Excel file not found:\n{file_path}"
        )

# ============================================================
# 3. LOAD THE CLEAN DATASETS
# ============================================================

occupations = pd.read_excel(
    OCCUPATION_FILE,
    dtype={"soc_code": "string"},
)

industries = pd.read_excel(
    INDUSTRY_FILE,
    dtype={"industry_code": "string"},
)

print("=" * 65)
print("AI RISK VS OPPORTUNITY INTELLIGENCE PLATFORM")
print("PYTHON TO SQL SERVER DATA IMPORT")
print("=" * 65)

print(f"\nOccupation records loaded: {len(occupations)}")
print(f"Industry records loaded: {len(industries)}")

# Validate row counts before connecting.
if len(occupations) != EXPECTED_OCCUPATION_ROWS:
    raise ValueError("Occupation dataset has an unexpected row count.")

if len(industries) != EXPECTED_INDUSTRY_ROWS:
    raise ValueError("Industry dataset has an unexpected row count.")

# Validate required columns.
if list(occupations.columns) != [
    "soc_code",
    "occupation_title",
    "ai_exposure_score",
]:
    raise ValueError("Occupation dataset columns do not match.")

if list(industries.columns) != [
    "industry_code",
    "industry_description",
    "ai_exposure_score",
]:
    raise ValueError("Industry dataset columns do not match.")

# ============================================================
# 4. CONNECT TO SQL SERVER
# ============================================================

connection_string = (
    f"DRIVER={{{DRIVER}}};"
    f"SERVER={SERVER};"
    f"DATABASE={DATABASE};"
    "Trusted_Connection=yes;"
    "Encrypt=yes;"
    "TrustServerCertificate=yes;"
)

connection = None

try:
    connection = pyodbc.connect(
        connection_string,
        timeout=10,
    )

    cursor = connection.cursor()

    print("\nSQL Server connection: SUCCESS")
    print(f"Database: {DATABASE}")

    # ========================================================
    # 5. PREVENT ACCIDENTAL DUPLICATE IMPORTS
    # ========================================================

    cursor.execute(
        "SELECT COUNT(*) FROM dbo.OccupationExposure"
    )
    existing_occupations = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM dbo.IndustryExposure"
    )
    existing_industries = cursor.fetchone()[0]

    print(f"\nExisting occupation rows: {existing_occupations}")
    print(f"Existing industry rows: {existing_industries}")

    if existing_occupations != 0 or existing_industries != 0:
        raise RuntimeError(
            "At least one SQL table already contains records. "
            "Import stopped to avoid duplicate data. "
            "Check the table contents in SSMS before continuing."
        )

    # ========================================================
    # 6. PREPARE OCCUPATION RECORDS
    # ========================================================

    occupation_records = [
        (
            str(row.soc_code),
            str(row.occupation_title),
            float(row.ai_exposure_score),
        )
        for row in occupations.itertuples(index=False)
    ]

    # ========================================================
    # 7. PREPARE INDUSTRY RECORDS
    # ========================================================

    industry_records = [
        (
            str(row.industry_code),
            str(row.industry_description),
            float(row.ai_exposure_score),
        )
        for row in industries.itertuples(index=False)
    ]

    # ========================================================
    # 8. INSERT RECORDS INTO SQL SERVER
    # ========================================================

    cursor.executemany(
        """
        INSERT INTO dbo.OccupationExposure
            (SOC_Code, Occupation_Title, AI_Exposure_Score)
        VALUES (?, ?, ?)
        """,
        occupation_records,
    )

    print("\nOccupation records inserted.")

    cursor.executemany(
        """
        INSERT INTO dbo.IndustryExposure
            (Industry_Code, Industry_Description, AI_Exposure_Score)
        VALUES (?, ?, ?)
        """,
        industry_records,
    )

    print("Industry records inserted.")

    # ========================================================
    # 9. VERIFY IMPORT COUNTS
    # ========================================================

    cursor.execute(
        "SELECT COUNT(*) FROM dbo.OccupationExposure"
    )
    final_occupations = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM dbo.IndustryExposure"
    )
    final_industries = cursor.fetchone()[0]

    if (
        final_occupations != EXPECTED_OCCUPATION_ROWS
        or final_industries != EXPECTED_INDUSTRY_ROWS
    ):
        raise RuntimeError(
            "SQL row counts do not match expected counts."
        )

    # Commit only after both imports and count checks succeed.
    connection.commit()

    print("\n" + "=" * 65)
    print("DATA IMPORT COMPLETED SUCCESSFULLY")
    print("=" * 65)
    print(f"Occupation records in SQL Server: {final_occupations}")
    print(f"Industry records in SQL Server: {final_industries}")
    print("Both tables passed the row-count checks.")

except Exception:
    if connection is not None:
        connection.rollback()

    print("\nIMPORT FAILED. Changes in this transaction were rolled back.")
    raise

finally:
    if connection is not None:
        connection.close()
        print("\nSQL Server connection closed.")
