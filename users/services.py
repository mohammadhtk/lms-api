from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from core.exceptions import BusinessLogicException
from .models import CustomUser, Student, Teacher
from . import selectors


# Register a new user
def register_user(validated_data):
    email = validated_data.get('email')

    if selectors.get_user_by_email(email):
        raise BusinessLogicException("User with this email already exists.")

    user = CustomUser.objects.create_user(**validated_data)

    # Create profile based on role
    if user.role == 'student':
        Student.objects.create(user=user)
    elif user.role == 'teacher':
        Teacher.objects.create(user=user)

    return user


# Authenticate user and return tokens
def authenticate_user(email, password):
    user = authenticate(username=email, password=password)

    if not user:
        # Try with email as username
        try:
            user_obj = CustomUser.objects.get(email=email)
            user = authenticate(username=user_obj.username, password=password)
        except CustomUser.DoesNotExist:
            pass

    if not user:
        raise BusinessLogicException("Invalid credentials.")

    if not user.is_active:
        raise BusinessLogicException("User account is disabled.")

    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
        'user': user
    }


def change_password(user, old_password, new_password):
    if not user.check_password(old_password):
        raise BusinessLogicException("Old password is incorrect.")

    user.set_password(new_password)
    user.save()

    return user


def update_user_profile(user, validated_data):
    for attr, value in validated_data.items():
        setattr(user, attr, value)
    user.save()

    return user


def update_student_profile(student_id, validated_data):
    student = selectors.get_student_by_id(student_id)

    if not student:
        raise BusinessLogicException("Student not found.")

    for attr, value in validated_data.items():
        if attr != 'user_id':
            setattr(student, attr, value)
    student.save()

    return student


def update_teacher_profile(teacher_id, validated_data):
    teacher = selectors.get_teacher_by_id(teacher_id)

    if not teacher:
        raise BusinessLogicException("Teacher not found.")

    for attr, value in validated_data.items():
        if attr != 'user_id':
            setattr(teacher, attr, value)
    teacher.save()

    return teacher


def deactivate_user(user_id):
    user = selectors.get_user_by_id(user_id)

    if not user:
        raise BusinessLogicException("User not found.")

    user.is_active = False
    user.save()

    return user


def activate_user(user_id):
    user = selectors.get_user_by_id(user_id)

    if not user:
        raise BusinessLogicException("User not found.")

    user.is_active = True
    user.save()

    return user
