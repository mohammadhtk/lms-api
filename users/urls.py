from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views

router = DefaultRouter()
router.register(r'register', views.UserRegistrationView, basename='register')
router.register(r'users', views.UserViewSet, basename='users')
router.register(r'students', views.StudentViewSet, basename='students')
router.register(r'teachers', views.TeacherViewSet, basename='teachers')

urlpatterns = [
    # JWT Authentication
    path('auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Router URLs
    path('', include(router.urls)),
]
