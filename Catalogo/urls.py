from django.urls import path
from Catalogo import views

urlpatterns = [
    path('', views.index, name='index'),
    path('cervezas/', views.CervezaListView.as_view(), name='cervezas'),
    path('cerveza/<pk>', views.CervezaDetailView.as_view(), name='cerveza'),
    path('cerveza/new/', views.CervezaCreateView.as_view(), name='cerveza_new'),
]
