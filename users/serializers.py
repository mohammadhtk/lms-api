from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import CustomUser, Student, Teacher


# Serializer for CustomUser model
class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.ReadOnlyField()

    class Meta:
        model = CustomUser
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name', 'full_name',
            'role', 'phone_number', 'date_of_birth', 'address', 'profile_picture',
            'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

# Serializer for user registration
class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = [
            'username', 'email', 'password', 'password_confirm',
            'first_name', 'last_name', 'role', 'phone_number',
            'date_of_birth', 'address'
        ]

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = CustomUser.objects.create_user(**validated_data)

        # Create profile based on role
        if user.role == 'student':
            Student.objects.create(user=user)
        elif user.role == 'teacher':
            Teacher.objects.create(user=user)

        return user


# Serializer for Student model
class StudentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    user_id = serializers.IntegerField(write_only=True, required=False)

    class Meta:
        model = Student
        fields = [
            'id', 'user', 'user_id', 'student_code', 'current_level',
            'joined_date', 'total_courses_taken', 'attendance_rate',
            'emergency_contact_name', 'emergency_contact_phone', 'notes',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'student_code', 'joined_date', 'created_at', 'updated_at']


# Serializer for Teacher model
class TeacherSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    user_id = serializers.IntegerField(write_only=True, required=False)

    class Meta:
        model = Teacher
        fields = [
            'id', 'user', 'user_id', 'teacher_code', 'specialization',
            'experience_years', 'bio', 'qualifications', 'hourly_rate',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'teacher_code', 'created_at', 'updated_at']


# Serializer for password change
class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators=[validate_password])
    new_password_confirm = serializers.CharField(required=True)

    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError({"new_password": "Password fields didn't match."})
        return attrs
