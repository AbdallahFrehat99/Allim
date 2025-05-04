from django.db import models
import bcrypt
import re

class UserManager(models.Manager):
    def validator(self,postdata):
        errors = {}
        if len(postdata['first_name']) < 3:
            errors["first_name"] = "First name should be at least 2 characters."

        if len(postdata['last_name']) < 3:
            errors["last_name"] = "Last name should be at least 3 characters."
            

        # if len(postdata['specialization']) < 1:
        #     errors["specialization"] = "Please select whether you are a Teacher or a Student. "

        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postdata['email']):            
            errors['email'] = "Invalid email address!"
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
    dob = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    teachers = models.ManyToManyField(Teacher, related_name='students') 
    objects = UserManager()


class Course(models.Model):
    course_name = models.CharField(max_length=45, unique=True)
    description = models.TextField()
    teachers = models.ManyToManyField(Teacher, related_name='courses')  
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Lecture(models.Model):
    topic = models.CharField(max_length=100)
    url = models.URLField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lectures')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

def Create_account(postdata):
    password = postdata['password']
    pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()   
    Teacher.objects.create(
        first_name = postdata['first_name'], 
        last_name = postdata['last_name'], 
        email = postdata['email'],
        # specialization = postdata['specialization'], Note: i didn't know how to do this one
        password = pw_hash  )

