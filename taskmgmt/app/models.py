from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
    creator = models.ForeignKey(User, on_delete=models.PROTECT, related_name='task_creator')  #Deleting a user should not delete task info
    executor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='task_executor') 
    name = models.CharField(max_length=255)
    cost = models.DecimalField(max_digits=8, decimal_places=2)
    is_done = models.BooleanField(default=False)
    deadline = models.DateTimeField() #(blank=False, null=True) #review this decision, deadline should not be empty, but leave null to avoid potential database issues

    def __str__(self):
        return f'Task: {self.name} - Due: {self.deadline} - Assigned to:{self.executor}'