from django.contrib import admin
from . models import *
from .models import Notice
# Register your models here.
admin.site.register(Notes)
admin.site.register(Homework)
admin.site.register(QuizCategory)

class QuizQuestionAdmin(admin.ModelAdmin):
    list_display=['question','category','level']
admin.site.register(QuizQuestion,QuizQuestionAdmin)


class UserSubmittedAnswerAdmin(admin.ModelAdmin):
    list_display=['id','question','user','right_answer']
admin.site.register(UserSubmittedAnswer,UserSubmittedAnswerAdmin)

class UserCategoryAttemptsAdmin(admin.ModelAdmin):
    list_display=['category','user','attempt_time']
admin.site.register(UserCategoryAttempts,UserCategoryAttemptsAdmin)


admin.site.register(Notice)