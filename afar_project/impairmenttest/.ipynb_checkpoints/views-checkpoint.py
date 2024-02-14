from django.shortcuts import render
from django.http import request,response
from django.contrib import messages
import pandas as pd

def imparimenttest(request):
    table=impairment(request)
    context={"table":table}

    return render (request,"impairment.html",context)

def impairment(request):
    #read the asset_register file
    file_path="csv_path/sample/asset_register.xlsx"
    primary_df=pd.read_excel(file_path)
    impaitment_part=pd.DataFrame([""])
    primary_df=primary_df[["Financial Year","Purchase date","Bill no","Economic Code","Category","Name of Item","Brand Name"]]
    table=primary_df.to_html(index=False)
    return table



# Create your views here.
