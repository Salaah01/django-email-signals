from django.urls import path, include
from . import views

urlpatterns = [
    path(
        "model-attrs/<int:content_type_id>/",
        views.model_attrs,
        name="django_signals_model_attrs",
    ),
]
