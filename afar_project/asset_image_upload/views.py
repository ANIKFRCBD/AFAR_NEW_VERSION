import os
from PIL import Image as PILImage
from django.shortcuts import render
import pandas as pd

def get_asset_code_options():
    df = pd.read_excel('csv_path/excel_files/asset_register.xlsx')
    options = df.iloc[1:, 4].tolist()
    return options


def asset_image_upload(request):
    asset_code_options = get_asset_code_options()

    file_path = 'csv_path/excel_files/asset_register.xlsx'  
    df_sheet = pd.read_excel(file_path)
    df=df_sheet

    df=df[['Financial Year', 'Purchase date', 'Sl ', 'Bill no','Economic Code',
    'Category', 'Name of Item', 'Brand Name', 'Model/Type', 'Units',
    'Modified Number', 'Price','Salvage Value', 'Sold (unit)','Sales proceeds','Years used(sold items)','FY of Items sold',
    'Cost of Assets Sold', 'Current Balance', 'Expected life',
    'Depreciation Method', 'Location']]
    df["Asset Code"]=0

    df=df[['Financial Year', 'Purchase date', 'Sl ', 'Bill no','Asset Code','Economic Code',
    'Category', 'Name of Item', 'Brand Name', 'Model/Type', 'Units',
    'Modified Number', 'Price','Salvage Value', 'Sold (unit)','Sales proceeds','Years used(sold items)', 'FY of Items sold',
    'Cost of Assets Sold', 'Current Balance', 'Expected life',
    'Depreciation Method', 'Location']]

    len_csv_t = len(df)

    if(len_csv_t > 1):
        df["Current Balance"]=df["Price"]-df["Cost of Assets Sold"]

        #Asset_code_generation_updated_by_anik_mallick
        df["Asset Code"]="FRC" + "-" +  df.iloc[:, 22].astype(str).iloc[0]+"-"+df.iloc[:, 21].astype(str).iloc[0] + "-" + df.iloc[:, 6].astype(str).str[:1]  + "-" +df.iloc[:, 0].astype(str).str.extract(r'(\d{2})(\d{2})').iloc[:, 1] + "-" +df.iloc[:,2].astype(str).str[:-2].apply(lambda x: x.zfill(4))
        df.fillna('', inplace=True)
        numeric_cols = df.select_dtypes(include='number').columns 
        df[numeric_cols] = df[numeric_cols].applymap(lambda x: f'{x:.2f}' if not pd.isnull(x) else '') 

        df = df.astype(str)

    df.to_excel(file_path,index=False)

    if request.method == 'POST':
        dropdown_option = request.POST['dropdown_asset_code']
        uploaded_image = request.FILES['image']

        image = PILImage.open(uploaded_image)
        save_path = os.path.join('asset_image_upload_folder', dropdown_option + '.jpg')
        image.save(save_path, 'JPEG')
        
        # Optionally, you can save the image path in your database
        # For example, if you have a model named Image:
        # Image.objects.create(name=dropdown_option, path=save_path)



            
    return render(request, 'asset_image_upload.html', {'asset_code_options': asset_code_options})