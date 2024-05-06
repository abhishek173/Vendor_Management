from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import VendorSerializer
from rest_framework import status
from . models import Vendor

@api_view(["GET","POST"])
def vendor_list(request):
    if request.method == "GET":
        vendors = Vendor.objects.all()
        serializer = VendorSerializer(vendors,many=True)
        return Response(serializer.data)


    elif request.method == "POST":
        serializer = VendorSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    


    
@api_view(['GET','PUT','DELETE'])
def vendor_detail(request,vendor_id):
    try:
        vendor = Vendor.objects.get(pk=vendor_id)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == "GET":
        serializer = VendorSerializer(vendor)
        return Response(serializer.data)
    
    elif request.method == "PUT":
        serializer = VendorSerializer(vendor,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == "DELETE":
        vendor.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)