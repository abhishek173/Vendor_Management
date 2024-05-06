from django.urls import path
from . import views
from vendor_performance.views import AcknowledgePOView

urlpatterns = [
   path('', views.purchase_order_list),
   path('<int:po_id>/', views.purchase_order_detail),
   path('<int:po_id>/acknowledge/', AcknowledgePOView.as_view(), name='acknowledge_po')
]

