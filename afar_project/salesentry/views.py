from django.shortcuts import render
from django.http import request,response
from django.contrib import messages
import pandas as pd
from .forms import sales_entry_form,entryfinder_sales
from .models import sales_entry_model
from datetime import datetime

file_path_register="csv_path/excel_files/asset_register.xlsx"
file_path_to_sales_register="csv_path/excel_files/asset_sales_register.xlsx"
#Show the impairment page
def sales_entry_app(request):
    sales_entry_post(request)
    file=accounting_for_recoverable_amount(request)
    form,data=sales_entry_save(request)  
    search=search_entry(request)
    search=search.fillna(" ").to_html(index=False)
    forms_entryfinder,data=entry_finder(request)
    # no_use=impariement_year_entry(request)

    context = {"form":form.as_table,
               "entry_finder":forms_entryfinder,
               "search":search,
               "file":file}
    return render (request,"sales_entry.html",context)
def sales_entry_post(request):
    file=pd.read_excel(file_path_register)
    sales_table=file
    sales_table.to_excel(file_path_to_sales_register,index=False)

#get data of impairment
def sales_entry_save(request):
    data=(0,0,0,"",0)
    Value_in_use=0
    Fair_value_less_cost_to_sale=0
    form=sales_entry_form(request.POST)
    if request.method=="POST":
        if form.is_valid():
            form.save()
            Asset_code=form.cleaned_data["Asset_code"]
            Number=form.cleaned_data["Number"]
            sales_proceeds=form.cleaned_data["Sales_proceeds"]
            Financial_year=form.cleaned_data["Financial_year"]
            Year_elapsed=form.cleaned_data["Year_elapsed"]
            data=(sales_proceeds,Number,Asset_code,Financial_year,Year_elapsed)
        else:
            print(form.errors)   
    return form,data

#find the asset entry data inpu
def entry_finder(request):
    data=0
    forms1=entryfinder_sales(request.POST)
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
    data_sheet=pd.read_excel(file_path_to_sales_register)
    d=data_sheet[data_sheet["Asset Code"] == Asset_Code]
    return d

# calculate the impairment
def accounting_for_recoverable_amount(request):
    file=pd.read_excel(file_path_to_sales_register)
    pd.set_option('display.float_format', '{:.1f}'.format)
    colunmn_list=list(file.columns)
    no_use,data=sales_entry_save(request)   
    if data[0] is not None and "":
        Sales_procced=data[0]
        Number=data[1]
        element_to_match=data[2]
        Financial_year=data[3]
        year_elapsed=data[4]
        file.loc[file["Asset Code"]==element_to_match,"Sales proceeds"]=float(Sales_procced)
        file.loc[file["Asset Code"]==element_to_match,"Sold (unit)"]=float(Number)
        file.loc[file["Asset Code"]==element_to_match,"FY of Items sold"]=str(Financial_year)
        file.loc[file["Asset Code"]==element_to_match,"Years used(sold items)"]=str(year_elapsed)

    else:
        file=file
    file.to_excel(file_path_to_sales_register,index=False)
    asset_register=pd.read_excel(file_path_register)
    asset_register["Sales proceeds"]=file["Sales proceeds"]
    asset_register["Sold (unit)"]=file["Sold (unit)"]
    asset_register["FY of Items sold"]=file["FY of Items sold"]
    asset_register["Years used(sold items)"]=file["Years used(sold items)"]
    asset_register.to_excel(file_path_register,index=False)
    return file