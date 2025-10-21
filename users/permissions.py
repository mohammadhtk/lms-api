from rest_framework import permissions

# Permission to check if user is the profile owner.
class IsProfileOwner(permissions.BasePermission):

    # check if user owns the profile.
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


# Custom permissions for role-based access control.
# Permission class for admin users.
class IsAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role == 'admin'

# Permission class for teacher users.
class IsTeacher(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role == 'teacher'

# Permission class for student users.
class IsStudent(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role == 'student'

# Permission class for receptionist users.
class IsReceptionist(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role == 'receptionist'

# Permission class for admin or teacher users.
class IsAdminOrTeacher(permissions.BasePermission):

    def has_permission(self, request, view):
        return (
                request.user and
                request.user.is_authenticated and
                request.user.role in ['admin', 'teacher']
        )


# Permission class for object owner or admin.
class IsOwnerOrAdmin(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.user.role == 'admin':
            return True
        return obj.user == request.user or getattr(obj, 'student', None) == request.user

