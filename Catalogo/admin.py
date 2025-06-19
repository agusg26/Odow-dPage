from django.contrib import admin

# Register your models here.
from Catalogo.models import Cerveza, Formato, Categoria, GraduacionAlcoholica, Servicio, Chopera, Bar, Barra, Usuario, Envasado
admin.site.register(Cerveza)
admin.site.register(Formato)
admin.site.register(Categoria)
admin.site.register(GraduacionAlcoholica)
admin.site.register(Servicio)
admin.site.register(Chopera)
admin.site.register(Bar)
admin.site.register(Barra)
admin.site.register(Usuario)
admin.site.register(Envasado)