from src.config import load_config
from src.ingestion import get_excel_files


def main():

    config = load_config()

    raw_folder = config["paths"]["raw_data"]

    excel_files = get_excel_files(raw_folder)

    print("\nExcel files found:\n")

    for file in excel_files:
        print(file.name)


if __name__ == "__main__":
    main()