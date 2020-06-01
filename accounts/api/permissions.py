from rest_framework import permissions

class UserPermission(permissions.BasePermission):
    """
    Global permission check for blacklisted IPs.

    """

    message = "You are authenticate, please logout to try again"

    def has_permission(self, request, view):
        
        return not request.user.is_authenticated

class IsOwnerOrReadOnly(permissions.BasePermission):

    message = "You must be the owner of the status"

    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.

        message = "You are not the owner of status"

        if request.method in permissions.SAFE_METHODS:
            return True

        # Instance must have an attribute named `user`.
        return obj.owner == request.user