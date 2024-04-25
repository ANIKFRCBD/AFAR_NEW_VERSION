"""afar_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django import views
from django.contrib import admin
from django.urls import path,include
from afar_project.views import asset_register,data_entry,modify_database,success,genSchedule,depriciation,list_test,register,asset_info,current_asset_info,download_predefined_csv,file_upload,asset_schedule,data_entry_pre,file_upload_pre,download_csv,delete_extra_columns,download_csv_dep,download_csv_schedule,frc_asset_register,frc_dep,frc_data_entry,download_csv_frc_asset,delete_rows_asset_register,download_csv_frc_dep,download_csv_frc_asset_schedule
from dashboard.views import dashboard,dashboard_summary_of_assets
from users.views import opening,signin,signup,SignUpModel
from impairmenttest import views as impairment
from assetregister import views as asset_register_main
from depreciation import views as dep
from frc_file_upload import views as frc_file_upload
from salesentry import views as salesentry
from frc_asset_schedule import views as frc_asset_schedule
from dataentry import views as frc_data_entry
from datadelete import views as datadelete
from asset_image_upload import views as asset_image_upload
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',opening,name='opening'),
    path('dashboard', dashboard, name='dashboard'),
    path('asset_register', asset_register,name="asset_register"),
    path('signin',signin,name='signin'),
    path('signup',signup,name='signup'),
    path('data_entry/',data_entry,name="data_entry"),
    path('modify_database/',modify_database,name="modify_database"),
    path('success/',success),
    # path('genSchedule/',genSchedule,name="genSchedule"),
    path('depriciation/',depriciation,name="depriciation"),
    path('asset_schedule/', asset_schedule, name='asset_schedule'),
    path('list_test/',list_test,name="list_test"),
    path('register/',register,name="register"),
    path('asset_info/',asset_info,name="asset_info"),
    path('current_asset_info/',current_asset_info,name="current_asset_info"),
    path('download_predefined_csv/', download_predefined_csv, name='download_predefined_csv'),
    path('file_upload/', file_upload, name='file_upload'),
    path('data_entry_pre/', data_entry_pre, name='data_entry_pre'),
    path('file_upload_pre/', file_upload_pre, name='file_upload_pre'),
    path('download_csv/', download_csv, name='download_csv'),
    path('download_csv/', download_csv, name='download_csv'),
    path('delete_extra_columns/', delete_extra_columns, name='delete_extra_columns'),
    path('download_csv_dep/', download_csv_dep, name='download_csv_dep'),
    path('download_csv_schedule/', download_csv_schedule, name='download_csv_schedule'),
    path('download_csv_frc_asset/', download_csv_frc_asset, name='download_csv_frc_asset'),
    path('download_csv_frc_dep/', download_csv_frc_dep, name='download_csv_frc_dep'),
    path('download_csv_frc_asset_schedule/', download_csv_frc_asset_schedule, name='download_csv_frc_asset_schedule'),
    path('delete_rows_asset_register/', delete_rows_asset_register, name='delete_rows_asset_register'),
    path('frc_asset_register/', asset_register_main.frc_asset_register, name='frc_asset_register'),
    path('frc_asset_schedule/', frc_asset_schedule.frc_asset_schedule, name='frc_asset_schedule'),
    path('frc_dep/', dep.dep, name='frc_dep'),
    path('frc_system/', frc_file_upload.frc_system, name='frc_system'),
    path('merge_files/', frc_file_upload.merge_files, name='merge_files'),
    path('frc_data_entry/', frc_data_entry.frc_data_entry, name='frc_data_entry'),
    path('impariment/', impairment.imparimenttest, name='impairment'),
    path('sales_entry/', salesentry.sales_entry_app, name='sales_entry'),
    path('datadelete/', datadelete.datadeletepage,name='delete'),
    path('datainit',datadelete.datainit,name='datainit'),
    path('asset_image_upload/', asset_image_upload.asset_image_upload, name='asset_image_upload_app'),
    path('detail/<str:asset_code_value>/', asset_register_main.data_profile, name='data_profile'),
    ]