import datetime
from django.contrib.auth.models import AbstractUser
from django.db import models


def avatar_upload_to(obj, filename):
    return f"avatars/{filename}"


def poster_upload_to(obj, filename):
    return f"posters/{filename}"


class Student(AbstractUser):
    role = models.ForeignKey('Role', on_delete=models.CASCADE)
    course = models.ManyToManyField('Course', related_name='student_course', blank=True)
    avatar = models.ImageField(blank=True, upload_to=avatar_upload_to, default='avatar/default.png')
    lecture_finished = models.ManyToManyField('Lecture', related_name='lecture_finished', blank=True)
    course_finished = models.ManyToManyField('Course', related_name='course_finished', blank=True)

    def __str__(self):
        return self.username


class Role(models.Model):
    title = models.CharField(max_length=20)

    def __str__(self):
        return self.title


class Category(models.Model):
    title = models.CharField(max_length=50)
    is_enabled = models.BooleanField()

    def __str__(self):
        return self.title


class Course(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    price = models.IntegerField()
    is_enabled = models.BooleanField()
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True, blank=True)
    date_end = models.DateTimeField()
    photo = models.ImageField(blank=True, upload_to=poster_upload_to, default='posters/default.png')

    def __str__(self):
        return self.title


class Lecture(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    video = models.CharField(max_length=255)
    photo = models.ImageField(blank=True, null=True, upload_to=poster_upload_to)
    course = models.ForeignKey('Course', on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Comment(models.Model):
    user = models.ForeignKey('Student', on_delete=models.CASCADE)
    course = models.ForeignKey('Course', on_delete=models.CASCADE)
    message = models.TextField()
    is_approved = models.BooleanField()

    def __str__(self):
        return f"{self.user.username} -> {self.course.title}"


class Homework(models.Model):
    lecture = models.ForeignKey('lecture', on_delete=models.CASCADE)
    description = models.TextField()

    def __str__(self):
        return self.description


class HomeworkStudentDone(models.Model):
    user = models.ForeignKey('Student', on_delete=models.CASCADE)
    user_homework = models.TextField()
    homework = models.ForeignKey('Homework', on_delete=models.CASCADE)
    mark = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user.username} -> {self.homework.lecture.title}"


class Subscription(models.Model):
    user = models.ForeignKey('Student', on_delete=models.CASCADE)
    course = models.ForeignKey('Course', on_delete=models.CASCADE)
    payment_id = models.CharField(max_length=255)
    payment_message = models.CharField(max_length=255)
    payment_status = models.CharField(max_length=255)
    date = models.IntegerField()

    def __str__(self):
        return f"{self.user.username} -> {datetime.datetime.utcfromtimestamp(self.date).ctime()}"


models = [Role, Category, Comment, HomeworkStudentDone]
summer_models = [Homework, Course, Lecture]
