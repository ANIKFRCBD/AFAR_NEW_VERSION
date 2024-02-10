from django.shortcuts import render
import pandas as pd
from datetime import datetime
from afar_project.views import calculate_values,calculate_costs



# Create your views here.
def dep(request):
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