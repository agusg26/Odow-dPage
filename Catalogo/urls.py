from django.urls import path
from Catalogo import views

urlpatterns = [
    path('', views.index, name='index'),
    path('cervezas/', views.CervezaListView.as_view(), name='cervezas'),
    path('cerveza/<pk>', views.CervezaDetailView.as_view(), name='cerveza'),
    path('cerveza/new/', views.CervezaCreateView.as_view(), name='cerveza_new'),
    path('servicios/<cerveza_id>', views.ServicioListView.as_view(), name='servicios'),
    path('servicio/<int:pk>/', views.ServicioDetailView.as_view(), name='servicio'),
    path('venta/<int:cerveza_id>/servicio/<int:servicio_id>/', views.realizar_venta, name='venta'),
    path('NuestrosServicios/', views.ServicioEstaticoListView.as_view(), name='servicioEstatico_list'),
    path('NuestrosServicios/nuevo/', views.ServicioCreateView.as_view(), name='servicio_crear'),
    path('NuestrosServicios/<int:pk>/editar/', views.ServicioUpdateView.as_view(), name='servicio_editar'),
    path('NuestrosServicios/<int:pk>/eliminar/', views.ServicioDeleteView.as_view(), name='servicio_eliminar'),
]
