from . import views
from django.urls import path

urlpatterns = [
    path("process-image/", views.ImageProc.as_view(), name="image_proc"),
    path("", views.index, name="index")
]