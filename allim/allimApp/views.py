from django.shortcuts import render, redirect
from django.contrib import messages
from . import models
from .models import Teacher
import bcrypt
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.conf import settings
import openai, json

def index(request):
    return render(request,'index.html')

def Login_page(request):
    return render(request,'login.html')

def register_page(request):
    return render(request,'registration.html')

def reg_form(request):
    if request.method == "POST":
        errors = Teacher.objects.validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/register')
        if request.POST['you_are'] == 'teacher':
            models.create_teacher_account(request.POST)
            return redirect('/teacher/dashboard')
        elif request.POST['you_are'] == 'student':
            models.create_student_account(request.POST)
            return redirect('/student/dashboard')
    return redirect('/register')

def Login_form(request):
    if request.method == 'POST':
        loged_in_user=models.check_loged_user(request,request.POST)
        if loged_in_user['user']:
            if loged_in_user['password']:
                if request.POST['you_are'] == 'teacher':
                    return redirect('/teacher/dashboard')
                elif request.POST['you_are'] == 'student':
                    return redirect('/student/dashboard')
            else:
                messages.error(request, "Incorrect password.")
        else:
            messages.error(request, "Email not registered.")   
        return redirect('/login')
    else:
        return redirect('/')



def teacher_dashboard(request):
    return render(request,'teacher_dashboard.html')

def student_dashboard(request):
    return render(request,'student_dashboard.html')

        #OpenAI Ai      
openai.api_key = settings.OPENAI_API_KEY

def chatbot_view(request):
    return render(request, "chatbot.html")

@csrf_exempt
def get_bot_response(request):
    if request.method == "POST":
        data = json.loads(request.body)
        user_message = data.get("message", "")

        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": user_message}
                ]
            )
            bot_reply = response.choices[0].message["content"].strip()
            return JsonResponse({"response": bot_reply})
        except Exception as e:
            return JsonResponse({"response": f"Error: {str(e)}"})