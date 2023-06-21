from rest_framework import serializers
from .models import *


class DetectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Detection
        fields = ["happy", "sad",
                  "neutral", "detectionError", "start_time", "end_time", "emotion"]
