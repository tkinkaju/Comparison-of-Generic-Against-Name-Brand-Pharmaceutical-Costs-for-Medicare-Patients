YEARS = ["2020","2019","2018","2017","2016","2015","2014","2013"]
DRUGS = ["Adalimumab","Atorvastatin Calcium", "Donepezil Hcl", "Etanercept", "Sertraline Hcl", "Vortioxetine Hydrobromide", "Zolpidem Tartrate"]
# DRUGNAME = "Dextroamphetamine-Amphetamine"

doctorDataFile = open("input data files\\NPPES doctors shortened.csv")
doctorDictionary = dict()
print("creating dictionary")
for doctorLine in doctorDataFile:
    npiNumber = doctorLine.split(",")[0].strip("\"")
    doctorDictionary[npiNumber] = doctorLine

for YEAR in YEARS:
    for DRUG in DRUGS:
        DRUG_SOURCE_FILE_NAME = "Medicare_Part_D_Prescribers_by_Provider_and_Drug_"+YEAR
        DRUGNAME = DRUG

        errorNumbers = []
        drugSourceFile = open("input data files\\"+DRUG_SOURCE_FILE_NAME+".csv")
        mapDataFile = open("map source data\\"+YEAR + "\\" +DRUGNAME + ".csv", "w")
        mapDataFile.write("state,state_fips,zip_code,brnd_name,gnrc_name,totl_day_sply,totl_drg_cost\n")
        print("creating drug-map data")
        for line in drugSourceFile:
            line = line.split(",")
            test = line[9].replace("\"","")
            if(test == DRUG and len(line[4])==2):
                try:
                    doctorLine = doctorDictionary[line[0]].split(",")
                    zipCode = doctorLine[2].replace("\n","")
                    zipCode = zipCode[:6]+"\""
                    if(len(line[8])==1):
                        mapDataFile.write(line[4]+","+line[5]+","+zipCode+","+line[9]+","+line[10]+","+line[13]+","+line[14]+"\n")
                    else:
                        mapDataFile.write(line[4]+","+line[5]+","+zipCode+","+line[8]+","+line[9]+","+line[12]+","+line[13]+"\n")
                except:
                    errorNumbers.append(line[0])

        logFile = open("log files\\"+YEAR + "-" +DRUGNAME + "-log.csv", "w")
        print("creating log file")
        for number in errorNumbers:
            logFile.write(number + "\n")

print("completed") 