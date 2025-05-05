from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from . import models
from .models import Teacher,Student,Course,Lecture
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
            request.session['t_id']=request.POST['email']
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
                    request.session['t_id']=request.POST['email']
                    return redirect('/teacher/dashboard')
                elif request.POST['you_are'] == 'student':
                    request.session['s_id']=request.POST['email']
                    return redirect('/student/dashboard')
            else:
                messages.error(request, "Incorrect password.")
        else:
            messages.error(request, "Email not registered.")   
        return redirect('/login')
    else:
        return redirect('/')



def teacher_dashboard(request):
    context={
        'teacher':models.get_teacher(request.session['t_id']),
        'courses':models.get_teacher_courses(request.session['t_id'])
    }
    return render(request,'teacher_dashboard.html',context)

def student_dashboard(request):
    context={
        'student':models.get_student(request.session['s_id']),
        'courses': Student.courses.all()
    }
    return render(request,'student_dasboard.html',context)

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
        

def log_out(request):
    request.session.clear()
    return redirect('/login')


def create_course_page(request):
    return render(request,'add_course.html')

def create_course(request):
    models.create_course(request.POST,request.session['t_id'])
    return redirect('/teacher/dashboard')
#################################################################################################
# def student_dashboard(request):
#     if 'user_id' not in request.session or request.session.get('role') != 'student':
#         return redirect('/login')

#     student = get_object_or_404(Student, id=request.session['user_id'])
#     context = {
#         'student': student,
#         'courses': student.courses.all()
#     }
#     return render(request, 'student/dashboard.html', context)


def student_profile(request):
    if 'user_id' not in request.session or request.session.get('role') != 'student':
        return redirect('login_page')

    student = get_object_or_404(Student, id=request.session['user_id'])
    return render(request, 'student/student_profile.html', {'student': student})

def edit_student_profile(request):
    student = request.user.student 
    if request.method == 'POST':
        student.first_name = request.POST.get('first_name')
        student.last_name = request.POST.get('last_name')
        student.email = request.POST.get('email')
        student.save()
        messages.success(request, "Your profile has been updated successfully.")
        return redirect('student_profile')
    return render(request, 'edit_student_profile.html', {'student': student})



def enroll_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    student = request.user.student 

    if student.courses.filter(id=course.id).exists():
        messages.info(request, "You are already enrolled in this course.")
    else:
        student.courses.add(course)
        messages.success(request, f"You have successfully enrolled in {course.course_name}.")

    return redirect('view_all_courses')

def delete_course(request,c_id):
    models.delete_course(c_id)
    return redirect('/teacher/dashboard')


from django.contrib import messages

def add_lecture(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if request.method == 'POST':
        Lecture.objects.create(
            topic=request.POST['topic'],
            url=request.POST.get('url', ''),
            description=request.POST.get('description', ''),
            duration=request.POST.get('duration') or None,
            course=course
        )
        messages.success(request, 'Lecture added successfully!')
        return redirect('course_lectures', course_id=course.id)
    return render(request, 'add_lecture.html', {'course': course})


def course_lectures(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    lectures = Lecture.objects.filter(course=course)
    return render(request, 'teacher/course_lectures.html', {
        'course': course,
        'lectures': lectures,
    })
