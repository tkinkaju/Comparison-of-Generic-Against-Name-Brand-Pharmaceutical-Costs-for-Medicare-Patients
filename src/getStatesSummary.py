"""
getStatesSummary.py processes data from pharmaceutical sales of seven drugs in 50 US states for 2020. It reads seven CSV files
containing pharmaceutical data for each drug, extracts the relevant data for each state and drug, and calculates the total
days, total cost, and average cost per day for name brand and generic drugs separately. Then it calculates the percentage of
name brand drugs sold in each state and writes all the calculated data for each state, drug, and drug type (name brand or
generic) to a CSV file named states_summary.csv. Finally, the code creates a separate CSV file for each drug type containing
the same data as in states_summary.csv, but only for that specific drug type. These drug-type-specific CSV files are saved in
the "map source data/2020/statesSummaries" directory.

"""

import csv
import os

YEARS = ["2020","2019","2018","2017","2016","2015","2014","2013"]

DRUG_FILE_NAMES = [ 'Adalimumab.csv', 'Atorvastatin Calcium.csv', 'Donepezil Hcl.csv',
                    'Etanercept.csv', 'Sertraline Hcl.csv', 'Vortioxetine Hydrobromide.csv', 'Zolpidem Tartrate.csv']

BRAND_NAMES = [ 'Humira Pen', 'Lipitor', 'Aricept', 'Enbrel', 'Zoloft', 'Trintellix', 'Ambien' ]

GENERIC_NAMES = [ 'Adalimumab', 'Atorvastatin Calcium', 'Donepezil Hcl',
                  'Etanercept', 'Sertraline Hcl', 'Vortioxetine Hydrobromide', 'Zolpidem Tartrate' ]


STATES = [ 'AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA',
           'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD',
           'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ',
           'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC',
           'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY' ]

iteration = 0

jsonsDataFile= open("map source data\\jsons.csv")
jsonsDictionary = dict()
print("creating dictionary")
for line in jsonsDataFile:
    state = line.split(",")[0].replace("\"", "")
    line = line[3:].replace("\n","").strip("\"")
    jsonsDictionary[state] = line.replace("\"\"","\"")

for YEAR in YEARS:
    with open("states_summary.csv", "w", newline="") as output_file:
        writer = csv.writer(output_file)
        writer.writerow(['state', 'brnd_name', 'brnd_total_days', 'brnd_total_cost', 'brnd_avg_cost', 'gen_name', 'gen_total_day', 'gen_total_cost', 'gen_avg_cost', 'percent_brand', 'hypothetical_savings', 'geojson'])
            
        statesIter = 0
        for state in STATES:  #Will run 50 times
            # print(state)

            drugIter = 0
            for drug_file_name in DRUG_FILE_NAMES:   #Will run 7 times(one for each drug) for each state
                with open(f"map source data/{YEAR}/{drug_file_name}", "r") as file:
                    reader = csv.reader(file)
                    next(reader)

                    brnd_total_days, brnd_total_cost = 0, 0
                    gen_total_days, gen_total_cost = 0, 0

                    for row in enumerate(reader):
                        #Get avg cost per day for name brand 
                        if (row[1][0] == STATES[statesIter] and BRAND_NAMES[drugIter] in row[1][3]):
                            brnd_total_days += int(row[1][5])
                            brnd_total_cost += float(row[1][6])

                        #Get avg cost per day for generic
                        if (row[1][0] == STATES[statesIter] and GENERIC_NAMES[drugIter] in row[1][3]):
                            gen_total_days += int(row[1][5])
                            gen_total_cost += float(row[1][6])

                    #Getting percent_brand
                    if(brnd_total_days > 0 or gen_total_days > 0):
                        percent_brand = round((brnd_total_days / (brnd_total_days + gen_total_days) * 100), 6)
                    else:
                        percent_brand = 0

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

                    #Get hypothetical_savings
                    if brnd_avg_cost != 'N/A' and gen_avg_cost != 'N/A':
                        hypothetical_savings = round((brnd_avg_cost - gen_avg_cost) * brnd_total_days, 2)
                    else: 
                        hypothetical_savings = 'N/A'

                    #Add geocode
                    geojson = jsonsDictionary[STATES[statesIter]]

                    writer.writerow([STATES[statesIter], brnd_name, brnd_total_days, brnd_total_cost, brnd_avg_cost, gen_name, gen_total_days, gen_total_cost, gen_avg_cost, percent_brand, hypothetical_savings, geojson])
                    drugIter += 1
            statesIter += 1




    #Creating individual csv's for each drug type(As of now just for 2020)
    with open('states_summary.csv', newline='') as input_file:
        reader = csv.DictReader(input_file)
        drug_files = {}

        for row in reader:
            drug_type = row['gen_name']

            if drug_type not in drug_files:
                directory_path = os.path.abspath(os.path.join(os.getcwd(), "map source data", YEAR, "statesSummaries"))
                print(directory_path)
                if not os.path.exists(directory_path):
                    os.makedirs(directory_path)
                # drug_file = open(os.path.join(directory_path, drug_type + "_states_final.csv"), "w", newline='') 
                drug_file = open(os.path.join(directory_path, drug_type + ".js"), "w", newline='')
                drug_file.write("export default `")
                writer = csv.DictWriter(drug_file, fieldnames=reader.fieldnames)
                writer.writeheader()
                drug_files[drug_type] = (drug_file, writer)

            drug_file, writer = drug_files[drug_type]
            writer.writerow(row)

        for drug_file, writer in drug_files.values():
            drug_file.write("`;")
            drug_file.close()
