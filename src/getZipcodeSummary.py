import csv
import os

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

zipCodeData = {}

csv_file_path = './src/zipCodeProcessing/US_ZIP_codes_to_longitude_and_latitude.csv'


with open("zipcode_summary.csv", "w", newline="") as output_file:
    writer_ = csv.writer(output_file)
    writer_.writerow(['zipcode', 'brnd_name', 'brnd_total_days', 'brnd_total_cost', 'brnd_avg_cost', 'gen_name', 'gen_total_day', 'gen_total_cost', 'gen_avg_cost'])

    drugIter = 0
    for drug_file_name in DRUG_FILE_NAMES:   # run through each drug file
        with open(f"map source data/2020/{drug_file_name}", "r") as file:
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
                    drugSummary.brandTotalDays += float(row[daySup])
                    drugSummary.brandTotalCost += float(row[dayCst])
                
                if genericName in row[brdName]:
                    drugSummary.genericTotalDays += float(row[daySup])
                    drugSummary.genericTotalCost += float(row[dayCst])

            drugIter += 1
    
    for zipData in zipCodeData.values():
        for summary in zipData.drugs:
            writer_.writerow([zipData.code, summary.brandName, summary.brandTotalDays, round(summary.brandTotalCost, 2),
                                summary.brandAvgCost(), summary.genericName, summary.genericTotalDays, 
                                round(summary.genericTotalCost, 2), summary.genericAvgCost()])



#Creating individual csv's for each drug type(As of now just for 2020)
YEAR = "2020"
with open('zipcode_summary.csv', newline='') as input_file:
    reader = csv.DictReader(input_file)
    drug_files = {}

    directory_path = './map source data/2020/zipcodeSummaries'
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)

    for row in reader:
        drug_type = row['gen_name']

        if drug_type not in drug_files:
            drug_file = open(os.path.join(directory_path, drug_type + "_zipcodes_final.csv"), "w", newline='')
            writer_ = csv.DictWriter(drug_file,fieldnames=reader.fieldnames)
            writer_.writeheader()
            drug_files[drug_type] = (drug_file, writer_)

        drug_file, writer = drug_files[drug_type]
        writer.writerow(row)

    for drug_file, writer in drug_files.values():
        drug_file.close()