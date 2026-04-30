from django import forms
from django.contrib.auth import get_user_model
from students.models import Student
from lecturers.models import Lecturer
from courses.models import Course, Enrollment
from payments.models import Payment

User = get_user_model()

class BootstrapFormMixin:
    def apply_bootstrap(self):
        for field_name, field in self.fields.items():
            widget = field.widget
            if isinstance(widget, forms.CheckboxInput):
                widget.attrs['class'] = 'form-check-input'
            elif isinstance(widget, forms.Select):
                widget.attrs['class'] = 'form-select'
            elif isinstance(widget, forms.ClearableFileInput):
                widget.attrs['class'] = 'form-control'
            else:
                widget.attrs['class'] = 'form-control'

            widget.attrs.setdefault('placeholder', field.label)


class StudentRegistrationForm(BootstrapFormMixin, forms.ModelForm):
    first_name = forms.CharField(max_length=150)
    last_name = forms.CharField(max_length=150)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = Student
        fields = [
            'student_nic',
            'student_image',
            'nic_copy',
            'date_of_birth',
            'gender',
            'address',
        ]
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'address': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_bootstrap()

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email already exists.")
        return email

    def clean_student_nic(self):
        nic = self.cleaned_data.get('student_nic')
        if nic == '':
            return None
        return nic

class LecturerRegistrationForm(BootstrapFormMixin, forms.ModelForm):
    first_name = forms.CharField(max_length=150)
    last_name = forms.CharField(max_length=150)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Lecturer
        fields = ['department', 'specialization', 'phone']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_bootstrap()

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email already exists.")
        return email


# class CourseForm(BootstrapFormMixin, forms.ModelForm):
#     class Meta:
#         model = Course
#         fields = ['course_name', 'description', 'credits']
#         widgets = {
#             'description': forms.Textarea(attrs={'rows': 3}),
#         }
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.apply_bootstrap()

class CourseForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Course
        fields = ['course_name', 'description', 'credits', 'course_fee']

        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_bootstrap()

class AssignCourseForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Course
        fields = ['lecturer']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_bootstrap()

class EnrollmentForm(forms.ModelForm):
    class Meta:
        model = Enrollment
        fields = ['student', 'course']

        widgets = {
            'student': forms.Select(attrs={'class': 'form-select'}),
            'course': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['student'].queryset = User.objects.filter(role='STUDENT')
        self.fields['course'].queryset = Course.objects.all()

# class PaymentForm(BootstrapFormMixin, forms.ModelForm):
#     class Meta:
#         model = Payment
#         fields = ['student', 'amount', 'payment_method', 'status',]
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.apply_bootstrap()

class PaymentForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['student', 'course', 'amount', 'payment_method', 'status']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_bootstrap()