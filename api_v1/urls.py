from django.urls import path
from rest_framework import routers
from api_v1.views import CustomerViewSet, TransactionViewSet, Transfer

router = routers.DefaultRouter()
router.register(r'customers', CustomerViewSet)
router.register(r'transactions', TransactionViewSet)

urlpatterns = [
    path('transfer/', Transfer.as_view()),
]

urlpatterns += router.urls
