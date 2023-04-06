import os
print(os.getcwd())

file = open("input data files\\npidata_pfile_20050523-20230312.csv")
newFile = open("input data files\\NPPES doctors shortened.csv", "w")
for line in file:
    line = line.replace("\",\"", "\"~\"")
    line = line.split("~")
    # print(line[0])      
    if((line[47].startswith("\"20") or line[47].startswith("\"17") or line[47].startswith("\"36") or  line[47].startswith("\"39") or line[47].startswith("\"10") or line[47].startswith("\"16") or line[51].startswith("\"20") or line[51].startswith("\"17") or line[51].startswith("\"36") or  line[51].startswith("\"39") or line[51].startswith("\"10")or line[51].startswith("\"16"))and line[25]=="\"US\""):
        if(len(line[23])<=4):
            newFile.write(line[0]+","+line[23]+","+line[24]+"\n")
        else:
            newFile.write(line[0]+","+line[24]+","+line[25]+"\n")
# Manually added doctors
print("completed")  