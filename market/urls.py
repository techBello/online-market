from django.urls import path # type: ignore
from .views import home, about # type: ignore

urlpatterns = [
    path('', home, name='home'),
    path('/about', about, name='about'),
    path('/contact', about, name='contact')
]