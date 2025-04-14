from django.views.generic.base import TemplateView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import messages


class IndexView(TemplateView):
    template_name = 'index.html'


class CustomLoginView(LoginView):
    template_name = 'login.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(
            self.request,
            ("Вы залогинены"),
            extra_tags='alert-success'
        )
        return response


class CustomLogoutView(LogoutView):
    def dispatch(self, request, *args, **kwargs):
        messages.success(
            request,
            ("Вы разлогинены"),
            extra_tags='alert-info'
        )
        return super().dispatch(request, *args, **kwargs)

