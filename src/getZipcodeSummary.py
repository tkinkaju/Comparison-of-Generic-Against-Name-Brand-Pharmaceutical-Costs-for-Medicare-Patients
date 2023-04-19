import csv

DRUG_FILE_NAMES = [ 'Adalimumab.csv', 'Atorvastatin Calcium.csv', 'Donepezil Hcl.csv',
                    'Etanercept.csv', 'Sertraline Hcl.csv', 'Vortioxetine Hydrobromide.csv', 'Zolpidem Tartrate.csv']

BRAND_NAMES = [ 'Humira', 'Lipitor', 'NOT SURE?', 'Enbrel??', 'Zoloft?', 'Trintellix?', 'Ambien?' ]
#FOR HUMIRA--> contains others such as --> 'Humira Pen', 'Humira(Cf) Pen'
#But maybe I could do .contains('Humira')?

GENERIC_NAMES = [ 'Adalimumab', 'Atorvastatin Calcium', 'Donepezil Hcl',
                  'Etanercept', 'Sertraline Hcl', 'Vortioxetine Hydrobromide', 'Zolpidem Tartrate' ]


STATES = [ 'AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA',
           'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD',
           'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ',
           'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC',
           'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY' ]

ZIP_CODES = []