from rest_framework import serializers

class BMISerializer(serializers.Serializer):
    age = serializers.IntegerField(min_value=0)
    gender = serializers.ChoiceField(choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')])
    height_cm = serializers.FloatField(min_value=0)
    weight_kg = serializers.FloatField(min_value=0)