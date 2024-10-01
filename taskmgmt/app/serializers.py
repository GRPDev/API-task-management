from rest_framework import serializers
from .models import * 
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username','password','email']

class TaskSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Task
        fields = '__all__'
  

class TaskCreateSerializer(serializers.ModelSerializer):
    deadline = serializers.DateField(input_formats=['%Y-%m-%dT%H:%M:%SZ', '%Y/%m/%d', '%Y-%m-%d'])
    
    class Meta:
        model = Task
        fields = ['executor', 'name', 'cost', 'deadline']

    def to_internal_value(self, data):
        # must bypass automatic ForeignKey validation
        executor_id = data.get('executor')
        if executor_id is not None:
            try:
                executor = User.objects.get(id=executor_id)
                data['executor'] = executor.id  
            except User.DoesNotExist:
                data['executor'] = None  
        return super().to_internal_value(data)
    
    def validate(self, data):
        creator = self.context['request'].user
        executor = data.get('executor')
        if creator == executor:
            #TEST_NIGHTMARE
            #raise serializers.ValidationError({"error": "The creator of a task cannot be its executor"}) 
            raise serializers.ValidationError("The creator of a task cannot be its executor", code='error')
        return data

    
class TaskCreatedByUserSerializer(serializers.ModelSerializer):
    deadline = serializers.DateTimeField(format='%Y-%m-%d')    
    creator = serializers.ReadOnlyField(source='creator.id')
    
    class Meta:
        model = Task
        fields = ['executor', 'name', 'cost', 'deadline', 'creator']

class TaskWithExecutorSerializer(serializers.ModelSerializer):
    deadline = serializers.DateTimeField(format='%Y-%m-%d')

    class Meta:
        model = Task 
        fields = ['executor', 'name', 'cost', 'deadline']
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if representation['executor'] is None:
            representation['executor'] = 'undefined'
        return representation

class UserTasksSerializer(serializers.ModelSerializer):
    deadline = serializers.DateTimeField(format='%Y-%m-%d')

    class Meta:
        model = Task
        fields = ['executor', 'name', 'cost', 'deadline']

class UserTasksStatsSerializer(serializers.Serializer):
    completed_tasks = serializers.IntegerField()
    pending_tasks = serializers.IntegerField()
    overdue_tasks = serializers.IntegerField()
    assigned_tasks = serializers.IntegerField()
    total_earned = serializers.DecimalField(max_digits=10, decimal_places=2)
    total_spent = serializers.DecimalField(max_digits=10, decimal_places=2)

class UnassignedTasksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['executor', 'name', 'cost', 'deadline']

#additional

class UserStatusSerializer(serializers.ModelSerializer):
    is_logged_in = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_logged_in']

    def get_is_logged_in(self, obj):
        # This method will need to be adjusted to reflect if the user is logged in
        # Here we're assuming you want to check if the current request user is logged in
        request = self.context.get('request')
        return request and request.user.is_authenticated