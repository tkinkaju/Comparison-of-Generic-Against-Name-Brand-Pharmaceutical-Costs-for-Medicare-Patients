import csv
import os

YEARS = ["2020","2019","2018","2017","2016","2015","2014","2013"]

DRUG_FILE_NAMES = [ 'Adalimumab.csv', 'Atorvastatin Calcium.csv', 'Donepezil Hcl.csv',
                    'Etanercept.csv', 'Sertraline Hcl.csv', 'Vortioxetine Hydrobromide.csv', 'Zolpidem Tartrate.csv']

BRAND_NAMES = [ 'Humira Pen', 'Lipitor', 'Aricept', 'Enbrel', 'Zoloft', 'Trintellix', 'Ambien' ]

GENERIC_NAMES = [ 'Adalimumab', 'Atorvastatin Calcium', 'Donepezil Hcl',
                  'Etanercept', 'Sertraline Hcl', 'Vortioxetine Hydrobromide', 'Zolpidem Tartrate' ]

'''
STATES = [ 'AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA',
           'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD',
           'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ',
           'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC',
           'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY' ]
           '''


ZIP_CODE_MAP = {}

print('reading zipcodes into memory...')
zipCount = 0
with open('./src/zipCodeProcessing/US_ZIP_codes_to_longitude_and_latitude.csv', 'r') as zipCodeFile:
    reader = csv.DictReader(zipCodeFile)
    next(reader)

    for row in reader:
        code = str(row['Zip']).rjust(5, '0')

        ZIP_CODE_MAP[code] = {'lat':row['Latitude'], 'lon':row['Longitude']}
        zipCount += 1

print(f'{zipCount} zip codes loaded')

class ZipCodeSummary():

    def __init__(self, code):
        self.code = code
        self.drugs = []

    def hasBrand(self, brand):
        for drug in self.drugs:
            if drug.brandName == brand:
                return True
        return False
    
    def getSummary(self, brandName):
        for drug in self.drugs:
            if drug.brandName == brandName:
                return drug
        return None

class DrugSummary():
    def __init__(self, brandName, genericName):
        self.brandName = brandName
        self.genericName = genericName
        self.brandTotalDays = 0
        self.brandTotalCost = 0
        self.genericTotalDays = 0
        self.genericTotalCost = 0

    def genericAvgCost(self):
        return  round(self.genericTotalCost / self.genericTotalDays, 2) if self.genericTotalDays != 0 else 'N/A'
    
    def brandAvgCost(self):
        return  round(self.brandTotalCost / self.brandTotalDays, 2) if self.brandTotalDays != 0 else 'N/A'
    
    def percentBrand(self):
        return  round(self.brandTotalDays / (self.brandTotalDays + self.genericTotalDays) * 100.0, 6) if (self.brandTotalDays + self.genericTotalDays) > 0 else 'N/A'

for YEAR in YEARS:
    zipCodeData = {}

    csv_file_path = './src/zipCodeProcessing/US_ZIP_codes_to_longitude_and_latitude.csv'


    with open("zipcode_summary.csv", "w", newline="") as output_file:
        writer_ = csv.writer(output_file)
        writer_.writerow(['zipcode', 'brnd_name', 'brnd_total_days', 'brnd_total_cost', 'brnd_avg_cost', 'gen_name', 'gen_total_day', 'gen_total_cost', 'gen_avg_cost', 'percent_brand','lat', 'lon'])

        drugIter = 0
        for drug_file_name in DRUG_FILE_NAMES:   # run through each drug file
            with open(f"map source data/{YEAR}/{drug_file_name}", "r") as file:
                reader = csv.reader(file)
                col = next(reader)

                brandName = BRAND_NAMES[drugIter]
                genericName = GENERIC_NAMES[drugIter]
                daySup = col.index('totl_day_sply')
                dayCst = col.index('totl_drg_cost')
                brdName = col.index('brnd_name')
                zipCol = col.index('zip_code')
                for row in reader:
                    code = row[zipCol]
                    if not code in zipCodeData:
                        zipCodeData[code] = ZipCodeSummary(code)
                    zipData = zipCodeData[code]
                    if not zipData.hasBrand(brandName):
                        zipData.drugs += [DrugSummary(brandName, genericName)]

                    drugSummary = zipData.getSummary(brandName)

                    if brandName in row[brdName]:
                        drugSummary.brandTotalDays += int(row[daySup])
                        drugSummary.brandTotalCost += float(row[dayCst])
                    
                    if genericName in row[brdName]:
                        drugSummary.genericTotalDays += int(row[daySup])
                        drugSummary.genericTotalCost += float(row[dayCst])

                drugIter += 1
        
        for zipData in zipCodeData.values():
            lat = ZIP_CODE_MAP[zipData.code]['lat'] if zipData.code in ZIP_CODE_MAP else 'N/A'
            lon = ZIP_CODE_MAP[zipData.code]['lon'] if zipData.code in ZIP_CODE_MAP else 'N/A'
            for summary in zipData.drugs:
                writer_.writerow([zipData.code, summary.brandName, summary.brandTotalDays, round(summary.brandTotalCost, 2),
                                    summary.brandAvgCost(), summary.genericName, summary.genericTotalDays, 
                                    round(summary.genericTotalCost, 2), summary.genericAvgCost(), summary.percentBrand(), lat, lon])



    #Creating individual csv's for each drug type(As of now just for 2020)
    with open('zipcode_summary.csv', newline='') as input_file:
        reader = csv.DictReader(input_file)
        drug_files = {}

        directory_path = './map source data/'+YEAR+'/zipcodeSummaries'
        if not os.path.exists(directory_path):
            os.makedirs(directory_path)

        for row in reader:
            drug_type = row['gen_name']

            if drug_type not in drug_files:
                # drug_file = open(os.path.join(directory_path, drug_type + "_zipcodes_final.csv"), "w", newline='')
                drug_file = open(os.path.join(directory_path, drug_type + ".js"), "w", newline='')#comment out if you want a csv
                writer_ = csv.DictWriter(drug_file,fieldnames=reader.fieldnames)
                drug_file.write("export default `")#comment out if you want a csv
                writer_.writeheader()
                drug_files[drug_type] = (drug_file, writer_)

            drug_file, writer = drug_files[drug_type]
            writer.writerow(row)

        for drug_file, writer in drug_files.values():
            drug_file.write("`;")#comment out if you want a csv
            drug_file.close()