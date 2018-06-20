# censuscleaning.py
# https://factfinder.census.gov/faces/tableservices/jsf/pages/productview.xhtml?pid=ACS_16_5YR_B19001B&prodType=table
import pandas as pd
# year = '16'
race = 'white'
# ACS_11_5YR_B19001H_with_ann


def make_year(filepath_ending, year, race, export=True):
  '''
  Races to choose:
  - 'black'
  - 'white'
  - 'all'

  Filepath endings:
  White:
  - ACS_10_5YR_B19001H_with_ann.csv
  Black:
  - ACS_09_5YR_B19001B_with_ann.csv
  All:
  - ACS_10_5YR_S1901_with_ann.csv
  '''
  # filename = 'rawMapData/ACS_' + year + '_5YR_B19001B_with_ann.csv'
  filename = 'rawMapData/{}/ACS_'.format(race) + year + filepath_ending

  df = pd.read_csv(filename, encoding='latin-1', header=1)
  df['percent_poor'] = (df['Estimate; Total: - Less than $10,000']
                        + df['Estimate; Total: - $10,000 to $14,999']
                        + df['Estimate; Total: - $15,000 to $19,999']
                        + df["Estimate; Total: - $20,000 to $24,999"]) / df['Estimate; Total:']

  df['County'] = df['Geography'].str.split(",", expand=True)[0]
  df['State'] = df['Geography'].str.split(",", expand=True)[1]
  # df['Id2'] = pd.to_numeric(df['Id2'])
  df = df.dropna(axis=0, subset=['Id2'])
  df['Id2'] = df['Id2'].astype(int)
  # print(df['Id2'].astype(int))
  df['id'] = df['Id2'].apply(str).str.zfill(5)
  print(df['id'])
  # print(df.info())

  cols = ['id', 'County', 'State', 'percent_poor', "Estimate; Total:", "Estimate; Total: - Less than $10,000", "Estimate; Total: - $10,000 to $14,999", "Estimate; Total: - $15,000 to $19,999", "Estimate; Total: - $20,000 to $24,999", "Estimate; Total: - $25,000 to $29,999", "Estimate; Total: - $30,000 to $34,999", "Estimate; Total: - $35,000 to $39,999",
          "Estimate; Total: - $40,000 to $44,999", "Estimate; Total: - $45,000 to $49,999", "Estimate; Total: - $50,000 to $59,999", "Estimate; Total: - $60,000 to $74,999", "Estimate; Total: - $75,000 to $99,999", "Estimate; Total: - $100,000 to $124,999", "Estimate; Total: - $125,000 to $149,999", "Estimate; Total: - $150,000 to $199,999", "Estimate; Total: - $200,000 or more"]
  keep = df[cols]
  keep['year'] = year
  if export:
      keep.to_csv('MapData/{}/{}20{}map.csv'.format(race, race, year))
  return keep

years = ['10', '11', '12', '13', '14', '15', '16']

final = pd.DataFrame()
for year in years:
# x = make_year('_5YR_B19001H_with_ann.csv', year, 'white', export=True)
  x = make_year('_5YR_B19001H_with_ann.csv', year, 'all', export=True)
  final = pd.concat([final, x])

print(final.tail())

# print(keep['id'])
# final.to_csv('MapData/{}map.csv'.format(race, year))




def clean_all_race(year, export):
    filename = 'rawMapData/all/ACS_' + year + '_5YR_S1901_with_ann.csv'
    df = pd.read_csv(filename, encoding='latin-1', header=1)
    print(df.columns)
    df['percent_poor'] = (df['Households; Estimate; Less than $10,000']
                          + df['Households; Estimate; $10,000 to $14,999']
                          + df['Households; Estimate; $15,000 to $24,999']) / 100

    df['County'] = df['Geography'].str.split(",", expand=True)[0]
    df['State'] = df['Geography'].str.split(",", expand=True)[1]
    # df['Id2'] = pd.to_numeric(df['Id2'])
    df = df.dropna(axis=0, subset=['Id2'])
    df['Id2'] = df['Id2'].astype(int)
    # print(df['Id2'].astype(int))
    df['id'] = df['Id2'].apply(str).str.zfill(5)
    print(df['id'])
    # print(df.info())

    cols = ['id', 'County', 'State', 'percent_poor', "Households; Estimate; Total",
            "Households; Estimate; Less than $10,000",
            "Households; Estimate; $10,000 to $14,999",
            "Households; Estimate; $15,000 to $24,999",
            "Households; Estimate; $25,000 to $34,999",
            "Households; Estimate; $35,000 to $49,999",
            "Households; Estimate; $50,000 to $74,999",
            "Households; Estimate; $75,000 to $99,999",
            "Households; Estimate; $100,000 to $149,999",
            "Households; Estimate; $150,000 to $199,999",
            "Households; Estimate; $200,000 or more"]

    sub = ["Households; Estimate; Less than $10,000",  # 0
           "Households; Estimate; $10,000 to $14,999",
           "Households; Estimate; $15,000 to $24,999",

           "Households; Estimate; $25,000 to $34,999",  # 4

           "Households; Estimate; $35,000 to $49,999",  # 5

           "Households; Estimate; $50,000 to $74,999",  # 6

           "Households; Estimate; $75,000 to $99,999",  # 7

           "Households; Estimate; $100,000 to $149,999",  # 8
           "Households; Estimate; $150,000 to $199,999",
           "Households; Estimate; $200,000 or more"]

    subset = df[sub]
    print(subset.sum(axis=1))
    keep = df[cols]
    keep['year'] = year
    if export:
        keep.to_csv('MapData/all/all20{}map.csv'.format(year))
    return keep

# for year in years:
#     x = clean_all_race(year, export=True)
