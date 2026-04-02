from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.http import JsonResponse
from .models import CustomUser, Assignment, AssignmentSubmission, Notification
from .forms import LoginForm, AssignmentForm, SubmissionForm, ReviewForm


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    form = LoginForm(request, data=request.POST or None)
    error = None

    if request.method == 'POST':
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
        else:
            error = "Invalid credentials. Please try again."

    return render(request, 'assignments/login.html', {'form': form, 'error': error})


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def dashboard(request):
    user = request.user
    if user.role == 'student':
        return student_dashboard(request)
    elif user.role == 'faculty':
        return faculty_dashboard(request)
    else:
        return redirect('/admin/')


def student_dashboard(request):
    user = request.user
    all_assignments = Assignment.objects.filter(assigned_to=user)
    pending = all_assignments.filter(status='pending')
    submitted = all_assignments.filter(status='submitted')
    completed = all_assignments.filter(status='completed')
    rejected = all_assignments.filter(status='rejected')
    notifications = Notification.objects.filter(user=user, is_read=False)[:5]

    context = {
        'user': user,
        'pending': pending,
        'submitted': submitted,
        'completed': completed,
        'rejected': rejected,
        'total': all_assignments.count(),
        'notifications': notifications,
        'unread_count': notifications.count(),
    }
    return render(request, 'assignments/student_dashboard.html', context)


def faculty_dashboard(request):
    user = request.user
    # Faculty sees only students in their category
    my_students = CustomUser.objects.filter(role='student', category=user.category, is_active=True)
    assigned = Assignment.objects.filter(assigned_by=user)
    pending_review = AssignmentSubmission.objects.filter(
        assignment__assigned_by=user,
        is_accepted=None
    )
    total_assignments = assigned.count()
    completed = assigned.filter(status='completed').count()
    pending = assigned.filter(status='pending').count()
    rejected_count = assigned.filter(status='rejected').count()

    form = AssignmentForm(faculty_user=user)

    if request.method == 'POST' and 'create_assignment' in request.POST:
        form = AssignmentForm(faculty_user=user, data=request.POST)
        if form.is_valid():
            assignment = form.save(commit=False)
            assignment.assigned_by = user
            assignment.save()
            # Notify student
            Notification.objects.create(
                user=assignment.assigned_to,
                message=f"New assignment assigned: '{assignment.title}' (#{assignment.assignment_number})",
                notification_type='info'
            )
            messages.success(request, f"Assignment '{assignment.title}' assigned successfully!")
            return redirect('dashboard')
        else:
            messages.error(request, "Please fix the errors below.")

    context = {
        'user': user,
        'my_students': my_students,
        'assigned': assigned[:10],
        'pending_review': pending_review,
        'total_assignments': total_assignments,
        'completed': completed,
        'pending': pending,
        'rejected_count': rejected_count,
        'form': form,
    }
    return render(request, 'assignments/faculty_dashboard.html', context)


@login_required
def submit_assignment(request, assignment_id):
    user = request.user
    if user.role != 'student':
        return redirect('dashboard')

    assignment = get_object_or_404(Assignment, id=assignment_id, assigned_to=user)

    if assignment.status not in ['pending', 'rejected']:
        messages.warning(request, "This assignment cannot be submitted.")
        return redirect('dashboard')

    # Check if already has a submission (resubmit after rejection)
    existing_submission = None
    try:
        existing_submission = assignment.submission
    except AssignmentSubmission.DoesNotExist:
        pass

    form = SubmissionForm(request.POST or None, instance=existing_submission)
    if form.is_valid():
        submission = form.save(commit=False)
        submission.assignment = assignment
        submission.student = user
        submission.is_accepted = None
        submission.save()
        assignment.status = 'submitted'
        assignment.save()
        messages.success(request, "Assignment submitted successfully! Awaiting review.")
        return redirect('dashboard')

    return render(request, 'assignments/submit_assignment.html', {
        'assignment': assignment,
        'form': form,
        'existing': existing_submission
    })


@login_required
def reject_assignment(request, assignment_id):
    """Student rejects/refuses an assignment"""
    user = request.user
    if user.role != 'student':
        return redirect('dashboard')

    assignment = get_object_or_404(Assignment, id=assignment_id, assigned_to=user)
    if assignment.status == 'pending':
        assignment.status = 'rejected'
        assignment.save()
        Notification.objects.create(
            user=assignment.assigned_by,
            message=f"{user.get_display_name()} rejected assignment: '{assignment.title}'",
            notification_type='error'
        )
        messages.info(request, "Assignment rejected.")
    return redirect('dashboard')


@login_required
def review_submission(request, submission_id):
    """Faculty reviews a student's submission"""
    user = request.user
    if user.role != 'faculty':
        return redirect('dashboard')

    submission = get_object_or_404(AssignmentSubmission, id=submission_id, assignment__assigned_by=user)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            action = form.cleaned_data['action']
            remarks = form.cleaned_data.get('teacher_remarks', '')
            submission.teacher_remarks = remarks
            submission.reviewed_at = timezone.now()

            if action == 'accept':
                submission.is_accepted = True
                submission.assignment.status = 'completed'
                notif_msg = f"🎉 Your assignment '{submission.assignment.title}' has been ACCEPTED!"
                notif_type = 'success'
            else:
                submission.is_accepted = False
                submission.assignment.status = 'rejected'
                notif_msg = f"Your assignment '{submission.assignment.title}' was rejected. Please resubmit."
                notif_type = 'error'

            submission.save()
            submission.assignment.save()

            Notification.objects.create(
                user=submission.student,
                message=notif_msg,
                notification_type=notif_type
            )
            messages.success(request, f"Assignment {'accepted' if action == 'accept' else 'rejected'} successfully.")
            return redirect('dashboard')

    return render(request, 'assignments/review_submission.html', {
        'submission': submission,
        'form': ReviewForm()
    })


@login_required
def mark_notifications_read(request):
    Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
    return JsonResponse({'status': 'ok'})


@login_required
def assignment_detail(request, assignment_id):
    user = request.user
    if user.role == 'student':
        assignment = get_object_or_404(Assignment, id=assignment_id, assigned_to=user)
    else:
        assignment = get_object_or_404(Assignment, id=assignment_id, assigned_by=user)
    
    return render(request, 'assignments/assignment_detail.html', {'assignment': assignment})


@login_required
def all_assignments(request):
    user = request.user
    if user.role == 'faculty':
        assignments_qs = Assignment.objects.filter(assigned_by=user)
    else:
        assignments_qs = Assignment.objects.filter(assigned_to=user)
    
    status_filter = request.GET.get('status', '')
    if status_filter:
        assignments_qs = assignments_qs.filter(status=status_filter)

    return render(request, 'assignments/all_assignments.html', {
        'assignments': assignments_qs,
        'status_filter': status_filter
    })


# ── Error handlers ──────────────────────────────────────────────────────────
def handler404(request, exception):
    return render(request, '404.html', status=404)


def handler500(request):
    return render(request, '500.html', status=500)
