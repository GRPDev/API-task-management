from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.generics import ListAPIView, CreateAPIView
from django.utils import timezone
from django.db.models import Sum
from .models import Task, User
from .serializers import (
    UserSerializer, UserStatusSerializer,
    TaskCreateSerializer, TaskCreatedByUserSerializer,
    TaskWithExecutorSerializer, UserTasksSerializer,
    UserTasksStatsSerializer, MarkTaskDoneSerializer,
)


class ClearDatabaseView(APIView):
    
    def get(self, request):
        Task.objects.all().delete()
        User.objects.all().delete()
        return Response({'message': 'All data cleared successfully'}, status=status.HTTP_200_OK)

    def post(self, request):
        Task.objects.all().delete()
        User.objects.all().delete()
        return Response({'message': 'All data cleared successfully'}, status=status.HTTP_200_OK)


class UserCreateView(APIView):
    def get(self, request):
        return Response(
            {"message": "Use POST to create a new user with 'username', 'password', and 'email'."},
            status=status.HTTP_200_OK
        )

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email')

        if not username or not password or not email:
            return Response(
                {'error': 'Username, password, and email are required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if User.objects.filter(username=username).exists():
            return Response(
                {'error': 'Username already exists'},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = User.objects.create_user(username=username, password=password, email=email)
        return Response(
            {'id': user.id, 'username': user.username, 'email': user.email},
            status=status.HTTP_201_CREATED
        )


class UsersView(APIView):
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)


class UsersListView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserStatusSerializer
    
    def get_serializer_context(self):
        return {'request': self.request}


class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response(
                {'error': 'Invalid credentials'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        user = authenticate(username=username, password=password)

        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)

        return Response(
            {'error': 'Invalid credentials'},
            status=status.HTTP_401_UNAUTHORIZED
        )


class LogoutView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        Token.objects.filter(user=request.user).delete()

        if not Token.objects.filter(user=request.user).exists():
            return Response({'message': 'Successfully logged out'}, status=status.HTTP_200_OK)


class TaskCreateView(CreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskCreateSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)
    
    def post(self, request):
        print('request data', request.data)
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        errors = serializer.errors
        if 'non_field_errors' in errors:
            error_message = errors['non_field_errors'][0]
            print('Serializer errors', errors)
            return Response({'error': error_message}, status=status.HTTP_400_BAD_REQUEST)

        print(errors)
        return Response(errors, status=status.HTTP_400_BAD_REQUEST)


class TasksCreatedByUser(ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = TaskCreatedByUserSerializer
    
    def get_queryset(self):
        return Task.objects.filter(creator=self.request.user)


class TaskWithExecutorAPIView(ListAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskWithExecutorSerializer


class UserTasksAPIView(ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = UserTasksSerializer

    def get_queryset(self):
        return Task.objects.filter(executor=self.request.user)


class UserTasksStatsAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
        
    def get(self, request):
        qty_completed_tasks = Task.objects.filter(
            is_done=True, executor=self.request.user
        ).count()

        qty_pending_tasks = Task.objects.filter(
            is_done=False, executor=self.request.user
        ).count()

        qty_overdue_tasks = Task.objects.filter(
            is_done=False, deadline__lt=timezone.now(), executor=self.request.user
        ).count()

        qty_tasks_assigned = Task.objects.filter(executor=self.request.user).count()

        amount_earned = Task.objects.filter(
            is_done=True, executor=self.request.user
        ).aggregate(earned_sum=Sum('cost'))

        if amount_earned['earned_sum'] is None:
            amount_earned['earned_sum'] = 0

        amount_spent = Task.objects.filter(creator=self.request.user).aggregate(spent_sum=Sum('cost'))

        if amount_spent['spent_sum'] is None:
            amount_spent['spent_sum'] = 0
        
        data = {
            'completed_tasks': qty_completed_tasks,
            'pending_tasks': qty_pending_tasks,
            'overdue_tasks': qty_overdue_tasks,
            'assigned_tasks': qty_tasks_assigned,
            'total_earned': amount_earned['earned_sum'],
            'total_spent': amount_spent['spent_sum'],
        }

        serializer = UserTasksStatsSerializer(data=data)

        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UnassignedTasksAPIView(ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = UserTasksSerializer

    def get_queryset(self):
        return Task.objects.filter(executor=None).order_by('cost')


class BecomeExecutorAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def patch(self, request, task_id):
        task = Task.objects.filter(pk=task_id).first()

        if not task:
            return Response({"error": "Task not found"}, status=status.HTTP_404_NOT_FOUND)

        if task.creator == self.request.user.id:
            return Response(
                {"error": "You cannot assign yourself as executor of your own task"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if task.executor is not None:
            return Response(
                {"error": "This task already has an executor"},
                status=status.HTTP_400_BAD_REQUEST
            )

        task.executor = self.request.user
        task.save()
        return Response(
            {'message': 'You have been assigned as the executor of the task'},
            status=status.HTTP_200_OK
        )


class MarkTaskDoneAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def patch(self, request, task_id):
        task = Task.objects.filter(pk=task_id).first()

        if not task:
            return Response({"error": "Task not found"}, status=status.HTTP_404_NOT_FOUND)
        if task.is_done == True:
            return Response({'message': 'Task is already marked as done'}, status=status.HTTP_400_BAD_REQUEST )
        if task.executor != self.request.user:
            return Response(
                {"error": "You are not authorized to mark this task as done"},
                status=status.HTTP_403_FORBIDDEN
            )
        else:
            task.is_done = True
            task.save()
            task_response = MarkTaskDoneSerializer(task).data
            return Response(
                {'message': 'Task marked as done', 'task': task_response},
                status=status.HTTP_200_OK
            )

