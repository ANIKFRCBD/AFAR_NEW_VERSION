from django.shortcuts import render
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from .forms import institutionname_form

def institutionname(request):
    context = {"form": None}
    if request.method == "POST":
        data = institutionname_form(request.POST, request.FILES)
        if data.is_valid():
            institution_name = data.cleaned_data['Name']
            website = data.cleaned_data['Website']
            district = data.cleaned_data['District']
            address = data.cleaned_data['address']
            ministry = data.cleaned_data['authority']
            logo_file = data.cleaned_data['document']
            
            fs = FileSystemStorage(location='institutionmedia')
            file_name = fs.save(logo_file.name, logo_file)
            
            list_of_elements = [institution_name, website, district, address, ministry, file_name]
            context.update({'form_data': list_of_elements})
        else:
            context.update({'form': data})
    else:
        data = 0
        context.update({'form': data})
    
    return render(request, "institution_registration.html", context)
