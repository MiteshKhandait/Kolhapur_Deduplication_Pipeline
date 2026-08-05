import pandas as pd
import re 



def standardize_source_columns(
    df: pd.DataFrame
) -> pd.DataFrame:
    """
    Standardize source-related columns into a single
    'Source_File' column.
    """

    if {"Source", "File"}.issubset(df.columns):

        mask = df["Source_File"].isna()

        df.loc[mask, "Source_File"] = (
            df.loc[mask, "Source"]
            .fillna("")
            .astype(str)
            .str.strip()
            + " "
            + df.loc[mask, "File"]
            .fillna("")
            .astype(str)
            .str.strip()
        ).str.strip()

        df = df.drop(
            columns=["Source", "File"]
        )

    return df


def standardize_text_columns(
    df: pd.DataFrame,
    config: dict
) -> pd.DataFrame:
    """
    Standardize text columns by removing leading and
    trailing whitespace, converting to lowercase,
    and replacing multiple spaces with a single space.
    """

    text_columns = config["dtype_columns"]["string"]

    for column in text_columns:

        if column in df.columns:

            df[column] = (
                df[column]
                .astype("string")
                .str.strip()
                .str.lower()
                .str.replace(r"\s+", " ", regex=True)
            )

    return df


def clean_address(
    df: pd.DataFrame,
    config: dict
) -> pd.DataFrame:
    """
    Clean the Address column by normalizing Unicode
    characters, removing selected punctuation,
    and collapsing multiple spaces.
    """

    if "Address" not in df.columns:
        return df

    address = df["Address"].astype("string")

    replacements = config["address_cleaning"]["unicode_replacements"]

    for old, new in replacements.items():

        address = address.str.replace(
            old,
            new,
            regex=False
        )

    address = (
        address
        .str.replace(
            config["address_cleaning"]["remove_pattern"],
            "",
            regex=True
        )
        .str.replace(r"\s+", " ", regex=True)
        .str.strip()
    )

    df["Address"] = address

    return df


def clean_mobile_numbers(
    df: pd.DataFrame
) -> pd.DataFrame:
    """
    Standardize the Mobile No. column by removing
    formatting characters while preserving the
    original number.
    """

    if "Mobile No." not in df.columns:
        return df

    df["Mobile No."] = (
        df["Mobile No."]
        .astype("string")
        .str.strip()
        .str.replace(".0", "", regex=False)
        .str.replace(" ", "", regex=False)
        .str.replace("-", "", regex=False)
        .str.replace("+91", "", regex=False)
        .str.replace(r"[()]", "", regex=True)
        .replace("", pd.NA)
    )

    return df


def clean_pincode(
    df: pd.DataFrame
) -> pd.DataFrame:
    """
    Standardize the PinCode column by removing
    unnecessary formatting.
    """

    if "PinCode" not in df.columns:
        return df

    df["PinCode"] = (
        df["PinCode"]
        .astype("string")
        .str.strip()
        # .str.replace(".0", "", regex=False)
        .replace("", pd.NA)
    )

    return df


def clean_email_ids(
    df: pd.DataFrame
) -> pd.DataFrame:
    """
    Standardize the Email Id column by removing
    unnecessary whitespace.
    """

    if "Email Id" not in df.columns:
        return df

    df["Email Id"] = (
        df["Email Id"]
        .astype("string")
        .str.strip()
        .str.replace(" ", "", regex=False)
        .replace("", pd.NA)
    )

    return df



def detect_invalid_rows(
    master_df: pd.DataFrame,
    config: dict
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Detect rows containing known anomalous patterns.

    Parameters
    ----------
    master_df : pd.DataFrame
        Master dataset loaded from the parquet file.

    config : dict
        Configuration dictionary.

    Returns
    -------
    clean_df : pd.DataFrame
        Dataset after removing invalid rows.

    invalid_rows : pd.DataFrame
        Detected invalid rows with exclusion reason.
    """

    patterns = config["invalid_row_patterns"]["patterns"]

    reason = config["invalid_row_patterns"]["reason"]

    invalid_mask = pd.Series(
        False,
        index=master_df.index
    )

    # Convert once instead of once per pattern
    string_df = master_df.astype(str)

    for pattern in patterns:

        current_mask = string_df.apply(
            lambda column: column.str.contains(
                pattern,
                regex=False,
                na=False
            )
        ).any(axis=1)

        invalid_mask |= current_mask

    invalid_rows = (
        master_df.loc[invalid_mask]
        .copy()
    )

    invalid_rows["Exclusion_Reason"] = reason

    clean_df = (
        master_df.loc[~invalid_mask]
        .copy()
    )

    print("\n========== INVALID ROW DETECTION ==========")
    print(f"Invalid rows detected : {len(invalid_rows)}")
    print(f"Remaining rows        : {len(clean_df)}")
    print("==========================================\n")

    return clean_df, invalid_rows