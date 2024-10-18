from django.shortcuts import render
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from .forms import institutionname_form
import json as j
import os
from django.conf import settings

def institutionname(request):
    context = {"form": institutionname_form()}
    if request.method == "POST":
        data = institutionname_form(request.POST, request.FILES)
        # Checkvalidation
        if data.is_valid():
            institution_name = data.cleaned_data['Name']
            website = data.cleaned_data['Website']
            district = data.cleaned_data['District']
            address = data.cleaned_data['address']
            ministry = data.cleaned_data['authority']
            logo_file = data.cleaned_data['document']
            
            fs = FileSystemStorage(location='institutionmedia')
            file_name = fs.save(f"{institution_name}.png", logo_file)
            
            list_of_elements = [institution_name, website, district, address, ministry, file_name]
            #save file in JSON
            information={"Institute_name":institution_name,"website":website,"district":district,"address":address,"ministry":ministry,"file_location":os.path.join(settings.BASE_DIR,"institutionmedia",f"{institution_name}.png")}
            file_path = os.path.join(settings.BASE_DIR, 'institutionname', f"{institution_name}.json")
            with open(file_path,"w") as file:
                j.dump(information,file,indent=4)
            context.update({'form_data': list_of_elements, 'info': list_of_elements})
        else:
            context.update({'form': data})
    else:
        context.update({'info': None})
    
    return render(request, "institution_registration.html", context)
