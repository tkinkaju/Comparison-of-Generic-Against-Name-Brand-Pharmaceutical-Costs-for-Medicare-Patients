import csv

DRUG_FILE_NAMES = [ 'Adalimumab.csv', 'Atorvastatin Calcium.csv', 'Dextroamphetamine-Amphetamine.csv', 'Donepezil Hcl.csv',
                    'Etanercept.csv', 'Sertraline Hcl.csv', 'Vortioxetine Hydrobromide.csv', 'Zolpidem Tartrate.csv']

BRAND_NAMES = [ 'Humira', 'Lipitor', 'Adderall', 'Aricept', 'Enbrel', 'Zoloft', 'Trintellix', 'Ambien' ]
#FOR HUMIRA--> contains others such as --> 'Humira Pen', 'Humira(Cf) Pen'
#But maybe I could do .contains('Humira')?

GENERIC_NAMES = [ 'Adalimumab', 'Atorvastatin Calcium', 'Dextroamphetamine/Amphetamine', 'Donepezil Hcl',
                  'Etanercept', 'Sertraline Hcl', 'Vortioxetine Hydrobromide', 'Zolpidem Tartrate' ]


STATES = [ 'AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA',
           'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD',
           'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ',
           'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC',
           'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY' ]

iteration = 0


with open("statesOutputTest.csv", "w", newline="") as output_file:
    writer = csv.writer(output_file)
    writer.writerow(['state', 'brnd_name', 'brnd_total_days', 'brnd_total_cost', 'brnd_avg_cost', 'gen_name', 'gen_total_day', 'gen_total_cost', 'gen_avg_cost'])
        
    statesIter = 0
    for state in STATES:  #Will run 50 times
        print(state)

        drugIter = 0
        for drug_file_name in DRUG_FILE_NAMES:   #Will run 8 times(one for each drug) for each state
            with open(f"map source data/2020/{drug_file_name}", "r") as file:
                reader = csv.reader(file)
                next(reader)

                brnd_total_days, brnd_total_cost = 0, 0
                gen_total_days, gen_total_cost = 0, 0

                for row in enumerate(reader):
                    # if (row[1][0] == 'AL'):
                    #     print(row[1])

                    #Get avg cost per day for name brand 
                    if (row[1][0] == STATES[statesIter] and BRAND_NAMES[drugIter] in row[1][3]):
                        # print(row[1][3])
                        brnd_total_days += float(row[1][5])
                        brnd_total_cost += float(row[1][6])

                    #Get avg cost per day for generic
                    if (row[1][0] == STATES[statesIter] and GENERIC_NAMES[drugIter] in row[1][3]):
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

                writer.writerow([STATES[statesIter], brnd_name, brnd_total_days, brnd_total_cost, brnd_avg_cost, gen_name, gen_total_days, gen_total_cost, gen_avg_cost])
                drugIter += 1
        statesIter += 1


        #For each state, loop through the list looking for each drug type 
        # for drug_file_name in DRUG_FILE_NAMES:
        #     print("State: " + str(STATES[iteration]) + "Brand Name: " + str(BRAND_NAMES[iteration]) + "       Generic: " + str(GENERIC_NAMES[iteration]))

        #     with open(f"map source data/2020/{drug_file_name}", "r") as file:
        #         reader = csv.reader(file)
        #         next(reader)
                
        #         brnd_total_days, brnd_total_cost = 0, 0
        #         gen_total_days, gen_total_cost = 0, 0

        #         for row in enumerate(reader):
        #             #Get avg cost per day for name brand 
        #             if BRAND_NAMES[iteration] in row[1][3]:  #Is this a good enough check?
        #                 brnd_total_days += float(row[1][5])
        #                 brnd_total_cost += float(row[1][6])

        #             #Get avg cost per day for generic
        #             if GENERIC_NAMES[iteration] in row[1][3]:
        #                 gen_total_days += float(row[1][5])
        #                 gen_total_cost += float(row[1][6])

        #         brnd_name = BRAND_NAMES[iteration]
        #         brnd_total_days = round(brnd_total_days, 2)
        #         brnd_total_cost = round(brnd_total_cost, 2)
        #         if brnd_total_days != 0:
        #             brnd_avg_cost = round(brnd_total_cost/brnd_total_days, 2)
        #         else:
        #             brnd_avg_cost = "N/A"

        #         gen_name = GENERIC_NAMES[iteration]
        #         gen_total_days = round(gen_total_days, 2)
        #         gen_total_cost = round(gen_total_cost, 2)
        #         if gen_total_days != 0:
        #             gen_avg_cost = round(gen_total_cost/gen_total_days, 2)
        #         else: 
        #             gen_avg_cost = "N/A"

        #         writer.writerow([STATES[iteration], brnd_name, brnd_total_days, brnd_total_cost, brnd_avg_cost, gen_name, gen_total_days, gen_total_cost, gen_avg_cost])

        #         iteration += 1