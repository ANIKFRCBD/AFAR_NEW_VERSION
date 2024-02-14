import csv
from datetime import date
import datetime
from django.http import HttpResponse
from django.shortcuts import redirect, render
from afar_app.models import input_field
from afar_app.models import model_asset_info
import pandas as pd
import numpy as np
from datetime import datetime
import re
import os
from django.conf import settings
from django.contrib import messages

def frc_system(request):
    if request.method == 'POST':
        # Assuming your form field name is 'file'
        uploaded_file = request.FILES.get('file')

        if uploaded_file:
            # Read the existing Excel file
            existing_file_path = 'csv_path/sample/asset_register.xlsx'
            existing_df = pd.read_excel(existing_file_path)

            # Read the uploaded Excel file
            uploaded_df = pd.read_excel(uploaded_file)

            if len(existing_df['Financial Year']) > len(uploaded_df['Financial Year']):
                file = existing_df
            else:
                file = uploaded_df

            # Write the concatenated DataFrame to a new Excel file
            file_path = 'csv_path/sample/asset_register.xlsx'
            file.to_excel(file_path, index=False)
            return redirect('frc_asset_register')  # Redirect to appropriate view after upload

    return render(request, 'frc_system') 
