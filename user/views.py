"""
Views for the user API
"""

from rest_framework import generics, authentication, permissions
from . import serializers
from uljesaKojadinovic.models import LibraryUser

class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system"""
    print('kskskssk')
    serializer_class = serializers.CreateLibraryUserSerializer
    permission_classes = [permissions.AllowAny]


class ManageUserView(generics.RetrieveUpdateDestroyAPIView):
    """Manage the authenticated user."""
    serializer_class = serializers.CreateLibraryUserSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = LibraryUser.objects.all()

    def get_object(self):
        """Retrieve, update and delete API user"""
        return self.request.user

class ListUserAPIView(generics.ListAPIView):
    queryset = LibraryUser.objects.all()
    serializer_class = serializers.LibraryUserSerializerLastName
    permission_classes = [permissions.AllowAny]
