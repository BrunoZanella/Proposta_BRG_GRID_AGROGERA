# -*- Mode: Python; coding: utf-8 -*-
from django.conf.urls import *
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.views.generic.base import TemplateView
from django.conf import settings
from . import views

 
admin.site.site_header = 'Brasil Geradores'           
admin.site.index_title = 'ADMINISTRAÇÃO'       
admin.site.site_title = 'BRG'                      

urlpatterns = [
	path('proposta_Brg/<int:id>/', views.proposta_Brg, name='proposta_Brg'),
 	path('proposta_Grid/<int:id>/', views.proposta_Grid, name='proposta_Grid'),
	path('proposta_Agrogera/<int:id>/', views.proposta_Agrogera, name='proposta_Agrogera'),
     path('', admin.site.urls),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

