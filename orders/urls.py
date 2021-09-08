from django.urls import path
from .views import *


urlpatterns = [
    path('products/', FetchProducts.as_view(), name='products'),
    path('agents/',FetchAgents.as_view(),name='agents'),
    path('organizations/',FetchOrganization.as_view(),name='organizations'),
    path('states/',FetchStates.as_view(),name='states'),
    path('stores/', FetchStore.as_view(), name='stores'),
    path('barcodes/', FetchBarcodes.as_view(), name='fetch-barcodes'),
    path('order-buyer/', OrderForBuyer.as_view(), name='order-buyer'),
    path('order-supplier/', OrderSupplier.as_view(), name='order-supplier'),
    path('order-acceptance/', OrderAcceptance.as_view(), name='order-acceptance'),
    path('order-shipments/', OrderShipments.as_view(), name='order-shipments'),
    path('order-inventory/', OrderInventory.as_view(), name='order_inventory'),
    path('order-posting/', OrderPostings.as_view(), name='order_posting'),
    path('order-loss/', OrderLoss.as_view(), name='order_loss'),
    path('order-internal/', InternalOrder.as_view(), name='order_internal'),


]
