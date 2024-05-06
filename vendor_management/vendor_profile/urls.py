from django.urls import path
from . import views
from vendor_performance.views import VendorPerformanceView

urlpatterns = [
    path('', views.vendor_list),
    path('<int:vendor_id>/',views.vendor_detail),
    path('<int:vendor_id>/performance/',VendorPerformanceView.as_view(), name='vendor_performance')
]

