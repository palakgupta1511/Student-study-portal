from django.urls import path
from . import views

from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('',views.home,name="home"),
     
    
    path('homework',views.homework,name="homework"),
    path('update_homework/<int:pk>',views.update_homework,name="update-homework"),
    path('delete_homework/<int:pk>',views.delete_homework,name="delete-homework"),
    
    path('youtube',views.youtube,name="youtube"),
    
    path('todo',views.todo,name="todo"),
    path('update_todo/<int:pk>',views.update_todo,name="update-todo"),
    path('delete_todo/<int:pk>',views.delete_todo,name="delete-todo"),
    
     path('books',views.books,name="books"),
     
     path('dictionary',views.dictionary,name="dictionary"),
     
      path('all-categories', views.all_categories,name='all_categories'),
      path('category-questions/<int:cat_id>', views.category_questions,name='category_questions'),
      path('submit-answer/<int:cat_id>/<int:quest_id>', views.submit_answer,name='submit_answer'),
      path('result',views.result,name="result"),
      path('notice_board/', views.notice_board, name='notice_board'),
      path('search-articles', views.search_articles, name='search_articles'),
    #   path('messages/interface/<int:recipient_id>/', views.messaging_interface, name='messaging_interface'),
    #   path('messages/send/<int:recipient_id>/', views.send_message, name='send_message'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
