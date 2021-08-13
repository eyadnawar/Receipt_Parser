from rest_framework_mongoengine import serializers
from .models import *

class ReceiptsSerializer(serializers.DocumentSerializer):
    class Meta:
        model = Receipts
        fields = ['receipt']