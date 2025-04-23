from rest_framework import serializers
from django.contrib.auth import get_user_model
from users.models import UserProfile, Language

User  = get_user_model()

class UserSignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['id','email', 'password']

    def create(self, validated_data):
        email = validated_data['email']
        username = email.split('@')[0]
        user = User(email=email, username=username)
        user.set_password(validated_data['password'])
        user.save()
        UserProfile.objects.create(user=user)
        return user
class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = ['id','name']

class UserProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='user.email',read_only=True)
    language = LanguageSerializer(read_only=True,many=True)
    language_ids = serializers.PrimaryKeyRelatedField(
        queryset=Language.objects.all(), many=True, write_only=True, required=False
    )

    class Meta:
        model = UserProfile
        fields = ['id','email','bio', 'profile_pic', 'date_of_birth', 'cover_photo', 'language','language_ids']

    def update(self, instance, validated_data):
        language_ids = validated_data.pop('language_ids', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if language_ids is not None:
            instance.language.set(language_ids)
        return instance


