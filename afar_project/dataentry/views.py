from django.shortcuts import render,redirect
from django.http import request
import pandas as pd
from django.contrib.auth.models import User as users
from datetime import datetime
# Create your views here.
def frc_data_entry(request):
    csv_file_path = 'csv_path/asset_info/asset_info.csv'
    df = pd.read_csv(csv_file_path)
    user_list=users.objects.all()
    current_user=request.user.username
    print(current_user)
    df_csv = pd.read_csv('csv_path/asset_info/asset_info.csv')

    # Extract values from the first column
    dropdown_categories = df.iloc[:, 0].tolist()

    if request.method == 'POST':
        file_path = 'csv_path/excel_files/asset_register.xlsx'
        df = pd.read_excel(file_path)
        # Extracting form data from the POST request
        purchase_date = request.POST.get('purchase_date')
        purchase_date = datetime.strptime(purchase_date, '%Y-%m-%d')
        purchase_year = purchase_date.year
        purchase_month = purchase_date.month
        purchase_date = purchase_date.strftime('%m/%d/%Y')

        # Determine the financial year
        if purchase_month <= 6:
            purchase_year -= 1

        financial_year = f"{purchase_year}-{purchase_year + 1}"

        # Extract remaining form data
        serial_no = request.POST.get('serial_no')
        bill_no = request.POST.get('bill_no')
        category = request.POST.get('category')
        name_of_item = request.POST.get('name_of_item')
        quantity = float(request.POST.get('quantity') or 0)
        price = float(request.POST.get('price') or 0)
        warranty = request.POST.get('warranty')
        vendor = request.POST.get('vendor')
        vendor_address = request.POST.get('vendor_address')
        vendor_contact = request.POST.get('vendor_contact')
        sold_units = 0  # Assuming no initial sold units
        location = request.POST.get('location')
        current_condition = request.POST.get('current_condition')
        user_name = request.POST.get('user_name')

        # Get the matching row from the DataFrame based on the category
        matching_row = df_csv[df_csv['Category'] == category].iloc[0]

        # Extract values from the matching row
        economic_code = matching_row['Economic Code']
        expected_life = matching_row['Expected Life(post)']

        # Create the new row dictionary
        new_row = {
            'Financial Year': financial_year,
            'Purchase date': purchase_date,
            'Sl': serial_no,
            'Bill no': bill_no,
            'Category': category,
            'Name of Item': name_of_item,
            'Units': quantity,
            'Price': price,
            'Warranty (months)': warranty,
            'Vendor': vendor,
            'Vendor Address': vendor_address,
            'Vendor Contact': vendor_contact,
            'Sold (unit)': sold_units,
            'Location': location,
            'Economic Code': economic_code,
            'Expected life': expected_life,
            'Entry By': user_name,
            'Current Condition': current_condition
        }
        # Append the new row to the DataFrame using loc
        df.loc[len(df)] = new_row

        # Save the DataFrame back to the Excel file
        df.to_excel(file_path, index=False)
        # return render (request,'asset_image_upload.html')
        

    return render(request, 'frc_data_entry.html',{'dropdown_categories': dropdown_categories,'user':current_user})