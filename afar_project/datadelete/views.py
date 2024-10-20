from django.shortcuts import render,redirect
from django.http import request
import pandas as pd
from django.contrib.auth.models import User as users
from datetime import datetime
from . forms import deletedata


file_path='csv_path/excel_files/asset_register.xlsx'
Dep_file_path='csv_path/excel_files/depreciation.xlsx'


def datadeletepage(request):
    return render(request,'datadelete.html')




def datainit(request):
    file_read_asset_reg=pd.read_excel(file_path)
    file_read_depreciation=pd.read_excel(Dep_file_path)
    #initialize the form
    checker_for_asset_register=file_read_asset_reg[["Asset Code"]]
    checker_for_depreciation=file_read_depreciation[["Asset Code"]]
    asset_code=request.POST.get('asset_code')
    print(asset_code)
    if asset_code in checker_for_asset_register.values:
        print (checker_for_asset_register.values)
        file_read_asset_reg=file_read_asset_reg[file_read_asset_reg["Asset Code"]!=asset_code]
        file_read_asset_reg.to_excel(file_path,index=False)
    else:
        print("no match")

    if asset_code in checker_for_depreciation.values:
        print (checker_for_depreciation.values)
        file_read_depreciation=file_read_depreciation[file_read_depreciation["Asset Code"]!=asset_code]
        file_read_depreciation.to_excel(Dep_file_path,index=False)
    else:
        print("no match")
    return redirect('delete')