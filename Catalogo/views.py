from django.shortcuts import render

# Create your views here.
from django.views import generic
from .models import Cerveza, Formato, Servicio, Chopera, Barra

def index(request):
    return render(request, 'index.html')


class CervezaListView(generic.ListView):
    model = Cerveza
    template_name = 'cerveza_list.html'
    context_object_name = 'cervezas'

class CervezaDetailView(generic.DetailView):
    model = Cerveza
    template_name = 'cerveza_detail.html'
    context_object_name = 'cerveza'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['formatos'] = self.object.formato_set.all()
        return context

class CervezaCreateView(generic.CreateView):
    model = Cerveza
    fields = ['nombre', 'descripcion', 'estilo', 'porcentaje_alcohol', 'ibu']
    template_name = 'cerveza_new.html'
    success_url = '/catalogo/cervezas/' 

class CervezaUpdateView(generic.UpdateView):
    model = Cerveza
    fields = ['nombre', 'descripcion', 'estilo', 'porcentaje_alcohol', 'ibu']
    template_name = 'cerveza_form.html'
    success_url = '/catalogo/cervezas/'
