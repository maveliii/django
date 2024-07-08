from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from mainApp.models import AppMainVendor as Vendor
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
def main(request):
    # Annotate Vendor with the count of PurchaseOrders
    if request.session.get('authenticated_admin') != "maveli123":
        return redirect('adminlogin')
    
    vendor = Vendor.objects.annotate(po_count=Count('appmainpurchaseorder__pono') ,pending_inspection_count=Count('appmainpurchaseorder__pono', filter=Q(appmainpurchaseorder__inspectiondate__isnull=True)))
    purchase = PurchaseOrder.objects.all()
    
    return render(request, 'index.html', {
        "vendor": vendor,
        "purchase": purchase
    })


#redirected from 'main' when admin clicks on a vendor shows all PO's of a vendor
def purchaseorder(request,vendorno):
    purchase = PurchaseOrder.objects.filter(vendorno=vendorno)
    return render(request, 'purchase.html', {"purchase": purchase})



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
        pono = request.POST.get('pono')
        new_date = request.POST.get('new_date')
        
        try:
            purchase_order = PurchaseOrder.objects.get(pono=pono)
            purchase_order.inspectiondateproposed = new_date
            purchase_order.status = "Inspection Date Proposed"
            purchase_order.alerts = "Inspection date Proposed Click to View"
            purchase_order.iasubmissiondate = datetime.now()
            purchase_order.save()
            return JsonResponse({'success': True})
        except PurchaseOrder.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Purchase Order not found'})
    return JsonResponse({'success': False, 'error': 'Invalid request'})


#when admin approves inspection date the date from proposed inspection date get saved to inspection date
def approve_inspection(request, pono):
    if request.method == 'POST':
        order = get_object_or_404(PurchaseOrder, pono=pono)
        order.inspectiondate = order.inspectiondateproposed
        order.status = "Inspection Date Approved"
        order.alerts = None
        order.save()
        send_mail(
                'Inspection Date Approved',
                f'The inspection date for PO {order.pono} has been approved and set to {order.inspectiondate}.',
                settings.EMAIL_HOST_USER,
                ['mavelinitc@gmail.com'],  # Replace with the recipient's email
                fail_silently=False,
            )
        return redirect('purchaseorder', vendorno=order.vendorno_id)
    return HttpResponse(status=405)  # Method not allowed if not POST


#when admin rejects inspection date the date from proposed inspection date get deleted
def reject_inspection(request, pono):
    if request.method == 'POST':
        order = get_object_or_404(PurchaseOrder, pono=pono)
        
        # Assuming the rejection reason is submitted via POST data
        rejection_reason = request.POST.get('reject_reason', '')

        # Update fields and save the order
        order.inspectiondateproposed = None
        order.inspectiondate = None 
        order.alerts = None
         # Save rejection reason or use another field
        order.save()

        # Send email notification
        send_mail(
            'Inspection Date Rejected',
            f'The inspection date for PO {order.pono} has been rejected.\n\nRejection Reason: {rejection_reason}\n\nPlease update your changed inspection date in the portal.',
            settings.EMAIL_HOST_USER,
            ['mavelinitc@gmail.com'],  # Replace with the recipient's email
            fail_silently=False,
        )

        # Redirect to the purchase order page or any other appropriate page
        return redirect('purchaseorder', vendorno=order.vendorno_id)

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


@csrf_protect
def adminlogin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        request.session['authenticated_admin'] = username
        if username == "maveli123":
            if password == "maveli*1":
                request.session['authenticated_admin'] = username
                return redirect('home')
            else:
                messages.error(request, "Invalid password") # Redirect to the vendor purchase order page after successful login
        else:
            messages.error(request, "Invalid username")
    
    return render(request, 'adminlogin.html') 

    
    
