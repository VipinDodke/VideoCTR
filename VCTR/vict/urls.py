from django.urls import path
from .import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path("",views.index,name="IndexHome"),
    path(r"vict/view/<myid>/", views.view, name="View"),
    path(r"vict/gift/<mid>/", views.gift, name="Gift"),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
