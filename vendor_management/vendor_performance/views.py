from rest_framework.views import APIView
from rest_framework.response import Response
from vendor_profile.models import Vendor
from purchase_order.models import PurchaseOrder
from .serializers import VendorPerformanceSerializer, AcknowledgePOSerializer


class VendorPerformanceView(APIView):
    def get(self, request, vendor_id):
        vendor = Vendor.objects.get(pk=vendor_id)
        performance_metrics = {
            'on_time_delivery_rate': vendor.calculate_on_time_delivery_rate(),
            'quality_rating_avg': vendor.calculate_quality_rating_avg(),
            'average_response_time': vendor.calculate_average_response_time(),
            'fulfillment_rate': vendor.calculate_fulfillment_rate()
        }
        serializer = VendorPerformanceSerializer(performance_metrics)
        return Response(serializer.data)
    
class AcknowledgePOView(APIView):
    def post(self, request, po_id):
        po = PurchaseOrder.objects.get(pk=po_id)
        serializer = AcknowledgePOSerializer(data=request.data)
        if serializer.is_valid():
            acknowledgment_date = serializer.validated_data['acknowledgment_date']
            po.acknowledgment_date = acknowledgment_date
            po.save()
            return Response(status=200)
        else:
            return Response(serializer.errors, status=400)