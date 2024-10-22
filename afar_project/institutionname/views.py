from django.shortcuts import render,redirect
from django.http import HttpResponse ,request
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
            street_address = data.cleaned_data['street_address']
            ministry = data.cleaned_data['authority']
            phone=data.cleaned_data["phone"]
            email=data.cleaned_data["email"]
            logo_file = data.cleaned_data['logo']
            acronym=data.cleaned_data["Abbreviation"]
            fs = FileSystemStorage(location='static')
            file_name = fs.save(f"{institution_name}.png", logo_file)
            
            list_of_elements = [institution_name, website, district, street_address, ministry,phone,email,file_name,acronym]
            #save file in JSON
            information={"Institute_name":institution_name,"website":website,"district":district,"address":street_address,"ministry":ministry,"phone":phone,"email":email,"file_location":os.path.join(settings.BASE_DIR,"institutionmedia",f"{institution_name}.png"),"acronym":acronym}
            file_path = os.path.join(settings.BASE_DIR, 'static', "institution.json")
            with open(file_path,"w") as file:
                j.dump(information,file,indent=4)
            context.update({'form_data': list_of_elements, 'info': list_of_elements,"file+location":information["file_location"]})
        else:
            context.update({'form': data})
    else:
        context.update({'info': None})
    
    return render(request, "institution_registration.html", context)

def sign_in_again(request):
    return redirect("signin")
def view_institution(request):
    return render(request,"institution_view.html")


