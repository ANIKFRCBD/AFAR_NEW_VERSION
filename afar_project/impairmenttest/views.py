from django.shortcuts import render
from django.http import request,response
from django.contrib import messages
import pandas as pd
from .forms import impairmententry,entryfinder
from .models import impairmententry_model

file_path="csv_path/sample/asset_register.xlsx"
def imparimenttest(request): 
    search=search_entry(request)
    search=search.fillna(" ").to_html()
    table = impairment(request) 
    form=impairment_data_request_and_save(request)
    forms_entryfinder=entry_finder(request)
    context = {"table":table,
               "form":form.as_table,
               "entry_finder":forms_entryfinder,
               "search":search}
    return render (request,"impairment.html",context)

def impairment(request):
    #read the asset_register file
    file_path="csv_path/sample/asset_register.xlsx"
    primary_df=pd.read_excel(file_path)
    impairment_part=pd.DataFrame({"Book_Value":[],"Fair_value_less_cost_to_sale": [],"Value_in_use":[]})
    primary_df=primary_df[["Financial Year","Purchase date","Bill no","Economic Code","Category","Name of Item","Brand Name"]]
    primary_df.columns = ["Financial_Year","Purchase_date","Bill_no","Economic_Code","Category","Name_of_Item","Brand_Name"]
    primary_df=pd.concat([primary_df,impairment_part],join="outer")
    primary_df=primary_df.fillna(0)
    table=primary_df.to_dict(orient="records")
    return table

def impairment_data_request_and_save(request):
    saved_data=0
    form=impairmententry(request.POST)
    if request.method=="POST":
        if form.is_valid():
            saved_data=form.save()
        else:
            print(form.errors)   
    return form

def entry_finder(request):
    forms1=entryfinder(request.POST)
    if request.method=="POST":
        if forms1.is_valid():
            forms1=forms1
        else:
            print(forms1.errors)
    
    return forms1 

def search_entry(request):
    form=entry_finder(request)
    print(form)
    bill_no=form.cleaned_data['bill_no']
    Category=form.cleaned_data['Category']
    Financial_Year=form.cleaned_data['Financial_Year']

    file=file_path
    data=pd.read_excel(file)  
    d=data.loc[(data["Bill no"] == float(bill_no)) & (data["Financial Year"] == Financial_Year) | (data["Category"] == Category)]  
    return d
# Create your views here.
