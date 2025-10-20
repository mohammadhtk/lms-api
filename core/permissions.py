from rest_framework import permissions


# Permission to check if user is a student.
class IsStudent(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'student'


# Permission to check if user is a teacher
class IsTeacher(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'teacher'


# Permission to check if user is an admin
class IsAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'admin'


# Permission to check if user is a receptionist.
class IsReceptionist(permissions.BasePermission):
    
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'receptionist'


# Object-level permission to only allow owners of an object to edit it
class IsOwnerOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner
        return obj.user == request.user or obj == request.user


# Permission to check if user is a teacher or admin
class IsTeacherOrAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ['teacher', 'admin']


# Permission to check if the student is the owner of the resource
class IsStudentOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if hasattr(obj, 'student'):
            return obj.student.user == request.user
        return False
