from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from mainApp.models import AppMainVendor as Vendor
from mainApp.models import AppMainUsers as UserMain
from mainApp.models import  AppMainPurchaseorder as PurchaseOrder
from mainApp.serializers import VendorsSerializer, PurchaseOrdersSerializer
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Count, Q
from .forms import DetailsForm
from datetime import datetime
from django.contrib.auth.hashers import make_password
import json
from django.template.loader import render_to_string




@csrf_exempt
def vendorApi(request, id=0):
    if request.method == 'GET':
        try:
            vendors = Vendor.objects.all()
            vendors_serializer = VendorsSerializer(vendors, many=True)
            return JsonResponse(vendors_serializer.data, safe=False)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    
    elif request.method == 'POST':
        try:
            vendor_data = JSONParser().parse(request)
            vendors_serializer = VendorsSerializer(data=vendor_data)
            if vendors_serializer.is_valid():
                vendors_serializer.save()
                return JsonResponse("Added successfully", safe=False)
            return JsonResponse("Failed to Add", safe=False)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    
    elif request.method == 'PUT':
        try:
            vendor_data = JSONParser().parse(request)
            vendor = Vendor.objects.get(vendor_no=vendor_data['vendor_no'])
            vendors_serializer = VendorsSerializer(vendor, data=vendor_data)
            if vendors_serializer.is_valid():
                vendors_serializer.save()
                return JsonResponse("Updated successfully", safe=False)
            return JsonResponse("Failed to Update", safe=False)
        except Vendor.DoesNotExist:
            return JsonResponse("Vendor not found", safe=False, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    
    elif request.method == 'DELETE':
        try:
            vendor = Vendor.objects.get(vendor_no=id)
            vendor.delete()
            return JsonResponse("Deleted successfully", safe=False)
        except Vendor.DoesNotExist:
            return JsonResponse("Vendor not found", safe=False, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

@csrf_exempt
def purchaseorderApi(request, id=0):
    if request.method == 'GET':
        try:
            purchaseorders = PurchaseOrder.objects.all()
            purchaseorders_serializer = PurchaseOrdersSerializer(purchaseorders, many=True)
            return JsonResponse(purchaseorders_serializer.data, safe=False)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    
    elif request.method == 'POST':
        try:
            purchaseorders_data = JSONParser().parse(request)
            purchaseorders_serializer = PurchaseOrdersSerializer(data=purchaseorders_data)
            if purchaseorders_serializer.is_valid():
                purchaseorders_serializer.save()
                return JsonResponse("Added successfully", safe=False)
            return JsonResponse("Failed to Add", safe=False)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    
    elif request.method == 'PUT':
        try:
            purchaseorders_data = JSONParser().parse(request)
            purchaseorder = PurchaseOrder.objects.get(po_no=purchaseorders_data['po_no'])
            purchaseorders_serializer = PurchaseOrdersSerializer(purchaseorder, data=purchaseorders_data)
            if purchaseorders_serializer.is_valid():
                purchaseorders_serializer.save()
                return JsonResponse("Updated successfully", safe=False)
            return JsonResponse("Failed to Update", safe=False)
        except PurchaseOrder.DoesNotExist:
            return JsonResponse("Purchase order not found", safe=False, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    
    elif request.method == 'DELETE':
        try:
            purchaseorder = PurchaseOrder.objects.get(po_no=id)
            purchaseorder.delete()
            return JsonResponse("Deleted successfully", safe=False)
        except PurchaseOrder.DoesNotExist:
            return JsonResponse("Purchase order not found", safe=False, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

# Temporary page whcih shows option vendors/admin      
def mainmain(request):
    return render(request, 'mainindex.html')


#Temporary page which shows all vendors
def vendorMain(request):
    vendors=Vendor.objects.all()
    return render(request, 'allvendors.html',{"vendor":vendors})


# admin page main shows all vendors        
def mainadmin(request,username):
    # Annotate Vendor with the count of PurchaseOrders
    user=get_object_or_404(UserMain,username=username)
    if (request.session.get('authenticated_admin') != username) | (user.role != 'admin'):
        return redirect('adminlogin')
    else:
        vendor = Vendor.objects.annotate(po_count=Count('appmainpurchaseorder__pono') ,pending_inspection_count=Count('appmainpurchaseorder__pono', filter=Q(appmainpurchaseorder__inspectiondate__isnull=True)))
        purchase = PurchaseOrder.objects.all()
        
        return render(request, 'indexadmin.html', {
            "vendor": vendor,
            "purchase": purchase,
            "username":username
        })
    
def mainadminpanel(request,username):
    user=get_object_or_404(UserMain,username=username)
    users=UserMain.objects.all()
    vendors=Vendor.objects.all().order_by('vendorname')
    if (request.session.get('authenticated_admin') != username) | (user.role != 'admin') :
        return redirect('adminlogin')
    else:
        return render(request,'adminpanel.html',{'username':username,'vendors':vendors,'users':users})

def addvendor(request, username):
    # Ensure the user is authenticated as an admin
    user = get_object_or_404(UserMain, username=username)
    if (request.session.get('authenticated_admin') != username) or (user.role != 'admin'):
        return redirect('adminlogin')

    if request.method == 'POST':
        vendorno = request.POST.get('vendorno')
        vendorname = request.POST.get('vendorname')
        territory = request.POST.get('territory')
        email = request.POST.get('email')
        email2 = request.POST.get('email2')
        email3 = request.POST.get('email3')
        email4 = request.POST.get('email4')
        password = request.POST.get('password')  # Hashing the password
        iaalertdays = request.POST.get('iaalertdays')

        # Check if a vendor with the given vendorno already exists
        vendor = Vendor.objects.filter(vendorno=vendorno).first()

        if vendor:
            # Update existing vendor
            vendor.vendorname = vendorname
            vendor.territory = territory
            vendor.email = email
            vendor.email2 = email2
            vendor.email3 = email3
            vendor.email4 = email4
            vendor.password = password  # Ensure to hash the password
            vendor.iaalertdays = iaalertdays
            vendor.save()
            messages.success(request, "Vendor updated successfully!")
            return redirect('adminpanel', username=username)
        else:
            # Create new vendor
            Vendor.objects.create(
                vendorno=vendorno,
                vendorname=vendorname,
                territory=territory,
                email=email,
                email2=email2,
                email3=email3,
                email4=email4,
                password=password,  # Ensure to hash the password
                iaalertdays=iaalertdays
            )
            messages.success(request, "Vendor added successfully!")
            return redirect('adminpanel', username=username)

    return redirect('adminpanel', username=username)


def deletevendor(request,username):
    user=get_object_or_404(UserMain,username=username)
    if (request.session.get('authenticated_admin') != username) | (user.role != 'admin'):
        return redirect('adminlogin')
    else:
        if request.method == 'POST':
            # Confirm deletion by checking a specific form or a confirmation in the modal
            # Perform deletion
            vendorno=request.POST['vendormain']
            vendor=get_object_or_404(Vendor,vendorno=vendorno)
            vendor.delete()
            messages.success(request, f"Vendor '{vendor.vendorname}' deleted successfully!")
            return redirect('adminpanel', username=username)  # Redirect to admin panel or any desired page

        # Typically, this view would only be accessed via POST requests
        # In case of GET requests, handle appropriately (redirect, error page, etc.)
        return redirect('adminpanel', username=request.user.username)

def deleteuser(request,username):
    user=get_object_or_404(UserMain,username=username)
    if (request.session.get('authenticated_admin') != username) | (user.role != 'admin'):
        return redirect('adminlogin')
    else:
        if request.method == 'POST':
            # Confirm deletion by checking a specific form or a confirmation in the modal
            # Perform deletion
            username1=request.POST['userid']
            user=get_object_or_404(UserMain,username=username1)
            user.delete()
            messages.success(request, f"User '{username1}' deleted successfully!")
            return redirect('adminpanel', username=username)  # Redirect to admin panel or any desired page

        # Typically, this view would only be accessed via POST requests
        # In case of GET requests, handle appropriately (redirect, error page, etc.)
        return redirect('adminpanel', username=username)
    

def adduser(request,username):
    user=get_object_or_404(UserMain,username=username)
    if (request.session.get('authenticated_admin') != username) | (user.role != 'admin'):
        return redirect('adminlogin')
    else:
        if request.method == 'POST':
            username1 = request.POST['username']
            role = request.POST['role']
            email = request.POST['useremail']
            password = request.POST['userpassword']  # Hashing the password
            user = UserMain.objects.filter(username=username1).first()

            if user:
                user.username=username1
                user.role=role
                user.password=password
                user.email=email
                user.save()
                messages.success(request, "User updated successfully!")
                return redirect('adminpanel',username)
            else:
                UserMain.objects.create(
                    username=username1,
                    role=role,
                    password=password,
                    email=email
                )
                messages.success(request, "User added successfully!")
                return redirect('adminpanel',username)
        
def mainuser(request,username):
    # Annotate Vendor with the count of PurchaseOrders
    if request.session.get('authenticated_admin') != username:
        return redirect('adminlogin')
    else:
        purchase = PurchaseOrder.objects.filter(username=username)
        vendors = Vendor.objects.annotate(po_count=Count('appmainpurchaseorder__pono', filter=Q(appmainpurchaseorder__username=username)) ,pending_inspection_count=Count('appmainpurchaseorder__pono', filter=Q(appmainpurchaseorder__inspectiondate__isnull=True)&Q(appmainpurchaseorder__username=username)))
        purchase_vendor_numbers = purchase.values_list('vendorno', flat=True)

# Filter out vendors that do not have any matching purchase orders
        vendors_to_keep = [vendor for vendor in vendors if vendor.vendorno in purchase_vendor_numbers]

        return render(request, 'indexuser.html', {
            "vendor": vendors_to_keep,
            "purchase": purchase,
            "username": username
        })

def mainqa(request,username):
    # Annotate Vendor with the count of PurchaseOrders
    if request.session.get('authenticated_admin') != username:
        return redirect('adminlogin')
    else:
        purchase = PurchaseOrder.objects.filter(username=username)
        vendors = Vendor.objects.annotate(po_count=Count('appmainpurchaseorder__pono', filter=Q(appmainpurchaseorder__username=username)) ,pending_inspection_count=Count('appmainpurchaseorder__pono', filter=Q(appmainpurchaseorder__inspectiondate__isnull=True)&Q(appmainpurchaseorder__username=username)))
        purchase_vendor_numbers = purchase.values_list('vendorno', flat=True)

# Filter out vendors that do not have any matching purchase orders
        vendors_to_keep = [vendor for vendor in vendors if vendor.vendorno in purchase_vendor_numbers]

        return render(request, 'indexuser.html', {
            "vendor": vendors_to_keep,
            "purchase": purchase,
            "username": username
        })
#redirected from 'main' when admin clicks on a vendor shows all PO's of a vendor
def purchaseorder(request,vendorno,username):
    user=get_object_or_404(UserMain,username=username)
    if (request.session.get('authenticated_admin') != username) | ((user.role != 'user') & (user.role != 'qa')):
        return redirect('adminlogin')
    else:
        purchase = PurchaseOrder.objects.filter(Q(vendorno=vendorno) & Q(username=username))
        vendor = get_object_or_404(Vendor, vendorno=vendorno)
        users =UserMain.objects.all()
        return render(request, 'purchase.html', {"purchase": purchase,"vendorno":vendorno, "username":username,"vendorname":vendor.vendorname,"users":users,"role":user.role})

def adminpurchaseorder(request,vendorno,username):
    user=get_object_or_404(UserMain,username=username)
    if (request.session.get('authenticated_admin') != username) | (user.role != 'admin'):
        return redirect('adminlogin')
    else:
        purchase = PurchaseOrder.objects.filter(vendorno=vendorno)
        users = UserMain.objects.all()
        vendor = get_object_or_404(Vendor, vendorno=vendorno)
        return render(request, 'adminpurchase.html', {"purchase": purchase, "users": users , "vendorno":vendorno , "username":username ,"vendorname":vendor.vendorname})


#Original vendor page which each vendor will access after signIn will be different for each vendor shows PO's of each vendor
@csrf_exempt
def vendorpurchaseorder(request, vendorno):
    order = get_object_or_404(Vendor, vendorno=vendorno)
    vendorname = order.vendorname


    # this code below is to get the other vendorno with the same vendorname
    vendorno2 = vendorno 
    order1 = Vendor.objects.filter(vendorname=vendorname).exclude(vendorno=vendorno).first()
    if order1:
        vendorno2 = order1.vendorno
    
    #check if the vendor signedin
    if request.session.get('authenticated_vendor') != vendorno:
        return redirect('signin', vendorno=vendorno)
    
    #filtering PO's for the particular vendor
    purchase = PurchaseOrder.objects.filter(Q(vendorno=vendorno2) | Q(vendorno=vendorno))
    

    #for document submission
    if request.method == "POST":
        form = DetailsForm(request.POST, request.FILES)
        
        if form.is_valid():
            DocType = form.cleaned_data['doctype']
            PONO = form.cleaned_data['pono']
            
            for file in request.FILES.getlist('files'):
                form = DetailsForm(request.POST, {
                    'docname': '',
                    'doc': file,
                    'doctype': DocType,
                    'pono': PONO
                })
                if form.is_valid():
                    form.save()
            
            return render(request, 'vendorpurchase.html', {
                "purchase": purchase,
                "vendorno": vendorno,
                "vendorname": vendorname,
                "form": form,
            })
    else:
        form = DetailsForm()
    
    #rendering page
    return render(request, 'vendorpurchase.html', {
        "purchase": purchase,
        "vendorno": vendorno,
        "vendorname": vendorname,
        "form": form,
    })


#for updating inspection date proposed for the vendor
@csrf_exempt
def update_inspection_date(request):
    if request.method == 'POST':
        pnos = request.POST.getlist('pnos[]')
        new_date = request.POST.get('new_date')
        
        try:
            for pono in pnos:
                purchase = get_object_or_404(PurchaseOrder,pono=pono)
                purchase.inspectiondateproposed=new_date
                purchase.status="Inspection Date Proposed"
                purchase.alerts="Inspection date Proposed Click to View"
                purchase.iasubmissiondate=datetime.now()
                purchase.vendoralerts=None
                purchase.save()
            return JsonResponse({'success': True})
        except PurchaseOrder.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Purchase Order not found'})
    
    return JsonResponse({'success': False, 'error': 'Invalid request'})

def assignuser(request,username):
    user=get_object_or_404(UserMain,username=username)
    if (request.session.get('authenticated_admin') != username) | (user.role != 'admin'):
        print("im here")
        return redirect('adminlogin')
    else:
        if request.method == 'POST':
            selected_ponos = json.loads(request.POST.get('selected_ponos', '[]'))
            print(selected_ponos)
            user_id=request.POST['assign_user']
            
            for pono in selected_ponos:
                if user_id == 'Assign User':
                    order = get_object_or_404(PurchaseOrder, pono=pono)
                    return redirect('adminpurchaseorder', vendorno=order.vendorno_id, username=username)
                else:
                    print(pono)
                    user = get_object_or_404(UserMain, username=user_id)
                    order = get_object_or_404(PurchaseOrder, pono=pono)
                    order.username = user
                    order.save()
            return redirect('adminpurchaseorder', vendorno=order.vendorno_id, username=username)

#when admin approves inspection date the date from proposed inspection date get saved to inspection date
def approve_inspection(request,vendorno,username):
    user=get_object_or_404(UserMain,username=username)
    if request.session.get('authenticated_admin') != username:
        return redirect('adminlogin')
    else:
        if request.method == 'POST':
            selected_ponos = json.loads(request.POST.get('selected_ponos', '[]'))
            user=get_object_or_404(UserMain, username=username)
            orders = []
            for pono in selected_ponos:
                order = get_object_or_404(PurchaseOrder, pono=pono)
                order.inspectiondate = order.inspectiondateproposed
                order.status = "Inspection Date Approved"
                order.alerts = None
                order.save()
                orders.append(order)

            # Prepare the context for the email template
            context = {
                'orders': orders
            }

            # Render the email template
            email_body = render_to_string('email_template.html', context)

            # Send the email
            send_mail(
                'Inspection Dates Approved',
                '',
                settings.EMAIL_HOST_USER,
                ['maveliprivate@gmail.com'],  # Replace with the recipient's email
                html_message=email_body,
                fail_silently=False,
            )
            if(user.role=='admin'):
                return redirect('adminpurchaseorder', vendorno=vendorno, username=username)
            else:
                return redirect('purchaseorder', vendorno=vendorno, username=username)
        return HttpResponse(status=405)  # Method not allowed if not POST


#when admin rejects inspection date the date from proposed inspection date get deleted
def reject_inspection(request, vendorno, username):
    user=get_object_or_404(UserMain,username=username)
    if request.session.get('authenticated_admin') != username:
        return redirect('adminlogin')
    else:
        if request.method == 'POST':
            selected_ponos = json.loads(request.POST.get('selected_ponos', '[]'))
            user = get_object_or_404(UserMain, username=username)
            rejection_reason = request.POST.get('reject_reason', '')
            newdate = request.POST.get('bulk_inspection_date')
            orders = []

            for pono in selected_ponos:
                order = get_object_or_404(PurchaseOrder, pono=pono)
                # Update fields and save the order
                
                if newdate:
                    order.inspectiondate = newdate
                    order.inspectiondateproposed = newdate
                else:
                    order.inspectiondate = None
                    order.inspectiondateproposed = None
                    order.iasubmissiondate = None
                order.alerts = None
                order.status = "Inspection date to be proposed"
                order.vendoralerts = f"Time:{datetime.now().strftime('%Y-%m-%d %H:%M')} <br> Inspection date rejected <br> Reason:{rejection_reason}"  # Assuming rejection_reason is a field in your PurchaseOrder model
                order.save()

                # Append order to the list with rejection reason
                orders.append({'order': order, 'rejection_reason': rejection_reason})

            # Prepare the context for the email template
            context = {
                'orders': orders,
                'vendorno': vendorno
            }

            # Render the email template
            email_body = render_to_string('rejection_email_template.html', context)

            # Send the email
            send_mail(
                'Inspection Dates Rejected',
                '',
                settings.EMAIL_HOST_USER,
                ['maveliprivate@gmail.com'],  # Replace with the recipient's email
                html_message=email_body,
                fail_silently=False,
            )

            # Redirect to the purchase order page or any other appropriate page
            if user.role == 'admin':
                return redirect('adminpurchaseorder', vendorno=vendorno, username=username)
            else:
                return redirect('purchaseorder', vendorno=vendorno, username=username)

        # If not a POST request, return method not allowed
        return HttpResponse(status=405)

#signin page    
@csrf_protect
def signin(request, vendorno):
    if request.method == 'POST':
        # Assuming 'vendorno' is passed in as a parameter or retrieved from the session
        username = vendorno  # Use vendorno as the username
        password = request.POST['password']
        
        order=get_object_or_404(Vendor, vendorno=vendorno)

        if order.password == password:
            request.session['authenticated_vendor'] = vendorno
            return redirect('vendorpurchaseorder',vendorno=vendorno)  # Redirect to the vendor purchase order page after successful login
        else:
            messages.error(request, "Invalid password.")
    
    return render(request, 'signin.html', {'vendorno':vendorno})

def vendoraccount(request, vendorno):
    if request.session.get('authenticated_vendor') != vendorno:
        return redirect('signin', vendorno=vendorno)
    
    vendor = get_object_or_404(Vendor, vendorno=vendorno)
    this = False
    
    if request.method == 'POST':
        this = True
        oldpass = request.POST['old_password']
        newpass = request.POST['new_password']
        confirmpass = request.POST['confirm_new_password']
        
        if oldpass != vendor.password:
            messages.error(request, "Old password incorrect")
        elif newpass != confirmpass:
            messages.error(request, "Passwords don't match")
        else:
            vendor.password = newpass
            vendor.save()  # Save the changes to the vendor
            messages.success(request, "Password successfully changed")
    
    # Clear 'this' when the page is refreshed
    if this and request.method != 'POST':
        this = False
        messages.error(request, "")
    
    return render(request, 'vendoraccount.html', {'vendor': vendor, 'this': this})


@csrf_protect
def adminlogin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # Check for admin credentials
        try:
            admin = UserMain.objects.get(username=username, password=password)
            request.session['authenticated_admin'] = admin.username
            if admin.role == 'admin' : # Store admin ID in session
                return redirect('adminhome',admin.username)
            elif admin.role == 'user':
                return redirect('userhome',admin.username)# Redirect to the admin dashboard or another page
            else:
                return redirect('qahome',admin.username)
        except UserMain.DoesNotExist:
            messages.error(request, 'Invalid credentials or not an admin user') # Redirect to the vendor purchase order page after successful login
    
    return render(request, 'adminlogin.html') 

    
    
