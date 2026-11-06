# EdTech Experiment & Causal Analysis

## Project Overview

This project evaluates whether a new educational intervention improves learner outcomes using A/B testing and causal analysis.

The intervention studied is **Personalised Weekly Progress Feedback**. Learners are divided into treatment and control groups, and their completion, assessment performance, dropout, attendance, and assignment submission are compared.

The project also estimates the impact of a previous regional change using **Difference-in-Differences (DiD)**, comparing Ahmedabad with Surat.

## Objectives

- Design an A/B experiment for an educational intervention.
- Check treatment and control group balance.
- Measure treatment effects with confidence intervals.
- Evaluate course completion as the primary outcome.
- Analyze assessment scores and dropout.
- Check attendance and assignment submission as guardrail metrics.
- Analyze treatment effects across regions.
- Estimate historical impact using Difference-in-Differences.
- Check the parallel-trends assumption.
- Make a final data-driven recommendation.

## Data

The experiment dataset contains activity records for **10,000 learners** over a **40-week course**.

The raw dataset contains **406,000 rows** because some learners have duplicate activity records. After cleaning duplicate learner-week records, the analysis dataset contains **400,000 records**.

The data includes:

- Learner ID
- Region
- Treatment assignment
- Attendance
- Assignment submission
- Assessment score
- Active status
- Dropout status
- Completion status

A separate historical dataset contains monthly outcome data for Ahmedabad and Surat for the Difference-in-Differences analysis.

### Important Note

The datasets used in this project are **synthetic datasets generated for this analysis**. An actual experiment dataset was not supplied on the project page, so the data was generated to reproduce the structure and data-quality issues described in the project requirements.

Therefore, the numerical results should not be interpreted as real-world results from an actual coaching institute.

## Data Quality Checks

The analysis included:

- Duplicate enrolment and activity detection
- Duplicate learner-week removal
- Missing attendance analysis
- Identification of structural missing values caused by learner inactivity
- Identification of genuine missing attendance among active learners
- Treatment/control balance checking
- Sample Ratio Mismatch testing

After cleaning, every learner had 40 weekly records.

## Experiment Design

### Intervention

Personalised Weekly Progress Feedback.

### Primary Metric

Course completion rate.

### Secondary Metric

Average assessment score.

### Supporting Outcome

Dropout rate.

### Guardrail Metrics

- Attendance rate
- Assignment submission rate

### Sample Size

Power analysis assumptions:

- Baseline completion rate: 10%
- Target completion rate: 14%
- Minimum detectable effect: 4 percentage points
- Significance level: 5%
- Statistical power: 80%

Required sample size:

- 1,029 learners per group
- 2,058 learners total

The experiment contains 10,000 learners, which is above the calculated requirement.

## Main Experiment Results

### Course Completion

- Control: **10.54%**
- Treatment: **11.74%**
- Effect: **+1.20 percentage points**
- 95% CI: approximately **-0.03 to +2.44 percentage points**

The completion-rate improvement was not statistically significant at the 5% level.

### Assessment Score

- Control mean: **64.64**
- Treatment mean: **68.11**
- Effect: **+3.47 points**
- 95% CI: approximately **+3.16 to +3.79 points**

The treatment effect was statistically significant.

### Dropout

The treatment group had a dropout rate approximately **0.09 percentage points lower** than the control group.

The confidence interval included zero, so there was no statistically significant evidence of a reduction in dropout.

### Guardrail Metrics

The treatment improved both engagement measures:

- Attendance: **+6.67 percentage points**
- Assignment submission: **+3.64 percentage points**

Both effects were statistically significant.

## Regional Analysis

Assessment scores were higher in the treatment group across all four regions.

| Region | Treatment Effect |
|---|---:|
| Ahmedabad | +3.34 |
| Rajkot | +3.23 |
| Surat | +3.95 |
| Vadodara | +3.17 |

The treatment-by-region interaction terms were not statistically significant. Therefore, there was no strong evidence that the assessment-score treatment effect differed between regions.

## Difference-in-Differences

The historical analysis compares Ahmedabad with Surat.

The pre-change trends were broadly similar, although they were not perfectly identical.

The Difference-in-Differences analysis estimated an effect of approximately:

**+5.19 points**

95% confidence interval:

**+4.72 to +5.66 points**

The estimated effect was statistically significant.

This result should be interpreted under the parallel-trends assumption.

## Final Recommendation

### Decision: EXTEND

The experiment should be extended rather than immediately rolled out or stopped.

The treatment produced significant improvements in assessment performance, attendance, and assignment submission. However, the primary outcome, course completion, did not show a statistically significant improvement.

A further complete course cycle should therefore be used to determine whether the observed improvements in learning performance and engagement eventually translate into higher completion.

## Limitations

The experiment assumes that treatment assignment was correctly randomized and that learners generally followed their assigned conditions.

Potential issues include:

- Treatment non-compliance
- Contamination between groups
- Missing data
- Learner dropout before outcomes are observed
- Incorrect treatment assignment
- Changes in outcome recording

The Difference-in-Differences analysis depends on the parallel-trends assumption. Other region-specific changes occurring at the same time as the intervention could also affect the estimate.

Because the datasets are synthetic, the numerical results demonstrate the analysis methodology rather than representing actual institutional outcomes.

## Technologies Used

- Python
- Pandas
- NumPy
- Matplotlib
- SciPy
- Statsmodels
- Scikit-learn
- Jupyter Notebook

## Project Structure

```text
EdTech_Experiment_Causal_Analysis/
├── data/
├── notebooks/
├── outputs/
├── report/
└── README.md
```