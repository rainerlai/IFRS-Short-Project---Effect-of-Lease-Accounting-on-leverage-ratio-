#Code fully prepared in its entirety by Rainer Lai

import pandas as pd
import numpy as np
import os

'''
Inputs:
Leases_working file.csv
Siccodes.csv
'''

#%%

#Sorting Siccodes.csv as dictionary data for Type to Siccode
siccodes = pd.read_csv("Siccodes.csv")

siccode_dict = {}

for i in range(0,siccodes['Type'].count()):

    if siccodes.iat[i,0] == 'NoDur':
        for k in range(int(siccodes.iat[i,1]),int(siccodes.iat[i,2]+1)):
            siccode_dict[k] = 'NoDur'
     
    if siccodes.iat[i,0] == 'Durbl':
        for k in range(int(siccodes.iat[i,1]),int(siccodes.iat[i,2]+1)):
            siccode_dict[k] = 'Durbl'
    
    if siccodes.iat[i,0] == 'Manuf':
        for k in range(int(siccodes.iat[i,1]),int(siccodes.iat[i,2]+1)):
            siccode_dict[k] = 'Manuf'
        
    if siccodes.iat[i,0] == 'Enrgy':
        for k in range(int(siccodes.iat[i,1]),int(siccodes.iat[i,2]+1)):
            siccode_dict[k] = 'Enrgy'
        
    if siccodes.iat[i,0] == 'Chems':
        for k in range(int(siccodes.iat[i,1]),int(siccodes.iat[i,2]+1)):
            siccode_dict[k] = 'Chems'
        
    if siccodes.iat[i,0] == 'BusEq':
        for k in range(int(siccodes.iat[i,1]),int(siccodes.iat[i,2]+1)):
            siccode_dict[k] = 'BusEq'
        
    if siccodes.iat[i,0] == 'Telcm':
        for k in range(int(siccodes.iat[i,1]),int(siccodes.iat[i,2]+1)):
            siccode_dict[k] = 'Telcm'
        
    if siccodes.iat[i,0] == 'Utils':
        for k in range(int(siccodes.iat[i,1]),int(siccodes.iat[i,2]+1)):
            siccode_dict[k] = 'Utils'
        
    if siccodes.iat[i,0] == 'Shops':
        for k in range(int(siccodes.iat[i,1]),int(siccodes.iat[i,2]+1)):
            siccode_dict[k] = 'Shops'
        
    if siccodes.iat[i,0] == 'Hlth':
        for k in range(int(siccodes.iat[i,1]),int(siccodes.iat[i,2]+1)):
            siccode_dict[k] = 'Hlth'
        
    if siccodes.iat[i,0] == 'Money':
        for k in range(int(siccodes.iat[i,1]),int(siccodes.iat[i,2]+1)):
            siccode_dict[k] = 'Money'
            
#%%

#Siccode Type Identifier
def iden(SPI):
    if not int(SPI) in siccode_dict.keys():
        return "Other"
    else:
        return siccode_dict[int(SPI)]

#%%

#PV of Lease
def PV_x(years_after):
    # 1/(1+0.1)**years_after
    if years_after == 0:
        return 0
    
    years = int()
    if years_after >= 5:
        years = 5
        
    discount_table = []
    for i in range (6,100):
        discount_table += [1/((1+0.1)**i)]
    
    sum_of_pvs = float()
    
    for i in range(years):
        sum_of_pvs += discount_table[i]
    return sum_of_pvs

#%%        

#Import csv file and remove all blank lines (i.e ommited info)
Lease_df = pd.read_csv("Leases_working file.csv", skip_blank_lines = True)

Lease_df.index

Lease_df.dropna(how = "all", inplace = True)

#%%

#Add new Column that takes in the most recent and latest rental commitment from year 1 to year 5
Lease_df["Rental Commitment - Year 6th and beyond"] = 0.0

for i in range(0,Lease_df["Rental Commitment - Year 6th and beyond"].count()):

    if Lease_df.iat[i,11] != 0:
        Lease_df.iat[i,17] = Lease_df.iat[i,11]
        
    elif Lease_df.iat[i,10] != 0:
        Lease_df.iat[i,17] = Lease_df.iat[i,10]
        
    elif Lease_df.iat[i,9] != 0:
        Lease_df.iat[i,17] = Lease_df.iat[i,9]
        
    elif Lease_df.iat[i,8] != 0:
        Lease_df.iat[i,17] = Lease_df.iat[i,8]
        
    elif Lease_df.iat[i,7] != 0:
        Lease_df.iat[i,17] = Lease_df.iat[i,7]
    
    else:
        continue

#%%

#Approx year of t+6
Lease_df["No. Years 6th year and beyond"] = round(Lease_df["Rental Commitments - Minimum - 5 Year Total"] / Lease_df["Rental Commitment - Year 6th and beyond"],0)
Lease_df.replace([np.inf, -np.inf], np.nan, inplace = True) 
Lease_df.fillna(0, inplace = True)

#%%

# PV of all Lease Payments
Lease_df["PV of Lease Payments"] = ( (Lease_df["Rental Commitments - Minimum - 5 Year Total"] / Lease_df["No. Years 6th year and beyond"] ) * Lease_df["No. Years 6th year and beyond"].apply(PV_x) )

Lease_df.replace([np.inf, -np.inf], np.nan, inplace = True) 
Lease_df.fillna(0, inplace = True)
                                        
Lease_df["PV of Lease Payments"] += Lease_df["Rental Commitments - Minimum - 1st Year"] * 1/1.1000 \
                                    + Lease_df["Rental Commitments - Minimum - 2nd Year"] * 1/1.2100 \
                                    + Lease_df["Rental Commitments - Minimum - 3rd Year"] * 1/1.3310 \
                                    + Lease_df["Rental Commitments - Minimum - 4th Year"] * 1/1.4641 \
                                    + Lease_df["Rental Commitments - Minimum - 5th Year"] * 1/1.6105 
                                 
#%%
'''
#Leverage = Debt / Asset
#Post-IFRS-16, ROU Asset = PV of Lease Payments + Rental Expense 
#Post-IFRS-16, Lease Liability = ROU Asset - Rental Expense = PV of Lease Payments

Lease_df["Pre-IFRS16 Leverage"] = Lease_df["Total Debt Including Current"] / Lease_df["Assets - Total"]

Lease_df["Post-IFRS16 Leverage"] = (Lease_df["Total Debt Including Current"] + Lease_df["PV of Lease Payments"] ) / \
                                   (Lease_df["Assets - Total"] + Lease_df["PV of Lease Payments"] + Lease_df["Rental Expense"])

#%%

#Type Column Created accordingly to Industry Identifier
Lease_df["Type"] = Lease_df["Standard Industry Classification Code"].apply(iden)

#%%

#Export to csv for each Type Filter
for Type in ['NoDur','Durbl','Manuf','Enrgy','Chems','BusEq','Telcm','Utils','Shops','Hlth','Money','Other']:
    Lease_df[Lease_df["Type"] == Type].to_csv(f"{Type}.csv")

#%%

#Export into a Combined Excel with 12 sheets for each Type
writer = pd.ExcelWriter('Combined_Excel.xlsx', engine = 'xlsxwriter')

for Type in ['NoDur','Durbl','Manuf','Enrgy','Chems','BusEq','Telcm','Utils','Shops','Hlth','Money','Other']:
    Lease_df[Lease_df["Type"] == Type].to_excel(writer, sheet_name = Type, index = False)

writer.save(
'''
