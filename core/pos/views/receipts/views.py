import json

from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, TemplateView

from core.pos.forms import Receipts, ReceiptsForm
from core.security.mixins import PermissionMixin


class ReceiptsListView(PermissionMixin, TemplateView):
    template_name = 'receipts/list.html'
    permission_required = 'view_receipts'

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'search':
                data = []
                for i in Receipts.objects.filter():
                    item = i.toJSON()
                    item['current_number'] = i.get_current_number()
                    data.append(item)
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('receipts_create')
        context['title'] = 'Listado de Tipos de Comprobantes'
        return context


class ReceiptsCreateView(PermissionMixin, CreateView):
    model = Receipts
    template_name = 'receipts/create.html'
    form_class = ReceiptsForm
    success_url = reverse_lazy('receipts_list')
    permission_required = 'add_receipts'

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'add':
                data = self.get_form().save()
            elif action == 'validate_data':
                data = {'valid': True}
                queryset = Receipts.objects.all()
                pattern = request.POST['pattern']
                parameter = request.POST['parameter'].strip()
                if pattern == 'code':
                    data['valid'] = not queryset.filter(code__iexact=parameter).exists()
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['list_url'] = self.success_url
        context['title'] = 'Nuevo registro de un Tipo de Comprobante'
        context['action'] = 'add'
        return context


class ReceiptsUpdateView(PermissionMixin, UpdateView):
    model = Receipts
    template_name = 'receipts/create.html'
    form_class = ReceiptsForm
    success_url = reverse_lazy('receipts_list')
    permission_required = 'change_receipts'

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'edit':
                data = self.get_form().save()
            elif action == 'validate_data':
                data = {'valid': True}
                queryset = Receipts.objects.all().exclude(id=self.object.id)
                pattern = request.POST['pattern']
                parameter = request.POST['parameter'].strip()
                if pattern == 'code':
                    data['valid'] = not queryset.filter(code__iexact=parameter).exists()
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['list_url'] = self.success_url
        context['title'] = 'Edición de un Tipo de Comprobante'
        context['action'] = 'edit'
        return context


class ReceiptsDeleteView(PermissionMixin, DeleteView):
    model = Receipts
    template_name = 'receipts/delete.html'
    success_url = reverse_lazy('receipts_list')
    permission_required = 'delete_receipts'

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
