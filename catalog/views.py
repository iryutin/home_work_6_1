from django.shortcuts import render
from django.http import HttpResponse


def home(request):
    return render(request, "home.html")


# def contacts(request):
# return render(request, 'contacts.html')


def contacts(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        massage = request.POST.get("massage")
        return HttpResponse(f"Данные отправлены, {name}")
    return render(request, "contacts.html")
