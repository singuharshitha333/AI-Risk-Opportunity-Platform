# Data Sources and Methodology

## Dataset 1: Language Modeling AI Exposure

**Source:** Felten, Raj, and Seamans — AIOE research repository

**Repository:** https://github.com/AIOE-Data/AIOE

**Downloaded file:** `ai_exposure_language_modeling.xlsx`

### Sheet 1: LM AIOE
- **Analysis level:** Occupations
- **Number of records:** 774
- **Identifier:** SOC code
- **Occupation field:** Occupation title
- **Exposure measure:** Language Modeling AI Occupational Exposure

### Sheet 2: LM AIIE
- **Analysis level:** Industries
- **Number of records:** 250
- **Identifier:** NAICS
- **Industry field:** NAICS description
- **Exposure measure:** Language Modeling AI Industry Exposure

### Industry Identifier Handling

The language-modeling industry sheet contains six-character identifiers. Some are numeric-looking (for example, `611100`), while others are alphanumeric (for example, `3250A1`).

The identifier `3250A1` is associated with the description "Chemical Manufacturing (3251, 3252, 3253, and 3259 only)", indicating a grouped industry category.

These identifiers are preserved as text. They must not be converted to ordinary numbers or assumed to be standard six-digit NAICS codes without verification.

The original identifiers and descriptions will be retained during data cleaning.

## Interpretation and Limitations

The exposure scores are research-based measures. They must not be interpreted as percentages or direct probabilities of job loss.

Higher scores indicate higher exposure relative to the reference distribution used by the researchers. Exposure does not automatically imply that a job will disappear; AI may automate some tasks, assist workers, or change job responsibilities.

The dataset describes a published research measure, not a live tracker of AI adoption or current employment changes.

## Planned Use

The occupation-level dataset will be examined alongside employment projections and occupational skills information, subject to compatible identifiers and definitions.

The industry-level dataset will be analyzed separately unless a reliable industry-level employment dataset can be matched.

## Citation

Felten, E. W., Raj, M., and Seamans, R. (2021). Occupational, industry, and geographic exposure to artificial intelligence: A novel dataset and its potential uses. *Strategic Management Journal, 42*(12), 2195–2217.

The language-modeling extension should also be cited using the relevant publication details provided by the source repository.

## Data Quality Checks Planned

- Verify column names and data types.
- Check for missing values.
- Check for duplicate occupation and industry identifiers.
- Validate exposure score ranges.
- Preserve raw source files and document all cleaning steps.