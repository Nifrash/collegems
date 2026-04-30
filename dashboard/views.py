from accounts.decorators import role_required
from django.shortcuts import redirect, get_object_or_404
from courses.models import Course, Enrollment
from decimal import Decimal
from django.db.models import Sum
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect
from students.models import Student
from courses.models import Enrollment
from payments.models import Payment

@login_required
def dashboard_redirect(request):
    user = request.user
    if user.is_superuser or user.role == 'ADMIN':
        return redirect('admin_dashboard')
    elif user.role == 'STAFF':
        return redirect('staff_dashboard')
    elif user.role == 'LECTURER':
        return redirect('lecturer_dashboard')
    elif user.role == 'STUDENT':
        return redirect('student_dashboard')
    return redirect('login')

@login_required
@role_required('ADMIN')
def admin_dashboard(request):
    return render(request, 'dashboard/admin_dashboard.html')

@login_required
@role_required('LECTURER')
def lecturer_dashboard(request):
    return render(request, 'dashboard/lecturer_dashboard.html')

def is_student(user):
    return user.is_authenticated and user.role == 'STUDENT'

@login_required
@user_passes_test(is_student)
def student_dashboard(request):
    try:
        student_profile = request.user.student_profile
    except Student.DoesNotExist:
        return redirect('student_create')

    enrollments = Enrollment.objects.filter(
        student=request.user
    ).select_related('course', 'course__lecturer', 'course__lecturer__user')

    payments = Payment.objects.filter(
        student=student_profile
    ).select_related('course').order_by('-id')

    course_balances = []

    total_course_fees = Decimal('0.00')
    total_paid = Decimal('0.00')

    for enrollment in enrollments:
        course = enrollment.course

        paid_amount = Payment.objects.filter(
            student=student_profile,
            course=course,
            status='PAID'
        ).aggregate(total=Sum('amount'))['total'] or Decimal('0.00')

        remaining = course.course_fee - paid_amount

        total_course_fees += course.course_fee
        total_paid += paid_amount

        course_balances.append({
            'course': course,
            'paid_amount': paid_amount,
            'remaining': remaining,
        })

    total_remaining = total_course_fees - total_paid

    return render(request, 'dashboard/student_dashboard.html', {
        'student': student_profile,
        'enrollments': enrollments,
        'payments': payments,
        'course_balances': course_balances,
        'total_course_fees': total_course_fees,
        'total_paid': total_paid,
        'total_remaining': total_remaining,
    })

@login_required
def enroll_course(request, course_id):
    if request.user.role != "STUDENT":
        return redirect("dashboard")

    student_profile = get_object_or_404(Student, user=request.user)
    course = get_object_or_404(Course, id=course_id)

    Enrollment.objects.get_or_create(
        student=student_profile,
        course=course
    )

    return redirect("student_dashboard")