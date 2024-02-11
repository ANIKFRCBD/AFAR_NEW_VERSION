from django.shortcuts import render
import pandas as pd
from datetime import datetime
from afar_project.views import calculate_values,calculate_costs


file_path='csv_path/sample/asset_register.xlsx'
def dep(request):
    #call functions
    dep_sheet,colums_to_add,year_data=dep_sheet_maker(request)
    print(type(dep_sheet))
    #peocess the html
    dep_data=dep_sheet #for Depreciation calculation
    html=dep_sheet.to_html(index=False) # for html template
    print(type(html))
    header_html = html.split('<tbody>')[0]  # Extract headers part
    rows_html = '<tbody>' + html.split('<tbody>')[1]  # Extract rows part


    return render(request, 'frc_dep.html', {'header_html': header_html, 'rows_html': rows_html})
# Create your views here.
def dep_sheet_maker(request):
    df = pd.read_excel(file_path)
    pd.set_option('display.float_format', '{:.2f}'.format)
    df=df[['Financial Year','Asset Code','Purchase date','Sl ','Bill no','Economic Code','Category','Name of Item','Brand Name','Model/Type','Units','Modified Number','Price','Sold (unit)','Cost of Assets Sold','Current Balance']]
    df['Accumulated Depreciation']=0
    df['Units']=df['Units'].fillna(0)
    df['Sold (unit)']=df['Sold (unit)'].fillna(0)
    df['Modified Number']=df['Modified Number'].fillna(0)
    df[['Cost of Assets Sold']]=df[['Cost of Assets Sold']].fillna(0)
    df['Current Balance']=df['Price']-df['Cost of Assets Sold']
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
    df.to_excel("depreciation.xlsx",index=False)
    
    return df,columns_to_add,year_data
# def depreciation_calculation(request):


    