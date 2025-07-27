from django.shortcuts import render
from menu.models import Menu


def index(request):
    return render(request, 'index.html', {'menus': Menu.objects.all()})