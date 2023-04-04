from django import template
from django.db.models import Avg

from core.models import HomeworkStudentDone, Lecture

register = template.Library()

@register.filter(name='get_code')
def get_code(link):
    return link.split('/')[-1]

@register.filter(name='avg')
def avg(course_name):
    homework = HomeworkStudentDone.objects.filter(homework__lecture__course=course_name).aggregate(Avg('mark'))

    if homework.get('mark__avg'):
        return homework.get('mark__avg')
    else:
        return 0

@register.filter(name='width')
def width(course_id):
    lectures = Lecture.objects.filter(course_id=course_id)
    lectures_count = lectures.count()
    percent = 0.0
    if lectures_count:
        percent = lectures.filter(lecture_finished__course=course_id).count() / lectures_count * 100
        print(lectures.filter(lecture_finished__course=course_id))
    return percent