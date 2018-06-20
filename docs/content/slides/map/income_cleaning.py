# income_cleaning.py
# https://factfinder.census.gov/faces/tableservices/jsf/pages/productview.xhtml?pid=ACS_16_5YR_B19001B&prodType=table
import pandas as pd
import os
import zipfile
import re


def _purge(dir, pattern):
    """
    Remove files from dir. From: https://stackoverflow.com/questions/1548704/delete-multiple-files-matching-a-pattern
    """
    for f in os.listdir(dir):
        if re.search(pattern, f):
            os.remove(os.path.join(dir, f))


def clean_mean_income_zip_files(race):
                                                                # Conditions when we need to run:
                                                                # processedZips dir doesn't exist.
                                                                # processedZips has not been cleaned and it contains too many files.
                                                                # processedZips
                                                                # is empty
    if not os.path.exists("processedZips/" + race) or len(os.listdir('processedZips/' + race)) == 1 or len(os.listdir('processedZips/' + race)) > len(os.listdir('rawIncomeDatazips/' + race)):
        onlyfiles = [f for f in os.listdir(
            'rawIncomeDatazips/' + race) if os.path.isfile(os.path.join('rawIncomeDatazips/' + race, f))]
        print(onlyfiles)
        # onlyfiles.remove('.DS_Store')
        for file in onlyfiles:
            print(file)

            zip_ref = zipfile.ZipFile(
                'rawIncomeDatazips/' + race + "/" + file, 'r')
            if not os.path.exists("processedZips/" + race):
                os.makedirs("processedZips/" + race)
            zip_ref.extractall("processedZips/" + race)
            zip_ref.close()

        _purge("processedZips/" + race, "txt")
        _purge("processedZips/" + race, "metadata")
        _purge("processedZips/" + race, ".DS")  # Remove DS Store
        print(os.listdir("processedZips/" + race))
    else:
        print("Zip cleaning already completed.")

clean_mean_income_zip_files('black')


def clean_annual_mean_income_files(file, race, year, export=True):
    full_df = pd.read_csv(file, encoding='latin-1', header=1)
    print("-" * 10)
    full_df = full_df.dropna(axis=0, subset=['Id2'])
    full_df['Id2'] = full_df['Id2'].astype(int)

    full_df['id'] = full_df['Id2'].apply(str).str.zfill(5)
    print(full_df.columns)
    full_df['median_income'] = full_df[
        'Estimate; Median household income in the past 12 months (in 2010 inflation-adjusted dollars)']
    cols = ['id', 'median_income']
    keep = full_df[cols]
    keep['year'] = year
    if not os.path.exists("median_income/" + race):
        os.makedirs("median_income/" + race)
    if export:
        keep.to_csv('median_income/{}/{}20{}map.csv'.format(race, race, year))
    return keep

race = 'black'
for file in os.listdir('processedZips/' + race):
    year = file[4:6]
    clean_annual_mean_income_files(
        'processedZips/' + race + '/' + file, race, year)
# filter to just files with data


# # year = '16'
# race = 'white'
# # ACS_11_5YR_B19001H_with_ann


# def make_year(filepath_ending, year, race, export=True):
#     # filename = 'rawMapData/ACS_' + year + '_5YR_B19001B_with_ann.csv'
#     filename = 'rawMapData/{}/ACS_'.format(race) + year + filepath_ending

#     df = pd.read_csv(filename, encoding='latin-1', header=1)
#     df['percent_poor'] = (df['Estimate; Total: - Less than $10,000']
#                           + df['Estimate; Total: - $10,000 to $14,999']
#                           + df['Estimate; Total: - $15,000 to $19,999']
#                           + df["Estimate; Total: - $20,000 to $24,999"]) / df['Estimate; Total:']

#     df['County'] = df['Geography'].str.split(",", expand=True)[0]
#     df['State'] = df['Geography'].str.split(",", expand=True)[1]
#     # df['Id2'] = pd.to_numeric(df['Id2'])
#     df = df.dropna(axis=0, subset=['Id2'])
#     df['Id2'] = df['Id2'].astype(int)
#     # print(df['Id2'].astype(int))
#     df['id'] = df['Id2'].apply(str).str.zfill(5)
#     print(df['id'])
#     # print(df.info())

#     cols = ['id', 'County', 'State', 'percent_poor', "Estimate; Total:", "Estimate; Total: - Less than $10,000", "Estimate; Total: - $10,000 to $14,999", "Estimate; Total: - $15,000 to $19,999", "Estimate; Total: - $20,000 to $24,999", "Estimate; Total: - $25,000 to $29,999", "Estimate; Total: - $30,000 to $34,999", "Estimate; Total: - $35,000 to $39,999",
#             "Estimate; Total: - $40,000 to $44,999", "Estimate; Total: - $45,000 to $49,999", "Estimate; Total: - $50,000 to $59,999", "Estimate; Total: - $60,000 to $74,999", "Estimate; Total: - $75,000 to $99,999", "Estimate; Total: - $100,000 to $124,999", "Estimate; Total: - $125,000 to $149,999", "Estimate; Total: - $150,000 to $199,999", "Estimate; Total: - $200,000 or more"]
#     keep = df[cols]
#     keep['year'] = year
#     if export:
#         keep.to_csv('MapData/{}/{}20{}map.csv'.format(race, race, year))
#     return keep

# years = ['10', '11', '12', '13', '14', '15', '16']

# # final = pd.DataFrame()
# # for year in years:
# # x = make_year('_5YR_B19001H_with_ann.csv', year, 'white', export=True)
# # x = make_year('_5YR_B19001H_with_ann.csv', year, 'white', export=True)

# #     final = pd.concat([final, x])

# # print(final.tail())

# # print(keep['id'])
# # final.to_csv('MapData/{}map.csv'.format(race, year))


# #

# # all

# def clean_all_race(year, export):
#     filename = 'rawMapData/all/ACS_' + year + '_5YR_S1901_with_ann.csv'
#     df = pd.read_csv(filename, encoding='latin-1', header=1)
#     print(df.columns)
#     df['percent_poor'] = (df['Households; Estimate; Less than $10,000']
#                           + df['Households; Estimate; $10,000 to $14,999']
#                           + df['Households; Estimate; $15,000 to $24,999']) / 100

#     df['County'] = df['Geography'].str.split(",", expand=True)[0]
#     df['State'] = df['Geography'].str.split(",", expand=True)[1]
#     # df['Id2'] = pd.to_numeric(df['Id2'])
#     df = df.dropna(axis=0, subset=['Id2'])
#     df['Id2'] = df['Id2'].astype(int)
#     # print(df['Id2'].astype(int))
#     df['id'] = df['Id2'].apply(str).str.zfill(5)
#     print(df['id'])
#     # print(df.info())

#     cols = ['id', 'County', 'State', 'percent_poor', "Households; Estimate; Total",
#             "Households; Estimate; Less than $10,000",
#             "Households; Estimate; $10,000 to $14,999",
#             "Households; Estimate; $15,000 to $24,999",
#             "Households; Estimate; $25,000 to $34,999",
#             "Households; Estimate; $35,000 to $49,999",
#             "Households; Estimate; $50,000 to $74,999",
#             "Households; Estimate; $75,000 to $99,999",
#             "Households; Estimate; $100,000 to $149,999",
#             "Households; Estimate; $150,000 to $199,999",
#             "Households; Estimate; $200,000 or more"]

#     sub = ["Households; Estimate; Less than $10,000",  # 0
#            "Households; Estimate; $10,000 to $14,999",
#            "Households; Estimate; $15,000 to $24,999",

#            "Households; Estimate; $25,000 to $34,999",  # 4

#            "Households; Estimate; $35,000 to $49,999",  # 5

#            "Households; Estimate; $50,000 to $74,999",  # 6

#            "Households; Estimate; $75,000 to $99,999",  # 7

#            "Households; Estimate; $100,000 to $149,999",  # 8
#            "Households; Estimate; $150,000 to $199,999",
#            "Households; Estimate; $200,000 or more"]

#     subset = df[sub]
#     print(subset.sum(axis=1))
#     keep = df[cols]
#     keep['year'] = year
#     if export:
#         keep.to_csv('MapData/all/all20{}map.csv'.format(year))
#     return keep

# for year in years:
#     x = clean_all_race(year, export=True)
