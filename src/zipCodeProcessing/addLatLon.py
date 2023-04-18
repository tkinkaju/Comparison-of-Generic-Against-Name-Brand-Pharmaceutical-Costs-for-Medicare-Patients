import sys
import csv

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('Usage: \naddLatLang.py <sourceFilePath> <destination>')
        exit(0)
    
    # read zip table into dictionary
    zipCodeCoords = {}
    zip_col = 7
    lon_col = 3
    lat_col = 4

    print('reading zipcodes into memory...')
    zipCount = 0
    with open('US_ZIP_codes_to_longitude_and_latitude.csv', 'r') as zipCodeFile:
        reader = csv.reader(zipCodeFile)
        next(reader)

        for row in reader:
            code = str(row[zip_col]).rjust(5, '0')

            zipCodeCoords[code] = {'lat':row[lat_col], 'lon':row[lon_col]}
            zipCount += 1
    
    print(f'{zipCount} zip codes loaded')


    dest = open(sys.argv[2], 'w')
    colName = 'totl_day_sply'

    print('Reading file...')
    # open source file, look for header named zip_code
    with open(sys.argv[1], 'r') as src:
        reader = csv.reader(src)
        cols = next(reader)
        zip_col_src = cols.index('zip_code')
        val_col = cols.index(colName)

        if zip_col_src < 0 or val_col < 0:
            print("Could not find required columns")
            exit(1)

        dest.write('id, value, point_latitude, point_longitude\n')
        count = 0
        for row in reader:
            if row[zip_col_src] in zipCodeCoords:
                dest.write(f"{count},{row[val_col]},{ zipCodeCoords[row[zip_col_src]]['lat'] },{ zipCodeCoords[row[zip_col_src]]['lon'] }\n")

            count += 1


    # loop through file, adding a point_latitude, point_longitude

    dest.close()
    print('done')