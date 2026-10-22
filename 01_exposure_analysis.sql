
USE AIRiskOpportunityDB;
GO

-- =========================================================
-- AI RISK VS OPPORTUNITY INTELLIGENCE PLATFORM
-- SQL ANALYSIS
-- =========================================================


-- 1. Verify the number of records in both tables

SELECT
    'Occupations' AS Dataset,
    COUNT(*) AS Total_Records
FROM dbo.OccupationExposure

UNION ALL

SELECT
    'Industries' AS Dataset,
    COUNT(*) AS Total_Records
FROM dbo.IndustryExposure;


-- 2. Overall occupation exposure statistics

SELECT
    COUNT(*) AS Total_Occupations,
    MIN(AI_Exposure_Score) AS Minimum_Score,
    MAX(AI_Exposure_Score) AS Maximum_Score,
    CAST(AVG(AI_Exposure_Score) AS DECIMAL(10, 4))
        AS Average_Score
FROM dbo.OccupationExposure;


-- 3. Top 10 occupations by exposure score

SELECT TOP 10
    SOC_Code,
    Occupation_Title,
    AI_Exposure_Score
FROM dbo.OccupationExposure
ORDER BY AI_Exposure_Score DESC;


-- 4. Bottom 10 occupations by exposure score

SELECT TOP 10
    SOC_Code,
    Occupation_Title,
    AI_Exposure_Score
FROM dbo.OccupationExposure
ORDER BY AI_Exposure_Score ASC;


-- 5. Occupation exposure category distribution
-- Categories are analytical thresholds for this project,
-- not official categories from the dataset publisher.

SELECT
    CASE
        WHEN AI_Exposure_Score >= 1
            THEN 'High Exposure'
        WHEN AI_Exposure_Score >= 0
            THEN 'Moderate Exposure'
        ELSE 'Lower Exposure'
    END AS Exposure_Category,
    COUNT(*) AS Number_of_Occupations,
    CAST(AVG(AI_Exposure_Score) AS DECIMAL(10, 4))
        AS Average_Score
FROM dbo.OccupationExposure
GROUP BY
    CASE
        WHEN AI_Exposure_Score >= 1
            THEN 'High Exposure'
        WHEN AI_Exposure_Score >= 0
            THEN 'Moderate Exposure'
        ELSE 'Lower Exposure'
    END
ORDER BY Average_Score DESC;


-- 6. Overall industry exposure statistics

SELECT
    COUNT(*) AS Total_Industries,
    MIN(AI_Exposure_Score) AS Minimum_Score,
    MAX(AI_Exposure_Score) AS Maximum_Score,
    CAST(AVG(AI_Exposure_Score) AS DECIMAL(10, 4))
        AS Average_Score
FROM dbo.IndustryExposure;


-- 7. Top 10 industries by exposure score

SELECT TOP 10
    Industry_Code,
    Industry_Description,
    AI_Exposure_Score
FROM dbo.IndustryExposure
ORDER BY AI_Exposure_Score DESC;


-- 8. Bottom 10 industries by exposure score

SELECT TOP 10
    Industry_Code,
    Industry_Description,
    AI_Exposure_Score
FROM dbo.IndustryExposure
ORDER BY AI_Exposure_Score ASC;


-- 9. Industry exposure category distribution

SELECT
    CASE
        WHEN AI_Exposure_Score >= 1
            THEN 'High Exposure'
        WHEN AI_Exposure_Score >= 0
            THEN 'Moderate Exposure'
        ELSE 'Lower Exposure'
    END AS Exposure_Category,
    COUNT(*) AS Number_of_Industries,
    CAST(AVG(AI_Exposure_Score) AS DECIMAL(10, 4))
        AS Average_Score
FROM dbo.IndustryExposure
GROUP BY
    CASE
        WHEN AI_Exposure_Score >= 1
            THEN 'High Exposure'
        WHEN AI_Exposure_Score >= 0
            THEN 'Moderate Exposure'
        ELSE 'Lower Exposure'
    END
ORDER BY Average_Score DESC;
