import os
from PIL import Image as PILImage
from django.shortcuts import render
import pandas as pd

def asset_image_upload(request):
    file_path = 'csv_path/excel_files/asset_register.xlsx'  
    df_sheet = pd.read_excel(file_path)
    df=df_sheet
    asset_code_options = set(df["Asset Code"])
    if request.method == 'POST':
        dropdown_option = request.POST['dropdown_asset_code']
        uploaded_image = request.FILES['image']

        image = PILImage.open(uploaded_image)
        save_path = os.path.join('static',"asset_images",dropdown_option + '.jpg')
        image.save(save_path, 'JPEG')
        
        # Optionally, you can save the image path in your database
        # For example, if you have a model named Image:
        # Image.objects.create(name=dropdown_option, path=save_path)



            
    return render(request, 'asset_image_upload.html', {'asset_code_options': asset_code_options})