# urls.py
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from workboards.views import WorkBoardViewSet, TaskViewSet, LoginView, SignupView

router = DefaultRouter()
router.register(r'workboards', WorkBoardViewSet)
router.register(r'tasks', TaskViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/login/', LoginView.as_view(), name='token_obtain_pair'),
    path('api/signup/', SignupView.as_view(), name='signup'),
    path('api-auth/', include('rest_framework.urls')),
]
