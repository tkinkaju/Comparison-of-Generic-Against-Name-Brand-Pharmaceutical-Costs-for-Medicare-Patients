"""
Uploads relevant information about zip codes to the database.
Replace the user, password, host and database parameters in the dbConfig.json file to connect to your database
"""
import mysql.connector
import json
import os.path as path
import csv

dbConfig = {}

if not path.isfile('./src/dbConfig.json'):
    print("Please copy the example dbConfig to ./src/dbConfig.json and put in your database settings")
    exit(1)
else:
    dbConfig = json.load(open('./src/dbConfig.json'))
    if not ('user' in dbConfig and 'password' in dbConfig and 'host' in dbConfig and 'database' in dbConfig):
        print("Your configuration is missing some files, please see the example config file")
        exit(1)

try:
    cnx = mysql.connector.connect(user=dbConfig['user'], password=dbConfig['password'], host=dbConfig['host'], database=dbConfig['database'])
    cursor = cnx.cursor()

    query = "DROP TABLE IF EXISTS zip_code_map"
    cursor.execute(query)

    query = "CREATE TABLE IF NOT EXISTS zip_code_map (zip char(5) PRIMARY KEY, latitude Float(24), longitude Float(24))"
    cursor.execute(query)

    baseQuery  = "INSERT INTO zip_code_map (zip, latitude, longitude) VALUES  (%s, %s, %s) "


    with open('./src/zipCodeProcessing/US_ZIP_codes_to_longitude_and_latitude.csv', 'r') as zipCodeFile:
        reader = csv.DictReader(zipCodeFile)
        next(reader)

        for row in reader:
            code = str(row['Zip']).rjust(5, '0')
            cursor.execute(baseQuery, (code, row['Latitude'], row['Longitude']))

        print(f'Done')   

    print("Commiting changes...")  
    cnx.commit()
    cursor.close()
    cnx.close()
except mysql.connector.Error as e:
    print('sql error: ')
    print(e)