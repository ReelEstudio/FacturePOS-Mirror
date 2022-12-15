import json
import os
import random
import string

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from core.pos.models import *
from core.security.models import *


def insert_data():
    numbers = list(string.digits)

    Receipts(name='FACTURA', code='01', start_number='000000000', end_number='999999999').save()
    Receipts(name='LIQUIDACIÓN DE COMPRA DE BIENES Y PRESTACIÓN DE SERVICIOS', code='03', start_number='000000000', end_number='999999999').save()
    Receipts(name='NOTA DE CRÉDITO', code='04', start_number='000000000', end_number='999999999').save()
    Receipts(name='NOTA DE DÉBITO', code='05', start_number='000000000', end_number='999999999').save()
    Receipts(name='GUÍA DE REMISIÓN', code='06', start_number='000000000', end_number='999999999').save()
    Receipts(name='COMPROBANTE DE RETENCIÓN', code='07', start_number='000000000', end_number='999999999').save()

    with open(f'{settings.BASE_DIR}/deploy/json/products.json', encoding='utf8') as json_file:
        for item in json.load(json_file):
            product = Product()
            product.name = item['name']
            product.code = item['code']
            product.category = product.get_or_create_category(name=item['category'])
            product.price = float(item['price'])
            product.pvp = float(item['pvp'])
            product.save()
            print(f'record inserted product {product.id}')

    category = Category(name='SERVICIOS')
    category.save()
    Product(name='FORMATEO DE COMPUTADORAS', category=category, inventoried=False, with_tax=False, pvp=15.00, code='FORMATEO85451').save()

    with open(f'{settings.BASE_DIR}/deploy/json/customers.json', encoding='utf8') as json_file:
        data = json.load(json_file)
        for item in data[0:20]:
            provider = Provider()
            provider.name = item['company'].upper()
            provider.ruc = f"0{''.join(random.choices(numbers, k=12))}"
            provider.mobile = f"0{''.join(random.choices(numbers, k=9))}"
            provider.address = item['country']
            provider.email = item['email']
            provider.save()
            print(f'record inserted provider {provider.id}')

    for i in range(1, 10):
        purchase = Purchase()
        purchase.number = ''.join(random.choices(numbers, k=8))
        purchase.provider_id = random.randint(1, Provider.objects.count())
        purchase.save()
        print(f'record inserted purchase {purchase.id}')

        for d in range(1, 5):
            detail = PurchaseDetail()
            detail.purchase_id = purchase.id
            detail.product_id = random.randint(1, Product.objects.all().count())
            while purchase.purchasedetail_set.filter(product_id=detail.product_id).exists():
                detail.product_id = random.randint(1, Product.objects.all().count())
            detail.cant = random.randint(1, 50)
            detail.price = detail.product.pvp
            detail.subtotal = float(detail.price) * detail.cant
            detail.save()
            detail.product.stock += detail.cant
            detail.product.save()

        purchase.calculate_invoice()

    user = User(names='Consumidor Final', dni='9999999999999', email='davilawilliam94@gmail.com', username='9999999999999')
    user.set_password(user.dni)
    user.save()
    user.groups.add(Group.objects.get(pk=settings.GROUPS.get('client')))
    client = Client()
    client.user = user
    client.birthdate = date(1994, 10, 19)
    client.mobile = '9999999999'
    client.address = 'Milagro, cdla. Paquisha'
    client.identification_type = IDENTIFICATION_TYPE[3][0]
    client.send_email_invoice = False
    client.save()

    user = User(names='William Jair Dávila Vargas', dni='0928363993', email='wdavilav1994@gmail.com', username='0928363993')
    user.set_password(user.dni)
    user.save()
    user.groups.add(Group.objects.get(pk=settings.GROUPS.get('client')))
    client = Client()
    client.user = user
    client.birthdate = date(1994, 10, 19)
    client.mobile = '0979014551'
    client.address = 'Milagro, cdla. Paquisha'
    client.save()

    user = User(names='LIBRIMUNDI LIBRERÍA INTERNACIONAL S.A.', dni='1791411293001', email='williamjairdavilavargas@gmail.com', username='1791411293001')
    user.set_password(user.dni)
    user.save()
    user.groups.add(Group.objects.get(pk=settings.GROUPS.get('client')))
    client = Client()
    client.user = user
    client.birthdate = date(1994, 10, 19)
    client.mobile = '0979014552'
    client.address = 'Milagro, cdla. Paquisha'
    client.identification_type = IDENTIFICATION_TYPE[1][0]
    client.save()

    with open(f'{settings.BASE_DIR}/deploy/json/customers.json', encoding='utf8') as json_file:
        data = json.load(json_file)
        for item in data[21:41]:
            user = User()
            user.names = f"{item['first']} {item['last']}"
            user.dni = f"0{''.join(random.choices(numbers, k=9))}"
            user.email = item['email']
            user.username = user.dni
            user.set_password(user.dni)
            user.save()
            user.groups.add(Group.objects.get(pk=settings.GROUPS.get('client')))
            client = Client()
            client.user = user
            client.birthdate = date(random.randint(1969, 2006), random.randint(1, 12), random.randint(1, 28))
            client.mobile = f"0{''.join(random.choices(numbers, k=9))}"
            client.address = item['country']
            client.save()
            print(f'record inserted client {client.id}')

    # for i in range(1, random.randint(6, 10)):
    #     sale = Sale()
    #     sale.voucher_number = f'{Sale.objects.count() + 1:09d}'
    #     sale.receipts_id = 1
    #     sale.employee_id = 1
    #     sale.client_id = random.randint(1, Client.objects.all().count())
    #     sale.iva = 0.12
    #     sale.save()
    #     print(f'record inserted sale {sale.id}')
    #     for d in range(1, 8):
    #         list_products = list(Product.objects.filter(stock__gt=0).values_list(flat=True))
    #         if len(list_products):
    #             detail = SaleDetail()
    #             detail.sale_id = sale.id
    #             detail.product_id = random.choice(list_products)
    #             detail.cant = random.randint(1, detail.product.stock)
    #             detail.price = detail.product.pvp
    #             detail.save()
    #             detail.product.stock -= detail.cant
    #             detail.product.save()
    #     sale.calculate_detail()
    #     sale.calculate_invoice()
    #     sale.cash = sale.total
    #     sale.voucher_number = sale.generate_voucher_number()
    #     sale.save()


insert_data() # comment
