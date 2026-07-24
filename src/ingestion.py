from pathlib import Path


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