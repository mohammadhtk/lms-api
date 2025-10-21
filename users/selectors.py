from django.db.models import Q
from .models import CustomUser, Student, Teacher

# database query logic
# Get user by ID
def get_user_by_id(user_id):
    try:
        return CustomUser.objects.get(id=user_id)
    except CustomUser.DoesNotExist:
        return None

# Get user by email
def get_user_by_email(email):
    try:
        return CustomUser.objects.get(email=email)
    except CustomUser.DoesNotExist:
        return None

# Get all users with optional filters
def get_all_users(role=None, is_active=None):
    queryset = CustomUser.objects.all()

    if role:
        queryset = queryset.filter(role=role)

    if is_active is not None:
        queryset = queryset.filter(is_active=is_active)

    return queryset.order_by('-created_at')

# Get student by ID
def get_student_by_id(student_id):
    try:
        return Student.objects.select_related('user').get(id=student_id)
    except Student.DoesNotExist:
        return None

# Get student by student code
def get_student_by_code(student_code):
    try:
        return Student.objects.select_related('user').get(student_code=student_code)
    except Student.DoesNotExist:
        return None

# Get all students
def get_all_students():
    return Student.objects.select_related('user').order_by('-created_at')

# Get teacher by ID
def get_teacher_by_id(teacher_id):
    try:
        return Teacher.objects.select_related('user').get(id=teacher_id)
    except Teacher.DoesNotExist:
        return None

# Get all teachers
def get_all_teachers():
    return Teacher.objects.select_related('user').order_by('-created_at')

# Search users by name or email
def search_users(query):
    return CustomUser.objects.filter(
        Q(first_name__icontains=query) |
        Q(last_name__icontains=query) |
        Q(email__icontains=query) |
        Q(username__icontains=query)
    )
