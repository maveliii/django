from django.conf import settings
import json
from django.core.mail import send_mail
from mainApp.models import AppMainPurchaseorder as PurchaseOrder
from mainApp.models import AppMainVendor as Vendor
from datetime import datetime, timedelta
from django.utils.html import format_html


def send_alert_mails():
    vendors = Vendor.objects.all()
    for vendor in vendors:
        main_content = ''
        vendor_no = vendor.vendorno
        purchases = PurchaseOrder.objects.filter(vendorno=vendor_no, shipdate=datetime.now() + timedelta(days=vendor.iaalertdays-4))

        if purchases.exists():
            table_content = '<table border="1" style="border-collapse: collapse;">'
            table_content += '<tr><th>BU Name</th><th>PO#</th><th>Last Delivery Date</th></tr>'
            
            for purchase in purchases:
                table_content += format_html(
                    '<tr><td>{}</td><td>{}</td><td>{}</td></tr>',
                    purchase.customer,
                    purchase.pono,
                    purchase.shipdate.strftime('%Y-%m-%d')  # Adjust to the correct attribute name for the customer
                )
            
            table_content += '</table>'
            main_content += f'<p>Dear Supplier,</p>'
            main_content += "<p>Please submit  IA for below PO's:</p>"
            main_content += table_content
            main_content += '<p>Please submit the same using the following link</p>'
            main_content += f'<p>http://10.0.0.208:8000/{vendor.vendorno}/signin</p>'
            main_content += '<p>This is an automatically generated mail. Please do not reply</p>'
            main_content += '<p>Regards,</p><p>J&J sourcing</p>'

            send_mail(
                subject=f'Ia Alert - {vendor.vendorname}',
                message='This is a test mail with HTML content.',  # Plain text version (fallback)
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=['maveliprivate@gmail.com'],  # Ensure 'email' field exists in Vendor model
                html_message=main_content,  # HTML content of the email
                fail_silently=False,
            )

            print(f'Email sent to {vendor.vendorname} {vendor.vendorno}')