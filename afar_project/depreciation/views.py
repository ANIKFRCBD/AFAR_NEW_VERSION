from django.shortcuts import render
import pandas as pd
from datetime import datetime
from afar_project.views import calculate_values,calculate_costs


file_path='csv_path/excel_files/asset_register.xlsx'
Dep_file_path='csv_path/excel_files/depreciation.xlsx'

def dep(request):
    #call functions
    dep_sheet,colums_to_add,year_data=dep_sheet_maker(request)
    data_sheet_updated=depreciation_calculation(request)
    #peocess the html
    dep_data=dep_sheet #for Depreciation calculation
    # html=data_sheet_updated.to_html(index=False) # for html template
    header_html = data_sheet_updated.columns.tolist()  # Extract headers part
    rows_html = data_sheet_updated.values.tolist()  # Extract rows part
    data_sheet_updated.to_excel(Dep_file_path,index=False)
    return render(request, 'frc_dep.html', {'header_html': header_html,"rows_html":rows_html})
# Create your views here.
def dep_sheet_maker(request):
    df = pd.read_excel(file_path)
    pd.set_option('display.float_format', '{:.1f}'.format)
    # data extraction and cleaning
    df=df[['Financial Year','Asset Code','Purchase date','Sl ','Bill no','Economic Code',
           'Category','Name of Item','Brand Name','Model/Type','Units','Modified Number','Price','Salvage Value',
           'Expected life','Sold (unit)','Years used(sold items)','FY of Items sold',
           'Cost of Assets Sold','Current Balance']]
    df['Rate of Depreciation']=1/df['Expected life']
    df['Accumulated Depreciation']=0
    df['Accumulated Depreciation on Sold items']=0    
    df['Units']=df['Units'].fillna(0)
    df['Sold (unit)']=df['Sold (unit)'].fillna(0)
    df['Model/Type']=df['Model/Type'].fillna(" ")
    df['Brand Name']=df['Brand Name'].fillna(" ")
    df['Economic Code']=df['Economic Code'].fillna(" ")
    df['Modified Number']=df['Modified Number'].fillna(0)
    df[['Cost of Assets Sold']]=df[['Cost of Assets Sold']].fillna(0)
    df[['FY of Items sold']]=df[['FY of Items sold']].fillna(0)
    df['Current Balance']=df['Price']-df['Cost of Assets Sold']

    years=df['Financial Year'].drop_duplicates()
    if "Accumulated Depreciation Net" not in list(df.columns):
        df["Accumulated Depreciation Net"]=0
    else:
        df=df
    if "Book Value" not in list(df.columns):
        df["Book Value"]=0
    else:
        df=df
    years=df['Financial Year'].drop_duplicates()   
    current_year=datetime.now()
    # print(current_year.year)
    year={}
    #getting year Values as a list to iterate
    for i in years:
        d=i.split('-')
        year[f'{i}']=int(d[1])
    val=year.values()
    years=[]
    for i in val:
        years.append(i)
    years.sort()
    # find out the numbers of years to add
    columns_to_create=current_year.year-int(years[0])
    #check whether any new year-based column is to be added
    if len(years)<columns_to_create:
    # print(columns_to_create)
        years_new=[]
        for i in range(columns_to_create+1):
            p=int(years[0])+i
            years_new.append(p)
        # years_new.append(list[i])
        years_dict={}
        for i in years_new:
            years_dict[f'{int(i)-1}-{i}']=int(i)
        for i in years_dict.keys():
            df[i]=0
        columns_to_add=int(columns_to_create)
        year_data=years_dict
    else:
        #if no more year based columns to be added
        for i in years:
            df[i]=0
        columns_to_add=len(years)
        year_data=years
    #Write it to excel file
    df.to_excel(Dep_file_path,index=False)
    
    return df,columns_to_add,year_data

#Calculation of Depreciation
def depreciation_calculation(request):
    # Generate the depreciation sheet and necessary columns
    data_sheet, columns_to_add, year_data = dep_sheet_maker(request)
    data_sheet = data_sheet.fillna(0)  # Fill NaN values early to prevent issues
    
    # Identify the columns to iterate over (year-based columns)
    columns_to_iter = data_sheet.columns[-columns_to_add:]
    total_columns = len(data_sheet.columns)
    iteration_from_last = len(columns_to_iter)
    
    # Calculate accumulated depreciation initially
    data_sheet['Accumulated Depreciation'] = data_sheet[columns_to_iter].sum(axis=1)
    
    # Loop through each row and calculate the depreciation per year
    for index, row in data_sheet.iterrows():
        year_elapsed = 1
        years_used = float(row["Years used(sold items)"])  # Ensure float compatibility
        current_balance = float(row["Current Balance"])
        rate_of_depreciation = float(row["Rate of Depreciation"])
        
        for column in data_sheet.columns[total_columns - iteration_from_last:]:
            financial_year = float(row["Financial Year"][:4])
            current_column_year = float(str(column[:4]))

            # Calculate depreciation for current year
            if financial_year <= current_column_year and year_elapsed <= row["Expected life"]:
                if years_used > 0:
                    value = (row["Cost of Assets Sold"] + current_balance) * rate_of_depreciation
                    years_used -= 1
                else:
                    value = current_balance * rate_of_depreciation
                
                # Assign value after rounding to maintain precision
                data_sheet.loc[index, column] = round(value, 2)
            
            # Increment year_elapsed after the current year is considered
            if current_column_year >= financial_year:
                year_elapsed += 1

    # Calculate the accumulated depreciation on sold items
    data_sheet["Accumulated Depreciation on Sold items"] = (
        data_sheet["Cost of Assets Sold"] * data_sheet["Rate of Depreciation"] * data_sheet["Years used(sold items)"]
    ).round(2)

    # Recalculate accumulated depreciation for each row
    data_sheet["Accumulated Depreciation"] = data_sheet[columns_to_iter].sum(axis=1)
    
    # Calculate net accumulated depreciation and book value
    data_sheet["Accumulated Depreciation Net"] = (
        data_sheet["Accumulated Depreciation"] - data_sheet["Accumulated Depreciation on Sold items"]
    ).round(2)
    data_sheet["Book Value"] = (
        data_sheet["Current Balance"] - data_sheet["Accumulated Depreciation Net"]
    ).round(2)
    
    # Save the updated data to the Excel file
    data_sheet.to_excel(Dep_file_path, index=False)
    
    return data_sheet



    