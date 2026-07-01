from rest_framework import permissions

class IsStaffOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow staff members to edit objects,
    while allowing read-only access to everyone (anonymous or authenticated).
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_authenticated and request.user.is_staff

class IsTripOwner(permissions.BasePermission):
    """
    Custom permission to enforce that users can only view or edit their own trips.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user

class IsItineraryDayOwner(permissions.BasePermission):
    """
    Custom permission to enforce that users can only view or edit itinerary days of their own trips.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return obj.trip.user == request.user
