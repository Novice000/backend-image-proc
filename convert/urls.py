from . import views
from django.urls import path

urlpatterns = [
    path("remove-background/", views.ImageRemoveBg.as_view(), name="remove-bg"),
    path("compress-image/", views.ImageCompress.as_view(), name="compress-image"),
    path("convert-image/", views.ImageConvert.as_view(), name="convert-image"),
]