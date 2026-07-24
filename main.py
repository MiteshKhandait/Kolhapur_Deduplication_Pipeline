from src.config import load_config
from src.ingestion import get_excel_files


# def main():

#     config = load_config()

#     raw_folder = config["paths"]["raw_data"]

#     excel_files = get_excel_files(raw_folder)

#     print("\nExcel files found:\n")

#     for file in excel_files:
#         print(file.name)


# if __name__ == "__main__":
#     main()


# from src.config import load_config
# from src.ingestion import read_excel_files

# config = load_config()

# dataframes = read_excel_files(config)

# print(f"\nTotal files loaded: {len(dataframes)}")

# for i, df in enumerate(dataframes, start=1):
#     print(f"\nDataFrame {i}")
#     print(df[config["date_columns"]].dtypes)
#     print(df[config["date_columns"]].head())


from src.config import load_config
from src.ingestion import read_excel_files

# config = load_config()

# dataframes = read_excel_files(config)

# print(f"\nTotal files loaded: {len(dataframes)}")

# for i, df in enumerate(dataframes, start=1):

#     print(f"\n===== DataFrame {i} =====")

#     print(df.dtypes)

from src.ingestion import merge_dataframes

# from src.config import load_config
# from src.ingestion import (
#     read_excel_files,
#     merge_dataframes
# )

# config = load_config()

# dataframes = read_excel_files(config)

# master_df = merge_dataframes(dataframes)

# print("\nMaster Dataset")
# print(master_df.shape)
# # print(master_df.head())
# print(master_df.columns.tolist())

from src.ingestion import (
    read_excel_files,
    merge_dataframes,
    validate_master_dataframe
)

config = load_config()

dataframes = read_excel_files(config)

master_df = merge_dataframes(dataframes)

validate_master_dataframe(master_df)