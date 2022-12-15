import json

from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import FormView, DeleteView

from core.pos.models import ReceiptStates
from core.reports.forms import ReportForm
from core.security.mixins import PermissionMixin


class ReceiptStatesListView(PermissionMixin, FormView):
    template_name = 'receipt_states/list.html'
    form_class = ReportForm
    permission_required = 'view_receipt_states'

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'search':
                data = []
                start_date = request.POST['start_date']
                end_date = request.POST['end_date']
                receipts = request.POST['receipts']
                queryset = ReceiptStates.objects.filter()
                if len(start_date) and len(end_date):
                    queryset = queryset.filter(date_joined__range=[start_date, end_date])
                if len(receipts):
                    queryset = queryset.filter(receipts_id=receipts)
                for i in queryset:
                    data.append(i.toJSON())
            else:
                data['error'] = 'No ha ingresado una opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Estado de Comprobantes'
        return context


class ReceiptStatesDeleteView(PermissionMixin, DeleteView):
    model = ReceiptStates
    template_name = 'receipt_states/delete.html'
    success_url = reverse_lazy('devolution_list')
    permission_required = 'delete_devolution'

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            self.get_object().delete()
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Notificación de eliminación'
        context['list_url'] = self.success_url
        return context
