"""
Serializer for user API
"""

from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers
from uljesaKojadinovic.models import LibraryUser
from django.utils.translation import gettext_lazy as _


class CreateLibraryUserSerializer(serializers.ModelSerializer):
    """Serializer for the user object."""

    class Meta:
        model = get_user_model()
        fields = ['id', 'email', 'password', 'first_name', 'last_name', 'phone_number',
                  'date_joined', 'membership_duration', 'start_date', 'end_date', 'fee', 'duration', 'is_active']
        extra_kwargs = {'password': {'write_only': True, 'min_length': 7}}

    def create(self, validated_data):
        """Create and return user with encrypted data"""
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """Update API user data"""
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user

class LibraryUserSerializerLastName(serializers.ModelSerializer):
    class Meta:
        model = LibraryUser
        fields = ['id', 'last_name', 'first_name',]























