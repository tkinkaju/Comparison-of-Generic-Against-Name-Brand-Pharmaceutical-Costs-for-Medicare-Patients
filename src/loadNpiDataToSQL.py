"""
Uploads relvant parts of the the NPI dataset to a mysql database.
Expects file in the following location:
./NpiDataSet/NPPES_Data_Dissemination_April_2023/npidata_pfile_20050523-20230409.csv
Please rename the file used in the code accordingly

Data used can be obtained from: 
https://download.cms.gov/nppes/NPI_Files.html

Down load the 'Full Replacement Monthly NPI File'

Replace the user, password, host and database parameters below to connect to your database
"""
import mysql.connector
import csv

def isCorrectNPIType(row):
    desiredCodeStarts = ['20', '17', '36', '39', '10', '16']
    def isDesiredType(code):
        return code[:2] in desiredCodeStarts

    taxomyCode1 = row['Healthcare Provider Taxonomy Code_1']
    taxomyCode2 = row['Healthcare Provider Taxonomy Code_2']
    taxomyCode3 = row['Healthcare Provider Taxonomy Code_3']
    countryCode = row['Provider Business Mailing Address Country Code (If outside U.S.)']

    return (isDesiredType(taxomyCode1) or isDesiredType(taxomyCode2) or isDesiredType(taxomyCode3)) and countryCode == 'US'

try:
    cnx = mysql.connector.connect(user='XXX', password='XXX', host='localhost', database='XXX')
    cursor = cnx.cursor()

    query = "DROP TABLE IF EXISTS practice_NPI_location"
    cursor.execute(query)

    query = "CREATE TABLE IF NOT EXISTS practice_NPI_location (npi char(10) PRIMARY KEY, zip_code char(5), state char(2))"
    cursor.execute(query)

    baseQuery  = "INSERT INTO practice_NPI_location (npi, state, zip_code) VALUES  (%s, %s, %s) "

    with open("./NpiDataSet/NPPES_Data_Dissemination_April_2023/npidata_pfile_20050523-20230409.csv") as input_file:
        reader = csv.DictReader(input_file)
        for line in reader:
            if isCorrectNPIType(line):
                state = line['Provider Business Mailing Address State Name']
                zipCode = line['Provider Business Mailing Address Postal Code']
                if(len(state) == 2):
                    print(line['NPI'])
                    cursor.execute(baseQuery, (line['NPI'], state, zipCode[:5]))

    print("Commiting changes...")  
    cnx.commit()
    cursor.close()
    cnx.close()
except mysql.connector.Error as e:
    print('sql error: ')
    print(e)