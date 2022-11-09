from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View

from users.forms import UserCreateForm, UserUpdateForm


class RegisterView(View):
    def get(self, request):
        create_form = UserCreateForm
        context = {
            'form': create_form
        }
        return render(request, 'users/register.html', context)

    def post(self, request):
        create_form = UserCreateForm(data=request.POST)

        if create_form.is_valid():
            create_form.save()
            return redirect('login')
        else:
            context = {
                'form': create_form
            }
            return render(request, 'users/register.html', context)


class LoginView(View):
    def get(self, request):
        login_form = AuthenticationForm()

        return render(request, 'users/login.html', {'login_form': login_form})

    def post(self, request):
        login_form = AuthenticationForm(data=request.POST)

        if login_form.is_valid():
            user = login_form.get_user()
            login(request, user)
            messages.success(request, 'You are successfully logged in.')

            return redirect('book_list')
        else:
            return render(request, 'users/login.html', {'login_form': login_form})


class ProfileView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'users/profile.html', {'user': request.user})


class LogoutView(View):
    def get(self, request):
        logout(request)
        messages.info(request, 'You are successfully logged out.')
        return redirect('landing_page')


class ProfileUpdateView(View):
    def get(self, request):
        update_form = UserUpdateForm(instance=request.user)
        return render(request, 'users/profile_edit.html', {'update_form': update_form})

    def post(self, request):
        update_form = UserUpdateForm(instance=request.user, data=request.POST)

        if update_form.is_valid():
            update_form.save()
            return render(request, 'users/profile.html')
        else:
            return render(request, 'users/profile_edit.html', {'update_form': update_form})
