from django.shortcuts import render

# Create your views here.
from django.views import generic
from .models import Cerveza, Servicio, Barril, DetallePedido, Pedido

#gepeto
from django.views.generic import FormView, DeleteView
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from .models import Cerveza, Pedido, DetallePedido, Servicio, Chopera
from .forms import VentaForm, ServicioForm, BarrilForm, ChoperaForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

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
    fields = ['nombre', 'descripcion', 'estilo', 'porcentaje_alcohol', 'ibu', 'foto']
    template_name = 'cerveza_form.html'
    success_url = '/catalogo/cervezas/'


@login_required
def borrar_cerveza(request, pk):
    cerveza = get_object_or_404(Cerveza, pk=pk)

    if request.method == 'POST':
        cerveza.delete()
        return redirect('cervezas') 
    
    return redirect('cervezas')



class ServicioListView(generic.ListView):
    model = Servicio
    template_name = 'servicio_list.html'
    context_object_name = 'servicios'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cerveza_id = self.kwargs.get('cerveza_id')
        cerveza = get_object_or_404(Cerveza, pk=cerveza_id)
        context['cerveza'] = cerveza
        context['barriles'] = cerveza.barriles.all()  
        return context

class ServicioDetailView(generic.DetailView):
    model = Cerveza
    template_name = 'cerveza_detail.html'
    context_object_name = 'servicio'

#vista que recive 2 parametros desde la url
def realizar_venta(request, cerveza_id, servicio_id):

    cerveza = get_object_or_404(Cerveza, id=cerveza_id)
    servicio = get_object_or_404(Servicio, id=servicio_id)

    if request.method == 'POST':
        form = VentaForm(cerveza, request.POST)
        if form.is_valid():
            barril = form.cleaned_data['barril']
            cantidad = form.cleaned_data['cantidad']

            if cantidad > barril.stock:
                form.add_error('cantidad', 'Cantidad mayor al stock disponible')
            else:
                if servicio.tipo.nombre == 'Chopera':
                    choperas_disponibles = Chopera.objects.filter(disponible=True)
                    cantidad_choperas = choperas_disponibles.count()

                    if cantidad_choperas == 0:
                        form.add_error(None, "No hay choperas disponibles para este servicio.")
                    elif cantidad > cantidad_choperas:
                        form.add_error('cantidad', f'Solo hay {cantidad_choperas} choperas disponibles.')
                    else:
                        # crear pedido, asignar choperas, etc.
                        pedido = Pedido.objects.create(servicio=servicio)
                        DetallePedido.objects.create(
                            pedido=pedido,
                            barril=barril,
                            cantidad=cantidad,
                            subtotal=barril.calcular_precio() * cantidad
                        )
                        pedido.actualizar_total()

                        # Marcar las choperas asignadas como ocupadas (las primeras 'cantidad')
                        choperas_asignadas = choperas_disponibles[:cantidad]
                        for chopera in choperas_asignadas:
                            chopera.disponible = False
                            chopera.save()

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

#para control de barriles y stock
def editar_stock_barriles(request, cerveza_id):
    cerveza = get_object_or_404(Cerveza, pk=cerveza_id)
    barriles = Barril.objects.filter(cerveza=cerveza)

    if request.method == "POST":
        form = BarrilForm(request.POST)
        if form.is_valid():
            nuevo_barril = form.save(commit=False)
            nuevo_barril.cerveza = cerveza

            # busca si ya existe un barril con la misma cerveza y litros
            barril_existente = Barril.objects.filter(
                cerveza=cerveza,
                litros=nuevo_barril.litros 
            ).first()

            if barril_existente:
                #sumar el stock del nuevo barril al existente
                barril_existente.stock += nuevo_barril.stock
                barril_existente.save()
            else:
                nuevo_barril.save()

            return redirect('editar_stock_barriles', cerveza_id=cerveza.id)
    else:
        form = BarrilForm()

    return render(request, 'editar_stock_barriles.html', {
        'cerveza': cerveza,
        'barriles': barriles,
        'form': form
    })



def editar_barril(request, barril_id):
    barril = get_object_or_404(Barril, pk=barril_id)

    if request.method == 'POST':
        form = BarrilForm(request.POST, instance=barril)
        if form.is_valid():
            form.save()
            return redirect('editar_stock_barriles', cerveza_id=barril.cerveza.id)
    else:
        form = BarrilForm(instance=barril)

    return render(request, 'editar_barril.html', {'form': form, 'barril': barril})

def eliminar_barril(request, barril_id):
    barril = get_object_or_404(Barril, pk=barril_id)
    cerveza_id = barril.cerveza.id

    if request.method == 'POST':
        barril.delete()
        return redirect(reverse('editar_stock_barriles', kwargs={'cerveza_id': cerveza_id}))
    else:
        return redirect(reverse('editar_stock_barriles', kwargs={'cerveza_id': cerveza_id}))

#para control de choperas y stock
def editar_stock_choperas(request):
    choperas = Chopera.objects.all()

    if request.method == 'POST':
        form = ChoperaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('editar_stock_choperas')
    else:
        form = ChoperaForm()

    return render(request, 'editar_stock_choperas.html', {
        'choperas': choperas,
        'form': form
    })

# Editar una chopera existente
def editar_chopera(request, chopera_id):
    chopera = get_object_or_404(Chopera, pk=chopera_id)

    if request.method == 'POST':
        form = ChoperaForm(request.POST, instance=chopera)
        if form.is_valid():
            form.save()
            return redirect('editar_stock_choperas')
    else:
        form = ChoperaForm(instance=chopera)

    return render(request, 'editar_chopera.html', {'form': form, 'chopera': chopera})

def eliminar_chopera(request, chopera_id):
    chopera = get_object_or_404(Chopera, pk=chopera_id)

    if request.method == 'POST':
        chopera.delete()
        return redirect('editar_stock_choperas')

    return redirect('editar_stock_choperas')