from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.shortcuts import render, redirect
from django.views.generic import FormView, ListView, DetailView, TemplateView
from core.forms import RegistrationForm
from core.models import Course, Category, Lecture, Comment, Homework, HomeworkStudentDone


class RegistrationView(FormView):
    template_name = 'registration.html'
    form_class = RegistrationForm
    success_url = '/login/'

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class ProfileView(LoginRequiredMixin, ListView):
    template_name = 'profile.html'
    model = get_user_model()


class IndexView(LoginRequiredMixin, ListView):
    template_name = 'index.html'
    model = Course
    paginate_by = 6

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = Category.objects.all()
        context.update({
            'categories': categories
        })
        return context

    def get_queryset(self):
        if self.request.user.role.title == 'Teacher':
            return Course.objects.filter(student_course=self.request.user.id)
        else:
            courses = Course.objects.all().annotate(
                count=Count('student_course')
            ).order_by('-count')
            return courses


class CourseByCategoryView(LoginRequiredMixin, ListView):
    template_name = 'includes/courses.html'
    model = Course
    paginate_by = 6

    def get_queryset(self):
        return Course.objects.filter(category_id=self.request.GET.get('category')).annotate(
            count=Count('student_course')
        ).order_by('-count')


class CourseView(LoginRequiredMixin, DetailView):
    template_name = 'course.detail.html'
    model = Course

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        courses = Course.objects.filter(student_course__username=self.request.user)
        if Course.objects.get(title__contains=kwargs.get('object')) in courses:
            lectures = Lecture.objects.filter(course_id=kwargs.get('object'))
            context['lectures'] = lectures
            comments = Comment.objects.filter(course_id=kwargs.get('object'))
            context['comments'] = comments
        else:
            pass
        return context


class AddCommentView(LoginRequiredMixin, TemplateView):
    template_name = 'includes/comments.html'

    def post(self, request, *args, **kwargs):
        Comment.objects.create(
            message=request.POST.get('comment'),
            course_id=kwargs.get('pk'),
            user_id=request.user.id,
            is_approved=True
        )
        return redirect(request.META['HTTP_REFERER'])


class StudentsView(LoginRequiredMixin, ListView):
    template_name = 'students.html'
    get_user_model()

    def get_queryset(self):
        return get_user_model().objects.filter(course=self.kwargs.get('pk'))


class LectureView(LoginRequiredMixin, DetailView):
    template_name = 'lecture_detail.html'
    model = Lecture
    pk_url_kwarg = 'pk_lecture'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        homeworks = Homework.objects.filter(lecture_id=kwargs.get('object').id)
        context.update({
            'homeworks': homeworks
        })
        return context

    def post(self, request, *args, **kwargs):
        current_lecture = Lecture.objects.get(id=kwargs.get('pk_lecture'))
        if current_lecture in request.user.lecture_finished.all():
            request.user.lecture_finished.remove(
                kwargs.get('pk_lecture')
            )
        else:
            request.user.lecture_finished.add(
                kwargs.get('pk_lecture')
            )

        return redirect(request.META['HTTP_REFERER'])


class EvaluateHomeworkView(LoginRequiredMixin, TemplateView):
    template_name = 'lecture_detail.html'

    def post(self, request, *args, **kwargs):
        homework = HomeworkStudentDone.objects.get(id=kwargs.get('pk_homework'))
        mark = request.POST.get('mark')
        homework.mark = mark
        homework.save()

        return redirect(request.META['HTTP_REFERER'])
