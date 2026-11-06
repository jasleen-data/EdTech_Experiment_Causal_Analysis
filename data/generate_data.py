import numpy as np
import pandas as pd
from pathlib import Path

# ---------------------------------------------------------
# 1. Basic settings
# ---------------------------------------------------------

SEED = 42
rng = np.random.default_rng(SEED)

N_LEARNERS = 10000
WEEKS = 40

DATA_DIR = Path(__file__).resolve().parent
RAW_FILE = DATA_DIR / "raw_learner_activity.csv"
HISTORICAL_FILE = DATA_DIR / "historical_region_data.csv"


# ---------------------------------------------------------
# 2. Create learner-level information
# ---------------------------------------------------------

learner_ids = [
    f"L{number:05d}"
    for number in range(1, N_LEARNERS + 1)
]

regions = rng.choice(
    ["Ahmedabad", "Surat", "Vadodara", "Rajkot"],
    size=N_LEARNERS,
    p=[0.35, 0.30, 0.20, 0.15]
)

batches = rng.choice(
    [f"B{number:03d}" for number in range(101, 151)],
    size=N_LEARNERS
)

enrolment_dates = pd.to_datetime(
    rng.choice(
        pd.date_range("2025-01-01", "2025-09-30"),
        size=N_LEARNERS
    )
)

# Random treatment assignment for the A/B experiment
treatment = rng.binomial(
    1,
    0.50,
    size=N_LEARNERS
)

learner_df = pd.DataFrame({
    "learner_id": learner_ids,
    "batch_id": batches,
    "region": regions,
    "enrolment_date": enrolment_dates,
    "treatment": treatment
})


# ---------------------------------------------------------
# 3. Introduce duplicate enrolment records
# ---------------------------------------------------------

duplicate_candidates = learner_df.sample(
    n=150,
    random_state=SEED
).copy()

duplicate_candidates["enrolment_date"] = (
    duplicate_candidates["enrolment_date"]
    + pd.to_timedelta(
        rng.integers(1, 5, size=len(duplicate_candidates)),
        unit="D"
    )
)

duplicate_candidates["duplicate_record"] = True

learner_df["duplicate_record"] = False

duplicate_learner_rows = duplicate_candidates[
    [
        "learner_id",
        "batch_id",
        "region",
        "enrolment_date",
        "treatment",
        "duplicate_record"
    ]
]

duplicate_learner_rows.to_csv(
    DATA_DIR / "duplicate_enrolments.csv",
    index=False
)

# Add duplicate enrolments to learner-level data
learner_df = pd.concat(
    [
        learner_df,
        duplicate_candidates.drop(
            columns=["duplicate_record"]
        )
    ],
    ignore_index=True
)


# ---------------------------------------------------------
# 4. Generate weekly learning activity
# ---------------------------------------------------------

records = []

for row in learner_df.itertuples(index=False):

    # Learner-level ability
    learner_ability = rng.normal(0, 1)

    # Treatment effect is deliberately modest
    treatment_effect = (
        0.06
        if row.treatment == 1
        else 0.0
    )

    # Some learners are more likely to drop out
    dropout_risk = rng.uniform(0.02, 0.12)

    dropped = False

    for week in range(1, WEEKS + 1):

        # Once a learner drops out, later activity becomes limited
        if dropped:

            attendance = np.nan
            assignment = 0
            assessment = np.nan
            active_status = "Inactive"

        else:

            attendance_probability = (
                0.72
                + 0.06 * learner_ability
                + treatment_effect
                - 0.002 * week
            )

            attendance_probability = np.clip(
                attendance_probability,
                0.20,
                0.98
            )

            attendance = rng.binomial(
                1,
                attendance_probability
            )

            assignment_probability = (
                0.65
                + 0.08 * learner_ability
                + treatment_effect
            )

            assignment_probability = np.clip(
                assignment_probability,
                0.20,
                0.98
            )

            assignment = rng.binomial(
                1,
                assignment_probability
            )

            assessment = (
                60
                + 7 * learner_ability
                + 4 * attendance
                + 3 * assignment
                + 3 * row.treatment
                + rng.normal(0, 8)
            )

            assessment = np.clip(
                assessment,
                0,
                100
            )

            # Dropout becomes more likely with poor engagement
            weekly_dropout_probability = (
                dropout_risk
                * (
                    1.15
                    - 0.35 * attendance
                    - 0.20 * assignment
                )
            )

            if rng.random() < weekly_dropout_probability:
                dropped = True
            active_status = "Inactive" if dropped else "Active"

        completion_status = (
            "Completed"
            if (
                week == WEEKS
                and not dropped
                and attendance == 1
            )
            else "Not Completed"
        )

        dropout_status = (
            "Dropped"
            if dropped
            else "Not Dropped"
        )

        records.append({
            "learner_id": row.learner_id,
            "batch_id": row.batch_id,
            "region": row.region,
            "enrolment_date": row.enrolment_date,
            "treatment": row.treatment,
            "week": week,
            "attendance": attendance,
            "assignment_submitted": assignment,
            "assessment_score": assessment,
            "active_status": active_status,
            "dropout_status": dropout_status,
            "completion_status": completion_status
        })


raw_df = pd.DataFrame(records)


# ---------------------------------------------------------
# 5. Introduce missing attendance records
# ---------------------------------------------------------

missing_mask = (
    rng.random(len(raw_df)) < 0.015
)

raw_df.loc[
    missing_mask,
    "attendance"
] = np.nan


# ---------------------------------------------------------
# 6. Introduce inconsistent active/dropout statuses
# ---------------------------------------------------------

problem_rows = raw_df[
    raw_df["dropout_status"] == "Dropped"
].sample(
    n=min(
        200,
        (
            raw_df["dropout_status"] == "Dropped"
        ).sum()
    ),
    random_state=SEED
).index

raw_df.loc[
    problem_rows,
    "active_status"
] = "Active"


# ---------------------------------------------------------
# 7. Save raw activity data
# ---------------------------------------------------------

raw_df.to_csv(
    RAW_FILE,
    index=False
)


# ---------------------------------------------------------
# 8. Create historical regional data
# ---------------------------------------------------------

periods = pd.date_range(
    "2024-01-01",
    periods=12,
    freq="MS"
)

historical_records = []

for region in ["Ahmedabad", "Surat"]:

    for period_number, period in enumerate(
        periods,
        start=1
    ):

        post_change = (
            1
            if period_number >= 8
            else 0
        )

        for learner_number in range(1, 501):

            baseline = (
                70
                + rng.normal(0, 4)
                + 0.5 * period_number
            )

            historical_effect = (
                5
                if (
                    region == "Ahmedabad"
                    and post_change == 1
                )
                else 0
            )

            outcome = (
                baseline
                + historical_effect
                + rng.normal(0, 5)
            )

            historical_records.append({
                "region": region,
                "period": period,
                "post_change": post_change,
                "treated": (
                    1
                    if region == "Ahmedabad"
                    else 0
                ),
                "outcome_score": outcome
            })


historical_df = pd.DataFrame(
    historical_records
)

historical_df.to_csv(
    HISTORICAL_FILE,
    index=False
)


# ---------------------------------------------------------
# 9. Print a simple summary
# ---------------------------------------------------------

print("Data generation completed successfully.")
print(f"Raw activity rows: {len(raw_df):,}")
print(f"Unique learners: {raw_df['learner_id'].nunique():,}")
print(
    "Duplicate enrolment learners: "
    f"{len(duplicate_candidates):,}"
)
print(
    "Missing attendance values: "
    f"{raw_df['attendance'].isna().sum():,}"
)
print(
    "Inconsistent active/dropout rows: "
    f"{(
        (raw_df['dropout_status'] == 'Dropped')
        & (raw_df['active_status'] == 'Active')
    ).sum():,}"
)
print(f"Historical rows: {len(historical_df):,}")
print(f"Raw data saved to: {RAW_FILE}")
print(
    f"Historical data saved to: "
    f"{HISTORICAL_FILE}"
)