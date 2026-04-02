from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from .models import CustomUser, Assignment, AssignmentSubmission, Notification


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ['student_id', 'get_full_name', 'username', 'email', 'role', 'category', 'course_name', 'phone_number', 'is_active']
    list_filter = ['role', 'category', 'is_active']
    search_fields = ['username', 'first_name', 'last_name', 'email', 'student_id', 'phone_number']
    ordering = ['role', 'first_name']

    fieldsets = (
        ('Login Info', {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'email', 'phone_number', 'address', 'profile_image')}),
        ('Samyak Info', {'fields': ('role', 'student_id', 'course_name', 'category')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        ('Login Info', {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2'),
        }),
        ('Personal Info', {
            'fields': ('first_name', 'last_name', 'email', 'phone_number', 'address'),
        }),
        ('Samyak Info', {
            'fields': ('role', 'student_id', 'course_name', 'category'),
        }),
    )


class AssignmentSubmissionInline(admin.StackedInline):
    model = AssignmentSubmission
    extra = 0
    readonly_fields = ['submitted_at', 'reviewed_at']


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ['assignment_number', 'title', 'assigned_to', 'assigned_by', 'status', 'due_date', 'created_at']
    list_filter = ['status', 'assigned_by__category']
    search_fields = ['title', 'assignment_number', 'assigned_to__first_name', 'assigned_to__username']
    ordering = ['-created_at']
    inlines = [AssignmentSubmissionInline]

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['assigned_to'].queryset = CustomUser.objects.filter(role='student')
        form.base_fields['assigned_by'].queryset = CustomUser.objects.filter(role='faculty')
        return form


@admin.register(AssignmentSubmission)
class AssignmentSubmissionAdmin(admin.ModelAdmin):
    list_display = ['assignment', 'student', 'course_name', 'github_link', 'submitted_at', 'is_accepted']
    list_filter = ['is_accepted']
    search_fields = ['student__username', 'assignment__title']
    readonly_fields = ['submitted_at']


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['user', 'message', 'notification_type', 'is_read', 'created_at']
    list_filter = ['notification_type', 'is_read']
