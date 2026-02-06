from django.urls import path # type: ignore
from .views import home # type: ignore

urlpatterns = [
    path('', home, name='home'),
]