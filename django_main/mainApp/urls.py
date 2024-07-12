from django.urls import re_path as url
from mainApp import views
from django.urls import path

urlpatterns=[
    url(r'^vendors$',views.vendorApi),
    url(r'^vendors/([0-9]+)$',views.vendorApi),
    url(r'^purchaseorders$',views.purchaseorderApi),
    url(r'^purchaseorders/([0-9]+)$',views.purchaseorderApi),
    path('<str:username>/admin',views.mainadmin,name='adminhome'),
    path('<str:username>/adminpanel',views.mainadminpanel,name='adminpanel'),
    path('<str:username>/user',views.mainuser,name='userhome'),
    path('<str:username>/qa',views.mainqa,name='qahome'),
    path('adminlogin',views.adminlogin,name='adminlogin'),
    path('addvendor/<str:username>',views.addvendor,name='addvendor'),
    path('adduser/<str:username>',views.adduser,name='adduser'),
    path('vendor',views.vendorMain,name='vendors'),
    path('',views.mainmain,name='mainhome'),
    path('<str:vendorno>/<str:username>/purchase',views.purchaseorder,name="purchaseorder"),
    path('<str:vendorno>/<str:username>/adminpurchase',views.adminpurchaseorder,name="adminpurchaseorder"),
    path('<str:vendorno>/vendorpurchase',views.vendorpurchaseorder,name="vendorpurchaseorder"),
    path('<str:vendorno>/signin',views.signin,name='signin'),
    path('<str:vendorno>/vendoraccount',views.vendoraccount,name='vendoraccount'),
    path('<str:username>/deletevendor',views.deletevendor,name='deletevendor'),
    path('<str:username>/deleteuser',views.deleteuser,name='deleteuser'),
    path('approve/<str:vendorno>/<str:username>', views.approve_inspection, name='approve_inspection'),
    path('assignuser/<str:username>', views.assignuser, name='assignuser'),
    path('reject/<str:vendorno>/<str:username>', views.reject_inspection, name='reject_inspection'),
    path('update_inspection_date/', views.update_inspection_date, name='update_inspection_date')
]