from django.urls import path
from .import views
urlpatterns = [
    path("",views.index,name="IndexHome"),
    path("vict/view/<myid>/", views.view, name="View"),
]
