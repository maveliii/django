from django.urls import re_path as url
from mainApp import views
from django.urls import path

urlpatterns=[
    url(r'^vendors$',views.vendorApi),
    url(r'^vendors/([0-9]+)$',views.vendorApi),
    url(r'^purchaseorders$',views.purchaseorderApi),
    url(r'^purchaseorders/([0-9]+)$',views.purchaseorderApi),
    path('admin',views.main,name='home'),
    path('adminlogin',views.adminlogin,name='adminlogin'),
    path('vendor',views.vendorMain,name='vendors'),
    path('',views.mainmain,name='mainhome'),
    path('<str:vendorno>/purchase',views.purchaseorder,name="purchaseorder"),
    path('<str:vendorno>/vendorpurchase',views.vendorpurchaseorder,name="vendorpurchaseorder"),
    path('<str:vendorno>/signin',views.signin,name='signin'),
    path('approve/<str:pono>/', views.approve_inspection, name='approve_inspection'),
    path('reject/<str:pono>/', views.reject_inspection, name='reject_inspection'),
    path('update_inspection_date/', views.update_inspection_date, name='update_inspection_date')
]