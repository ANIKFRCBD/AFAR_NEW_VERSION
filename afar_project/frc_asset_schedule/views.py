from django.shortcuts import render
import pandas as pd
import re

def extract_numbers(string_data):
    # Use regular expression to find standalone numeric values in the string
    if type(string_data) == str:
        numeric_parts = re.findall(r'\b\d+(?:\.\d+)?\b', string_data)
        # Convert the list of numeric strings to floats
        numeric_values = [float(num) for num in numeric_parts]
        return numeric_values[0]
    return string_data

def frc_asset_schedule(request):
    file_path = 'csv_path/excel_files/asset_register.xlsx'

    # Read the CSV file into a DataFrame
    df = pd.read_excel(file_path)

    # Count the number of rows in the DataFrame
    len_csv = len(df)
    len_csv = len_csv - 1
    # Initialize an empty list to store the rows
    page_header = ['Economic Code','Particulars','Opening Balance','Purchases During the Period','Total','Sale of Assets','Net Balance','Rate of Depreciation','Opening Accumulated Depreciation','Depreciation Charges','Depreciation on Assets Sold','Net Accumulated Depreciation','Impairment Charges','Accumulated Impairment','WDV','Status']
    rows = []
    if len_csv > 0:
    # Read the CSV files into dataframes, skipping the header row
        df_asset_info = pd.read_excel('csv_path/excel_files/frc_asset_info.xlsx', header=None, skiprows = 1)
        df_asset_register = pd.read_excel('csv_path/excel_files/asset_register.xlsx', header=None, skiprows=1)
        df_depreciation = pd.read_excel('csv_path/excel_files/depreciation.xlsx', header=None, skiprows=1)
        df_imp = pd.read_excel('csv_path/excel_files/Impairment_data.xlsx', header=None, skiprows=1)

        # Initialize an empty list to store the rows
        page_header = ['Economic Code','Particulars','Opening Balance','Purchases During the Period','Total','Sale of Assets','Net Balance','Rate of Depreciation','Opening Accumulated Depreciation','Depreciation Charges','Depreciation on Assets Sold','Net Accumulated Depreciation','Impairment Charges','Accumulated Impairment','WDV','Status']

        result_rows = []
        result_rows.append(page_header)

        # Loop through each row in df_asset_info
        for index_info, row_info in df_asset_info.iterrows():
            asset_code_info = row_info.iloc[0] 

            sum_seventh_element_pre = sum_seventh_element_new = opening_balance = purchase_during_the_period = cost_of_asset_sold = opening_acc_dep = dep_charges = acc_dep_sold_items = net_acc_dep = net_balance = 0
            sum_seventh_element_post = 0
            present = 0
            pre_rate = pre_rate_percentage = post_rate = post_rate_percentage = depriciation_pre = depriciation_post = 0


            # Loop through each row in df_asset_register
            for index_reg, row_reg in df_depreciation.iterrows():
                taka = extract_numbers(str(row_reg.iloc[12]))
                asset_code_reg = row_reg.iloc[6]  
                pre_post_reg = row_reg.iloc[3]
                pre_rate = pre_rate_percentage = post_rate = post_rate_percentage = depriciation_pre = depriciation_post = 0

                
                if asset_code_info == asset_code_reg:
                    for i in range(25, len(row_reg) - 1):   # Excluding the last column
                        opening_acc_dep = opening_acc_dep + float(row_reg.iloc[i])
                    dep_charges = dep_charges + row_reg.iloc[-1]
                    acc_dep_sold_items = acc_dep_sold_items + row_reg.iloc[22]

                    cost_of_asset_sold = cost_of_asset_sold + row_reg[18]
                    if(row_reg[0] != "2023-2024"):
                        opening_balance = opening_balance + row_reg[12]
                    elif(row_reg[0] == "2023-2024"):
                        purchase_during_the_period = purchase_during_the_period + row_reg[19]

                    net_acc_dep = opening_acc_dep + dep_charges-acc_dep_sold_items

                    
                    
                    present = 1
                    if pre_post_reg == 'Pre':
                        sum_seventh_element_pre = sum_seventh_element_pre + float(taka)
                    elif pre_post_reg == 'New':
                        sum_seventh_element_new = sum_seventh_element_new + float(taka)
                    else :
                        sum_seventh_element_post = sum_seventh_element_post + float(taka)
            if(row_info.iloc[4] > 0):
                post_rate = 1 / float(row_info.iloc[4])
                depriciation_post = round(post_rate * sum_seventh_element_post,2)
                post_rate_percentage = "{:.2f}%".format(post_rate * 100)

            if(row_info.iloc[3] > 0):
                pre_rate = 1 / float(row_info.iloc[3])
                depriciation_pre = round(pre_rate * sum_seventh_element_pre,2)
                pre_rate_percentage = "{:.2f}%".format(pre_rate * 100)

            depriciation_charges = round(depriciation_pre + depriciation_post + sum_seventh_element_new,2)

            imp_charges = 0
            acc_imp = 0
            wdv = 0

            for index_reg, row_reg in df_imp.iterrows():
                asset_code_reg_imp = row_reg.iloc[4] 
                if asset_code_reg_imp == asset_code_info:
                    if (df_imp.columns[-1] != 'Accumulated Impairment'):
                        imp_charges = imp_charges + row_reg.iloc[-1]
                    acc_imp = acc_imp + row_reg.iloc[12]

                    
            

            if(present):
                total = round(opening_balance + purchase_during_the_period,2)
                net_balance = total - cost_of_asset_sold
                wdv = net_balance - net_acc_dep - acc_imp
                new_row = [row_info.iloc[2], row_info.iloc[0], round(opening_balance,2), purchase_during_the_period,total,round(cost_of_asset_sold,2),round(net_balance,2),post_rate_percentage, round(opening_acc_dep,2),round(dep_charges,2),round(acc_dep_sold_items,2),round(net_acc_dep,2),round(imp_charges,2),round(acc_imp,2),round(wdv,2)," "]
                result_rows.append(new_row)
        
        # Convert the list of rows into a DataFrame
        result_df = pd.DataFrame(result_rows)

        # Write the DataFrame to a new CSV file
        result_df.to_excel('csv_path/excel_files/frc_asset_schedule.xlsx', index=False, header=False)

        df_asset_schedule = pd.read_excel('csv_path/excel_files/frc_asset_schedule.xlsx')

        # page_header = df_asset_schedule.columns.tolist()
        rows = df_asset_schedule.values.tolist()

    return render(request, "frc_asset_schedule.html", {'page_header':page_header, 'rows': rows})
