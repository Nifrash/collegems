from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from .forms import LoginForm


class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    authentication_form = LoginForm
    redirect_authenticated_user = True

    def get_success_url(self):
        user = self.request.user

        if user.role == 'ADMIN':
            return reverse_lazy('admin_dashboard')

        elif user.role == 'STAFF':
            return reverse_lazy('staff_dashboard')

        elif user.role == 'STUDENT':
            return reverse_lazy('student_dashboard')

        elif user.role == 'LECTURER':
            return reverse_lazy('lecturer_dashboard')

        return reverse_lazy('login')


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('login')