import base64
import os.path
import smtplib
import subprocess
import sys

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path

from django.core.files import File
from tempfile import NamedTemporaryFile
from lxml import etree
from suds.client import Client

from config import settings
from core.pos.choices import VOUCHER_STATUS
from core.pos.models import Company, ReceiptStates


class XMLElectronicSignature:
    def __init__(self):
        self.company = Company.objects.first()
        self.base_dir = os.path.dirname(__file__)
        self.jar_path = self.get_absolute_path(os.path.join(os.path.dirname(self.base_dir), 'resources/jar/sri.jar'))
        self.certificate_path = self.get_absolute_path(f'{settings.BASE_DIR}/{self.company.get_electronic_signature()}')
        self.folder_signed = 'xml/firmados/'
        self.folder_generated = 'xml/generados/'
        self.folder_valid = 'xml/validos/'
        self.folder_authorized = 'xml/autorizados/'
        self.certificate_key = self.company.electronic_signature_key
        self.receipt_url = self.get_receipt_url()
        self.authorization_url = self.get_authorization_url()
        self.folder_divider = '\\' if sys.platform in ['win32', 'cygwin'] else '/'

    def get_absolute_path(self, path):
        return str(Path(path).absolute())

    def get_receipt_url(self):
        if self.company.environment_type == 2:
            return 'https://cel.sri.gob.ec/comprobantes-electronicos-ws/RecepcionComprobantesOffline?wsdl'
        return 'https://celcer.sri.gob.ec/comprobantes-electronicos-ws/RecepcionComprobantesOffline?wsdl'

    def get_authorization_url(self):
        if self.company.environment_type == 2:
            return 'https://cel.sri.gob.ec/comprobantes-electronicos-ws/AutorizacionComprobantesOffline?wsdl'
        return 'https://celcer.sri.gob.ec/comprobantes-electronicos-ws/AutorizacionComprobantesOffline?wsdl'

    def get_or_create_folder(self, folder, name=None):
        if not os.path.exists(folder):
            os.mkdir(folder, mode=0o777)
        if name is None:
            return folder
        return f'{folder}/{name}'

    def create_xml(self, instance):
        receipt_states = ReceiptStates()
        receipt_states.status = VOUCHER_STATUS[1][0]
        receipt_states.receipts = instance.receipts
        receipt_states.content_object = instance
        try:
            xml_text, access_code = instance.generate_xml()
            with NamedTemporaryFile(delete=True) as file_temp:
                xml_path = os.path.join(self.folder_generated, f'{instance.receipts.get_name_xml()}_{access_code}.xml')
                file_temp.write(xml_text.strip().encode())
                file_temp.flush()
                receipt_states.state = True
                receipt_states.archive.save(name=xml_path, content=File(file_temp))
                instance.access_code = access_code
                instance.save()
        except Exception as e:
            receipt_states.status = False
            receipt_states.errors = {'error': str(e)}
            receipt_states.save()
        finally:
            if receipt_states.state:
                instance.status = VOUCHER_STATUS[1][0]
                instance.save()
            return receipt_states.state

    def firm_xml(self, instance):
        queryset = ReceiptStates.objects.filter(object_id=instance.id, content_type__model=instance.__class__.__name__.lower(), status=VOUCHER_STATUS[1][0]).exclude(state=False)
        if queryset.exists():
            object_receipt_states = queryset[0]
            receipt_states = ReceiptStates()
            receipt_states.receipts = instance.receipts
            receipt_states.content_object = instance
            receipt_states.status = VOUCHER_STATUS[2][0]
            try:
                xml_name = object_receipt_states.archive.name.split('/')[-1]
                commands = ['java', '-jar', self.jar_path, self.certificate_path, self.certificate_key, object_receipt_states.get_full_file_path(), self.base_dir, xml_name]
                procedure = subprocess.run(args=commands, capture_output=True)
                if procedure.returncode == 0:
                    error = procedure.stdout.decode('utf-8')
                    if error.__contains__('Error'):
                        receipt_states.state = False
                        receipt_states.errors = {'error': error}
                        receipt_states.save()
                    else:
                        receipt_states.state = True
                        xml_name_full = os.path.join(self.base_dir, xml_name)
                        with open(xml_name_full, 'rb') as file:
                            xml_path = os.path.join(self.folder_signed, xml_name)
                            receipt_states.state = True
                            receipt_states.archive.save(name=xml_path, content=File(file))
                            receipt_states.save()
                        if os.path.exists(xml_name_full):
                            os.remove(xml_name_full)
                else:
                    receipt_states.state = False
                    receipt_states.errors = {'error': procedure.stderr.decode('utf-8')}
                    receipt_states.save()
            except Exception as e:
                receipt_states.state = False
                receipt_states.errors = {'error': str(e)}
                receipt_states.save()
            finally:
                if receipt_states.state:
                    instance.status = VOUCHER_STATUS[2][0]
                    instance.save()
                return receipt_states.state
        return False

    def validate(self, instance):
        queryset = ReceiptStates.objects.filter(object_id=instance.id, content_type__model=instance.__class__.__name__.lower(), status=VOUCHER_STATUS[2][0]).exclude(state=False)
        if queryset.exists():
            object_receipt_states = queryset[0]
            receipt_states = ReceiptStates()
            receipt_states.receipts = instance.receipts
            receipt_states.content_object = instance
            receipt_states.status = VOUCHER_STATUS[3][0]
            try:
                with open(object_receipt_states.get_full_file_path(), 'r') as file:
                    document = file.read().strip().encode('utf-8')
                base64_binary_xml = base64.b64encode(document).decode('utf-8')
                sri_client = Client(self.receipt_url)
                result = sri_client.service.validarComprobante(base64_binary_xml)
                status = result.estado
                if status == 'DEVUELTA':
                    receipt = result.comprobantes.comprobante[0]
                    content = {'access_code': receipt.claveAcceso, 'errors': []}
                    for count, value in enumerate(receipt.mensajes):
                        message = value[1][count]
                        values = dict()
                        for name in ['identificador', 'informacionAdicional', 'mensaje', 'tipo']:
                            if name in message:
                                values[name] = message[name]
                        content['errors'].append(values)
                    receipt_states.state = False
                    receipt_states.errors = content
                    receipt_states.save()
                elif status == 'RECIBIDA':
                    xml_name = object_receipt_states.archive.name.split('/')[-1]
                    with NamedTemporaryFile(delete=True) as file_temp:
                        xml_path = os.path.join(self.folder_valid, xml_name)
                        file_temp.write(document)
                        file_temp.flush()
                        receipt_states.state = True
                        receipt_states.archive.save(name=xml_path, content=File(file_temp))
            except Exception as e:
                receipt_states.state = False
                receipt_states.errors = {'error': str(e)}
                receipt_states.save()
            finally:
                if receipt_states.state:
                    instance.status = VOUCHER_STATUS[3][0]
                    instance.save()
                return receipt_states.state
        return False

    def authorize(self, instance):
        queryset = ReceiptStates.objects.filter(object_id=instance.id, content_type__model=instance.__class__.__name__.lower(), status=VOUCHER_STATUS[3][0]).exclude(state=False)
        if queryset.exists():
            object_receipt_states = queryset[0]
            receipt_states = ReceiptStates()
            receipt_states.receipts = instance.receipts
            receipt_states.content_object = instance
            receipt_states.status = VOUCHER_STATUS[4][0]
            try:
                sri_client = Client(self.authorization_url)
                invoice = object_receipt_states.content_object
                result = sri_client.service.autorizacionComprobante(invoice.access_code)
                if len(result):
                    receipt = result[2].autorizacion[0]
                    if receipt.estado == 'NO AUTORIZADO':
                        content = {'access_code': invoice.access_code, 'status': receipt.estado, 'authorization_date': str(receipt.fechaAutorizacion), 'errors': []}
                        for count, value in enumerate(receipt.mensajes):
                            message = value[1][count]
                            values = dict()
                            for name in ['identificador', 'informacionAdicional', 'mensaje', 'tipo']:
                                if name in message:
                                    values[name] = message[name]
                            content['errors'].append(values)
                        receipt_states.state = False
                        receipt_states.errors = content
                        receipt_states.save()
                    else:
                        xml_authorization = etree.Element('autorizacion')
                        etree.SubElement(xml_authorization, 'estado').text = receipt.estado
                        etree.SubElement(xml_authorization, 'numeroAutorizacion').text = receipt.numeroAutorizacion
                        etree.SubElement(xml_authorization, 'fechaAutorizacion', attrib={'class': "fechaAutorizacion"}).text = str(receipt.fechaAutorizacion.strftime("%d/%m/%Y %H:%M:%S"))
                        voucher_sri = etree.SubElement(xml_authorization, 'comprobante')
                        voucher_sri.text = etree.CDATA(receipt.comprobante)
                        xml_text = etree.tostring(xml_authorization, encoding="utf8", xml_declaration=True).decode('utf8').replace("'", '"')
                        with NamedTemporaryFile(delete=True) as file_temp:
                            xml_name = object_receipt_states.archive.name.split('/')[-1]
                            xml_path = os.path.join(self.folder_authorized, xml_name)
                            file_temp.write(xml_text.encode())
                            file_temp.flush()
                            receipt_states.state = True
                            receipt_states.archive.save(name=xml_path, content=File(file_temp))
                            instance.authorization_date = receipt.fechaAutorizacion
                            instance.xml_authorized = receipt_states.archive
                            instance.generate_pdf_authorized()
                            instance.save()
            except Exception as e:
                receipt_states.state = False
                receipt_states.errors = {'error': str(e)}
                receipt_states.save()
            finally:
                if receipt_states.state:
                    instance.status = VOUCHER_STATUS[4][0]
                    instance.save()
                return receipt_states.state
        return False

    def notify_by_email(self, instance, company, client):
        try:
            if client.send_email_invoice:
                message = MIMEMultipart('alternative')
                message['Subject'] = f'Notificación de {instance.receipts.name} {instance.voucher_number_full}'
                message['From'] = company.email_host_user
                message['To'] = client.user.email
                content = f'Estimado(a)\n\n{client.user.names.upper()}\n\n'
                content += f'{company.tradename} informa sobre documento electrónico emitido adjunto en formato XML Y PDF.\n\n'
                content += f'DOCUMENTO: {instance.receipts.name} {instance.voucher_number_full}\n'
                content += f"FECHA: {instance.date_joined.strftime('%Y-%m-%d')}\n"
                content += f'MONTO: {str(float(round(instance.total, 2)))}\n'
                content += f'CÓDIGO DE ACCESO: {instance.access_code}\n'
                content += f'AUTORIZACIÓN: {instance.access_code}'
                part = MIMEText(content)
                message.attach(part)
                with open(f'{settings.BASE_DIR}{instance.get_pdf_authorized()}', 'rb') as file:
                    part = MIMEApplication(file.read())
                    part.add_header('Content-Disposition', 'attachment', filename=f'{instance.access_code}.pdf')
                    message.attach(part)
                with open(f'{settings.BASE_DIR}{instance.get_xml_authorized()}', 'rb') as file:
                    part = MIMEApplication(file.read())
                    part.add_header('Content-Disposition', 'attachment', filename=f'{instance.access_code}.xml')
                    message.attach(part)
                server = smtplib.SMTP(company.email_host, company.email_port)
                server.starttls()
                server.login(company.email_host_user, company.email_host_password)
                server.sendmail(company.email_host_user, message['To'], message.as_string())
                server.quit()
            instance.status = VOUCHER_STATUS[5][0]
            instance.save()
        except:
            pass
