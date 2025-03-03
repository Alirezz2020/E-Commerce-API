from django.urls import path
from .views import ProductListView


app_name='home'
urlpatterns = [
    path('', ProductListView.as_view(), name='home'),
]
