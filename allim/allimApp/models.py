from django.db import models
import bcrypt
import re


class UserManager(models.Manager):
    def validator(self,postData):
        errors = {}
        if len(postData['first_name']) < 2:
            errors["first_name"] = "First name must be at least 2 characters."
        if not postData['first_name'].isalpha():
            errors["first_name"] = "First name must contain letters only."

        if len(postData['last_name']) < 2:
            errors["last_name"] = "Last name must be at least 2 characters."
        if not postData['last_name'].isalpha():
            errors["last_name"] = "Last name must contain letters only."

        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not postData['email'].strip():
            errors["email"] = "Email is required."
        if not EMAIL_REGEX.match(postData['email']):
            errors["email"] = "Invalid email address."

        if len(postData['password']) < 8:
            errors["password"] = "Password must be at least 8 characters."
        if postData['password'] != postData['confirm-password']:
            errors["confirm-password"] = "Password and confirmation do not match."
        
        return errors
            

class Teacher(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255 )
    specialization = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Student(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255 )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    teachers = models.ManyToManyField(Teacher, related_name='students') 
    objects = UserManager()


class Course(models.Model):
    course_name = models.CharField(max_length=45, unique=True)
    description = models.TextField()
    teachers = models.ForeignKey(Teacher,on_delete=models.CASCADE, related_name='courses')
    students=  models.ManyToManyField(Student, related_name='courses')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Lecture(models.Model):
    topic = models.CharField(max_length=100)
    url = models.URLField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lectures')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

def create_teacher_account(postdata):
    password = postdata['password']
    pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()   
    Teacher.objects.create(
        first_name = postdata['first_name'], 
        last_name = postdata['last_name'], 
        email = postdata['email'],
        password = pw_hash  )

def create_student_account(postdata):
    password = postdata['password']
    pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()   
    Student.objects.create(
        first_name = postdata['first_name'], 
        last_name = postdata['last_name'], 
        email = postdata['email'],
        password = pw_hash  )
    
def check_loged_user(request,user_data):
        email = user_data['email']
        password = user_data['password']
        you_are=user_data['you_are']
        login={
            'user':False,
            'password':False
        }
        if you_are =='teacher':
            users = Teacher.objects.filter(email=email)
        elif you_are == 'student':
            users = Student.objects.filter(email=email)            
        if users:
            login['user']=True
            user = users[0]
            if bcrypt.checkpw(password.encode(), user.password.encode()):
                request.session['user_id'] = user.id
                request.session['name'] = user.first_name
                login['password']=True
        return login

def get_teacher(email):
    return Teacher.objects.get(email=email)

def create_course(course,t_id):
    tech=Teacher.objects.get(email=t_id)
    Course.objects.create(course_name=course['title'],description=course['description'],teachers=tech)

def get_teacher_courses(email):
    tech=Teacher.objects.get(email=email)
    courses=Course.objects.filter(teachers=tech)
    return courses

def delete_course(c_id):
    deleted_course=Course.objects.get(id=c_id)
    deleted_course.delete()
