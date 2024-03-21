from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .forms import CustomCreationForm
from django.contrib.auth.decorators import login_required
from .models import CustomUser

@login_required
def account_info(request):
    user = CustomUser.objects.get(id=request.user.id)

    return render(
        request,
        "auth/user_edit.html",
        context = {"user": user}
    )


def register(request):
    if request.method == "POST":
        form = CustomCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("countries")
    else:
        form = CustomCreationForm()
        context = {
            "form": form,
            "request": request
        }

        return render(
            request,
            "auth/register_form.html",
            context
        )
   

def log_in(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("countries")
            else:
                messages.error(request, "Password or username is incorrect!")

    else:
        form = AuthenticationForm()

    return render(
        request,
        "auth/login_form.html",
        context={"form": form}
    )


@login_required(redirect_field_name="/")
def log_out(request):
    logout(request)
    return redirect("countries")
