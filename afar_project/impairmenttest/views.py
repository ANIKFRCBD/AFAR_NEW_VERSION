from django.shortcuts import render
from django.http import request,response
from django.contrib import messages
import pandas as pd
from .forms import impairmententry
from .models import impairmententry_model

def imparimenttest(request):
    form=impairment_data_request_and_save(request)
    table = impairment(request) 
    context = {"table":table,
               "form":form.as_table}
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
    # saved_data=0
    form=impairmententry(request.POST)
    if request.method=="POST":
        print(form.is_valid())
        if form.is_valid():
            saved_data=form.save()
        else:
            print(form.errors)   
    print(saved_data)
    return form

# def impairment_accounting(request):



# Create your views here.
