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
        'courses':models.get_student(request.session['s_id']).courses.all()
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

def student_profile(request):

    student = get_object_or_404(Student, email=request.session['s_id'])
    return render(request, 'profile_student.html', {'student': student})

def edit_student_page(request):
    context={
        'student':models.get_student(request.session['s_id'])
    }
    return render(request,'edit_student_profile.html',context)

def edit_student_profile(request):
    if request.method == 'POST':
        models.edit_student_profile(request.POST)
        messages.success(request, "Your profile has been updated successfully.")
        return redirect('/student_profile')
    return render(request, 'edit_student_profile.html')


def register_course(request):
    context={
        'courses':models.get_courses()
    }
    return render(request,'add_course1.html',context)

def enroll_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    student = models.get_student(request.session['s_id'])

    if student.courses.filter(id=course.id).exists():
        messages.info(request, "You are already enrolled in this course.")
    else:
        models.assign_course(course,student)
        messages.success(request, f"You have successfully enrolled in {course.course_name}.")

    return redirect('/enroll_course')

def delete_course(request,c_id):
    models.delete_course(c_id)
    return redirect('/teacher/dashboard')




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


def student_course_lectures(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    lectures = course.lectures.all()
    return render(request, 'student/course_lectures.html', {
        'course': course,
        'lectures': lectures
    })



def convert_youtube_url(url):
    # تحويل رابط YouTube إلى embed
    youtube_regex = r"(?:youtube\.com/watch\?v=|youtu\.be/)([a-zA-Z0-9_-]+)"
    match = re.search(youtube_regex, url)
    if match:
        video_id = match.group(1)
        return f"https://www.youtube.com/embed/{video_id}"
    return url  # يرجع الرابط الأصلي إذا لم يكن YouTube

def lecture_detail(request, lecture_id):
    lecture = get_object_or_404(Lecture, id=lecture_id)
    embed_url = convert_youtube_url(lecture.url)
    return render(request, 'student/lecture_detail.html', {
        'lecture': lecture,
        'embed_url': embed_url
    })

# def add_lecture(request, course_id):
#     course = get_object_or_404(Course, id=course_id)
#     if request.method == 'POST':
#         Lecture.objects.create(
#             topic=request.POST['topic'],
#             url=request.POST.get('url', ''),
#             description=request.POST.get('description', ''),
#             duration=request.POST.get('duration') or None,
#             course=course
#         )
#         messages.success(request, 'Lecture added successfully!')
#         return redirect('course_lectures', course_id=course.id)
#     return render(request, 'add_lecture.html', {'course': course})


# def course_lectures(request, course_id):
#     course = get_object_or_404(Course, id=course_id)
#     lectures = Lecture.objects.filter(course=course)
#     return render(request, 'teacher/course_lectures.html', {
#         'course': course,
#         'lectures': lectures,
#     })

def teacher_profile(request):
    teacher = get_object_or_404(Teacher, email=request.session['t_id'])
    return render(request, 'profile.html', {'teacher': teacher})

def edit_teacher_page(request):
    context={
        'teacher':models.get_teacher(request.session['t_id'])
    }
    return render(request,'edit_profile.html',context)

def edit_teacher_profile(request):
    if request.method == 'POST':
        models.edit_teacher_profile(request.POST)
        messages.success(request, "Your profile has been updated successfully.")
        return redirect('/teacher_profile')
    return render(request, 'edit_profile.html')