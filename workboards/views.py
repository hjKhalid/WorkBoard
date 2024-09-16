# views.py
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.views import APIView
from django.contrib.auth.models import User
from .model import WorkBoard, Task
from .serializers import WorkBoardSerializer, TaskSerializer

class WorkBoardViewSet(viewsets.ModelViewSet):
    queryset = WorkBoard.objects.all()
    serializer_class = WorkBoardSerializer

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

class LoginView(TokenObtainPairView):
    pass

class SignupView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        if username and password:
            try:
                user = User.objects.create_user(username=username, password=password)
                return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)
            except:
                return Response({"error": "User creation failed"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"error": "Invalid data"}, status=status.HTTP_400_BAD_REQUEST)
