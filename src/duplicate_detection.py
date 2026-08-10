import pandas as pd

def analyze_duplicate_udyam(
    df: pd.DataFrame
) -> pd.DataFrame:
    """
    Analyze duplicate Udyam Registration Numbers.

    Returns
    -------
    pd.DataFrame
        Summary table containing each duplicated
        Udyam Number and its record count.
    """

    duplicate_summary = (
        df.groupby("Udyam Reg. No")
          .size()
          .reset_index(name="Record_Count")
    )

    duplicate_summary = (
        duplicate_summary[
            duplicate_summary["Record_Count"] > 1
        ]
        .sort_values(
            "Record_Count",
            ascending=False
        )
        .reset_index(drop=True)
    )

    print("\n========== DUPLICATE UDYAM ANALYSIS ==========\n")

    print(f"Total Rows                : {len(df)}")

    print(
        f"Unique Udyam Numbers      : "
        f"{df['Udyam Reg. No'].nunique()}"
    )

    print(
        f"Duplicate Udyam Groups    : "
        f"{len(duplicate_summary)}"
    )

    print(
        f"Duplicate Records         : "
        f"{duplicate_summary['Record_Count'].sum()}"
    )

    print(
        f"Largest Duplicate Group   : "
        f"{duplicate_summary['Record_Count'].max()}"
    )

    print(
        f"Average Group Size        : "
        f"{duplicate_summary['Record_Count'].mean():.2f}"
    )

    print("\n=============================================\n")

    return duplicate_summary



def score_duplicate_pairs(
    df: pd.DataFrame,
    config: dict
) -> pd.DataFrame:
    """
    Compare duplicate Udyam record pairs and
    compute their weighted match score.
    """

    weights = config["duplicate_scoring"]["weights"]

    file_rank = config["origin_file_rank"]

    duplicate_df = df[
        df.duplicated(
            subset="Udyam Reg. No",
            keep=False
        )
    ].copy()

    results = []

    for group_no, (udyam_no, group) in enumerate(
        duplicate_df.groupby("Udyam Reg. No"),
        start=1
    ):

        if len(group) != 2:
            continue

        row1 = group.iloc[0]
        row2 = group.iloc[1]

        score = 0

        enterprise_match = (
            row1["Enterprise Name"] ==
            row2["Enterprise Name"]
        )

        owner_match = (
            row1["Owner Name"] ==
            row2["Owner Name"]
        )

        mobile_match = (
            row1["Mobile No."] ==
            row2["Mobile No."]
        )

        email_match = (
            row1["Email Id"] ==
            row2["Email Id"]
        )

        investment_changed = (
            row1["Investment Cost (In Rs.)"] !=
            row2["Investment Cost (In Rs.)"]
        )

        turnover_changed = (
            row1["Net Turnover (In Rs.)"] !=
            row2["Net Turnover (In Rs.)"]
        )

        if enterprise_match:
            score += weights["enterprise_name"]

        if owner_match:
            score += weights["owner_name"]

        if mobile_match:
            score += weights["mobile_number"]

        if email_match:
            score += weights["email_id"]

        if not investment_changed:
            score += weights["investment_cost"]

        if not turnover_changed:
            score += weights["turnover"]

        rank1 = file_rank.get(
            row1["Origin_File"],
            0
        )

        rank2 = file_rank.get(
            row2["Origin_File"],
            0
        )

        if rank1 >= rank2:

            latest_record = row1
            older_record = row2

        else:

            latest_record = row2
            older_record = row1

        results.append({

            "Duplicate_Group_ID":
                f"DUP{group_no:06d}",

            "Udyam Reg. No":
                udyam_no,

            "Enterprise_Match":
                enterprise_match,

            "Owner_Match":
                owner_match,

            "Mobile_Match":
                mobile_match,

            "Email_Match":
                email_match,

            "Investment_Changed":
                investment_changed,

            "Turnover_Changed":
                turnover_changed,

            "Match_Score":
                score,

            "Latest_Row_Index":
                latest_record.name,

            "Older_Row_Index":
                older_record.name,

            "Latest_Origin_File":
                latest_record["Origin_File"],

            "Older_Origin_File":
                older_record["Origin_File"]

        })

    comparison_df = pd.DataFrame(results)

    print("\n========== DUPLICATE SCORING ==========\n")

    print(
        f"Pairs Compared : {len(comparison_df)}"
    )

    print(
        f"High Confidence Threshold : "
        f"{config['duplicate_scoring']['threshold']['high_confidence']}"
    )

    print("\n=======================================\n")

    return comparison_df


def apply_business_rules(
    comparison_df,
    config
):

    review_threshold = (
        config["duplicate_scoring"]["threshold"]["manual_review"]
    )

    comparison_df = comparison_df.copy()

    actions = []

    reasons = []

    for _, row in comparison_df.iterrows():

        score = row["Match_Score"]

        if score <= review_threshold:

            actions.append("Review")

            reasons.append(
                "Low Confidence Duplicate"
            )

            continue

        actions.append("Remove")

        if (
            row["Enterprise_Match"]
            and
            row["Owner_Match"]
            and
            row["Mobile_Match"]
            and
            row["Email_Match"]
        ):

            reasons.append(
                "Exact Duplicate"
            )

        elif not row["Enterprise_Match"]:

            reasons.append(
                "Enterprise Name Updated"
            )

        elif not row["Owner_Match"]:

            reasons.append(
                "Ownership Information Updated"
            )

        elif not row["Mobile_Match"]:

            if (
                row["Investment_Changed"]
                or
                row["Turnover_Changed"]
            ):

                reasons.append(
                    "Business Information Updated"
                )

            else:

                reasons.append(
                    "Contact Information Updated"
                )

        elif not row["Email_Match"]:

            if (
                row["Investment_Changed"]
                or
                row["Turnover_Changed"]
            ):

                reasons.append(
                    "Business Information Updated"
                )

            else:

                reasons.append(
                    "Contact Information Updated"
                )

        else:

            reasons.append(
                "Duplicate"
            )

    comparison_df["Action"] = actions

    comparison_df["Decision_Reason"] = reasons

    return comparison_df


def split_datasets(
    clean_df,
    comparison_df
):

    remove_indices = comparison_df.loc[
        comparison_df["Action"] == "Remove",
        "Older_Row_Index"
    ].tolist()

    review_groups = comparison_df.loc[
        comparison_df["Action"] == "Review",
        "Udyam Reg. No"
    ]

    review_df = clean_df[
        clean_df["Udyam Reg. No"].isin(
            review_groups
        )
    ].copy()

    master_df = clean_df.drop(
        index=remove_indices,
        errors="ignore"
    )


    duplicate_df = clean_df.loc[
        remove_indices
    ].copy()

    duplicate_df = duplicate_df.merge(

        comparison_df[
            [
                "Duplicate_Group_ID",
                "Udyam Reg. No",
                "Match_Score",
                "Decision_Reason",
                "Action",
                "Latest_Origin_File"
            ]
        ],

        on="Udyam Reg. No",

        how="left"

    )

    return (

        master_df,

        duplicate_df,

        review_df

    )