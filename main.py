# from src.config import load_config
# from src.ingestion import get_excel_files


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


# from src.config import load_config
# from src.ingestion import read_excel_files

# config = load_config()

# dataframes = read_excel_files(config)

# print(f"\nTotal files loaded: {len(dataframes)}")

# for i, df in enumerate(dataframes, start=1):

#     print(f"\n===== DataFrame {i} =====")

#     print(df.dtypes)

# from src.ingestion import merge_dataframes

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

# from src.ingestion import (
#     read_excel_files,
#     merge_dataframes,
#     validate_master_dataframe,
#     save_master_dataset,
#     export_master_dataset_excel,
#     convert_dates_to_string
# )

# config = load_config()

# dataframes = read_excel_files(config)

# master_df = merge_dataframes(dataframes)

# validate_master_dataframe(master_df)

# from src.config import load_config


# config = load_config()

# master_df = load_master_dataset(config)

# from src.preprocessing import standardize_source_columns
# from src.preprocessing import standardize_text_columns

# master_df = standardize_source_columns(master_df)

# print(master_df.columns.tolist())

# print(master_df["Source_File"].isna().sum())

# print(master_df["Source_File"].head())

# from src.preprocessing import (
#     standardize_source_columns,
#     standardize_text_columns,
#     clean_address,
#     clean_mobile_numbers,
#     clean_pincode,
#     clean_email_ids,
#     detect_invalid_rows
# )

# # Preprocessing
# master_df = standardize_source_columns(master_df)
# master_df = standardize_text_columns(master_df, config)

# print(master_df["Enterprise Name"].head())
# print(master_df["Owner Name"].head())
# print(master_df["District"].head())
# print(master_df.columns.to_list())

# from src.preprocessing import (
#     standardize_source_columns,
#     standardize_text_columns,
#     clean_address
# )

# master_df = standardize_text_columns(
#     master_df,
#     config
# )

# master_df = clean_address(
#     master_df,
#     config
# )

# print(master_df["Address"].head(20))



# master_df = clean_mobile_numbers(master_df)

# master_df = clean_pincode(master_df)

# master_df = clean_email_ids(master_df)

# print(master_df["Mobile No."].head(20))
# print(master_df["Address"].head(10))
# print(master_df["PinCode"].head(20))
# print(master_df['Email Id'].head(20))

# save_master_dataset(
#     master_df,
#     config
# )

# # print(master_df.dtypes)

# excel_df = convert_dates_to_string(
#     master_df,
#     config
# )

# export_master_dataset_excel(
#     excel_df,
#     config
# )

# master_df, invalid_rows = detect_invalid_rows(
#     master_df,
#     config
# )

# print(f"Master Dataset : {master_df.shape}")

# print(f"Invalid Rows : {invalid_rows.shape}")

# print(invalid_rows.head(20))

# from src.config import load_config


# config = load_config()

# from src.ingestion import load_master_dataset



# master_df = load_master_dataset(config)


from src.config import load_config

from src.ingestion import (
    load_master_dataset,
    save_master_dataset,
    load_master_excel
)


# ==========================
# Load configuration
# ==========================

config = load_config()


# ==========================
# Load master dataset
# ==========================

# master_df = load_master_dataset(config)
master_df = load_master_excel(config)


# ==========================
# Temporary Testing
# ==========================

# print(master_df.shape)

# print()

# print(master_df.head())

# print()

# print(master_df.dtypes)

from src.preprocessing import detect_invalid_rows

clean_df, invalid_rows = detect_invalid_rows(
    master_df,
    config
)

# print(clean_df.shape)
# print(invalid_rows.shape)

# print()

# print(
#     invalid_rows[
#         [
#             "Enterprise Name",
#             "Exclusion_Reason"
#         ]
#     ].head(20)
# )

# save_master_dataset(
#     clean_df,
#     config
# )

# master_df = clean_df

# from src.duplicate_detection import (
#     find_duplicate_udyam_groups
# )

# duplicate_df = find_duplicate_udyam_groups(
#     master_df
# )

# print(duplicate_df.shape)

# print()

# print(
#     duplicate_df[
#         [
#             "Group_ID",
#             "Udyam Reg. No",
#             "Enterprise Name",
#             "Owner Name"
#         ]
#     ].head(100)
# )

# print(
#     invalid_rows["Enterprise Name"]
#     .head(50)
# )

# print()

# print(
#     invalid_rows["Owner Name"]
#     .head(50)
# )

from src.duplicate_detection import (
    analyze_duplicate_udyam,
    score_duplicate_pairs,
    apply_business_rules,
    split_datasets
)

duplicate_summary = analyze_duplicate_udyam(
    clean_df
)

# print(duplicate_summary.head(20))
comparison_df = score_duplicate_pairs(
    clean_df,
    config
)

# print(comparison_df.head(20))


# print(
#     comparison_df[
#         [
#             "Duplicate_Group_ID",
#             "Udyam Reg. No",
#             "Enterprise_Match",
#             "Owner_Match",
#             "Mobile_Match",
#             "Email_Match",
#             "Investment_Changed",
#             "Turnover_Changed",
#             "Match_Score",
#             "Latest_Origin_File",
#             "Older_Origin_File"
#         ]
#     ].head(20)
# )

# print("\n========== SCORE DISTRIBUTION ==========\n")

# print(
#     comparison_df["Match_Score"]
#     .value_counts()
#     .sort_index(ascending=False)
# )

# print("\n========================================\n")


# print(
#     comparison_df.loc[
#         comparison_df["Match_Score"] < 85,
#         [
#             "Enterprise_Match",
#             "Owner_Match",
#             "Mobile_Match",
#             "Email_Match",
#             "Match_Score"
#         ]
#     ]
#     .value_counts()
# )

# enterprise_mismatch_df = comparison_df[
#     (comparison_df["Enterprise_Match"] == False) &
#     (comparison_df["Owner_Match"] == True) &
#     (comparison_df["Mobile_Match"] == True) &
#     (comparison_df["Email_Match"] == True)
# ].copy()

# print(f"Enterprise mismatch pairs: {len(enterprise_mismatch_df)}")

# inspection_df = clean_df[
#     clean_df["Udyam Reg. No"].isin(
#         enterprise_mismatch_df["Udyam Reg. No"]
#     )
# ].copy()

# inspection_df = inspection_df.sort_values(
#     by=[
#         "Udyam Reg. No",
#         "Origin_File"
#     ]
# )

# print(
#     inspection_df[
#         [
#             "Udyam Reg. No",
#             "Enterprise Name",
#             "Owner Name",
#             "Mobile No.",
#             "Email Id",
#             "Origin_File"
#         ]
#     ].head(50)
# )

# inspection_df.to_excel(
#     "enterprise_name_mismatches.xlsx",
#     index=False
# )

# print(
#     "Enterprise mismatch file exported successfully."
# )


# mobile_mismatch_df = comparison_df[
#     (comparison_df["Enterprise_Match"] == True) &
#     (comparison_df["Owner_Match"] == True) &
#     (comparison_df["Mobile_Match"] == False) &
#     (comparison_df["Email_Match"] == True)
# ].copy()

# inspection_df = clean_df[
#     clean_df["Udyam Reg. No"].isin(
#         mobile_mismatch_df["Udyam Reg. No"]
#     )
# ]

# inspection_df.sort_values(
#     by=[
#         "Udyam Reg. No",
#         "Origin_File"
#     ]
# ).to_excel(
#     "mobile_mismatches.xlsx",
#     index=False
# )

# print("Mobile number mismatch file exported successfully.")


# email_mismatch_df = comparison_df[
#     (comparison_df["Enterprise_Match"] == True) &
#     (comparison_df["Owner_Match"] == True) &
#     (comparison_df["Mobile_Match"] == True) &
#     (comparison_df["Email_Match"] == False)
# ].copy()

# inspection_df = clean_df[
#     clean_df["Udyam Reg. No"].isin(
#         email_mismatch_df["Udyam Reg. No"]
#     )
# ]

# inspection_df.sort_values(
#     by=[
#         "Udyam Reg. No",
#         "Origin_File"
#     ]
# ).to_excel(
#     "email_mismatches.xlsx",
#     index=False
# )

# print("Email ID mismatch file exported successfully.")

# owner_mismatch_df = comparison_df[
#     comparison_df["Owner_Match"] == False
# ].copy()

# print(f"Owner mismatch pairs: {len(owner_mismatch_df)}")

# print(
#     owner_mismatch_df[
#         [
#             "Enterprise_Match",
#             "Owner_Match",
#             "Mobile_Match",
#             "Email_Match",
#             "Match_Score"
#         ]
#     ]
# )

# inspection_df = clean_df[
#     clean_df["Udyam Reg. No"].isin(
#         owner_mismatch_df["Udyam Reg. No"]
#     )
# ]

# inspection_df = inspection_df.sort_values(
#     by=[
#         "Udyam Reg. No",
#         "Origin_File"
#     ]
# )

# inspection_df.to_excel(
#     "owner_name_mismatches.xlsx",
#     index=False
# )

# print("Owner name mismatch file exported successfully.")

# print(comparison_df["Owner_Match"].value_counts())


# ============================================
# Inspect Low Confidence Duplicate Pairs
# ============================================

# low_score_df = comparison_df[
#     comparison_df["Match_Score"] <= 45
# ].copy()

# print(f"Low score pairs: {len(low_score_df)}")

# inspection_df = clean_df[
#     clean_df["Udyam Reg. No"].isin(
#         low_score_df["Udyam Reg. No"]
#     )
# ].copy()

# # Merge scoring information back into the original records
# inspection_df = inspection_df.merge(
#     low_score_df[
#         [
#             "Duplicate_Group_ID",
#             "Udyam Reg. No",
#             "Match_Score",
#             "Enterprise_Match",
#             "Owner_Match",
#             "Mobile_Match",
#             "Email_Match",
#             "Investment_Changed",
#             "Turnover_Changed"
#         ]
#     ],
#     on="Udyam Reg. No",
#     how="left"
# )

# inspection_df = inspection_df.sort_values(
#     by=[
#         "Duplicate_Group_ID",
#         "Origin_File"
#     ]
# )

# inspection_df.to_excel(
#     "low_score_duplicate_pairs.xlsx",
#     index=False
# )

# print("Low-score duplicate pairs exported successfully.")


comparison_df = apply_business_rules(
    comparison_df,
    config
)

master_df, duplicate_df, review_df = split_datasets(
    clean_df,
    comparison_df
)

master_df.to_excel(
    "master_deduplicated.xlsx",
    index=False
)

duplicate_df.to_excel(
    "duplicate_records.xlsx",
    index=False
)

review_df.to_excel(
    "low_score_review.xlsx",
    index=False
)

print("\nPipeline completed successfully.")
