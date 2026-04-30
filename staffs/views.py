from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum, Q
from accounts.decorators import role_required
from students.models import Student
from lecturers.models import Lecturer
from courses.models import Course, Enrollment
from payments.models import Payment
from .forms import (
    StudentRegistrationForm,
    LecturerRegistrationForm,
    CourseForm,
    AssignCourseForm,
    EnrollmentForm,
    PaymentForm,
)

User = get_user_model()
def generate_username(first_name, last_name):
    base_username = f"{first_name}.{last_name}".lower().replace(" ", "")

    username = base_username
    counter = 1

    while User.objects.filter(username=username).exists():
        username = f"{base_username}{counter}"
        counter += 1

    return username

@login_required
@role_required('STAFF')
def staff_dashboard(request):

    total_amount = Payment.objects.aggregate(total=Sum('amount'))['total'] or 0

    context = {
        'total_students': Student.objects.count(),
        'total_lecturers': Lecturer.objects.count(),
        'total_courses': Course.objects.count(),
        'total_enrollments': Enrollment.objects.count(),
        'total_payments': Payment.objects.count(),
        'total_payment_amount': total_amount,
        'recent_students': Student.objects.select_related('user').order_by('-id')[:5],
        'recent_payments': Payment.objects.select_related('student', 'student__user').order_by('-id')[:5],
    }
    return render(request, 'staffs/dashboard.html', context)
@login_required
@role_required('STAFF')
def register_student(request):
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = generate_username(first_name, last_name)

            user = User.objects.create_user(
                username=username,
                first_name=first_name,
                last_name=last_name,
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password'],
                role='STUDENT',
            )

            student = form.save(commit=False)
            student.user = user
            student.save()
            messages.success(request, f"Student registered successfully. Username: {username}")

            return redirect('student_list')
    else:
        form = StudentRegistrationForm()

    return render(request, 'staffs/register_student.html', {
        'form': form,
        'page_title': 'Register Student'
    })

@login_required
@role_required('STAFF')
def student_list(request):
    query = request.GET.get('q', '').strip()
    students = Student.objects.select_related('user')

    if query:
        students = students.filter(
            Q(student_id__icontains=query) |
            Q(student_nic__icontains=query) |
            Q(user__first_name__icontains=query) |
            Q(user__last_name__icontains=query) |
            Q(user__username__icontains=query) |
            Q(user__email__icontains=query)
        )

    students = students.order_by('-id')

    return render(request, 'staffs/student_list.html', {
        'students': students,
        'query': query,
        'page_title': 'Students',
    })

@login_required
@role_required('STAFF')
def register_lecturer(request):
    if request.method == 'POST':
        form = LecturerRegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = generate_username(first_name, last_name)

            user = User.objects.create_user(
                username=username,
                first_name=first_name,
                last_name=last_name,
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password'],
                role='LECTURER',
            )

            lecturer = form.save(commit=False)
            lecturer.user = user
            lecturer.save()

            messages.success(request, f'Lecturer registered successfully. Username: {username}')
            return redirect('lecturer_list')
    else:
        form = LecturerRegistrationForm()

    return render(request, 'staffs/register_lecturer.html', {
        'form': form,
        'page_title': 'Register Lecturer'
    })

@login_required
@role_required('STAFF')
def lecturer_list(request):
    lecturers = Lecturer.objects.select_related('user').order_by('-id')
    return render(request, 'staffs/lecturer_list.html', {'lecturers': lecturers, 'page_title': 'Lecturers'})


@login_required
@role_required('STAFF')
def register_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Course created successfully.')
            return redirect('course_list')
    else:
        form = CourseForm()
    return render(request, 'staffs/register_course.html', {'form': form, 'page_title': 'Register Course'})


@login_required
@role_required('STAFF')
def course_list(request):
    courses = Course.objects.select_related('lecturer', 'lecturer__user').order_by('-id')
    return render(request, 'staffs/course_list.html', {'courses': courses, 'page_title': 'Courses'})


@login_required
@role_required('STAFF')
def assign_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    if request.method == 'POST':
        form = AssignCourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            messages.success(request, 'Course assigned successfully.')
            return redirect('course_list')
    else:
        form = AssignCourseForm(instance=course)

    return render(
        request,
        'staffs/assign_course.html',
        {
            'form': form,
            'course': course,
            'page_title': 'Assign Lecturer',
        }
    )

@login_required
@role_required('STAFF')
def enroll_student(request):
    if request.method == 'POST':
        form = EnrollmentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Student enrolled successfully.')
            return redirect('enrollment_list')
    else:
        form = EnrollmentForm()

    return render(request, 'staffs/enroll_student.html', {
        'form': form,
        'page_title': 'Enroll Student'
    })

@login_required
@role_required('STAFF')
def enrollment_list(request):
    query = request.GET.get('q', '').strip()

    enrollments = Enrollment.objects.select_related(
        'student',
        'course'
    )

    if query:
        enrollments = enrollments.filter(
            Q(student__student_profile__student_id__icontains=query) |
            Q(student__first_name__icontains=query) |
            Q(student__last_name__icontains=query) |
            Q(student__username__icontains=query) |
            Q(course__course_code__icontains=query) |
            Q(course__course_name__icontains=query)
        )

    enrollments = enrollments.order_by('-id')

    return render(request, 'staffs/enrollment_list.html', {
        'enrollments': enrollments,
        'query': query,
        'page_title': 'Enrollments',
    })

@login_required
@role_required('STAFF')
def payment_list(request):
    payments = Payment.objects.select_related('student', 'student__user').order_by('-id')
    return render(request, 'staffs/payment_list.html', {'payments': payments, 'page_title': 'Payments'})

@login_required
@role_required('STAFF')
def add_payment(request):
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Payment added successfully.')
            return redirect('payment_list')
    else:
        form = PaymentForm()

    return render(
        request,
        'staffs/payment_form.html',
        {
            'form': form,
            'page_title': 'Add Payment',
            'title': 'Add Payment',
        }
    )

@login_required
@role_required('STAFF')
def edit_payment(request, pk):
    payment = get_object_or_404(Payment, pk=pk)

    if request.method == 'POST':
        form = PaymentForm(request.POST, instance=payment)
        if form.is_valid():
            form.save()
            messages.success(request, 'Payment updated successfully.')
            return redirect('payment_list')
    else:
        form = PaymentForm(instance=payment)

    return render(
        request,
        'staffs/payment_form.html',
        {
            'form': form,
            'page_title': 'Edit Payment',
            'title': 'Edit Payment',
        }
    )