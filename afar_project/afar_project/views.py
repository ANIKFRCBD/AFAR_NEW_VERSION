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

form_inputs = []

# Read the Excel file
df = pd.read_csv('csv_path/my_data.csv')

def extract_numbers(string_data):
    # Use regular expression to find standalone numeric values in the string
    if type(string_data) == str:
        numeric_parts = re.findall(r'\b\d+(?:\.\d+)?\b', string_data)
        # Convert the list of numeric strings to floats
        numeric_values = [float(num) for num in numeric_parts]
        return numeric_values[0]
    return string_data

def get_column_names_for_extra_input(file_path):
    df = pd.read_csv(file_path)
    column_names = df.columns[12:]
    return column_names

def read_csv_file(file_path):
    df = pd.read_csv(file_path)
    header = df.columns.tolist()
    data = df.values.tolist()
    data.insert(0, header)
    #open(file_path, 'w').close()
    return data

def extract_column_values(file_path):
    df = pd.read_csv(file_path)
    values = df.iloc[0:, 0].tolist()
    return values

def first_year(year_list):
    modified_list = []
    for item in year_list:
        first_four_chars = item[:4]  # Extract the first four characters
        number = int(first_four_chars)  # Convert the extracted characters to an integer
        modified_list.append(number)  # Add the integer to the result list
    return modified_list

def get_current_year(date_obj):
    year = date_obj.year
    month = date_obj.month
    if(month >= 7):
        return year
    return (year - 1)

def find_smallest_year(file_path):
    
    # Step 1: Read the CSV file into a DataFrame
    df_years = pd.read_csv(file_path)

    # Step 2: Extract the first four characters from each row, starting from the 2nd row
    # and convert them to integers
    years_list = []
    for i in range(0, len(df_years)):
        item = df_years.iloc[i, 0]  # Assuming the first column contains the values you want to convert
        first_four_chars = item[:4]
        number = int(first_four_chars)
        years_list.append(number)

    # Step 3: Find the smallest integer among the extracted integers
    smallest_year = min(years_list)

    return smallest_year

def find_smallest_year_from_my_data(file_path):
    
    # Read the CSV file into a DataFrame
    df = pd.read_csv(file_path)

    # Extract years from the date values
    df['Year'] = pd.to_datetime(df.iloc[:, 0]).dt.year

    # Find the smallest year
    smallest_year = df['Year'].min()

    return smallest_year

def delete_columns(file_path):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(file_path)

    # Get the number of columns in the DataFrame
    num_columns = len(df.columns)

    # Calculate the range of column indices to delete
    start_index = 13
    end_index = num_columns - 8

    # Delete the columns within the specified range
    df = df.drop(df.columns[start_index:end_index], axis=1)

    # Save the modified DataFrame back to the CSV file
    df.to_csv(file_path, index=False)

def add_columns_with_values(file_path,smallest_year,current_year):

    # Step 1: Read the CSV file into a DataFrame

    year_elapsed = current_year - smallest_year
    df = pd.read_csv(file_path)

    # Step 2: Get the current number of columns
    num_columns = len(df.columns)
    num_rows = df.shape[0]

    # Step 3: Create a list of empty values for the new columns
    empty_values = [np.nan] * num_rows
    # df = df.drop(df.columns[6], axis=1)
    # df.insert(loc=6, column='NewCol1',value=empty_values)

    pre_year = smallest_year
    post_year = smallest_year + 1
    for i in range(year_elapsed + 1):
        column_value = str(pre_year) + '-' + str(post_year)
        df.insert(loc=13 + i, column=column_value,value=empty_values)
        pre_year +=1
        post_year +=1

    # Step 4: Insert the new columns at the desired position (6th column)
    #df.insert(loc=6, column='NewCol1',value=empty_values)
    # df.insert(loc=num_columns + 1, column='NewCol2', value=empty_values)

    # Step 5: Assign values to the first row of the new columns
    #df.loc[0, 'NewCol1'] = 'Value1'

    # Step 6: Save the modified DataFrame back to the CSV file
    df.to_csv(file_path, index=False)

# Extract the data from the 5th to 10th columns of the 1st row
def asset_register(request):
    file_path = 'csv_path/my_data.csv'
    df_my_data = pd.read_csv(file_path)
    len_my_data = len(df_my_data)
    header_row = df_my_data.columns.tolist()
    if(len_my_data > 1):
        df_my_data = pd.read_csv(file_path, skiprows= 1)
    df_depreciation = pd.read_csv('csv_path/depriciation.csv')

    len_csv = len(df_depreciation)

    if(len_csv > 2):
        df_depreciation = pd.read_csv('csv_path/depriciation.csv', skiprows= 1)

        # Iterate through each row, excluding the header
        for index, row in df_depreciation.iterrows():
            if row.iloc[0] == '2023-2024':
                # Change the value of the 6th column (index 5) to 'New'
                df_my_data.at[index, df_my_data.columns[5]] = 'New'
        df_my_data.to_csv(file_path, index=False)

        new_file_path = 'csv_path/my_data.csv'
        df_another_data = pd.read_csv(new_file_path, header=None)
        df_another_data.columns = header_row
        df_another_data.to_csv(new_file_path, index=False)
    
    page_header = ['Economic Code','Particulars','Balance ( Pre MAB assets)','Accumulated Purchases( Post MAB)','Purchases (New)','Total','Rate ( Pre MAB Assets)','Rate ( Post MAB Assets)','Accumulated Depreciation','Depreciation ( Pre MAB)','Depreciation (Post MAB)','Depreciation ( New Purchases)','Depreciation Charges','Total Accumulated Depreciation','WDV','Status']
    result_rows = []

    file_path = 'csv_path/output_asset_register.csv'

    # Writing data to CSV file
    with open(file_path, 'w', newline='') as file:
        writer = csv.writer(file)
        
        # Write the page_header as the first row
        writer.writerow(page_header)
        
        # Write the result_rows as subsequent rows
        writer.writerows(result_rows)

    file_path = 'csv_path/my_data.csv'

    # Read the CSV file into a DataFrame
    df = pd.read_csv(file_path)

    # Count the number of rows in the DataFrame
    len_csv = len(df)
    len_csv = len_csv - 1
    page_header = ['Economic Code','Particulars','Balance ( Pre MAB assets)','Accumulated Purchases( Post MAB)','Purchases (New)','Total','Rate ( Pre MAB Assets)','Rate ( Post MAB Assets)','Accumulated Depreciation','Depreciation ( Pre MAB)','Depreciation (Post MAB)','Depreciation ( New Purchases)','Depreciation Charges','Total Accumulated Depreciation','WDV','Status']
    result_rows = []

    if request.method == 'POST' and len_csv > 0:
        page_header = ['Economic Code','Particulars','Balance ( Pre MAB assets)','Accumulated Purchases( Post MAB)','Purchases (New)','Total','Rate ( Pre MAB Assets)','Rate ( Post MAB Assets)','Accumulated Depreciation','Depreciation ( Pre MAB)','Depreciation (Post MAB)','Depreciation ( New Purchases)','Depreciation Charges','Total Accumulated Depreciation','WDV','Status']
        result_rows = []
        csv_files = ['csv_path/my_data.csv','csv_path/depriciation.csv','csv_path/asset_schedule.csv']  # Replace with your file paths
        for file in csv_files:
            # Read only the first row of the CSV file (header row)
            header_row = pd.read_csv(file, nrows=1, header=None)

            header_row.to_csv(file, index=False, header=False)
        file_path = 'csv_path/output_asset_register.csv'

        # Writing data to CSV file
        with open(file_path, 'w', newline='') as file:
            writer = csv.writer(file)
            
            # Write the page_header as the first row
            writer.writerow(page_header)
            
            # Write the result_rows as subsequent rows
            writer.writerows(result_rows)
                    

    elif len_csv > 0:
        # Define a function to parse 'Purchase Date' column as dates with the specified format
        date_parser = lambda x: pd.to_datetime(x, format='%m/%d/%Y')
        df = pd.read_csv('csv_path/my_data.csv')

        # Read the CSV file and parse 'Purchase Date' as dates with the specified format
        df['Purchase Date'] = pd.to_datetime(df['Purchase Date'], format='%m/%d/%Y')

        # Convert 'Purchase Date' column to the desired string format ('mm/dd/yyyy')
        df['Purchase Date'] = df['Purchase Date'].dt.strftime('%m/%d/%Y')

        df_backend = pd.read_csv('backend_csv/check.csv')

        header = df.columns.tolist()
        rows = df.values.tolist()
    
        df_dep = pd.read_csv('csv_path/depriciation.csv')
        if df_dep.shape[0] != 0:
            smallest_year = find_smallest_year('csv_path/depriciation.csv')
            current_year = get_current_year(date.today())

            current_year_elapsed = current_year - smallest_year
            pre_year_elapsed = int(df_backend.iloc[0, 0])

            if(current_year_elapsed != pre_year_elapsed):
                df_backend.iat[0, 0] = current_year_elapsed
                df_backend.to_csv('backend_csv/check.csv', index=False)
                delete_columns('csv_path/depriciation.csv')
                add_columns_with_values('csv_path/depriciation.csv',smallest_year,current_year)
            
            df = pd.read_csv('csv_path/depriciation.csv')
            num_columns = len(df.columns)
            start_index = 13
            end_index = num_columns - 8

            for row_index, row in df.iterrows():
                year_passed = 0
                current_row_year = row[0]
                first_four_chars = current_row_year[:4]
                current_row_year = int(first_four_chars)
                for column_index in range(start_index, end_index):
                    current_column_year = df.columns[column_index]
                    first_four_chars = current_column_year[:4]
                    current_column_year = int(first_four_chars)
                    if(current_column_year < current_row_year or year_passed >= row[-6]):
                        df.iat[row_index, column_index] = 0
                    else:
                        year_passed += 1
                        depriciation_rate = float(row[-8])
                        if isinstance(row[8], str) and ',' in row[8]:
                            price = float(row[8].replace(',', ''))
                        else:
                            price = float(row[8])
                        df.iat[row_index, column_index] = depriciation_rate*price
                    df.to_csv('csv_path/depriciation.csv', index=False)

        csv_file_path = 'csv_path/depriciation.csv'
        data = read_csv_file(csv_file_path)

        df_my_data = pd.read_csv('csv_path/my_data.csv')

        df_my_data['Purchase Date'] = pd.to_datetime(df_my_data['Purchase Date'], format='%m/%d/%Y')

        df_backend = pd.read_csv('backend_csv/check.csv')


        #delete previous data---------------
        df_dep = pd.read_csv(csv_file_path)

        # Keep only the header row
        header_row = df_dep.iloc[0:0]

        # Overwrite the DataFrame with the header row
        df_dep = header_row

        # Save the DataFrame back to the same CSV file
        df_dep.to_csv(csv_file_path, index=False)
        #delete previous data---------------

        # Extract the data (excluding the header row)
        my_data_list = df_my_data.values.tolist()[0:]  # Exclude the column row

        

        for  row_ind,my_data_row in enumerate(my_data_list):
            #inp
            purchase_date = my_data_list[row_ind][0].date()  # Assuming this is your date string in 'YYYY-MM-DD' format



            # Extract year and month from the original 'YYYY-MM-DD' format
            # purchase_year, purchase_month, _ = purchase_date.split('-')
            purchase_year = purchase_date.year
            purchase_month = purchase_date.month

            if(purchase_month <= 6):
                purchase_year -= 1

            financial_year = str(purchase_year) + '-' + str(purchase_year + 1)

            #inp
            form_inputs = []
            
            serial_no = my_data_list[row_ind][1]
            form_inputs.append(serial_no)
            bill_no = my_data_list[row_ind][2]
            bill_no = int(bill_no)
            form_inputs.append(bill_no)
            category = my_data_list[row_ind][3]
            form_inputs.append(category)
            category_from_user = category
            depriciation_method = my_data_list[row_ind][9]
            form_inputs.append(depriciation_method)
            name_of_item = my_data_list[row_ind][4]
            form_inputs.append(name_of_item)
            quantity_str = my_data_list[row_ind][6]
            quantity = extract_numbers(quantity_str)
            form_inputs.append(quantity_str)
            price = my_data_list[row_ind][7]
            if isinstance(price, str) and ',' in price:
                price = float(price.replace(',', ''))
            else:
                price = float(price)
            # df.iat[row_index, column_index] = depriciation_rate*price
            form_inputs.append(price)
            sold_quantity = my_data_list[row_ind][8]
            form_inputs.append(sold_quantity)
            location = my_data_list[row_ind][10]
            form_inputs.append(location)
            current_condition = my_data_list[row_ind][11]
            form_inputs.append(current_condition)

            csv_file_path = 'csv_path/asset_info/asset_info.csv'
            df = pd.read_csv(csv_file_path)

            # Extract values from the first column      
            dropdown_depreciation = df.iloc[:, 4].tolist()

            row_index = 0
            df = pd.read_csv('csv_path/asset_info/asset_info.csv')
            matching_rows = df.loc[df.iloc[:, 0] == category_from_user]

            # Get the index of the first matched row
            if len(matching_rows) > 0:
                row_index = matching_rows.index[0]

            row_data = get_row_by_index('csv_path/asset_info/asset_info.csv', row_index)

            economic_code = row_data[2]
            asset_code = 'asset_code'
            expected_life = row_data[3]
            deprication_rate = 1/row_data[3]
            var_quantity = quantity
            var_price = price
            var_sold_quantity = sold_quantity
            var_deprication_rate = 1/row_data[3]
            var_deprication_rate = round(var_deprication_rate, 2)
            if var_quantity == 0:
                costs_of_asset_sold = 0
            else:
                costs_of_asset_sold = (var_price / var_quantity)*var_sold_quantity
                costs_of_asset_sold = round(costs_of_asset_sold, 2)
            current_balance = var_price - (var_price / var_quantity)*var_sold_quantity
            current_balance = round(current_balance, 2)
            accumulated_depriciation_for_sold_items = var_price*var_deprication_rate
            accumulated_depriciation_for_sold_items = round(accumulated_depriciation_for_sold_items, 2)
            net_accumulated_depricaition = var_price*var_deprication_rate
            net_accumulated_depricaition = round(net_accumulated_depricaition, 2)
            year_elapsed = 3
            asset_code_generated = 'asset_code_gen'

            #(var_price / var_quantity)*var_sold_quantity

            # var_price - (var_price / var_quantity)*var_sold_quantity\
            # var_price*var_deprication_rate
            # var_price - var_price*var_deprication_rate

            depreciation_inputs = []

            depreciation_inputs = []
            
            depreciation_inputs.append("dshf")

            depreciation_inputs.clear()
            depreciation_inputs.extend((financial_year, purchase_date, serial_no, bill_no, economic_code, category, name_of_item, quantity_str, price, sold_quantity, costs_of_asset_sold, current_balance, year_elapsed, deprication_rate, asset_code, expected_life, depriciation_method, location,current_condition, accumulated_depriciation_for_sold_items, net_accumulated_depricaition))

            csv_file_path = 'csv_path/depriciation.csv'
            
            # Read existing CSV file into DataFrame
            df_depreciation = pd.read_csv(csv_file_path)

            num_columns = len(df_depreciation.columns)
            start_index = 13
            end_index = num_columns - 8
            for i in range(start_index, end_index):
                depreciation_inputs.insert(i,0)
            
            # Create a new DataFrame with user input as a row
            new_row = pd.DataFrame([depreciation_inputs], columns=df_depreciation.columns)
            
            # Concatenate the existing DataFrame with the new row
            df_depreciation = pd.concat([df_depreciation, new_row], ignore_index=True)
            
            # Write the updated DataFrame to the CSV file
            df_depreciation.to_csv(csv_file_path, index=False)



            csv_file_path = 'csv_path/depriciation.csv'

            df = pd.read_csv('csv_path/my_data.csv')
            df_backend = pd.read_csv('backend_csv/check.csv')

            df_dep = pd.read_csv('csv_path/depriciation.csv')
            # if df_dep.shape[0] != 0:
            smallest_year = find_smallest_year('csv_path/depriciation.csv')
            current_year = get_current_year(date.today())

            current_year_elapsed = current_year - smallest_year
            pre_year_elapsed = int(df_backend.iloc[0, 0])

            if(current_year_elapsed != pre_year_elapsed):
                df_backend.iat[0, 0] = current_year_elapsed
                df_backend.to_csv('backend_csv/check.csv', index=False)
                delete_columns('csv_path/depriciation.csv')
                add_columns_with_values('csv_path/depriciation.csv',smallest_year,current_year)

            #df_backend.iat[0, 0] = 
            df = pd.read_csv('csv_path/depriciation.csv')
            num_columns = len(df.columns)
            start_index = 13
            end_index = num_columns - 8

            
            if df_my_data.shape[0] != 0:
                smallest_year = find_smallest_year_from_my_data('csv_path/my_data.csv')
                current_year = get_current_year(date.today())

                current_year_elapsed = current_year - smallest_year
                pre_year_elapsed = int(df_backend.iloc[0, 0])

                if(current_year_elapsed != pre_year_elapsed):
                    df_backend.iat[0, 0] = current_year_elapsed
                    df_backend.to_csv('backend_csv/check.csv', index=False)
                    delete_columns('csv_path/depriciation.csv')
                    add_columns_with_values('csv_path/depriciation.csv',smallest_year,current_year)
                
                df = pd.read_csv('csv_path/depriciation.csv')
                num_columns = len(df.columns)
                start_index = 13
                end_index = num_columns - 8
                random_data = 100
                for row_index, row in df.iterrows():
                    random_data = df_my_data.shape[0]
                    year_passed = 0
                    current_row_year = row[0]
                    first_four_chars = current_row_year[:4]
                    current_row_year = int(first_four_chars)
                    for column_index in range(start_index, end_index):
                        current_column_year = df.columns[column_index]
                        first_four_chars = current_column_year[:4]
                        current_column_year = int(first_four_chars)
                        if(current_column_year < current_row_year  or year_passed >= row[-6]):
                            df.iat[row_index, column_index] = 0
                        else:
                            year_passed += 1
                            depriciation_rate = float(row[-8])
                            if isinstance(row[8], str) and ',' in row[8]:
                                price = float(row[8].replace(',', ''))
                            else:
                                price = float(row[8])
                            df.iat[row_index, column_index] = depriciation_rate*price
                        df.to_csv('csv_path/depriciation.csv', index=False)

        page_header = ['Financial Year','Purchase date','Sl','Bill no','Economic Code','Category','Pre/Post/New','Name of Item','Units','Price','Sold (unit)','Cost of Assets Sold','Current Balance','Asset Code','Expected life','Depreciation Method','Location','Current Depreciation','Accumulated depriciation','Current Condition']

        df_depreciation = pd.read_csv('csv_path/depriciation.csv', header=None, skiprows=1)

        result_rows = []
        i = 0
        df_my_data = pd.read_csv('csv_path/my_data.csv', header=None, skiprows=1)
        for index_info, row_info in df_depreciation.iterrows():
            i = i + 1
            new_row = [row_info.iloc[0], row_info.iloc[1], row_info.iloc[2],row_info.iloc[3],row_info.iloc[4],row_info.iloc[5],df_my_data[5][i-1],row_info.iloc[6],row_info.iloc[7],row_info.iloc[8],row_info.iloc[9],row_info.iloc[10],row_info.iloc[11],row_info.iloc[-7],row_info.iloc[-6],row_info.iloc[-5],row_info.iloc[-4],row_info.iloc[-2],row_info.iloc[-1],row_info.iloc[-3]]

            result_rows.append(new_row)

        file_path = 'csv_path/output_asset_register.csv'

        # Writing data to CSV file
        with open(file_path, 'w', newline='') as file:
            writer = csv.writer(file)
            
            # Write the page_header as the first row
            writer.writerow(page_header)
            
            # Write the result_rows as subsequent rows
            writer.writerows(result_rows)

    with open('csv_path/depriciation.csv', newline='') as csvfile:
        reader = csv.reader(csvfile)
        rows = list(reader)  # Convert the CSV reader object to a list

    header_row = rows[0]  # Assuming the first row is the header
    data_rows = rows[1:]  # Rows after the header are data rows

    # Extract unique values from the first column of data rows
    unique_rows_filter = set(row[0] for row in data_rows) 
    unique_rows_filter = sorted(unique_rows_filter, key=lambda x: x[:4])



    return render(request, 'index.html', {'page_header': page_header, 'result_rows': result_rows,'unique_rows_filter:':unique_rows_filter})

def get_row_by_index(csv_file_path, row_index):
    # Read CSV file into DataFrame
    df = pd.read_csv(csv_file_path)

    # Retrieve the row at the specified index
    row = df.iloc[row_index].tolist()

    return row

def data_entry(request):
    column_names = get_column_names_for_extra_input('csv_path/my_data.csv')
    if request.method == 'POST':
        deprication_inputs = []
        #inp
        # Assuming 'purchase_date' is the date string from request.POST.get('purchase_date')
        purchase_date = request.POST.get('purchase_date')
        purchase_date_model = purchase_date
        

        # Convert the string to a datetime object
        purchase_date = datetime.strptime(purchase_date, '%Y-%m-%d')
        purchase_year = purchase_date.year
        purchase_month = purchase_date.month

        purchase_date = purchase_date.strftime('%m/%d/%Y')
        # Extract year and month
        # purchase_year = purchase_date.year
        # purchase_month = purchase_date.month


        if(purchase_month <= 6):
            purchase_year -= 1

        financial_year = str(purchase_year) + '-' + str(purchase_year + 1)

        #inp
        serial_no = request.POST.get('serial_no')
        bill_no = request.POST.get('bill_no')
        category = request.POST.get('category')
        category_from_user = category
        name_of_item = request.POST.get('name_of_item')
        quantity = request.POST.get('quantity')
        price = float(request.POST.get('price'))
        sold_quantity = request.POST.get('sold_quantity')
        depriciation_method = request.POST.get('depriciation_method')
        deprication_rate = request.POST.get("deprication_rate")
        #form_inputs.append(deprication_rate)
        location = request.POST.get('location')
        current_condition = request.POST.get('current_condition')

        new_input_field = input_field(purchase_date=purchase_date_model, serial_no=serial_no,bill_no = bill_no,category = category,name_of_item = name_of_item, quantity = quantity,price = price,sold_quantity = sold_quantity,location = location,current_condition = current_condition)
        new_input_field.save()

        #inp
        form_inputs = []
        for field_name, field_value in request.POST.items():
            if field_name != 'csrfmiddlewaretoken':
                form_inputs.append(field_value)

        form_inputs.pop(0)
        form_inputs.insert(0,purchase_date)
        form_inputs.insert(5,'Post')
        
        csv_file_path = 'csv_path/my_data.csv'
        
        # Read existing CSV file into DataFrame
        df = pd.read_csv(csv_file_path)
        
        # Create a new DataFrame with user input as a row
        new_row = pd.DataFrame([form_inputs], columns=df.columns)
        
        # Concatenate the existing DataFrame with the new row
        df = pd.concat([df, new_row], ignore_index=True)
        
        # Write the updated DataFrame to the CSV file
        df.to_csv(csv_file_path, index=False)
        
        csv_file_path = 'csv_path/asset_info/asset_info.csv'
        df = pd.read_csv(csv_file_path)

        # Extract values from the first column      
        dropdown_categories = df.iloc[:, 0].tolist()

        csv_file_path = 'csv_path/asset_info/asset_info.csv'
        df = pd.read_csv(csv_file_path)

        # Extract values from the first column      
        dropdown_depreciation = df.iloc[:, 5].tolist()

        row_index = 0
        df = pd.read_csv('csv_path/asset_info/asset_info.csv')
        matching_rows = df.loc[df.iloc[:, 0] == category_from_user]

        # Get the index of the first matched row
        if len(matching_rows) > 0:
            row_index = matching_rows.index[0]

        row_data = get_row_by_index('csv_path/asset_info/asset_info.csv', row_index)

        economic_code = row_data[2]
        asset_code = 'asdf'
        expected_life = row_data[3]
        deprication_rate = 1/row_data[3]
        var_quantity = quantity
        var_price = price
        var_sold_quantity = sold_quantity
        var_deprication_rate = 1/row_data[3]
        costs_of_asset_sold = 2
        current_balance = 3
        accumulated_depriciation_for_sold_items = var_price*var_deprication_rate
        net_accumulated_depricaition = var_price - var_price*var_deprication_rate
        year_elapsed = 3
        asset_code_generated = 'asset_code_gen'

        #(var_price / var_quantity)*var_sold_quantity
        #var_price - (var_price / var_quantity)*var_sold_quantity

        depreciation_inputs = []

        depreciation_inputs = []
        for field_name, field_value in request.POST.items():
            if field_name != 'csrfmiddlewaretoken':
                depreciation_inputs.append(field_value)

        depreciation_inputs.clear()
        depreciation_inputs.extend((financial_year, purchase_date, serial_no, bill_no, economic_code, category, name_of_item, quantity, price, sold_quantity, costs_of_asset_sold, current_balance, year_elapsed, deprication_rate, asset_code, expected_life, depriciation_method, location,current_condition, accumulated_depriciation_for_sold_items, net_accumulated_depricaition))

        csv_file_path = 'csv_path/depriciation.csv'
        
        # Read existing CSV file into DataFrame
        df_depreciation = pd.read_csv(csv_file_path)

        num_columns = len(df_depreciation.columns)
        start_index = 13
        end_index = num_columns - 8
        for i in range(start_index, end_index):
            depreciation_inputs.insert(i,0)
        
        # Create a new DataFrame with user input as a row
        new_row = pd.DataFrame([depreciation_inputs], columns=df_depreciation.columns)
        
        # Concatenate the existing DataFrame with the new row
        df_depreciation = pd.concat([df_depreciation, new_row], ignore_index=True)
        
        # Write the updated DataFrame to the CSV file
        df_depreciation.to_csv(csv_file_path, index=False)



        csv_file_path = 'csv_path/depriciation.csv'

        df = pd.read_csv('csv_path/my_data.csv')
        df_backend = pd.read_csv('backend_csv/check.csv')

        df_dep = pd.read_csv('csv_path/depriciation.csv')
        # if df_dep.shape[0] != 0:
        smallest_year = find_smallest_year('csv_path/depriciation.csv')
        current_year = get_current_year(date.today())

        current_year_elapsed = current_year - smallest_year
        pre_year_elapsed = int(df_backend.iloc[0, 0])

        if(current_year_elapsed != pre_year_elapsed):
            df_backend.iat[0, 0] = current_year_elapsed
            df_backend.to_csv('backend_csv/check.csv', index=False)
            delete_columns('csv_path/depriciation.csv')
            add_columns_with_values('csv_path/depriciation.csv',smallest_year,current_year)

        #df_backend.iat[0, 0] = 
        df = pd.read_csv('csv_path/depriciation.csv')
        num_columns = len(df.columns)
        start_index = 13
        end_index = num_columns - 8

        for row_index, row in df.iterrows():
            year_passed = 0
            current_row_year = row[0]
            first_four_chars = current_row_year[:4]
            current_row_year = int(first_four_chars)
            yr_elapsed = current_year  - current_row_year
            df.iat[row_index, 12] = yr_elapsed
            for column_index in range(start_index, end_index):
                current_column_year = df.columns[column_index]
                first_four_chars = current_column_year[:4]
                current_column_year = int(first_four_chars)
                if(current_column_year < current_row_year or year_passed >= row[-6] ):
                    df.iat[row_index, column_index] = 0
                else:
                    year_passed += 1
                    depriciation_rate = float(row[-8])
                    price = float(row[8])
                    df.iat[row_index, column_index] = depriciation_rate*price
                df.to_csv('csv_path/depriciation.csv', index=False)

            unique_set = set(dropdown_depreciation)

            # Convert the set back to a list (optional)
            unique_list = list(unique_set)



        return render(request, 'data_entry.html',{'column_names': column_names,'dropdown_categories': dropdown_categories,'unique_list':unique_list})


    csv_file_path = 'csv_path/asset_info/asset_info.csv'
    df = pd.read_csv(csv_file_path)

    # Extract values from the first column
    dropdown_categories = df.iloc[:, 0].tolist()

    csv_file_path = 'csv_path/asset_info/asset_info.csv'
    df = pd.read_csv(csv_file_path)

    # Extract values from the first column      
    dropdown_depreciation = df.iloc[:, 5].tolist()
    # Convert the list to a set to remove duplicates
    unique_set = set(dropdown_depreciation)

    # Convert the set back to a list (optional)
    unique_list = list(unique_set)

    return render(request, "data_entry.html",{'column_names': column_names,'dropdown_categories': dropdown_categories,'unique_list':unique_list})

def modify_database(request):
    csv_path = 'csv_path/my_data.csv'
    row_index = 0
    data = []

    if request.method == 'POST':
        clicked_button = request.POST.get('clicked_button', '')
    
        with open(csv_path, 'r') as csv_file:
            reader = csv.reader(csv_file)
            rows = list(reader)

            # Append the values of the specified row to the list of row_values
        for value in rows[row_index]:
            data.append(value)

        for key, value in request.POST.items():
            if key != 'csrfmiddlewaretoken':  # Exclude the CSRF token
                data.append(value)

        rows[row_index] = data

        # Write the modified list of lists back to the CSV file
        with open(csv_path, 'w', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerows(rows)

    df = pd.read_csv('csv_path/my_data.csv')
    column_names = df.columns.tolist()
    del column_names[5]
    return render(request, 'modify_database.html', {'column_names': column_names})

def download_predefined_csv(request):
    csv_path = 'csv_path/my_data.csv'  # Replace with the path to your CSV file

    # Read the existing CSV file to retrieve the header row
    with open(csv_path, 'r', newline='') as file:
        reader = csv.reader(file)
        header_row = next(reader)  # Read the header row

    # Exclude the 5th element (index 4) from the header row
    header_row = header_row[:5] + header_row[6:]

    # Generate a CSV file with the retrieved header row
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="predefined_data.csv"'

    writer = csv.writer(response)
    writer.writerow(header_row)  # Write the header row to the downloaded file

    return response


def success(request):
    smallest_year = find_smallest_year_from_my_data('csv_path/my_data.csv')
    return render(request, "success.html",{'smallest_year': smallest_year})


def genSchedule(request):
    return render(request, "genSchedule.html")

def depriciation(request):
    #new---------------
    csv_file_path = 'csv_path/depriciation.csv'
    data = read_csv_file(csv_file_path)

    df_my_data = pd.read_csv('csv_path/my_data.csv')

    df_my_data['Purchase Date'] = pd.to_datetime(df_my_data['Purchase Date'], format='%m/%d/%Y')

    df_backend = pd.read_csv('backend_csv/check.csv')


    #delete previous data---------------
    df_dep = pd.read_csv(csv_file_path)

    # Keep only the header row
    header_row = df_dep.iloc[0:0]

    # Overwrite the DataFrame with the header row
    df_dep = header_row

    # Save the DataFrame back to the same CSV file
    df_dep.to_csv(csv_file_path, index=False)
    #delete previous data---------------

    # Extract the data (excluding the header row)
    my_data_list = df_my_data.values.tolist()[0:]  # Exclude the column row

    

    for  row_ind,my_data_row in enumerate(my_data_list):
        #inp
        purchase_date = my_data_list[row_ind][0].date()  # Assuming this is your date string in 'YYYY-MM-DD' format



        # Extract year and month from the original 'YYYY-MM-DD' format
        # purchase_year, purchase_month, _ = purchase_date.split('-')
        purchase_year = purchase_date.year
        purchase_month = purchase_date.month

        if(purchase_month <= 6):
            purchase_year -= 1

        financial_year = str(purchase_year) + '-' + str(purchase_year + 1)

        #inp
        form_inputs = []
        
        serial_no = my_data_list[row_ind][1]
        form_inputs.append(serial_no)
        bill_no = my_data_list[row_ind][2]
        form_inputs.append(bill_no)
        category = my_data_list[row_ind][3]
        form_inputs.append(category)
        category_from_user = category
        depriciation_method = my_data_list[row_ind][9]
        form_inputs.append(depriciation_method)
        name_of_item = my_data_list[row_ind][4]
        form_inputs.append(name_of_item)
        quantity_str = my_data_list[row_ind][6]
        quantity = extract_numbers(quantity_str)
        quantity = float(quantity)
        form_inputs.append(quantity_str)
        price = my_data_list[row_ind][7]
        if isinstance(price, str) and ',' in price:
            price = float(price.replace(',', ''))
        else:
            price = float(price)

        form_inputs.append(price)
        sold_quantity = my_data_list[row_ind][8]
        form_inputs.append(sold_quantity)
        location = my_data_list[row_ind][10]
        form_inputs.append(location)
        current_condition = my_data_list[row_ind][11]
        form_inputs.append(current_condition)

        csv_file_path = 'csv_path/asset_info/asset_info.csv'
        df = pd.read_csv(csv_file_path)

        # Extract values from the first column      
        dropdown_depreciation = df.iloc[:, 4].tolist()

        row_index = 0
        df = pd.read_csv('csv_path/asset_info/asset_info.csv')
        matching_rows = df.loc[df.iloc[:, 0] == category_from_user]

        # Get the index of the first matched row
        if len(matching_rows) > 0:
            row_index = matching_rows.index[0]

        row_data = get_row_by_index('csv_path/asset_info/asset_info.csv', row_index)

        economic_code = row_data[2]
        asset_code = 'asset_code'
        expected_life = row_data[3]
        deprication_rate = 1/row_data[3]
        var_quantity = quantity
        var_price = price
        var_sold_quantity = sold_quantity
        var_deprication_rate = (1/row_data[3])
        costs_of_asset_sold = (var_price / 12)*var_sold_quantity
        current_balance = var_price - (var_price / 21)*var_sold_quantity
        accumulated_depriciation_for_sold_items = var_price*var_deprication_rate
        net_accumulated_depricaition = var_price - var_price*var_deprication_rate
        year_elapsed = 3
        asset_code_generated = 'asset_code_gen'

        # var_quantity 571

        depreciation_inputs = []
        
        depreciation_inputs.append("dshf")

        depreciation_inputs.clear()
        depreciation_inputs.extend((financial_year, purchase_date, serial_no, bill_no, economic_code, category, name_of_item, quantity_str, price, sold_quantity, costs_of_asset_sold, current_balance, year_elapsed, deprication_rate, asset_code, expected_life, depriciation_method, location,current_condition, accumulated_depriciation_for_sold_items, net_accumulated_depricaition))

        csv_file_path = 'csv_path/depriciation.csv'
        
        # Read existing CSV file into DataFrame
        df_depreciation = pd.read_csv(csv_file_path)

        num_columns = len(df_depreciation.columns)
        start_index = 13
        end_index = num_columns - 8
        for i in range(start_index, end_index):
            depreciation_inputs.insert(i,0)
        
        # Create a new DataFrame with user input as a row
        new_row = pd.DataFrame([depreciation_inputs], columns=df_depreciation.columns)
        
        # Concatenate the existing DataFrame with the new row
        df_depreciation = pd.concat([df_depreciation, new_row], ignore_index=True)
        
        # Write the updated DataFrame to the CSV file
        df_depreciation.to_csv(csv_file_path, index=False)



        csv_file_path = 'csv_path/depriciation.csv'

        df = pd.read_csv('csv_path/my_data.csv')
        df_backend = pd.read_csv('backend_csv/check.csv')

        df_dep = pd.read_csv('csv_path/depriciation.csv')
        # if df_dep.shape[0] != 0:
        smallest_year = find_smallest_year('csv_path/depriciation.csv')
        current_year = get_current_year(date.today())

        current_year_elapsed = current_year - smallest_year
        pre_year_elapsed = int(df_backend.iloc[0, 0])

        if(current_year_elapsed != pre_year_elapsed):
            df_backend.iat[0, 0] = current_year_elapsed
            df_backend.to_csv('backend_csv/check.csv', index=False)
            delete_columns('csv_path/depriciation.csv')
            add_columns_with_values('csv_path/depriciation.csv',smallest_year,current_year)

        #df_backend.iat[0, 0] = 
        df = pd.read_csv('csv_path/depriciation.csv')
        num_columns = len(df.columns)
        start_index = 13
        end_index = num_columns - 8

        
        if df_my_data.shape[0] != 0:
            smallest_year = find_smallest_year_from_my_data('csv_path/my_data.csv')
            current_year = get_current_year(date.today())

            current_year_elapsed = current_year - smallest_year
            pre_year_elapsed = int(df_backend.iloc[0, 0])

            if(current_year_elapsed != pre_year_elapsed):
                df_backend.iat[0, 0] = current_year_elapsed
                df_backend.to_csv('backend_csv/check.csv', index=False)
                delete_columns('csv_path/depriciation.csv')
                add_columns_with_values('csv_path/depriciation.csv',smallest_year,current_year)
            
            df = pd.read_csv('csv_path/depriciation.csv')
            num_columns = len(df.columns)
            start_index = 13
            end_index = num_columns - 8
            random_data = 100
            for row_index, row in df.iterrows():
                random_data = df_my_data.shape[0]
                year_passed = 0
                current_row_year = row[0]
                first_four_chars = current_row_year[:4]
                current_row_year = int(first_four_chars)
                for column_index in range(start_index, end_index):
                    current_column_year = df.columns[column_index]
                    first_four_chars = current_column_year[:4]
                    current_column_year = int(first_four_chars)
                    if(current_column_year < current_row_year  or year_passed >= row[-6]):
                        df.iat[row_index, column_index] = 0
                    else:
                        year_passed += 1
                        depriciation_rate = float(row[-8])
                        price = float(row[8])
                        df.iat[row_index, column_index] = depriciation_rate*price
                    df.to_csv('csv_path/depriciation.csv', index=False)

    with open('csv_path/depriciation.csv', newline='') as csvfile:
        reader = csv.reader(csvfile)
        rows = list(reader)  # Convert the CSV reader object to a list

    header_row = rows[0]  # Assuming the first row is the header
    data_rows = rows[1:]  # Rows after the header are data rows

    # Extract unique values from the first column of data rows
    unique_rows_filter = set(row[0] for row in data_rows) 
    unique_rows_filter = sorted(unique_rows_filter, key=lambda x: x[:4])

    return render(request, 'depriciation.html', {'data': data,'unique_rows_filter':unique_rows_filter})

def list_test(request):
    smallest_year = find_smallest_year('csv_path/depriciation.csv')
    current_year = get_current_year(date.today())
    return render(request, 'list_test.html',{'smallest_year': smallest_year,'current_year':current_year})

def register(request):
    return render(request, "register.html")


def asset_info(request):
    if request.method == "POST":
        category = request.POST.get('category')
        code = request.POST.get('code')
        economicCode = request.POST.get('economicCode')
        expectedLifePre = request.POST.get('expectedLifePre')
        expectedLifePost = request.POST.get('expectedLifePost')
        depreciationMethod = request.POST.get('depreciationMethod')
        asset_form_inputs_loop = []
        for field_name, field_value in request.POST.items():
            if field_name != 'csrfmiddlewaretoken':
                asset_form_inputs_loop.append(field_value)

        asset_input_field = model_asset_info(category=category, code=code,economic_code = economicCode,expected_life_pre = expectedLifePre, expected_life_post = expectedLifePost,depreciation_method = depreciationMethod)
        asset_input_field.save()

        
        csv_file_path = 'csv_path/asset_info/asset_info.csv'
        
        # Read existing CSV file into DataFrame
        df = pd.read_csv(csv_file_path)
        
        # Create a new DataFrame with user input as a row
        new_row = pd.DataFrame([asset_form_inputs_loop], columns=df.columns)
        
        # Concatenate the existing DataFrame with the new row
        df = pd.concat([df, new_row], ignore_index=True)
        
        # Write the updated DataFrame to the CSV file
        df.to_csv(csv_file_path, index=False)

    return render(request, "asset_info.html")

def current_asset_info(request):
    df = pd.read_csv('csv_path/asset_info/asset_info.csv')

    header = df.columns.tolist()
    rows = df.values.tolist()

    return render(request, "current_asset_info.html",{'header': header, 'rows': rows})

def file_upload(request):
    if request.method == 'POST' and request.FILES['file']:
        uploaded_file = request.FILES['file']
        
        # Read the uploaded CSV file
        df_uploaded = pd.read_csv(uploaded_file)
        df_uploaded.insert(5, 'Pre/Post', 'Post')
        
        # Merge with another file (assuming 'another_file.csv' exists)
        df_actual = pd.read_csv('csv_path/my_data.csv')
        df_actual = pd.concat([df_actual, df_uploaded], ignore_index=True)

        # Save the merged DataFrame as df_another.csv
        df_actual.to_csv('csv_path/my_data.csv', index=False)
    
    return render(request, "file_upload.html")

df = pd.read_csv('csv_path/asset_schedule.csv')

def data_entry_pre(request):
    column_names = get_column_names_for_extra_input('csv_path/my_data.csv')
    if request.method == 'POST':
        deprication_inputs = []
        #inp
        # Assuming 'purchase_date' is the date string from request.POST.get('purchase_date')
        purchase_date = request.POST.get('purchase_date')
        purchase_date_model = purchase_date
        

        # Convert the string to a datetime object
        purchase_date = datetime.strptime(purchase_date, '%Y-%m-%d')
        purchase_year = purchase_date.year
        purchase_month = purchase_date.month

        purchase_date = purchase_date.strftime('%m/%d/%Y')
        # Extract year and month
        # purchase_year = purchase_date.year
        # purchase_month = purchase_date.month


        if(purchase_month <= 6):
            purchase_year -= 1

        financial_year = str(purchase_year) + '-' + str(purchase_year + 1)

        #inp
        serial_no = request.POST.get('serial_no')
        bill_no = request.POST.get('bill_no')
        category = request.POST.get('category')
        category_from_user = category
        name_of_item = request.POST.get('name_of_item')
        quantity = float(request.POST.get('quantity') or 0)
        price = float(request.POST.get('price'))
        sold_quantity = float(request.POST.get('sold_quantity'))
        depriciation_method = request.POST.get('depriciation_method')
        deprication_rate = request.POST.get("deprication_rate")
        #form_inputs.append(deprication_rate)
        location = request.POST.get('location')
        current_condition = request.POST.get('current_condition')

        new_input_field = input_field(purchase_date=purchase_date_model, serial_no=serial_no,bill_no = bill_no,category = category,name_of_item = name_of_item, quantity = quantity,price = price,sold_quantity = sold_quantity,location = location,current_condition = current_condition)
        new_input_field.save()

        #inp
        form_inputs = []
        for field_name, field_value in request.POST.items():
            if field_name != 'csrfmiddlewaretoken':
                form_inputs.append(field_value)

        form_inputs.pop(0)
        form_inputs.insert(0,purchase_date)
        form_inputs.insert(5,'Pre')
        
        csv_file_path = 'csv_path/my_data.csv'
        
        # Read existing CSV file into DataFrame
        df = pd.read_csv(csv_file_path)
        
        # Create a new DataFrame with user input as a row
        new_row = pd.DataFrame([form_inputs], columns=df.columns)
        
        # Concatenate the existing DataFrame with the new row
        df = pd.concat([df, new_row], ignore_index=True)
        
        # Write the updated DataFrame to the CSV file
        df.to_csv(csv_file_path, index=False)
        
        csv_file_path = 'csv_path/asset_info/asset_info.csv'
        df = pd.read_csv(csv_file_path)

        # Extract values from the first column      
        dropdown_categories = df.iloc[:, 0].tolist()

        csv_file_path = 'csv_path/asset_info/asset_info.csv'
        df = pd.read_csv(csv_file_path)

        # Extract values from the first column      
        dropdown_depreciation = df.iloc[:, 5].tolist()

        row_index = 0
        df = pd.read_csv('csv_path/asset_info/asset_info.csv')
        matching_rows = df.loc[df.iloc[:, 0] == category_from_user]

        # Get the index of the first matched row
        if len(matching_rows) > 0:
            row_index = matching_rows.index[0]

        row_data = get_row_by_index('csv_path/asset_info/asset_info.csv', row_index)

        economic_code = row_data[2]
        asset_code = 'asdf'
        expected_life = row_data[3]
        deprication_rate = 1/row_data[3]
        var_quantity = quantity
        var_price = price
        var_sold_quantity = sold_quantity
        var_deprication_rate = 1/row_data[3]
        costs_of_asset_sold = (var_price / var_quantity)*var_sold_quantity
        current_balance = var_price - (var_price / var_quantity)*var_sold_quantity
        accumulated_depriciation_for_sold_items = var_price*var_deprication_rate
        net_accumulated_depricaition = var_price - var_price*var_deprication_rate
        year_elapsed = 3
        asset_code_generated = 'asset_code_gen'

        depreciation_inputs = []

        depreciation_inputs = []
        for field_name, field_value in request.POST.items():
            if field_name != 'csrfmiddlewaretoken':
                depreciation_inputs.append(field_value)

        depreciation_inputs.clear()
        depreciation_inputs.extend((financial_year, purchase_date, serial_no, bill_no, economic_code, category, name_of_item, quantity, price, sold_quantity, costs_of_asset_sold, current_balance, year_elapsed, deprication_rate, asset_code, expected_life, depriciation_method, location,current_condition, accumulated_depriciation_for_sold_items, net_accumulated_depricaition))

        csv_file_path = 'csv_path/depriciation.csv'
        
        # Read existing CSV file into DataFrame
        df_depreciation = pd.read_csv(csv_file_path)

        num_columns = len(df_depreciation.columns)
        start_index = 13
        end_index = num_columns - 8
        for i in range(start_index, end_index):
            depreciation_inputs.insert(i,0)
        
        # Create a new DataFrame with user input as a row
        new_row = pd.DataFrame([depreciation_inputs], columns=df_depreciation.columns)
        
        # Concatenate the existing DataFrame with the new row
        df_depreciation = pd.concat([df_depreciation, new_row], ignore_index=True)
        
        # Write the updated DataFrame to the CSV file
        df_depreciation.to_csv(csv_file_path, index=False)



        csv_file_path = 'csv_path/depriciation.csv'

        df = pd.read_csv('csv_path/my_data.csv')
        df_backend = pd.read_csv('backend_csv/check.csv')

        df_dep = pd.read_csv('csv_path/depriciation.csv')
        # if df_dep.shape[0] != 0:
        smallest_year = find_smallest_year('csv_path/depriciation.csv')
        current_year = get_current_year(date.today())

        current_year_elapsed = current_year - smallest_year
        pre_year_elapsed = int(df_backend.iloc[0, 0])

        if(current_year_elapsed != pre_year_elapsed):
            df_backend.iat[0, 0] = current_year_elapsed
            df_backend.to_csv('backend_csv/check.csv', index=False)
            delete_columns('csv_path/depriciation.csv')
            add_columns_with_values('csv_path/depriciation.csv',smallest_year,current_year)

        #df_backend.iat[0, 0] = 
        df = pd.read_csv('csv_path/depriciation.csv')
        num_columns = len(df.columns)
        start_index = 13
        end_index = num_columns - 8

        for row_index, row in df.iterrows():
            year_passed = 0
            current_row_year = row[0]
            first_four_chars = current_row_year[:4]
            current_row_year = int(first_four_chars)
            yr_elapsed = current_year  - current_row_year
            df.iat[row_index, 12] = yr_elapsed
            for column_index in range(start_index, end_index):
                current_column_year = df.columns[column_index]
                first_four_chars = current_column_year[:4]
                current_column_year = int(first_four_chars)
                if(current_column_year < current_row_year or year_passed >= row[-6] ):
                    df.iat[row_index, column_index] = 0
                else:
                    year_passed += 1
                    depriciation_rate = float(row[-8])
                    price = float(row[8])
                    df.iat[row_index, column_index] = depriciation_rate*price
                df.to_csv('csv_path/depriciation.csv', index=False)

        csv_file_path = 'csv_path/asset_info/asset_info.csv'
        df = pd.read_csv(csv_file_path)

        # Extract values from the first column      
        dropdown_depreciation = df.iloc[:, 5].tolist()
        # Convert the list to a set to remove duplicates
        unique_set = set(dropdown_depreciation)

        # Convert the set back to a list (optional)
        unique_list = list(unique_set)


        return render(request, 'data_entry_pre.html',{'column_names': column_names,'dropdown_categories': dropdown_categories,'unique_list':unique_list})


    csv_file_path = 'csv_path/asset_info/asset_info.csv'
    df = pd.read_csv(csv_file_path)

    # Extract values from the first column
    dropdown_categories = df.iloc[:, 0].tolist()

    csv_file_path = 'csv_path/asset_info/asset_info.csv'
    df = pd.read_csv(csv_file_path)

    # Extract values from the first column      
    dropdown_depreciation = df.iloc[:, 5].tolist()
    # Convert the list to a set to remove duplicates
    unique_set = set(dropdown_depreciation)

    # Convert the set back to a list (optional)
    unique_list = list(unique_set)

    return render(request, "data_entry_pre.html",{'column_names': column_names,'dropdown_categories': dropdown_categories,'unique_list':unique_list})

def asset_schedule(request):
    file_path = 'csv_path/my_data.csv'

    # Read the CSV file into a DataFrame
    df = pd.read_csv(file_path)

    # Count the number of rows in the DataFrame
    len_csv = len(df)
    len_csv = len_csv - 1
    # Initialize an empty list to store the rows
    page_header = ['Economic Code','Particulars','Balance ( Pre MAB assets)','Accumulated Purchases( Post MAB)','Purchases (New)','Total','Rate ( Pre MAB Assets)','Rate ( Post MAB Assets)','Accumulated Depreciation','Depreciation ( Pre MAB)','Depreciation (Post MAB)','Depreciation ( New Purchases)','Depreciation Charges','Total Accumulated Depreciation','WDV','Status']
    rows = []
    if len_csv > 0:
    # Read the CSV files into dataframes, skipping the header row
        df_asset_info = pd.read_csv('csv_path/asset_info/asset_info.csv', header=None, skiprows = 1)
        df_asset_register = pd.read_csv('csv_path/my_data.csv', header=None, skiprows=1)

        # Initialize an empty list to store the rows
        page_header = ['Economic Code','Particulars','Balance ( Pre MAB assets)','Accumulated Purchases( Post MAB)','Purchases (New)','Total','Rate ( Pre MAB Assets)','Rate ( Post MAB Assets)','Accumulated Depreciation','Depreciation ( Pre MAB)','Depreciation (Post MAB)','Depreciation ( New Purchases)','Depreciation Charges','Total Accumulated Depreciation','WDV','Status']
        
        # new_row = [row_info.iloc[2], row_info.iloc[0], sum_seventh_element_pre, sum_seventh_element_post,0,total,pre_rate_percentage, post_rate_percentage,0,depriciation_pre,depriciation_post,0,depriciation_charges]

        result_rows = []
        result_rows.append(page_header)

        # Loop through each row in df_asset_info
        for index_info, row_info in df_asset_info.iterrows():
            asset_code_info = row_info.iloc[0]  # Second value of current df_asset_info row

            sum_seventh_element_pre = sum_seventh_element_new = 0
            sum_seventh_element_post = 0
            present = 0
            pre_rate = pre_rate_percentage = post_rate = post_rate_percentage = depriciation_pre = depriciation_post = 0


            # Loop through each row in df_asset_register
            for index_reg, row_reg in df_asset_register.iterrows():
                taka = extract_numbers(str(row_reg.iloc[7]))
                asset_code_reg = row_reg.iloc[3]  # Fourth element of df_asset_register row
                pre_post_reg = row_reg.iloc[5]  # Sixth element of df_asset_register row
                pre_rate = pre_rate_percentage = post_rate = post_rate_percentage = depriciation_pre = depriciation_post = 0

                # Check if the conditions are met
                if asset_code_info == asset_code_reg:
                    present = 1
                    if pre_post_reg == 'Pre':
                        # Calculate the sum of the 8th element of df_asset_info rows (7th in 0-based indexing)
                        sum_seventh_element_pre = sum_seventh_element_pre + float(taka)
                    elif pre_post_reg == 'Post':
                        # Calculate the sum of the 8th element of df_asset_info rows (7th in 0-based indexing)
                        sum_seventh_element_post = sum_seventh_element_post + float(taka)
                    elif pre_post_reg == 'New':
                        sum_seventh_element_new = sum_seventh_element_new + float(taka)
            if(row_info.iloc[4] > 0):
                post_rate = 1 / float(row_info.iloc[4])
                depriciation_post = post_rate * sum_seventh_element_post
                post_rate_percentage = "{:.2f}%".format(post_rate * 100)

            if(row_info.iloc[3] > 0):
                pre_rate = 1 / float(row_info.iloc[3])
                depriciation_pre = pre_rate * sum_seventh_element_pre
                pre_rate_percentage = "{:.2f}%".format(pre_rate * 100)

            depriciation_charges = depriciation_pre + depriciation_post + sum_seventh_element_new

            if(present):
                total = sum_seventh_element_post + sum_seventh_element_pre + sum_seventh_element_new
                new_row = [row_info.iloc[2], row_info.iloc[0], sum_seventh_element_pre, sum_seventh_element_post,sum_seventh_element_new,total,pre_rate_percentage, post_rate_percentage,0,depriciation_pre,depriciation_post,depriciation_post,depriciation_charges]
                result_rows.append(new_row)

        # Convert the list of rows into a DataFrame
        result_df = pd.DataFrame(result_rows)

        # Write the DataFrame to a new CSV file
        result_df.to_csv('csv_path/asset_schedule.csv', index=False, header=False)

        df_asset_schedule = pd.read_csv('csv_path/asset_schedule.csv')

        # page_header = df_asset_schedule.columns.tolist()
        rows = df_asset_schedule.values.tolist()


        # rows_list = []
        # with open(csv_file_asset_info, 'r') as file:
        #     reader = csv.reader(file)
        #     header = next(reader)
        #     for row in reader:
        #         del row[2]
        #         # Insert 'New Value' at index 1 (2nd element in zero-based index)
        #         row.insert(1, 'New Value')
                
        #         # Append the modified row to the list
        #         rows_list.append(row)

        # # Append the rows from the first CSV file to the second CSV file
        # with open(csv_file_asset_schedule, 'w', newline='') as file:
        #     writer = csv.writer(file)
        #     writer.writerow(page_header)  # Write the header row
        #     writer.writerows(rows_list)  # Write the modified rows


        #unused code
        context = {
            "df": df,
        }

        #unused code
        #calculation of total, and other respective columns
        # df['Total'] = df['Balance ( Pre MAB assets)']+df['Accumulated Purchases( Post MAB)']+df['Purchases (New)']
        # df['Depreciation ( Pre MAB)'] = df['Balance ( Pre MAB assets)'] * df['Rate ( Pre MAB Assets)']
        # df['Depreciation (Post MAB)'] = df['Accumulated Purchases( Post MAB)'] * df['Rate ( Post MAB Assets)']
        # df['Depreciation ( New Purchases)'] = df['Purchases (New)'] * df['Rate ( Post MAB Assets)']
        # df['Depreciation Charges'] = df['Depreciation ( Pre MAB)'] + df['Depreciation (Post MAB)']+df['Depreciation ( New Purchases)']
        # df['Total Accumulated Depreciation'] = df['Accumulated Depreciatio(opening)'] + df['Depreciation Charges']
        # df['WDV'] = df['Total'] - df['Total Accumulated Depreciation']

    return render(request, "asset_schedule.html", {'page_header':page_header, 'rows': rows})

def file_upload_pre(request):
    if request.method == 'POST' and request.FILES['file']:
        uploaded_file = request.FILES['file']
        
        # Read the uploaded CSV file
        df_uploaded = pd.read_csv(uploaded_file)
        df_uploaded.insert(5, 'Pre/Post', 'Pre')
        
        # Merge with another file (assuming 'another_file.csv' exists)
        df_actual = pd.read_csv('csv_path/my_data.csv')
        df_actual = pd.concat([df_actual, df_uploaded], ignore_index=True)

        # Save the merged DataFrame as df_another.csv
        df_actual.to_csv('csv_path/my_data.csv', index=False)
        
    return render(request, "file_upload_pre.html")

def download_csv(request):
    # Path to your existing CSV file
    existing_csv_file_path = 'csv_path/output_asset_register.csv'  # Replace with your file path

    # Create an HTTP response with CSV content type
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="downloaded_output_asset_register_file.csv"'  # File name to download

    # Write existing CSV file content to the response
    with open(existing_csv_file_path, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            response.write(','.join(row) + '\n')  # Assuming comma-separated values (CSV)

    return response

def download_csv_frc_asset(request):
    # Path to your existing CSV file
    file_path = os.path.join(settings.BASE_DIR, 'csv_path/sample/asset_register.xlsx')

    with open(file_path, 'rb') as file:
        response = HttpResponse(file.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=output_asset_register.xlsx'

    return response

def download_csv_frc_dep(request):
    # Path to your existing CSV file
    file_path = os.path.join(settings.BASE_DIR, 'csv_path/sample/modified_asset_register.xlsx')

    with open(file_path, 'rb') as file:
        response = HttpResponse(file.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=output_depreciation.xlsx'

    return response

def download_csv_frc_asset_schedule(request):
    # Path to your existing CSV file
    file_path = os.path.join(settings.BASE_DIR, 'csv_path/frc_asset_schedule.xlsx')

    with open(file_path, 'rb') as file:
        response = HttpResponse(file.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=output_frc_asset_schedule.xlsx'

    return response

def delete_rows_asset_register(request):
    if request.method == 'POST':
        # Path to your existing Excel file
        file_path = os.path.join(settings.BASE_DIR, 'csv_path/sample/asset_register.xlsx')
        file_path_1 = os.path.join(settings.BASE_DIR, 'csv_path/sample/asset_register.xlsx')

        if os.path.exists(file_path):
            # Read the existing Excel file
            df = pd.read_excel(file_path)

            # Drop all rows except the header
            df = df.head(0)

            # Save the modified DataFrame back to the Excel file
            df.to_excel(file_path, index=False)
            # Read the existing Excel file
            df = pd.read_excel(file_path_1)

            # Drop all rows except the header
            df = df.head(0)

            # Save the modified DataFrame back to the Excel file
            df.to_excel(file_path_1, index=False)
    return redirect('frc_asset_register')

def delete_extra_columns(request):
    if request.method == 'POST':
        # Replace 'file.csv' with your CSV file path
        file_path = 'csv_path/my_data.csv'
        df = pd.read_csv(file_path)

        # Determine the columns to delete
        columns_to_delete = df.columns[12:]  # Columns from last to 8th column from the beginning

        # Drop the columns
        df.drop(columns=columns_to_delete, inplace=True, axis=1)

        # Save the modified DataFrame back to the CSV file
        df.to_csv(file_path, index=False)
    return redirect('modify_database')

def download_csv_dep(request):
    # Path to your existing CSV file
    existing_csv_file_path = 'csv_path/depriciation.csv'  # Replace with your file path

    # Create an HTTP response with CSV content type
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="downloaded_depriciation_file.csv"'  # File name to download

    # Write existing CSV file content to the response
    with open(existing_csv_file_path, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            response.write(','.join(row) + '\n')  # Assuming comma-separated values (CSV)

    return response

def download_csv_schedule(request):

    # Path to your existing CSV file
    existing_csv_file_path = 'csv_path/asset_schedule.csv'  # Replace with your file path

    # Create an HTTP response with CSV content type
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="downloaded_schedule_file.csv"'  # File name to download

    # Write existing CSV file content to the response
    with open(existing_csv_file_path, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            response.write(','.join(row) + '\n')  # Assuming comma-separated values (CSV)

    return response


def extract_numeric(value):
    # Extract numeric values and sum them up
    numbers = re.findall(r'[-+]?\d*\.\d+|\d+', str(value))
    return sum(map(float, numbers))

def calculate_costs(row):
    price = float(row['Price'])
    units = extract_numeric(row['Units'])
    sold_units = extract_numeric(row['Sold (unit)']) if row['Sold (unit)'] != '' else 0

    if units != 0:
        costs_of_asset_sold = (price / units) * sold_units
        current_balance = price - costs_of_asset_sold
    else:
        costs_of_asset_sold = 0
        current_balance = price

    return pd.Series({'Costs of Asset Sold': costs_of_asset_sold, 'Current Balance': current_balance})

def frc_asset_register(request):
    file_path = 'csv_path/sample/asset_register.xlsx'  # Replace with the actual file path
    df = pd.read_excel(file_path)
    
    # Drop the specified columns
    # columns_to_exclude = ['Asset Code', 'Asset Code (!)','Current Depreciation']
    # df = df.drop(columns=columns_to_exclude)
    # Get the current date
    current_date = datetime.now()

    # Determine the year based on the month
    if current_date.month > 6:
        year_variable = str(current_date.year)
    else:
        year_variable = str(current_date.year - 1)

    # Apply the logic to each row
    file_path_t = 'csv_path/sample/asset_register.xlsx'
    # Read the CSV file into a DataFrame
    df_t = pd.read_excel(file_path_t)

    # Count the number of rows in the DataFrame
    len_csv_t = len(df_t)

    if(len_csv_t > 1):
        df["Current Balance"]=df["Price"]-df["Cost of Assets Sold"]
        # Convert the relevant columns to strings and add a new column "Asset Code" after the 4th column
        df.iloc[:, 17] = df.iloc[:, 17].astype(str)
        df.iloc[:, 6] = df.iloc[:, 6].astype(str)
        df.iloc[:, 0] = df.iloc[:, 0].astype(str)
        df.iloc[:, 2] = df.iloc[:, 2].astype(str)

        #Asset_code_generation_updated_by_anik_mallick
        df["Asset Code"]="FRC" + "-" +  df.iloc[:, 19].astype(str).iloc[0]+"-"+df.iloc[:, 18].astype(str).iloc[0] + "-" + df.iloc[:, 6].astype(str).str[:1] + "-" +df.iloc[:, 1].astype(str).str.extract(r'(\d{2})(\d{2})').iloc[:, 1] + "-" +df.iloc[:, 2].astype(str).str[:-2].apply(lambda x: x.zfill(4))
        
        df.fillna('', inplace=True)
        numeric_cols = df.select_dtypes(include='number').columns  # Select numeric columns
        df[numeric_cols] = df[numeric_cols].applymap(lambda x: f'{x:.2f}' if not pd.isnull(x) else '')  # Format numeric values to display 2 decimal places

        # Extract unique values from the first column
        unique_values = df.iloc[:, 0].unique().tolist()

        # Convert all values in the DataFrame to strings
        df = df.astype(str)

        excel_file_path = 'csv_path/sample/asset_register.xlsx'  # Change this to your desired file path

        # Save the DataFrame to an Excel file
        df.to_excel(excel_file_path, index=False)

        # Convert DataFrame to HTML
        excel_html = df.to_html(index=False)

        # Split the HTML table into headers and rows
        header_html = excel_html.split('<tbody>')[0]  # Extract headers part
        rows_html = '<tbody>' + excel_html.split('<tbody>')[1]  # Extract rows part

        return render(request, 'frc_asset_register.html', {'header_html': header_html, 'rows_html': rows_html, 'unique_values': unique_values})

    excel_file_path = 'csv_path/sample/asset_register.xlsx'  # Change this to your desired file path

    # Save the DataFrame to an Excel file
    df.to_excel(excel_file_path, index=False)

    # Convert DataFrame to HTML
    excel_html = df.to_html(index=False)

    # Split the HTML table into headers and rows
    header_html = excel_html.split('<tbody>')[0]  # Extract headers part
    rows_html = '<tbody>' + excel_html.split('<tbody>')[1]  # Extract rows part
        

    return render(request, 'frc_asset_register.html', {'header_html': header_html, 'rows_html': rows_html})


def calculate_values(row):
    # Extract values from the row
    expected_life = float(row['Expected life']) if row['Expected life'] != '' else 0
    price = float(row['Price'])

    # Calculate the formula
    if row.name != 0:  # Skip the header row
        if expected_life != 0:
            return (1 / expected_life) * price
        else:
            return 5
    else:
        return float(row[12])*(1/7)
    #float(1 / row[15])
    
def frc_dep(request):
    # Read the existing data from the Excel file
    file_path = 'csv_path/sample/asset_registerxxx.xlsx'
    df = pd.read_excel(file_path)
    df.fillna('', inplace=True)
    numeric_cols = df.select_dtypes(include='number').columns  # Select numeric columns
    df[numeric_cols] = df[numeric_cols].applymap(lambda x: f'{x:.2f}' if not pd.isnull(x) else '')  # Format 

    # Extract unique values from the first column (assuming it's the financial year column)
    unique_values = df.iloc[:, 0].unique().tolist()

    # Determine the smallest financial year from the existing data
    years = [int(year[:4]) for year in unique_values if year[:4].isdigit()]  # Extract year part and convert to integer
    smallest_year = min(years) if years else None

    # Get the current financial year based on the current date
    if smallest_year is not None:
        current_date = datetime.now()
        current_year = current_date.year
        current_financial_year = f"{current_year - 1}-{current_year}"

        # Calculate the range of financial years to be added
        if current_date.month > 6:
            financial_years_to_add = [f"{year}-{year+1}" for year in range(smallest_year, current_year + 1)]
        else:
            financial_years_to_add = [f"{year-1}-{year}" for year in range(smallest_year, current_year)]

        # Determine additional columns needed and set their values to 0
        for year in financial_years_to_add:
            df[year] = 0
        
        extra_columns = df.columns[20:]  # Assuming extra columns start from column index 23
        for index, row in df.iloc[0:].iterrows():
            calculated_values = calculate_values(row)
            df.loc[index, extra_columns] = calculated_values
        
        # for column_index in range(22, len(df.columns)):
        #     column_name = df.columns[column_index]
        #     # Iterate over rows within the column (excluding the header row)
        #     for index, value in df.iloc[1:, column_index].items():
        #         if(df.iloc[index, 0] != column_name):
        #             df.at[index,column_name] = 0
        #         else:
        #             continue
            
        for index, row in df.iloc[1:].iterrows():
            for column_name in df.columns[20:]:
                # Inner loop for columns
                if(df.iloc[index, 0] != column_name):
                    df.at[index,column_name] = 0
                else:
                    break

        for index, row in df.iloc[0:].iterrows():
            cn = 0
            e_life = float(df.iloc[index, 16]) if df.iloc[index, 16] != '' else 1
            for column_name in df.columns[20:]:
                if(e_life <= cn):
                    df.at[index, column_name] = 0
                else:
                    cn = cn + 1

    # Convert DataFrame to HTML
    numeric_cols = df.select_dtypes(include='number').columns  # Select numeric columns
    df[numeric_cols] = df[numeric_cols].applymap(lambda x: f'{x:.2f}' if not pd.isnull(x) else '')  # Format 
    
    excel_html = df.to_html(index=False)

    # Split the HTML table into headers and rows
    header_html = excel_html.split('<tbody>')[0]  # Extract headers part
    rows_html = '<tbody>' + excel_html.split('<tbody>')[1]  # Extract rows part

    # You can also save the modified DataFrame back to an Excel file
    df.to_excel('csv_path/sample/modified_asset_register.xlsx', index=False)

    return render(request, 'frc_dep.html', {'header_html': header_html, 'rows_html': rows_html, 'unique_values': unique_values})

def frc_data_entry(request):
    csv_file_path = 'csv_path/asset_info/asset_info.csv'
    df = pd.read_csv(csv_file_path)

    df_csv = pd.read_csv('csv_path/asset_info/asset_info.csv')

    # Extract values from the first column
    dropdown_categories = df.iloc[:, 0].tolist()

    if request.method == 'POST':
        file_path = 'csv_path/sample/asset_register.xlsx'
        df = pd.read_excel(file_path)

        purchase_date = request.POST.get('purchase_date')
        purchase_date = datetime.strptime(purchase_date, '%Y-%m-%d')
        purchase_year = purchase_date.year
        purchase_month = purchase_date.month
        purchase_date = purchase_date.strftime('%m/%d/%Y')

        if purchase_month <= 6:
            purchase_year -= 1

        financial_year = f"{purchase_year}-{purchase_year + 1}"

        serial_no = request.POST.get('serial_no')
        bill_no = request.POST.get('bill_no')
        category = request.POST.get('category')
        name_of_item = request.POST.get('name_of_item')
        quantity = float(request.POST.get('quantity') or 0)
        price = float(request.POST.get('price'))
        sold_quantity = float(request.POST.get('sold_quantity'))
        location = request.POST.get('location')
        current_condition = request.POST.get('current_condition')

        matching_row = df_csv[df_csv['Category'] == category].iloc[0]

        economic_code = matching_row['Economic Code']
        expected_life = matching_row['Expected Life(post)']
        depriciation_method = matching_row['Depriciation Method']

        new_row = {
            'Financial Year' : financial_year,
            'Purchase date': purchase_date,
            'Sl ': serial_no,
            'Bill no': bill_no,
            'Category': category,
            'Name of Item': name_of_item,
            'Units': quantity,
            'Price': price,
            'Sold (unit)': sold_quantity,
            'Location': location,
            'Economic Code':economic_code,
            'Expected life':expected_life,
            'Depreciation Method':depriciation_method,

            #'Current Condition': current_condition
        }

        # Append the new row to the DataFrame using loc
        df.loc[len(df)] = new_row

        # Save the DataFrame back to the Excel file
        df.to_excel(file_path, index=False)


    return render(request, 'frc_data_entry.html',{'dropdown_categories': dropdown_categories})
