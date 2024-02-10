from django.shortcuts import render
from django.http import request,response
from django.contrib import messages
import pandas as pd
from .forms import impairmententry,entryfinder
from .models import impairmententry_model

file_path="csv_path/sample/impairment_data.xlsx"


def imparimenttest(request): 
    search=search_entry(request)
    search=search.fillna(" ").to_html()
    table = impairment(request) 
    form,data=impairment_data_request_and_save(request)
    forms_entryfinder,data=entry_finder(request)
    file=accounting_for_recoverable_amount(request)
    context = {"table":table,
               "form":form.as_table,
               "entry_finder":forms_entryfinder,
               "search":search,
               "file":file}
    return render (request,"impairment.html",context)

def impairment(request):
    #read the asset_register file
    file_path="csv_path/sample/impairment_data.xlsx"
    primary_df=pd.read_excel(file_path)
    impairment_part=pd.DataFrame({"Book_Value":[],"Fair_value_less_cost_to_sale": [],"Value_in_use":[]})
    primary_df=primary_df[["Financial Year","Purchase date","Bill no","Economic Code","Category","Name of Item","Brand Name"]]
    primary_df.columns = ["Financial_Year","Purchase_date","Bill_no","Economic_Code","Category","Name_of_Item","Brand_Name"]
    primary_df=pd.concat([primary_df,impairment_part],join="outer")
    primary_df=primary_df.fillna(0)
    table=primary_df.to_dict(orient="records")
    return table

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
            data=(Value_in_use,Fair_value_less_cost_to_sale,Asset_code)
            print(data)
        else:
            print(form.errors)   
    return form,data

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



def search_entry(request):
    form,data=entry_finder(request)
    Asset_Code=data
    file=file_path
    data=pd.read_excel(file)
    d=data.loc[data["Asset Code"] == Asset_Code] 
    return d
# Create your views here.
def accounting_for_recoverable_amount(request):
    file=pd.read_excel(file_path)
    form,data=impairment_data_request_and_save(request)
    print(data)
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