from django.shortcuts import render
from django.http import request,response
from django.contrib import messages
import pandas as pd
from .forms import impairmententry,entryfinder
from .models import impairmententry_model
from datetime import datetime

file_path="csv_path/sample/impairment_data.xlsx"
file_path_register="csv_path/sample/asset_register.xlsx"

#Show the impairment page
def imparimenttest(request):
    table = impairment(request)
    form,data=impairment_data_request_and_save(request)  
    search=search_entry(request)
    search=search.fillna(" ").to_html(index=False)
    forms_entryfinder,data=entry_finder(request)
    no_use=impariement_year_entry(request)
    file=accounting_for_recoverable_amount(request)
    context = {"table":table,
               "form":form.as_table,
               "entry_finder":forms_entryfinder,
               "search":search,
               "file":file}
    return render (request,"impairment.html",context)

def impairment(request):
    #read the asset_register file
    primary_df=pd.read_excel(file_path) # change it to file_path_register if it gives any error

    
    if "Value in use" not in primary_df:
        impairment_part=pd.DataFrame({"Book Value":[],"Fair value less cost to sale": [],"Value in use":[],"Recoverable Value":[]})
        primary_df=primary_df[["Financial Year","Purchase date","Bill no","Economic Code","Category","Name of Item","Brand Name","Asset Code"]]
        primary_df=pd.concat([primary_df,impairment_part],join="outer")
    else:
        primary_df=primary_df
    
    test_accumulated="Accumulated Impairment"
    
    colunmn_list=list(primary_df.columns)
    print(type(colunmn_list))
    if  test_accumulated not in colunmn_list:
        primary_df[test_accumulated]=0
        print("column added")
    else:
        primary_df=primary_df
        print("no new column added")

    primary_df=primary_df.fillna(0)
    table=primary_df.to_dict(orient="records")
    primary_df.to_excel(file_path,index=False)
    return table,primary_df

#get data of impairment
def impairment_data_request_and_save(request):
    data=(0,0,0)
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

def impariement_year_entry(request):
    data_sheet=pd.read_excel(file_path)
    colunmn_list=list(data_sheet.columns)
    print(colunmn_list)
    no_use,data=impairment_data_request_and_save(request)
    print(data[3])
    if data[3] not in colunmn_list:
        if data[3]=="":
            data_sheet=data_sheet
        else:
            data_sheet[data[3]]=0
            print("column added")
            data_sheet.to_excel(file_path,index=False)
    else:
         data_sheet=data_sheet
         print("no new column added")
    return data_sheet
            



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
    print(data_sheet["Asset Code"])
    d=data_sheet[data_sheet["Asset Code"] == Asset_Code]
    return d

# calculate the impairment
def accounting_for_recoverable_amount(request):
    file=pd.read_excel(file_path)
    form,data=impairment_data_request_and_save(request)
    if data is not None:
        Value_in_use=data[0]
        Fair_value_less_cost_to_sale=data[1]
        element_to_match=data[2]
        if Value_in_use is not None:
            print(f'the key is: {element_to_match}')
            file.loc[file["Asset Code"]==element_to_match,"Value in use"]=float(Value_in_use)
            file.loc[file["Asset Code"]==element_to_match,"Fair value less cost to sale"]=float(Fair_value_less_cost_to_sale)
            print(f"the data are {Fair_value_less_cost_to_sale},{Value_in_use}")
    else:
        file.loc[file["Asset Code"]==element_to_match,"Value in use"]=0
        file.loc[file["Asset Code"]==element_to_match,"Fair value less cost to sale"]=0
        print("no data is sent")
    file.to_excel(file_path,index=False)
    return file