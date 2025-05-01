
from django.shortcuts import render
from django.http import HttpResponse

from catalog.models import Product


def home(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, "home.html", context)

def product_info(requst, pk):
    product = Product.objects.get(id=pk)
    context = {'product': product}
    return render(requst, "product_info.html", context)

def contacts(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        massage = request.POST.get("massage")
        return HttpResponse(f"Данные отправлены, {name}")
    return render(request, "contacts.html")
