from django.db import models

# Create your models here.

class Conversation(models.Model):
    id = models.AutoField(primary_key=True)
    customer_question = models.CharField(max_length=1000)
    bot_response = models.CharField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    solutions = models.TextField(blank=True, null=True)
    def __str__(self):
        return self.customer_question

class NetworkProblem(models.Model):
    problem = models.CharField(max_length=255)
    solution = models.TextField()