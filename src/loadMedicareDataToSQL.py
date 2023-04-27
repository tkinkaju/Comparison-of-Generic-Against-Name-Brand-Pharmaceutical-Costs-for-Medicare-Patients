"""
Uploads relvant parts of the the medicare dataset to a mysql database.
Requries the data to be named using the following convention:
./MedicareDataSet/Medicare_Part_D_Prescribers_by_Provider_and_Drug_<YEAR>.csv

Data used can be obtained from: 
https://data.cms.gov/provider-summary-by-type-of-service/medicare-part-d-prescribers/medicare-part-d-prescribers-by-provider-and-drug/data
You only need the columns: 'Prscrbr_NPI', 'Prscrbr_State_Abrvtn', 'Prscrbr_State_FIPS','Brnd_Name','Gnrc_Name','Tot_Day_Suply', 'Tot_Drug_Cst'

Replace the user, password, host and database parameters below to connect to your database
"""
import mysql.connector
import csv

YEARS = range(2013, 2021)
BASE_NAME = './MedicareDataSet/Medicare_Part_D_Prescribers_by_Provider_and_Drug_'

try:
    cnx = mysql.connector.connect(user='XXX', password='XXX', host='localhost', database='XXX')
    cursor = cnx.cursor()

    query = "CREATE TABLE IF NOT EXISTS filtered_medicare_data_set (npi char(10), state char(2), state_fips char(5), brand_name varchar(40), generic_name varchar(40), total_day_supply INT, total_drug_cost Float(24), year INT)"
    cursor.execute(query)

    query = "CREATE INDEX IF NOT EXISTS idx_medicare_state ON filtered_medicare_data_set (state);"
    cursor.execute(query)

    query = "CREATE INDEX  IF NOT EXISTS idx_medicare_year ON filtered_medicare_data_set (year);"
    cursor.execute(query)

    query = "CREATE INDEX  IF NOT EXISTS idx_medicare_npi ON filtered_medicare_data_set (npi);"
    cursor.execute(query)

    query = "CREATE INDEX  IF NOT EXISTS idx_medicare_generic_name ON filtered_medicare_data_set (generic_name);"
    cursor.execute(query)

    query = "CREATE INDEX  IF NOT EXISTS idx_medicare_brand_name ON filtered_medicare_data_set (brand_name);"
    cursor.execute(query)

    count = 0
    for year in YEARS:
        print(f'Year: {year}')
        with open(f'{BASE_NAME}{year}.csv', newline='') as data:
            reader = csv.DictReader(data)
            baseQuery  = "INSERT INTO filtered_medicare_data_set (npi, state, state_fips, brand_name, generic_name, total_day_supply, total_drug_cost, year) VALUES  (%s, %s, %s, %s, %s, %s, %s, %s) "
            for row in reader:
                count += 1
                if count % 10000 == 0:
                    print(f'{count}')
                cursor.execute(baseQuery, (row['Prscrbr_NPI'], row['Prscrbr_State_Abrvtn'], row['Prscrbr_State_FIPS'], row['Brnd_Name'],row['Gnrc_Name'], row['Tot_Day_Suply'], row['Tot_Drug_Cst'], year))
            
    print('Commiting')
    cnx.commit()
    print('Done')
    cursor.close()
    cnx.close()
except mysql.connector.Error as e:
    print(e)