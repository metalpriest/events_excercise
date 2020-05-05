from rest_framework.permissions import BasePermission


class AllowOwnerEditEvent(BasePermission):
    def has_object_permission(self, request, view, event):
        if request.method in ('PATCH', 'PUT', 'DELETE') and request.user != event.owner:
            return False

        return True
