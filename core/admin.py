from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django_summernote.admin import SummernoteModelAdmin

from core.models import models, Student, Subscription, summer_models

for model in models:
    admin.site.register(model)


class UserProfileAdmin(UserAdmin):
    fieldsets = (
        (None, {
            "fields": ("username", "password")
        }),
        ('Personal info', {
            "fields": (
                "first_name",
                "last_name",
                "email",
                "avatar",
                "lecture_finished",
                "course_finished",
                "course",
                "role"
            )
        }),
        ("Permissions", {
            "fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")
        }),
        ("Important dates", {
            "fields": ("last_login", "date_joined")
        })
    )


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    readonly_fields = [
        'payment_id',
        'payment_message',
        'payment_status',
        'user',
        'course',
        'date'
    ]


class CourseLectureHomeworkAdmin(SummernoteModelAdmin):
    summernote_fields = 'description'


admin.site.register(Student, UserProfileAdmin)

for s_model in summer_models:
    admin.site.register(s_model, CourseLectureHomeworkAdmin)