from django.shortcuts import render
import pandas as pd
from datetime import datetime
from django.shortcuts import render
from bs4 import BeautifulSoup
import os
from django.conf import settings
import qrcode as qr 



# Create your views here.
def frc_asset_register(request):
    file_path = 'csv_path/excel_files/asset_register.xlsx'  # Replace with the actual file path
    df_sheet = pd.read_excel(file_path)
    df=df_sheet
    df=df.fillna(0)
    # Generate Asset code by rearranging the dataframe
    df=df[['Financial Year', 'Purchase date', 'Sl ', 'Bill no','Economic Code',
       'Category', 'Name of Item', 'Brand Name', 'Model/Type', 'Units',
       'Modified Number', 'Price','Salvage Value', 'Sold (unit)','Sales proceeds','Years used(sold items)','FY of Items sold',
       'Cost of Assets Sold', 'Current Balance', 'Expected life',
       'Depreciation Method', 'Location']]
    df["Asset Code"]=0
    #Rearrange the dataframe
    df=df[['Financial Year', 'Purchase date', 'Sl ', 'Bill no','Asset Code','Economic Code',
       'Category', 'Name of Item', 'Brand Name', 'Model/Type', 'Units',
       'Modified Number', 'Price','Salvage Value', 'Sold (unit)','Sales proceeds','Years used(sold items)', 'FY of Items sold',
       'Cost of Assets Sold', 'Current Balance', 'Expected life',
       'Depreciation Method', 'Location']]
    # Get the current date
    current_date = datetime.now()

    # Determine the year based on the month
    if current_date.month > 6:
        year_variable = str(current_date.year)
    else:
        year_variable = str(current_date.year - 1)

    # Count the number of rows in the DataFrame
    len_csv_t = len(df)

    if(len_csv_t > 1):
        df["Current Balance"]=df["Price"]-df["Cost of Assets Sold"]

        #Asset_code_generation_updated_by_anik_mallick
        df["Asset Code"]="FRC" + "-" +  df.iloc[:, 22].astype(str).iloc[0]+"-"+df.iloc[:, 21].astype(str).iloc[0] + "-" + df.iloc[:, 6].astype(str).str[:1]  + "-" +df.iloc[:, 0].astype(str).str.extract(r'(\d{2})(\d{2})').iloc[:, 1] + "-" +df.iloc[:,2].astype(str).str[:-2].apply(lambda x: x.zfill(4))
        df.fillna('', inplace=True)
        numeric_cols = df.select_dtypes(include='number').columns  # Select numeric columns
        df[numeric_cols] = df[numeric_cols].applymap(lambda x: f'{x:.2f}' if not pd.isnull(x) else '')  # Format numeric values to display 2 decimal places

        # Extract unique values from the first column
        unique_values = df.iloc[:, 0].unique().tolist()

        # Convert all values in the DataFrame to strings
        df = df.astype(str)
         # Change this to your desired file path

        # Convert DataFrame to HTML
        
        excel_html = df.to_html(index=False)

        # Split the HTML table into headers and rows
        # header_html = excel_html.split('<tbody>')[0]  # Extract headers part
        # rows_html = '<tbody>' + excel_html.split('<tbody>')[1]  # Extract rows part
        # Parse the HTML string to extract column headers and rows
        soup = BeautifulSoup(excel_html, 'html.parser')
        table = soup.find('table')

        # Extract column headers
        column_headers = [th.get_text() for th in table.find_all('th')]

        # Extract rows
        rows = []
        for tr in table.find_all('tr')[1:]:
            rows.append([td.get_text() for td in tr.find_all('td')])
    df.to_excel(file_path,index=False)


    # return render(request, 'frc_asset_register.html', {'excel_html':excel_html,'header_html': header_html, 'rows_html': rows_html, 'unique_values': unique_values,})
    return render(request, 'frc_asset_register.html', {'column_headers': column_headers, 'rows': rows})

def data_profile(request, asset_code_value):
    # Load your Excel file into a DataFrame (assuming you already have this)
    df = pd.read_excel('csv_path/excel_files/asset_register.xlsx')

    # Find the row where the asset_code_value matches the value in the 5th column
    matched_row = df[df.iloc[:, 4] == asset_code_value]

    if not matched_row.empty:
        # Extract all column values of the matched row
        matched_values = matched_row.iloc[0].tolist()  # Assuming only one row is matched

        # Pass each column value as separate variables
        context = {}
        for i, value in enumerate(matched_values):
            context[f'value_{i+1}'] = value

        # Search for the image file in the folder
        image_filename = f"{asset_code_value}.jpg"  # Assuming image files have .jpg extension
        image_path_asset = os.path.join(settings.BASE_DIR,'static',"asset_images", image_filename)

        if os.path.exists(image_path_asset):
            # Combine the folder path and the relative image path
            relative_image_with_folder = image_path_asset
            context['image_path_asset'] = relative_image_with_folder
        else:
            context['image_path_asset'] = None

            # Search for the image file in the folder
        image_filename = f"{asset_code_value}.png"  # Assuming image files have .jpg extension
        image_path_qr = os.path.join(settings.BASE_DIR,"static","QR", image_filename)
        
        #generate#QR
        data_dr=asset_code_value
        #generation of QR
        qr_file=qr.make(data_dr)
        #save it to the destination
        qr_file.save(image_path_qr)
        print(image_path_qr)

        if os.path.exists(image_path_qr):
            relative_image_with_folder = image_path_qr
            context['image_path_qr'] = relative_image_with_folder
        else:
            context['image_path_qr'] = None

        return render(request, 'data_profile.html', context)
    else:
        # Handle case where no match is found
        return render(request, 'data_profile.html', {'error_message': 'No matching row found for the provided asset code.'})

