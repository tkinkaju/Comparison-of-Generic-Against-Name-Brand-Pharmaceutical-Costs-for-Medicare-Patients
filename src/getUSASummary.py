import csv

DRUG_FILE_NAMES = [ 'Adalimumab.csv', 'Atorvastatin Calcium.csv', 'Dextroamphetamine-Amphetamine.csv', 'Donepezil Hcl.csv',
                    'Etanercept.csv', 'Sertraline Hcl.csv', 'Vortioxetine Hydrobromide.csv', 'Zolpidem Tartrate.csv']

BRAND_NAMES = [ 'Humira', 'Lipitor', 'Adderall', 'Aricept', 'Enbrel', 'Zoloft', 'Trintellix', 'Ambien' ]
#FOR HUMIRA--> contains others such as --> 'Humira Pen', 'Humira(Cf) Pen'
#But maybe I could do .contains('Humira')?

GENERIC_NAMES = [ 'Adalimumab', 'Atorvastatin Calcium', 'Dextroamphetamine/Amphetamine', 'Donepezil Hcl',
                  'Etanercept', 'Sertraline Hcl', 'Vortioxetine Hydrobromide', 'Zolpidem Tartrate' ]

iteration = 0


with open("USA_summary.csv", "w", newline="") as output_file:
    writer = csv.writer(output_file)
    writer.writerow(['brnd_name', 'brnd_total_days', 'brnd_total_cost', 'brnd_avg_cost', 'gen_name', 'gen_total_day', 'gen_total_cost', 'gen_avg_cost'])

    for drug_file_name in DRUG_FILE_NAMES:

        print( "Brand Name: " + str(BRAND_NAMES[iteration]) + "       Generic: " + str(GENERIC_NAMES[iteration]))
        
        with open(f"map source data/2020/{drug_file_name}", "r") as file:
            reader = csv.reader(file)
            next(reader)
            
            brnd_total_days, brnd_total_cost = 0, 0
            gen_total_days, gen_total_cost = 0, 0

            for row in enumerate(reader):
                #Get avg cost per day for name brand 
                if BRAND_NAMES[iteration] in row[1][3]:  #Is this a good enough check?
                    brnd_total_days += float(row[1][5])
                    brnd_total_cost += float(row[1][6])

                #Get avg cost per day for generic
                if GENERIC_NAMES[iteration] in row[1][3]:
                    gen_total_days += float(row[1][5])
                    gen_total_cost += float(row[1][6])

            brnd_name = BRAND_NAMES[iteration]
            brnd_total_days = round(brnd_total_days, 2)
            brnd_total_cost = round(brnd_total_cost, 2)
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

            writer.writerow([brnd_name, brnd_total_days, brnd_total_cost, brnd_avg_cost, gen_name, gen_total_days, gen_total_cost, gen_avg_cost])

            iteration += 1






# for row in enumerate(reader):
#                 #Get avg cost per day for name brand 
#                 if row[1][3] != 'Atorvastatin Calcium': #plug in generic name here
#                     brnd_total_days += float(row[1][5])
#                     brnd_total_cost += float(row[1][6])
#                 #Get avg cost per day for generic
#                 if row[1][3] == 'Atorvastatin Calcium': #plug in generic name here
#                     gen_total_days += float(row[1][5])
#                     gen_total_cost += float(row[1][6])

#             brnd_name = 'Lipitor' #Put brand name here
#             brnd_total_days = round(brnd_total_days, 2)
#             brnd_total_cost = round(brnd_total_cost, 2)
#             brnd_avg_cost = round(brnd_total_cost/brnd_total_days, 2)
            
#             gen_name = 'Atorvastatin Calcium' #Put generic name here
#             gen_total_days = round(gen_total_days, 2)
#             gen_total_cost = round(gen_total_cost, 2)
#             gen_avg_cost = round(gen_total_cost/gen_total_days, 2)