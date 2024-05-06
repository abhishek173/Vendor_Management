from django.shortcuts import render
from rest_framework.decorators import api_view
from .models import PurchaseOrder
from .serializers import PurchaseOrderSerializer
from rest_framework.response import Response
from rest_framework import status

# Create your views here.
@api_view(['POST','GET'])
def purchase_order_list(request):
    if request.method == "GET":
        vendor_id = request.query_params.get('vendor',None)
        if vendor_id:
            purchase_orders = PurchaseOrder.objects.filter(vendor=vendor_id)
        else:
            purchase_orders = PurchaseOrder.objects.all()
        serializer = PurchaseOrderSerializer(purchase_orders,many=True)
        return Response(serializer.data)
    
    if request.method == 'POST':
        serializer = PurchaseOrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    
@api_view(['GET','PUT','DELETE',])
def purchase_order_detail(request,po_id):
    try:
        purchase_order = PurchaseOrder.objects.get(pk=po_id)
    except PurchaseOrder.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == "GET":
        serializer = PurchaseOrderSerializer(purchase_order)
        return Response(serializer.data)
    
    elif request.method == "PUT":
        serializer = PurchaseOrderSerializer(purchase_order,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == "DELETE":
        purchase_order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    