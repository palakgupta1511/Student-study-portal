from django.db import models
from django.contrib.auth.models import User
import uuid
import random

# Create your models here.
class Notes(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    title= models.CharField(max_length=200)
    description=models.TextField()
    class Meta:
         verbose_name = "notes"  
         verbose_name_plural = "notes"    
    def __str__(self):
        return self.title     
    
class Homework(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    subject= models.CharField(max_length=50)
    title= models.CharField(max_length=100)
    description=models.TextField()
    due=models.DateTimeField()
    is_finished=models.BooleanField(default=False)
    def __str__(self):
        return self.title  

class Todo(models.Model):
       user=models.ForeignKey(User, on_delete=models.CASCADE) 
       title= models.CharField(max_length=100)
       is_finished=models.BooleanField(default=False)
       def __str__(self):
        return self.title  
    
class QuizCategory(models.Model):
    title=models.CharField(max_length=100)
    detail=models.TextField()
    image=models.ImageField(upload_to='cat_imgs/')
    
    class Meta: 
         verbose_name_plural = "Quiz Categories"   
    def __str__(self):
        return self.title


class QuizQuestion(models.Model):
    category=models.ForeignKey(QuizCategory, on_delete=models.CASCADE)
    question=models.TextField()
    opt_1=models.CharField(max_length=200)
    opt_2=models.CharField(max_length=200)
    opt_3=models.CharField(max_length=200)
    opt_4=models.CharField(max_length=200)
    level=models.CharField(max_length=200)
    time_limit=models.IntegerField()
    right_opt=models.CharField(max_length=200)
    class Meta: 
         verbose_name_plural = "Quiz Questions" 
    def __str__(self):
        return self.question

class UserSubmittedAnswer(models.Model):
    question=models.ForeignKey(QuizQuestion, on_delete=models.CASCADE)  
    user=models.ForeignKey(User, on_delete=models.CASCADE) 
    right_answer=models.CharField(max_length=200)
    class Meta: 
         verbose_name_plural = "User submitted Answers" 
 
class UserCategoryAttempts(models.Model):
    category=models.ForeignKey(QuizCategory, on_delete=models.CASCADE)  
    user=models.ForeignKey(User, on_delete=models.CASCADE) 
    attempt_time =models.DateTimeField(auto_now_add=True)
    class Meta: 
         verbose_name_plural = "User Attempts Category" 
         
          
class Notice(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title        
    
    
# class Message(models.Model):
#     sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
#     recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
#     content = models.TextField()
#     timestamp = models.DateTimeField(auto_now_add=True)

