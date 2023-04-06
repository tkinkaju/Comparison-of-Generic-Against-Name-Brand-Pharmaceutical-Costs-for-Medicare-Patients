YEAR = "2020"
DRUG = "Sertraline Hcl"

doctorDataFile = open("input data files\\NPPES doctors shortened.csv")
doctorDictionary = dict()
print("creating dictionary")
for doctorLine in doctorDataFile:
    npiNumber = doctorLine.split(",")[0].strip("\"")
    doctorDictionary[npiNumber] = doctorLine


errorNumbers = []
drugSourceFile = open("input data files\\Medicare_Part_D_Prescribers_by_Provider_and_Drug_2020.csv")
mapDataFile = open("map source data\\"+YEAR + "\\" +DRUG + ".csv", "w")
mapDataFile.write("state,state_fips,zip_code,brnd_name,gnrc_name,totl_day_sply,totl_drg_cost\n")
print("creating drug-map data")
for line in drugSourceFile:
    fullLine = line
    line = line.split(",")
    # print(line[47])
    test = line[9].replace("\"","")
    if(test == DRUG):
        try:
            doctorLine = doctorDictionary[line[0]].split(",")
            zipCode = doctorLine[2].replace("\n","")
            mapDataFile.write(line[4]+","+line[5]+","+zipCode+","+line[8]+","+line[9]+","+line[12]+","+line[13]+"\n")
        except:
            errorNumbers.append(line[0])


logFile = open("log files\\"+YEAR + "-" +DRUG + "-log.csv", "w")
print("creating log file")
for number in errorNumbers:
    logFile.write(number + "\n")

print("completed") 