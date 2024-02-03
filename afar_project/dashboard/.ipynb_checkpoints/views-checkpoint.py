from django.shortcuts import render
from django.http import request
import pandas as pd

# Create your views here.
def dashboard(request):
    return render(request,"Dashboard.html")

def dashboard_summary_of_assets(request):
    file_path = 'csv_path/sample/asset_register.xlsx'  # Replace with the actual file path
    df = pd.read_excel(file_path)
    print(df)
