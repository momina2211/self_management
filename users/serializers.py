from rest_framework import serializers
from django.contrib.auth import get_user_model
from users.models import UserProfile
User  = get_user_model()

class UserSignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['email', 'password']

    def create(self, validated_data):
        user = User( email=validated_data['email'], )
        user.set_password(validated_data['password'])
        user.save()
        UserProfile.objects.create(user=user)
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['bio', 'profile_pic', 'date_of_birth', 'cover_photo', 'language']