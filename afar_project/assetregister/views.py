from django.shortcuts import render
import pandas as pd
from datetime import datetime
# Create your views here.
def frc_asset_register(request):
    file_path = 'csv_path/sample/asset_register.xlsx'  # Replace with the actual file path
    df_sheet = pd.read_excel(file_path)
    df=df_sheet
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
        header_html = excel_html.split('<tbody>')[0]  # Extract headers part
        rows_html = '<tbody>' + excel_html.split('<tbody>')[1]  # Extract rows part
    df.to_excel(file_path,index=False)

    return render(request, 'frc_asset_register.html', {'header_html': header_html, 'rows_html': rows_html, 'unique_values': unique_values})

