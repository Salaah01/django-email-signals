from django.urls import path
from . import views

urlpatterns = [
    path('model-attrs/<int:content_type_id>/', views.model_attrs,
         name='model_attrs'),
]
