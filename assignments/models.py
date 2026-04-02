from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


CATEGORY_CHOICES = [
    ('tech', 'Tech'),
    ('non_tech', 'Non-Tech'),
]

ROLE_CHOICES = [
    ('student', 'Student'),
    ('faculty', 'Faculty'),
]

ASSIGNMENT_STATUS = [
    ('pending', 'Pending'),
    ('submitted', 'Submitted'),
    ('completed', 'Completed'),
    ('rejected', 'Rejected'),
]


class CustomUser(AbstractUser):
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')
    student_id = models.CharField(max_length=50, unique=True, null=True, blank=True)
    phone_number = models.CharField(max_length=15, blank=True)
    course_name = models.CharField(max_length=100, blank=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='tech')
    address = models.TextField(blank=True)
    profile_image = models.ImageField(upload_to='profiles/', null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return f"{self.get_full_name() or self.username} ({self.role})"

    def get_display_name(self):
        return self.get_full_name() or self.username


class Assignment(models.Model):
    title = models.CharField(max_length=200)
    assignment_number = models.CharField(max_length=50)
    details = models.TextField()
    assigned_by = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE,
        related_name='assignments_created',
        limit_choices_to={'role': 'faculty'}
    )
    assigned_to = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE,
        related_name='assignments_received',
        limit_choices_to={'role': 'student'}
    )
    status = models.CharField(max_length=20, choices=ASSIGNMENT_STATUS, default='pending')
    due_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Assignment'
        verbose_name_plural = 'Assignments'

    def __str__(self):
        return f"[{self.assignment_number}] {self.title} → {self.assigned_to.get_display_name()}"

    def is_overdue(self):
        if self.due_date and self.status == 'pending':
            return timezone.now().date() > self.due_date
        return False


class AssignmentSubmission(models.Model):
    assignment = models.OneToOneField(Assignment, on_delete=models.CASCADE, related_name='submission')
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='submissions')
    student_name = models.CharField(max_length=100)
    course_name = models.CharField(max_length=100)
    submission_details = models.TextField()
    github_link = models.URLField(blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    teacher_remarks = models.TextField(blank=True)
    is_accepted = models.BooleanField(null=True)  # None=pending, True=accepted, False=rejected

    class Meta:
        ordering = ['-submitted_at']

    def __str__(self):
        return f"Submission: {self.assignment.title} by {self.student.get_display_name()}"


class Notification(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    notification_type = models.CharField(max_length=20, default='info')  # success, error, info
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Notif → {self.user.username}: {self.message[:50]}"
