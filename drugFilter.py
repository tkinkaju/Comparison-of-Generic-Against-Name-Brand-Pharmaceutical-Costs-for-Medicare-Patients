YEAR = "2020"
DRUG = "Sertraline Hcl"
DRUG_SOURCE_FILE_NAME = "Medicare_Part_D_Prescribers_by_Provider_and_Drug_2020"

doctorDataFile = open("input data files\\NPPES doctors shortened.csv")
doctorDictionary = dict()
print("creating dictionary")
for doctorLine in doctorDataFile:
    npiNumber = doctorLine.split(",")[0].strip("\"")
    doctorDictionary[npiNumber] = doctorLine


errorNumbers = []
drugSourceFile = open("input data files\\"+DRUG_SOURCE_FILE_NAME+".csv")
mapDataFile = open("map source data\\"+YEAR + "\\" +DRUG + ".csv", "w")
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
            mapDataFile.write(line[4]+","+line[5]+","+zipCode+","+line[8]+","+line[9]+","+line[12]+","+line[13]+"\n")
        except:
            errorNumbers.append(line[0])


logFile = open("log files\\"+YEAR + "-" +DRUG + "-log.csv", "w")
print("creating log file")
for number in errorNumbers:
    logFile.write(number + "\n")

print("completed") 