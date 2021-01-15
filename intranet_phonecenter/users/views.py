from .forms import RegisterForm, AccountSettingsForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import redirect

from .forms import RegisterForm
from .models import UserProfile

def is_teammember(user=None):
    if not user or user.is_anonymous:
        return False
    return user.is_teammember()

def hello_old(request):
    return HttpResponse("Hello world")


def hello(request):
    return render(
        request,
        "users/hello.html",
        {
            "message": "Hello world"
        }
    )


@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("users:login"))


def login_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("users:hello"))
    elif 'username' in request.POST and 'password' in request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if request.GET.get('next') is not None:
                return redirect(request.GET['next'])
            else:
                return HttpResponseRedirect(reverse("users:hello"))
        else:
            return render(
                request,
                'users/login.html',
                {
                    "auth_error": True,
                }
            )
    else:
        return render(
            request,
            'users/login.html',
            {}
        )


def register(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("users:hello"))
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            raw_password = form.cleaned_data['raw_password']
            user = UserProfile.objects.create_user(
                username=username,
                email=email,
                password=raw_password,
            )
            user.save()
            login(request, user)
            return HttpResponseRedirect(reverse("users:hello"))
    else:
        form = RegisterForm()
    return render(
        request,
        'utils/form.html',
        {
            'title': "Inscription",
            'form': form,
        })


@login_required
def myaccount(request):
    return render(
        request,
        'users/myaccount.html',
    )


@login_required
def account_settings(request):
    if request.method == 'POST':
        form = AccountSettingsForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
        else:
            print(form)
    else:
        form = AccountSettingsForm(instance=request.user)
    return render(
        request,
        'utils/form.html',
        {
            'url_form': reverse("users:register"),
            'title': "Mes informations",
            'form': form,
        }
    )


@user_passes_test(lambda u: u.is_superuser)
def role_attribution(request):
    users = UserProfile.objects.filter(
        teammember__isnull=True, customer__isnull=True).order_by("-id")
    return render(
        request,
        'users/role_attribution.html',
        {
            'users': users,
        }
    )
