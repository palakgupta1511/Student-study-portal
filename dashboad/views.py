from django.contrib import messages
from django.shortcuts import redirect
from django.shortcuts import render
from .models import Notes
from youtubesearchpython import VideosSearch
import requests
from . forms import *
import wikipedia
from django.contrib.auth.decorators import login_required
from django.views import generic
from django.shortcuts import render,  redirect
from django.http import JsonResponse  
from .models import *
from .models import QuizCategory
from django.http import HttpResponse
import random
from bs4 import BeautifulSoup
from django.http import JsonResponse 
import openai 

def home(request):
    return render(request,'dashboard/home.html')

def notice_board(request):
    notices = Notice.objects.all().order_by('-date_posted')
    return render(request, 'dashboard/notice_board.html', {'notices': notices})

openai.api_key = 'YOUR_API_KEY'

def get_completion(prompt): 
    print(prompt) 
    query = openai.Completion.create( 
        # engine="text-davinci-003", 
        # prompt=prompt, 
        # max_tokens=1024, 
        # n=1, 
        # stop=None, 
        temperature=0.5, 
        model='gpt-3.5-turbo',
        messages=[{"role": "user", "content": prompt }]
    ) 
    # response = query.choices[0].text 
    response = query.get('choices')[0]['message']['content']
    # print(response) 
    return response 
  
  
def chatbot(request): 
    if request.method == 'POST': 
        prompt = request.POST.get('prompt') 
        response = get_completion(prompt) 
        return JsonResponse({'response': response}) 
    return render(request, 'dashboard/chatbot.html') 

def notice_board(request):
    notices = Notice.objects.all().order_by('-date_posted')
    return render(request, 'dashboard/notice_board.html', {'notices': notices})

@login_required
def note_list(request):
    notes = Note.objects.filter(owner=request.user)
    return render(request, 'dashboard/note_list.html', {'notes': notes})

def note_detail(request, note_id):
    note = get_object_or_404(Note, id=note_id, owner=request.user)
    return render(request, 'dashboard/note_detail.html', {'note': note})

def note_create(request):
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.owner = request.user
            note.save()
            return redirect('note_list')
    else:
        form = NoteForm()
    return render(request, 'dashboard/note_form.html', {'form': form})

def note_update(request, note_id):
    note = get_object_or_404(Note, id=note_id, owner=request.user)
    if request.method == 'POST':
        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            form.save()
            return redirect('note_list')
    else:
        form = NoteForm(instance=note)
    return render(request, 'dashboard/note_form.html', {'form': form})

def note_delete(request, note_id):
    note = get_object_or_404(Note, id=note_id, owner=request.user)
    if request.method == 'POST':
        note.delete()
        return redirect('note_list')
    return render(request, 'dashboard/note_confirm_delete.html', {'note': note})


def youtube(request):
    if request.method == "POST":
        form = DashboardFom(request.POST)
        text =  request.POST['text']
        video= VideosSearch(text,limit=20)
        result_list= []
        for i in video.result()['result']:
            result_dict={
                'input':text,
                'title':i['title'],
                'duration':i['duration'],
                'thumbnail':i['thumbnails'][0]['url'],
                'channel':i['channel']['name'],
                'link':i['link'],
                'views':i['viewCount']['short'],
                'published':i['publishedTime'],
            }
            desc=''
            if i['descriptionSnippet']:
                for j in i['descriptionSnippet']:
                    desc += j['text']
            result_dict['description']=desc
            result_list.append(result_dict) 
            context={
                'form':form,
                'results' :result_list
                }
        return render(request,'dashboard/youtube.html',context)           
    else:     
        form= DashboardFom()
    context = {'form':form}
    return render(request,"dashboard/youtube.html",context)

@login_required
def todo(request):
    if request.method == "POST":
        form = TodoForm(request.POST)
        if form.is_valid():
            try:
                finished=request.POST['is_finished']
                if finished == 'on':
                    finished = True
                else:
                    finished = False 
            except:
                finished = False 
            todos = Todo(
                user = request.user,
                title= request.POST['title'],
                is_finished= finished
            ) 
            todos.save()
            messages.success(request, f'Todo Added From {request.user.username}!!')
    else:        
         form =TodoForm()
    todo=Todo.objects.filter(user=request.user)
    if len(todo) == 0:
        todos_done = True
    else:
        todos_done = False
    context = {
        'form':form,
        'todos':todo,
        'todos_done':todos_done
    }
    return render(request,"dashboard/todo.html",context)

@login_required
def update_todo(request,pk=None):
    todo =  Todo.objects.get(id=pk)
    if todo.is_finished == True :
        todo.is_finished =  False
    else:
        todo.is_finished= True   
    todo.save()
    return redirect('todo')    
@login_required
def delete_todo(request,pk=None):
    Todo.objects.get(id=pk).delete()
    return redirect("todo")


def books(request):
    if request.method == "POST":
        form = DashboardFom(request.POST)
        text =  request.POST['text']
        url = "https://www.googleapis.com/books/v1/volumes?q=" +text
        r=requests.get(url)
        answer= r.json()
        result_list= []
        for i in range(10):
            result_dict={
                'title':answer['items'][i]['volumeInfo']['title'],
                'subtitle':answer['items'][i]['volumeInfo'].get('subtitle'),
                'description':answer['items'][i]['volumeInfo'].get('description'),
                'count':answer['items'][i]['volumeInfo'].get('pagecount'),
                'categories':answer['items'][i]['volumeInfo'].get('categories'),
                'rating':answer['items'][i]['volumeInfo'].get('pageRating'),
                'thumbnail':answer['items'][i]['volumeInfo'].get('imageLinks').get('thumbnail'),
                'preview':answer['items'][i]['volumeInfo'].get('previewLink'),
            }
            result_list.append(result_dict) 
            context={
                'form':form,
                'results' :result_list
                }
        return render(request,'dashboard/books.html',context)           
    else:     
       form= DashboardFom()
    context = {'form':form}
    return render(request,"dashboard/books.html",context)

def dictionary(request):
    if request.method == "POST":
        form = DashboardFom(request.POST)
        text =  request.POST['text']
        url = "https://api.dictionaryapi.dev/api/v2/entries/en_US/" +text
        r=requests.get(url)
        answer= r.json()
        try:
            phonetics = answer[0]['phonetics'][0]['text']        
            audio = answer[0]['phonetics'][0]['audio']  
            definition = answer[0]['meanings'][0]['definitions'][0]['definition']  
            example =  answer[0]['meanings'][0]['definitions'][0]['example']  
            synonyms = answer[0]['meanings'][0]['definitions'][0]['synonyms']
            context = {
                'form':form,
                'input':text,
                'phonetics':phonetics,
                'audio':audio,
                'definition':definition,
                'example':example,
                'synonyms':synonyms
            }  
        except:
            context= {
                'form':form,
                'input': ''
            }  
        return render(request,"dashboard/dictionary.html",context) 
    else:     
        form = DashboardFom()
    context ={'form':form}
    return render(request,"dashboard/dictionary.html",context)


def register(request):
    if request.method == "POST":
        form=UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request,f"Accound Created for {username} !!")
            return redirect("login")
    else:        
         form=UserRegistrationForm()
    context={
        'form':form
    }
    return render(request,"dashboard/register.html",context)

@login_required
def profile(request):
    homeworks = Homework.objects.filter(is_finished=False,user=request.user)
    todos =Todo.objects.filter(is_finished=False,user=request.user)
    if len(homeworks) == 0:
        homework_done = True
    else:
        homework_done = False  
    if len(todos) == 0:
        todos_done = True
    else:
        todos_done = False 
    context = {
        'homeworks': homeworks,
        'todos': todos,
        'homework_done':homework_done,
        'todos_done': todos_done
    }          
    return render(request,"dashboard/profile.html",context)

def all_categories(request):
    context=QuizCategory.objects.all()
    return render(request , "dashboard/all-category.html",{'data':context})

from datetime import timedelta
def category_questions(request,cat_id):
    category=QuizCategory.objects.get(id=cat_id)
    question=QuizQuestion.objects.filter(category=category).order_by('id').first()
    return render(request , "dashboard/category-questions.html",{'question':question,'category':category})

def submit_answer(request,cat_id,quest_id):
    if request.method=='POST':
        category=QuizCategory.objects.get(id=cat_id)
        question=QuizQuestion.objects.filter(category=category,id__gt=quest_id).exclude(id=quest_id).order_by('id').first()
        if 'skip' in request.POST:
              if question:
                  quest=QuizQuestion.objects.get(id=quest_id)
                  user=request.user
                  answer="not submitted"
                  UserSubmittedAnswer.objects.create(user=user,question=quest,right_answer=answer)
                  return render(request , "dashboard/category-questions.html",{'question':question,'category':category})
        else:
            quest=QuizQuestion.objects.get(id=quest_id)
            user=request.user
            answer=request.POST['answer']
            UserSubmittedAnswer.objects.create(user=user,question=quest,right_answer=answer)     
        if question:
           return render(request , "dashboard/category-questions.html",{'question':question,'category':category})
        else:
            result=UserSubmittedAnswer.objects.filter(user=request.user)
            skipped=UserSubmittedAnswer.objects.filter(user=request.user,right_answer='not submitted').count()
            attempted=UserSubmittedAnswer.objects.filter(user=request.user).exclude(right_answer='Not Submitted').count()
            
            rightAns=0
            percentage=0
            for row in result:
                if row.question.right_opt == row.right_answer:
                    rightAns+=1
            percentage=(rightAns*100)/result.count() 
            return render(request , "dashboard/result.html",{'result':result,'total_skipped':skipped,'attempted':attempted,'rightAns':rightAns,'percentage':percentage})
    else:
        return HttpResponse('Method not allowed!')

def result(request): 
    result=UserSubmittedAnswer.objects.filter(user=request.user)
    skipped=UserSubmittedAnswer.objects.filter(user=request.user,right_answer='not submitted').count()
    attempted=UserSubmittedAnswer.objects.filter(user=request.user).exclude(right_answer='Not Submitted').count()
            
    rightAns=0
    percentage=0
    for row in result:
        if row.question.right_opt == row.right_answer:
            rightAns+=1
    percentage=(rightAns*100)/result.count()         
    return render(request , "dashboard/result.html",{'result':result,'total_skipped':skipped,'attempted':attempted,'rightAns':rightAns,'percentage':percentage})

# def send_message(request, recipient_id):
#     if request.method == 'POST':
#         content = request.POST.get('content')
#         recipient = User.objects.get(pk=recipient_id)
#         if content:
#             Message.objects.create(sender=request.user, recipient=recipient, content=content)
#             return redirect('inbox')
#     return render(request, 'dashboard/messaging_interface.html', {'recipient_id': recipient_id})


# def messaging_interface(request, recipient_id):
#     return render(request, 'messaging_interface.html', {'recipient_id': recipient_id})



def search_articles(request):
    if request.method == 'GET' and 'query' in request.GET:
        query = request.GET.get('query')
        articles = fetch_articles(query)
        context = {
            'query': query,
            'articles': articles
        }
        return render(request, 'dashboard/article_search_results.html', context)

    return render(request, 'dashboard/search_articles.html')

def fetch_articles(query):
    articles = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    # Define websites and their search URLs
    websites = [
        {'name': 'GeeksforGeeks', 'url': f'https://www.geeksforgeeks.org/?s={query}'},
        # {'name': 'JavaTpoint', 'url': f'https://www.javatpoint.com/search?q={query}'},
        # Add more websites and their search URLs as needed
    ]

    for site in websites:
        response = requests.get(site['url'],headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # if site['name'] == 'GeeksforGeeks':
        #     results = soup.find_all('div', class_='archive-title')
        #     articles.extend([{'title': result.a.text, 'url': result.a['href']} for result in results])
        # elif site['name'] == 'JavaTpoint':
        #     results = soup.find_all('div', class_='panel-body')
        #     articles.extend([{'title': result.a.text, 'url': result.a['href']} for result in results])


        if site['name'] == 'GeeksforGeeks':
            results = soup.find_all('div', class_='archive-title')
            for result in results:
                title = result.a.text.strip()
                url = result.a['href']
                articles.append({'title': title, 'url': url})

        elif site['name'] == 'JavaTpoint':
            results = soup.find_all('div', class_='panel-body')
            for result in results:
                title = result.a.text.strip()
                url = result.a['href']
                articles.append({'title': title, 'url': url})
        # Add more conditions to parse results for additional websites

    return articles
