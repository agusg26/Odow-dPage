from django.shortcuts import render

# Create your views here.
from django.views import generic
from .models import Cerveza, Servicio, Barril, DetallePedido, Pedido

#gepeto
from django.views.generic import FormView, DeleteView
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from .models import Cerveza, Pedido, DetallePedido, Servicio
from .forms import VentaForm, ServicioForm
from django.contrib.auth.mixins import LoginRequiredMixin

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
        context['barriles'] = self.object.barriles.all()
        return context

class CervezaCreateView(LoginRequiredMixin,generic.CreateView):
    model = Cerveza
    fields = ['nombre', 'descripcion', 'estilo', 'porcentaje_alcohol', 'ibu', 'precio_litro', 'foto']

    template_name = 'cerveza_new.html'
    success_url = '/catalogo/cervezas/' 

class CervezaUpdateView(LoginRequiredMixin,generic.UpdateView):
    model = Cerveza
    fields = ['nombre', 'descripcion', 'estilo', 'porcentaje_alcohol', 'ibu']
    template_name = 'cerveza_form.html'
    success_url = '/catalogo/cervezas/'

class ServicioListView(generic.ListView):
    model = Servicio
    template_name = 'servicio_list.html'
    context_object_name = 'servicios'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cerveza_id = self.kwargs.get('cerveza_id')
        context['cerveza'] = get_object_or_404(Cerveza, pk=cerveza_id)
        return context

class ServicioDetailView(generic.DetailView):
    model = Cerveza
    template_name = 'cerveza_detail.html'
    context_object_name = 'servicio'

#vista que recive 2 parametros desde la url
def realizar_venta(request, cerveza_id, servicio_id):

    #con estos se obtienen los 2 objetos con el id pasado por parametro
    cerveza = get_object_or_404(Cerveza, id=cerveza_id)
    servicio = get_object_or_404(Servicio, id=servicio_id)

    if request.method == 'POST':
        form = VentaForm(cerveza, request.POST)
        if form.is_valid():
            #se obtienen los datos del formulario. El barril y la cantidad
            barril = form.cleaned_data['barril']
            cantidad = form.cleaned_data['cantidad']

            #controla la cantidad solicitada
            if cantidad > barril.stock:
                form.add_error('cantidad', 'Cantidad mayor al stock disponible')
            else:
                #se crea un pedido con los datos 
                pedido = Pedido.objects.create(servicio=servicio)
                detalle = DetallePedido.objects.create(
                    pedido=pedido,
                    barril=barril,
                    cantidad=cantidad,
                    subtotal=barril.calcular_precio() * cantidad
                )
                pedido.actualizar_total()
                return redirect('cervezas') 
    else:
        form = VentaForm(cerveza)

    return render(request, 'venta_form.html', {
        'form': form,
        'cerveza': cerveza,
        'servicio': servicio,
    })

    
class ServicioEstaticoListView(generic.ListView):
    model = Servicio
    template_name = 'servicioEstatico_list.html'  # nombre del archivo HTML
    context_object_name = 'servicios'     # variable en el template

class ServicioCreateView(LoginRequiredMixin,generic.CreateView):
    model = Servicio
    form_class = ServicioForm
    template_name = 'servicio_form.html'
    success_url = reverse_lazy('servicioEstatico_list')   # redirige a la lista
    login_url = '/accounts/login/'


class ServicioUpdateView(LoginRequiredMixin,generic.UpdateView):
    model = Servicio
    form_class = ServicioForm
    template_name = 'servicio_form.html'
    success_url = reverse_lazy('servicioEstatico_list')

class ServicioDeleteView(LoginRequiredMixin,DeleteView):
    model = Servicio
    template_name = 'servicio_confirm_delete.html'
    success_url = reverse_lazy('servicioEstatico_list')