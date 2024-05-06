from django.db import models
from vendor_profile.models import Vendor
from django.db.models import F
from django.db.models import Avg
from vendor_performance.models import HistoricalPerformance

class PurchaseOrder(models.Model):
    po_number = models.CharField(max_length=50, unique=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    order_date = models.DateTimeField()
    delivery_date = models.DateTimeField()
    items = models.JSONField(default=list)  # Default empty list
    quantity = models.IntegerField()
    status_choices = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('canceled', 'Canceled')
    ]
    status = models.CharField(max_length=20, choices=status_choices)
    quality_rating = models.FloatField(null=True)
    issue_date = models.DateTimeField()
    acknowledgment_date = models.DateTimeField(null=True)

    def __str__(self):
        return self.po_number
    
    def change_status(self,new_status):
        self.status = new_status
        self.save()
        self.update_vendor_performance()

    def update_vendor_performance(self):

        #update on_time_delivery_rate
        completed_pos = PurchaseOrder.objects.filter(vendor=self.vendor,status='completed')
        on_time_pos = completed_pos.filter(delivery_date__lte=F('order_date'))
        on_time_rate = on_time_pos.count()/completed_pos.count() if completed_pos.count() > 0 else 0

        #update quality_rating_avg
        #Assuming quality_rating is a field in the PurchaseOrder model
        completed_pos_with_quality_rating = completed_pos.exclude(quality_rating=None)
        quality_rating_avg = completed_pos_with_quality_rating.aggregate(Avg('quality_rating'))['quality_rating__avg'] if completed_pos_with_quality_rating.count() > 0 else 0

        #update average_response_time
        #Assuming acknowldement_date is a field in the PurchaseOrder model
        response_times = PurchaseOrder.objects.filter(vendor=self.vendor).exclude(acknowledgement_date=None).annotate(response_time=F('acknowledgement_date') - F('order_date'))
        average_response_time = response_times.aggregate(Avg('response_times'))['response_time__avg']

        fulfilled_pos = completed_pos.filter(issues=None)
        fulfillment_rate = fulfilled_pos.count() / PurchaseOrder.objects.filter(Vendor=self.vendor).count() if PurchaseOrder.objects.filter(Vendor=self.vendor).count() > 0 else 0

        # Assumming there's only one HistoricalPrerformance record per vendor
        performance = HistoricalPerformance.objects.all().get_or_create(vendor=self.vendor)
        performance.on_time_delivery_rate = on_time_rate
        performance.quality_rating_avg = quality_rating_avg
        performance.average_response_time = average_response_time
        performance.fulfillment_rate = fulfillment_rate
        performance.save()
        
