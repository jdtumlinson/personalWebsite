from django.shortcuts import render

def homePage(request):
    return render(request, "homePage/homePage.html")

def aboutPage(request):
    return render(request, "homePage/about.html")

def projectsPage(request):
    return render(request, "homePage/projects.html")

def contactPage(request):
    return render(request, "homePage/contact.html")