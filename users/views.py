from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from core.permissions import IsAdmin, IsStudent, IsTeacher
from . import serializers, services, selectors
from .models import CustomUser, Student, Teacher

# ViewSet for user registration
class UserRegistrationView(viewsets.GenericViewSet):
    serializer_class = serializers.UserRegistrationSerializer
    permission_classes = [AllowAny]

    # Register a new user
    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = services.register_user(serializer.validated_data)

        return Response(
            serializers.UserSerializer(user).data,
            status=status.HTTP_201_CREATED
        )

# ViewSet for user management
class UserViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.UserSerializer
    permission_classes = [IsAuthenticated]

    # Get queryset based on user role
    def get_queryset(self):
        user = self.request.user

        if user.role == 'admin':
            return selectors.get_all_users()

        return CustomUser.objects.filter(id=user.id)

    # Get current user profile
    @action(detail=False, methods=['get'])
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    # Update current user profile
    @action(detail=False, methods=['put', 'patch'])
    def update_profile(self, request):
        serializer = self.get_serializer(
            request.user,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)

        user = services.update_user_profile(request.user, serializer.validated_data)

        return Response(serializers.UserSerializer(user).data)

    # Change user password
    @action(detail=False, methods=['post'])
    def change_password(self, request):
        serializer = serializers.PasswordChangeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        services.change_password(
            request.user,
            serializer.validated_data['old_password'],
            serializer.validated_data['new_password']
        )

        return Response(
            {"message": "Password changed successfully."},
            status=status.HTTP_200_OK
        )

    # Deactivate a user account
    @action(detail=True, methods=['post'], permission_classes=[IsAdmin])
    def deactivate(self, request, pk=None):
        user = services.deactivate_user(pk)
        return Response(serializers.UserSerializer(user).data)

    # Activate a user account.
    @action(detail=True, methods=['post'], permission_classes=[IsAdmin])
    def activate(self, request, pk=None):
        user = services.activate_user(pk)
        return Response(serializers.UserSerializer(user).data)

# ViewSet for student management
class StudentViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.StudentSerializer
    permission_classes = [IsAuthenticated]

    # Get queryset based on user role
    def get_queryset(self):
        user = self.request.user

        if user.role in ['admin', 'teacher', 'receptionist']:
            return selectors.get_all_students()
        elif user.role == 'student':
            return Student.objects.filter(user=user)

        return Student.objects.none()

    # Get current student profile
    @action(detail=False, methods=['get'])
    def my_profile(self, request):
        if request.user.role != 'student':
            return Response(
                {"error": "Only students can access this endpoint."},
                status=status.HTTP_403_FORBIDDEN
            )

        try:
            student = request.user.student_profile
            serializer = self.get_serializer(student)
            return Response(serializer.data)
        except Student.DoesNotExist:
            return Response(
                {"error": "Student profile not found."},
                status=status.HTTP_404_NOT_FOUND
            )


class TeacherViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.TeacherSerializer
    permission_classes = [IsAuthenticated]

    # Get queryset based on user role
    def get_queryset(self):
        user = self.request.user

        if user.role in ['admin', 'receptionist']:
            return selectors.get_all_teachers()
        elif user.role == 'teacher':
            return Teacher.objects.filter(user=user)
        elif user.role == 'student':
            # Students can view all teachers
            return selectors.get_all_teachers()

        return Teacher.objects.none()

    # Get current teacher profile
    @action(detail=False, methods=['get'])
    def my_profile(self, request):
        if request.user.role != 'teacher':
            return Response(
                {"error": "Only teachers can access this endpoint."},
                status=status.HTTP_403_FORBIDDEN
            )

        try:
            teacher = request.user.teacher_profile
            serializer = self.get_serializer(teacher)
            return Response(serializer.data)
        except Teacher.DoesNotExist:
            return Response(
                {"error": "Teacher profile not found."},
                status=status.HTTP_404_NOT_FOUND
            )
