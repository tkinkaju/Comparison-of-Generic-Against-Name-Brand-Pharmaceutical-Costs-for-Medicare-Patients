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

ZIP_CODES = []

csv_file_path = os.path.join(os.getcwd(), "Comparison-of-Generic-Against-Name-Brand-Pharmaceutical-Costs-for-Medicare-Patients", 'src', 'zipCodeProcessing', 'US_ZIP_codes_to_longitude_and_latitude.csv')

#Comparison-of-Generic-Against-Name-Brand-Pharmaceutical-Costs-for-Medicare-Patients\src\zipCodeProcessing\US_ZIP_codes_to_longitude_and_latitude.csv

with open(csv_file_path, newline='') as zipcsvfile:
    reader = csv.DictReader(zipcsvfile)
    #zip_codes = []
    for row in reader:
        ZIP_CODES.append(row['Zip'])


with open("zipcode_summary.csv", "w", newline="") as output_file:
    writer = csv.writer(output_file)
    writer.writerow(['zipcode', 'brnd_name', 'brnd_total_days', 'brnd_total_cost', 'brnd_avg_cost', 'gen_name', 'gen_total_day', 'gen_total_cost', 'gen_avg_cost'])
        
    zipsIter = 0
    for zip in ZIP_CODES:  #Will run many times
        print(zip)

        drugIter = 0
        for drug_file_name in DRUG_FILE_NAMES:   #Will run 7 times(one for each drug) for each zipcode
            with open(f"map source data/2020/{drug_file_name}", "r") as file:
                reader = csv.reader(file)
                next(reader)

                brnd_total_days, brnd_total_cost = 0, 0
                gen_total_days, gen_total_cost = 0, 0

                for row in enumerate(reader):

                    #Get avg cost per day for name brand 
                    if (row[1][0] == ZIP_CODES[zipsIter] and BRAND_NAMES[drugIter] in row[1][3]):
                        # print(row[1][3])
                        brnd_total_days += float(row[1][5])
                        brnd_total_cost += float(row[1][6])

                    #Get avg cost per day for generic
                    if (row[1][0] == ZIP_CODES[zipsIter] and GENERIC_NAMES[drugIter] in row[1][3]):
                        gen_total_days += float(row[1][5])
                        gen_total_cost += float(row[1][6])


                brnd_name = BRAND_NAMES[drugIter]
                brnd_total_days = round(brnd_total_days, 2)
                brnd_total_cost = round(brnd_total_cost, 2)
                if brnd_total_days != 0:
                    brnd_avg_cost = round(brnd_total_cost/brnd_total_days, 2)
                else:
                    brnd_avg_cost = "N/A"

                gen_name = GENERIC_NAMES[drugIter]
                gen_total_days = round(gen_total_days, 2)
                gen_total_cost = round(gen_total_cost, 2)
                if gen_total_days != 0:
                    gen_avg_cost = round(gen_total_cost/gen_total_days, 2)
                else: 
                    gen_avg_cost = "N/A"

                writer.writerow([ZIP_CODES[zipsIter], brnd_name, brnd_total_days, brnd_total_cost, brnd_avg_cost, gen_name, gen_total_days, gen_total_cost, gen_avg_cost])
                drugIter += 1
        zipsIter += 1



#Creating individual csv's for each drug type(As of now just for 2020)
YEAR = "2020"
with open('zipcode_summary.csv', newline='') as input_file:
    reader = csv.DictReader(input_file)
    drug_files = {}

    for row in reader:
        drug_type = row['gen_name']

        if drug_type not in drug_files:
            directory_path = os.path.abspath(os.path.join(os.getcwd(), "..", "Comparison-of-Generic-Against-Name-Brand-Pharmaceutical-Costs-for-Medicare-Patients", "map source data", "2020", "zipcodeSummaries"))
            print(directory_path)
            if not os.path.exists(directory_path):
                os.makedirs(directory_path)

            drug_file = open(os.path.join(directory_path, drug_type + "_zipcodes_final.csv"), "w")
            writer = csv.DictWriter(drug_file, fieldnames=reader.fieldnames)
            writer.writeheader()
            drug_files[drug_type] = (drug_file, writer)

        drug_file, writer = drug_files[drug_type]
        writer.writerow(row)

    for drug_file, writer in drug_files.values():
        drug_file.close()