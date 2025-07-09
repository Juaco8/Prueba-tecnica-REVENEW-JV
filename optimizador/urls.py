from django.urls import path
from .views import view_apply_model, view_edit_params

urlpatterns = [
    path("", view_apply_model, name = "url_apply_model"),
    path("editar/", view_edit_params, name = "url_edit_params"),
]