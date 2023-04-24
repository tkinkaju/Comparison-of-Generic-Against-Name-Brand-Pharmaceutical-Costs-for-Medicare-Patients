"""
getUSASummary.py reads data from multiple CSV files containing information about different drugs and calculates various metrics
related to brand-name and generic versions of these drugs, including total days prescribed, total cost, average cost per day, and
percentage of prescriptions for brand-name vs generic drugs. The calculated metrics are then written to a new CSV file called
"USA_summary.csv". Then the code creates individual CSV files for each drug type (based on their generic name) and stores these in
a new directory called "usaSummaries". Overall, the code aims to read in a large csv for each drug type, analyze the data, make
calculations based off the data, and then create new csv's that contain only the relevant information to each drug type.

"""

import csv
import os

DRUG_FILE_NAMES = [ 'Adalimumab.csv', 'Atorvastatin Calcium.csv', 'Donepezil Hcl.csv',
                    'Etanercept.csv', 'Sertraline Hcl.csv', 'Vortioxetine Hydrobromide.csv', 'Zolpidem Tartrate.csv']

BRAND_NAMES = [ 'Humira Pen', 'Lipitor', 'Aricept', 'Enbrel', 'Zoloft', 'Trintellix', 'Ambien' ]

GENERIC_NAMES = [ 'Adalimumab', 'Atorvastatin Calcium', 'Donepezil Hcl',
                  'Etanercept', 'Sertraline Hcl', 'Vortioxetine Hydrobromide', 'Zolpidem Tartrate' ]

iteration = 0

with open("USA_summary.csv", "w", newline="") as output_file:
    writer = csv.writer(output_file)
    writer.writerow(['brnd_name', 'brnd_total_days', 'brnd_total_cost', 'brnd_avg_cost', 'gen_name', 'gen_total_day', 'gen_total_cost', 'gen_avg_cost', 'percent_brand'])
    for drug_file_name in DRUG_FILE_NAMES:
        # print( "Brand Name: " + str(BRAND_NAMES[iteration]) + "      Generic: " + str(GENERIC_NAMES[iteration]))
        
        with open(f"map source data/2020/{drug_file_name}", "r") as file:
            reader = csv.reader(file)
            next(reader)
            
            brnd_total_days, brnd_total_cost = 0, 0
            gen_total_days, gen_total_cost = 0, 0

            for row in enumerate(reader):
                #Get avg cost per day for name brand 
                if BRAND_NAMES[iteration] in row[1][3]:
                    brnd_total_days += int(row[1][5])
                    brnd_total_cost += float(row[1][6])

                #Get avg cost per day for generic
                if GENERIC_NAMES[iteration] in row[1][3]:
                    gen_total_days += int(row[1][5])
                    gen_total_cost += float(row[1][6])

            brnd_name = BRAND_NAMES[iteration]
            brnd_total_days = round(brnd_total_days, 2)
            brnd_total_cost = round(brnd_total_cost, 2)

            #Getting percent_brand
            percent_brand = round(brnd_total_days / (brnd_total_days + gen_total_days), 6)

            if brnd_total_days != 0:
                brnd_avg_cost = round(brnd_total_cost/brnd_total_days, 2)
            else:
                brnd_avg_cost = "N/A"

            gen_name = GENERIC_NAMES[iteration]
            gen_total_days = round(gen_total_days, 2)
            gen_total_cost = round(gen_total_cost, 2)

            if gen_total_days != 0:
                gen_avg_cost = round(gen_total_cost/gen_total_days, 2)
            else: 
                gen_avg_cost = "N/A"

            writer.writerow([brnd_name, brnd_total_days, brnd_total_cost, brnd_avg_cost, gen_name, gen_total_days, gen_total_cost, gen_avg_cost, percent_brand])
            iteration += 1




#Creating individual csv's for each drug type(As of now just for 2020)
YEAR = "2020"
with open('USA_summary.csv', newline='') as input_file:
    reader = csv.DictReader(input_file)
    drug_files = {}

    for row in reader:
        drug_type = row['gen_name']

        if drug_type not in drug_files:
            directory_path = os.path.abspath(os.path.join(os.getcwd(), "..", "Comparison-of-Generic-Against-Name-Brand-Pharmaceutical-Costs-for-Medicare-Patients", "map source data", "2020", "usaSummaries"))
            print(directory_path)
            if not os.path.exists(directory_path):
                os.makedirs(directory_path)

            drug_file = open(os.path.join(directory_path, drug_type + "_usa_final.csv"), "w")
            writer = csv.DictWriter(drug_file, fieldnames=reader.fieldnames)
            writer.writeheader()
            drug_files[drug_type] = (drug_file, writer)

        drug_file, writer = drug_files[drug_type]
        writer.writerow(row)

    for drug_file, writer in drug_files.values():
        drug_file.close()