from django.shortcuts import render
from django.http import HttpResponse
from models import User, Post, Tag, Image, Like

# Create your views here.


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")