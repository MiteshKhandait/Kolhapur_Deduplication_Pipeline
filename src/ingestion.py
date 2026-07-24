from pathlib import Path
import pandas as pd


def get_excel_files(raw_folder: str) -> list[Path]:
    """
    Returns all Excel files present in the raw data folder.

    Parameters
    ----------
    raw_folder : str
        Path to the raw data folder.

    Returns
    -------
    list[Path]
        Sorted list of Excel file paths.
    """

    folder = Path(raw_folder)

    if not folder.exists():
        raise FileNotFoundError(
            f"Folder does not exist: {folder}"
        )

    # Find both .xlsx and .xls files
    excel_files = sorted(folder.glob("*.xlsx"))
    excel_files.extend(sorted(folder.glob("*.xls")))

    if not excel_files:
        raise FileNotFoundError(
            f"No Excel files found in {folder}"
        )

    return excel_files


def standardize_dtypes(
    df: pd.DataFrame,
    config: dict
) -> pd.DataFrame:
    """
    Standardize configured data types.
    """

    dtype_columns = config["dtype_columns"]

    # Integer columns
    for column in dtype_columns.get("integer", []):

        if column in df.columns:

            df[column] = pd.to_numeric(
                df[column],
                errors="coerce"
            ).astype("Int64")

    # Float columns
    for column in dtype_columns.get("float", []):

        if column in df.columns:

            df[column] = pd.to_numeric(
                df[column],
                errors="coerce"
            )

    # String columns
    for column in dtype_columns.get("string", []):

        if column in df.columns:

            df[column] = df[column].astype("string")

    return df

def standardize_dates(
    df: pd.DataFrame,
    config: dict
) -> pd.DataFrame:

    date_columns = config["date_columns"]

    for column in date_columns:

        if column in df.columns:

            df[column] = pd.to_datetime(
                df[column],
                errors="coerce",
                dayfirst=True,
                format="mixed"
            )

    return df


def read_excel_files(config: dict) -> list[pd.DataFrame]:
    """
    Read all Excel files, standardize them,
    and return a list of DataFrames.
    """

    raw_folder = config["paths"]["raw_data"]

    excel_files = get_excel_files(raw_folder)

    dataframes = []

    print("\nReading Excel files...\n")

    for file in excel_files:

        print(f"Reading: {file.name}")

        df = pd.read_excel(file)

        df = standardize_dates(df, config)

        df = standardize_dtypes(df, config)

        df["Origin_File"] = file.name

        dataframes.append(df)

    print("\nAll Excel files successfully loaded.\n")

    return dataframes



def merge_dataframes(
    dataframes: list[pd.DataFrame]
) -> pd.DataFrame:
    """
    Merge all DataFrames into a single master DataFrame.

    Parameters
    ----------
    dataframes : list[pd.DataFrame]
        List of DataFrames returned by read_excel_files().

    Returns
    -------
    pd.DataFrame
        Combined master DataFrame.
    """

    master_df = pd.concat(
        dataframes,
        ignore_index=True
    )

    return master_df


def validate_master_dataframe(
    master_df: pd.DataFrame
) -> None:
    """
    Validate the merged master DataFrame and
    print basic dataset information.
    """

    print("\n========== MASTER DATASET VALIDATION ==========\n")

    print(f"Rows    : {master_df.shape[0]}")
    print(f"Columns : {master_df.shape[1]}")

    duplicate_columns = master_df.columns[
        master_df.columns.duplicated()
    ]

    print(f"\nDuplicate column names : {len(duplicate_columns)}")

    if len(duplicate_columns):

        print(duplicate_columns.tolist())

    print(
        f"\nCompletely empty rows : "
        f"{master_df.isna().all(axis=1).sum()}"
    )

    print(
        f"Duplicate Udyam Numbers : "
        f"{master_df['Udyam Reg. No'].duplicated().sum()}"
    )

    print("\nValidation completed.\n")