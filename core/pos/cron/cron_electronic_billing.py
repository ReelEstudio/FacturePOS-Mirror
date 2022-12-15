import os

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from datetime import datetime
from core.pos.choices import VOUCHER_STATUS
from core.pos.models import Sale, CreditNote
from core.pos.utilities.xml_electronic_signature import XMLElectronicSignature


def electronic_invoicing_receipts_invoice():
    xml_electronic_signature = XMLElectronicSignature()
    date_joined = datetime.now().date()
    for instance in Sale.objects.filter(date_joined=date_joined).exclude(status=VOUCHER_STATUS[5][0]):
        status = instance.status
        if status == VOUCHER_STATUS[0][0]:
            xml_electronic_signature.create_xml(instance)
        elif status == VOUCHER_STATUS[1][0]:
            xml_electronic_signature.firm_xml(instance)
        elif status == VOUCHER_STATUS[2][0]:
            xml_electronic_signature.validate(instance)
        elif status == VOUCHER_STATUS[3][0]:
            xml_electronic_signature.authorize(instance)
        elif status == VOUCHER_STATUS[4][0]:
            xml_electronic_signature.notify_by_email(instance=instance, company=instance.company, client=instance.client)
    for instance in CreditNote.objects.filter(date_joined=date_joined).exclude(status=VOUCHER_STATUS[5][0]):
        status = instance.status
        if status == VOUCHER_STATUS[0][0]:
            xml_electronic_signature.create_xml(instance)
        elif status == VOUCHER_STATUS[1][0]:
            xml_electronic_signature.firm_xml(instance)
        elif status == VOUCHER_STATUS[2][0]:
            xml_electronic_signature.validate(instance)
        elif status == VOUCHER_STATUS[3][0]:
            xml_electronic_signature.authorize(instance)
        elif status == VOUCHER_STATUS[4][0]:
            xml_electronic_signature.notify_by_email(instance=instance, company=instance.company, client=instance.sale.client)


electronic_invoicing_receipts_invoice()
