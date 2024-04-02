from django.shortcuts import render, redirect
from django.views.generic import CreateView
from .forms import SignupForm, LoginUserForm
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.views.generic import FormView
from django.contrib.auth import authenticate, login
from django.contrib import messages

class UserRegisterView(CreateView):
    form_class = SignupForm
    template_name = 'registration/registration.html'
    success_url = reverse_lazy('home')

    # авторизоваться после регистрации
    def form_valid(self, form):
        super().form_valid(form)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password1']
        email = form.cleaned_data['email']
        first_name = form.cleaned_data['first_name']
        last_name = form.cleaned_data['last_name']
        user = authenticate(
            self.request,
            username=username,
            password=password,
            email=email,
            first_name=first_name,
            last_name=last_name
        )
        if user is not None:
            login(self.request, user)

        return redirect(self.get_success_url())

    # запретить регистрироваться, если уже вошли
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)

    # отобразить ошибки
    # def form_invalid(self, form):
    #     # messages.error(self.request, "There was an error with the form.")
    #     for field, errors in form.errors.items():
    #         field_label = form.fields[field].label
    #         for error in errors:
    #             print(field_label, error)
    #             messages.error(self.request, f"{field_label}: {error}", "danger")
    #     return super().form_invalid(form)


class UserLoginView(FormView):
    template_name = 'registration/login.html'
    form_class = LoginUserForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(self.request, username=username, password=password)
        if user is not None:
            login(self.request, user)
            return super().form_valid(form)
        return redirect('login')

    # запретить авторизованным пользователям логинится
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)

