from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import CustomUser, Assignment, AssignmentSubmission


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder': 'Student ID / Username',
            'class': 'form-input',
            'autocomplete': 'username'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Password',
            'class': 'form-input',
            'autocomplete': 'current-password'
        })
    )


class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ['assignment_number', 'title', 'details', 'assigned_to', 'due_date']
        widgets = {
            'assignment_number': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g. ASS-001'}),
            'title': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Assignment Title'}),
            'details': forms.Textarea(attrs={'class': 'form-input', 'rows': 5, 'placeholder': 'Describe the assignment...'}),
            'due_date': forms.DateInput(attrs={'class': 'form-input', 'type': 'date'}),
        }

    def __init__(self, faculty_user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Faculty sees only students in their category
        self.fields['assigned_to'].queryset = CustomUser.objects.filter(
            role='student',
            category=faculty_user.category,
            is_active=True
        )
        self.fields['assigned_to'].widget.attrs.update({'class': 'form-input'})
        self.fields['assigned_to'].label = 'Assign To Student'


class SubmissionForm(forms.ModelForm):
    class Meta:
        model = AssignmentSubmission
        fields = ['student_name', 'course_name', 'submission_details', 'github_link']
        widgets = {
            'student_name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Your Full Name'}),
            'course_name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Your Course Name'}),
            'submission_details': forms.Textarea(attrs={
                'class': 'form-input', 'rows': 6,
                'placeholder': 'Describe what you did, steps followed, challenges faced...'
            }),
            'github_link': forms.URLInput(attrs={
                'class': 'form-input',
                'placeholder': 'https://github.com/yourname/repo'
            }),
        }


class ReviewForm(forms.Form):
    action = forms.ChoiceField(choices=[('accept', 'Accept'), ('reject', 'Reject')], widget=forms.HiddenInput())
    teacher_remarks = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-input', 'rows': 3,
            'placeholder': 'Optional remarks for the student...'
        })
    )
