from django.urls import path

from .views import DepositCalculationView


urlpatterns = [
    path('deposit_calculation/',
         DepositCalculationView.as_view(),
         name='deposit_calculation')
]
