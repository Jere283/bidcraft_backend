from rest_framework import serializers

class PaymentSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=255, required=True)
    amount = serializers.IntegerField(required=True)
    currency = serializers.CharField(max_length=3, required=True)
    description = serializers.CharField(max_length=255, required=False)
