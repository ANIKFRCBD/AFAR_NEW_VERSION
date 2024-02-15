from django.shortcuts import render
from django.http import request,response
from django.contrib import messages
import pandas as pd
from .forms import impairmententry,entryfinder
from .models import impairmententry_model
from datetime import datetime

file_path="csv_path/excel_files/impairment_data.xlsx"
file_path_register="csv_path/excel_files/asset_register.xlsx"
file_path_depreciation="csv_path/excel_files/depreciation.xlsx"
#Show the impairment page
def imparimenttest(request):
    table = impairment(request)
    file=accounting_for_recoverable_amount(request)
    form,data=impairment_data_request_and_save(request)  
    search=search_entry(request)
    search=search.fillna(" ").to_html(index=False)
    forms_entryfinder,data=entry_finder(request)
    # no_use=impariement_year_entry(request)

    context = {"table":table,
               "form":form.as_table,
               "entry_finder":forms_entryfinder,
               "search":search,
               "file":file}
    return render (request,"impairment.html",context)

def impairment(request):
    #read the asset_register file
    data_sheet=pd.read_excel(file_path)# change it to file_path_register if it gives any error
    pd.set_option('display.float_format', '{:.1f}'.format) 
    primary_df=data_sheet
    depreciation_data_sheet=pd.read_excel(file_path_depreciation)
    test_accumulated="Accumulated Impairment"
    
    colunmn_list=list(primary_df.columns)
    print(type(colunmn_list))
    if  test_accumulated not in colunmn_list:
        primary_df[test_accumulated]=0
        print("column added")
    else:
        primary_df=primary_df
        print("no new column added")
    primary_df["Book Value"]=depreciation_data_sheet["Book Value"]

    primary_df=primary_df.fillna(0)
    table=primary_df.to_dict(orient="records")
    primary_df.to_excel(file_path,index=False)
    return table,primary_df

#get data of impairment
def impairment_data_request_and_save(request):
    data=(0,0,0,"")
    Value_in_use=0
    Fair_value_less_cost_to_sale=0
    form=impairmententry(request.POST)
    if request.method=="POST":
        if form.is_valid():
            form.save()
            Value_in_use=form.cleaned_data["Value_in_use"]
            Fair_value_less_cost_to_sale=form.cleaned_data["Fair_value_less_cost_to_sale"]
            Asset_code=form.cleaned_data["Asset_Code"]
            Financial_year=form.cleaned_data["Financial_year"]
            data=(Value_in_use,Fair_value_less_cost_to_sale,Asset_code,Financial_year)
        else:
            print(form.errors)   
    return form,data

# def impariement_year_entry(request):
#     data_sheet=pd.read_excel(file_path)
#     colunmn_list=list(data_sheet.columns)
#     print(colunmn_list)
#     no_use,data=impairment_data_request_and_save(request)
#     new_column=
#     print(data[3])
#     if data[3] not in colunmn_list:
#         if data[3]=="":
#             data_sheet=data_sheet
#         else:
#             data_sheet[data[3]]=0
#             print("column added")
#     else:
#          data_sheet=data_sheet
#          print("no new column added")
#     return data_sheet
            



#find the asset entry data inpu
def entry_finder(request):
    data=0
    forms1=entryfinder(request.POST)
    if request.method == "POST":
        if forms1.is_valid():
            forms1.save()
            data=forms1.cleaned_data["Asset_Code"]
        else:
            print(forms1.errors)    
    return forms1,data


#find the asset
def search_entry(request):
    form,data=entry_finder(request)
    Asset_Code=data
    data_sheet=pd.read_excel(file_path)
    d=data_sheet[data_sheet["Asset Code"] == Asset_Code]
    return d

# calculate the impairment
def accounting_for_recoverable_amount(request):
    file=pd.read_excel(file_path)
    pd.set_option('display.float_format', '{:.1f}'.format)
    colunmn_list=list(file.columns)
    no_use,data=impairment_data_request_and_save(request)
    new_column=data[3]   
    form,data=impairment_data_request_and_save(request)
    if data is not None:
        Value_in_use=data[0]
        Fair_value_less_cost_to_sale=data[1]
        element_to_match=data[2]
        if Value_in_use and Fair_value_less_cost_to_sale is not None:
            file.loc[file["Asset Code"]==element_to_match,"Value in use"]=float(Value_in_use)
            file.loc[file["Asset Code"]==element_to_match,"Fair value less cost to sale"]=float(Fair_value_less_cost_to_sale)
            file.loc[file["Asset Code"]==element_to_match,"Recoverable Amount"]=max(float(Value_in_use),float(Fair_value_less_cost_to_sale))
            if new_column is not "" or None:
                if  new_column not in colunmn_list:
                    file[new_column]=file["Recoverable Amount"]-file["Book Value"]
                    file.loc[file[new_column]<0,new_column]=0
                    new_years_added=len(file.columns)-13
                    if new_years_added<1:
                        file["Accumulated Impairment"]=file[new_column]
                    else:
                        file["Accumulated Impairment"]=file.iloc[:,-new_years_added:].sum(axis=1)
            else:
                file=file
            file.to_excel(file_path,index=False)
                       
        else:
            file.loc[file["Asset Code"]==element_to_match,"Value in use"]=0
            file.loc[file["Asset Code"]==element_to_match,"Fair value less cost to sale"]=0
            data_to_include=file.loc[file["Asset Code"]== element_to_match] 
            for index,row in data_to_include.iterrows():
                     file.at[index,"Recoverable Amount"]=row["Book Value"]
            new_years_added=len(file.columns)-13
            if new_column is not str("") or None:
                 if new_years_added<1:
                      file["Accumulated Impairment"]=file[new_column]
                 else:
                     file["Accumulated Impairment"]=file.iloc[:,-new_years_added:].sum(axis=1)
            else:
                file=file        
            file.to_excel(file_path,index=False)
            
    else:
        file=file
    file.to_excel(file_path,index=False)
    return file