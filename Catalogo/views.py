from django.shortcuts import render

# Create your views here.
from django.views import generic
from .models import Cerveza, Servicio, Barril, DetallePedido, Pedido
import calendar
from datetime import date, timedelta
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
def generar_calendario_html(servicio):
    hoy = date.today()
    año = hoy.year
    mes = hoy.month

    dias_ocupados = Pedido.objects.filter(
        servicio=servicio,
        fecha_alquiler__month=mes,
        fecha_alquiler__year=año
    ).values_list('fecha_alquiler', flat=True)

    class CalendarioDisponible(calendar.HTMLCalendar):
        def formatday(self, day, weekday):
            if day == 0:
                return '<td></td>'  # Día vacío

            fecha_actual = date(año, mes, day)
            if fecha_actual in dias_ocupados:
                return f'<td class="text-muted bg-light">{day}</td>'
            return f'<td class="text-success font-weight-bold">{day}</td>'

    cal = CalendarioDisponible()
    return cal.formatmonth(año, mes)

# en tu vista
def realizar_venta(request, cerveza_id, servicio_id):
    cerveza = get_object_or_404(Cerveza, id=cerveza_id)
    servicio = get_object_or_404(Servicio, id=servicio_id)

    calendario_html = generar_calendario_html(servicio)

    if request.method == 'POST':
        form = VentaForm(cerveza, request.POST)
        if form.is_valid():
            barril = form.cleaned_data['barril']
            cantidad = form.cleaned_data['cantidad']
            ubicacion_entrega=form.cleaned_data['ubicacion_entrega']
            provincia = request.POST.get('provincia')
            localidad = request.POST.get('localidad')
            direccion = request.POST.get('direccion')
            ubicacion = f"{direccion}, {localidad}, {provincia}"

            if cantidad > barril.stock:
                form.add_error('cantidad', 'Cantidad mayor al stock disponible')
            else:
                pedido = Pedido.objects.create(
                    servicio=servicio,
                    fecha_alquiler=form.cleaned_data['fecha_alquiler'],
                    ubicacion_entrega=ubicacion 
                )
                DetallePedido.objects.create(
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
        'calendario_html': calendario_html
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