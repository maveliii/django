from rest_framework import serializers
from mainApp.models import AppMainVendor as Vendor, AppMainPurchaseorder as PurchaseOrder

class VendorsSerializer(serializers.ModelSerializer):
    class Meta:
        model=Vendor
        fields=("vendor_no","vendor_name","email","region","ia_date")

class PurchaseOrdersSerializer(serializers.ModelSerializer):
    VendorNo = serializers.PrimaryKeyRelatedField(queryset=Vendor.objects.all())

    class Meta:
        model=PurchaseOrder
        fields=("po_no","vendor_no","customer","delivery_date","ia_sub","inspection_date")