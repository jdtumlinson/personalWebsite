from .forms import *
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as authLogin, logout as authLogout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.db import IntegrityError
from .scripts import brandfetchCalls

# Create your views here.

@login_required(login_url="login")
def applicationTracker(request):   
    sortField = request.GET.get("sort")
    order = request.GET.get("order", "asc")

    if not sortField:
        apps = Application.objects.filter(user=request.user).order_by("applicationStatus", "company")
    else:
        if order == "desc":
            sortField = f"-{sortField}"
        apps = Application.objects.filter(user=request.user).order_by(sortField)
        
    form_list = []
    for app in apps:
        form = applicationForm(initial= {
            "company": app.company,
            "title": app.title,
            "applicationStatus": app.applicationStatus,
            "dateApplied": app.dateApplied,
            "link": app.link,
            "domain": app.domain
        })
        form_list.append({"appform": form,"appInstance": app})
        
    return render(request, "applicationTracker/applicationTracker.html", {"form_list": form_list})



@login_required(login_url="login")
def updateApplication(request, app_id):
    application = get_object_or_404(Application, id=app_id, user=request.user)
    
    if request.method == "POST":
        form = applicationForm(request.POST, instance=application)
        if form.is_valid():
            form.save()
            return redirect("applicationTracker")
        print(form.errors)
    return redirect("applicationTracker")



@login_required(login_url="login")
def addApplication(request):
    if request.method == "POST":
        form = applicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.user = request.user
            application.save()
            return redirect("applicationTracker")
    else:
        form = applicationForm()
    
    return render(request, "applicationTracker/addApplication.html", {"form": form})



@login_required(login_url="login")
def deleteApplication(request, app_id):
    try:
        app = Application.objects.get(id=app_id, user=request.user)
        app.delete()
        messages.success(request, "Application deleted")
    except Application.DoesNotExist:
        messages.error(request, "Application not found")
    return redirect("applicationTracker")



def searchCompanies(request):
    query = request.GET.get("q", "").lower()
    suggestions = []
    
    if query: 
        companies = brandfetchCalls.brandfetch(query)
        suggestions = [c for c in companies if query in c["name"].lower()]
    return JsonResponse(suggestions, safe=False)



def createAccount(request):
    if request.user.is_authenticated:
        return redirect("applicationTracker")
    
    context = {}
    if request.method == "POST":
        form = createAccountForm(request.POST)
        if form.is_valid():
            try:
                User.objects.create_user(
                    username=form.cleaned_data["username"],
                    password=form.cleaned_data["password"]
                )
                
                return redirect("applicationTracker")
            except IntegrityError:
                context["error"] = "That username is already taken"
        else:
            context["error"] = form.errors
    else:
        form = createAccountForm()
    
    context["form"] = form
    return render(request, "applicationTracker/createAccount.html", context)



def login(request):
    context = {}
    
    if request.method == "POST":
        form = loginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data["username"], 
                password=form.cleaned_data["password"]
            )
            
            if user is not None:
                authLogin(request, user)
                return redirect("applicationTracker")
            else:
                context = {"error": "Username and password do not match any known user"}
    else:
        form = loginForm()
    
    context["form"] = form
    return render(request, "applicationTracker/login.html", context)


def logout(request):
    authLogout(request)
    return redirect("login")