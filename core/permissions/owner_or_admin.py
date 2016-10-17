__author__ = 'Bertrand'

from rest_framework import permissions
from django.contrib.auth.models import User

class IsOwnerOrAdminReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # selon le token passé en authorisation, on choppe l'utilisateur associé
        if request.user.is_anonymous():
            return False

        if request.user.is_superuser:
            return True

        # Instance must have an attribute named `owner`.
        return request.user.id == obj.user_id