from django.contrib import messages, auth
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import UrlList, Clicks
import string
import random


def land_page(request):
    if request.POST:
        if not request.session.has_key('userid'):
            return redirect('/login')
        user = request.session['userid']
        url = request.POST.get('key', '')

        is_url = UrlList.objects.filter(url=url, user_id=user)
        if not is_url:
            s, key = True, ""
            while s:
                key = "".join(random.choices(string.ascii_uppercase+string.digits, k=7))
                is_key = UrlList.objects.filter(key=key)
                if not is_key:
                    s = False
            UrlList.objects.create(key=key, url=url, user_id=user)
            short_url = "http://127.0.0.1:8000/l/"+key
            return render(request, 'index.html', {'short_url': short_url})
        query = UrlList.objects.get(url=url, user_id=user)
        url = "http://127.0.0.1:8000/l/"+query.key
        return render(request, 'index.html', {'info': 'You have already shortened this url!', 'url': url})

    return render(request, 'index.html')


@never_cache
def login_page(request):
    if request.session.has_key('userid'):
        return redirect('/')
    return render(request, 'login.html')


@never_cache
def login_handle(request):
    if request.session.has_key('userid'):
        return redirect('/')
    # if request.method == 'POST':
    username = request.POST.get('user', '')
    password = request.POST.get('password', '')
    print(username, password)
    user = authenticate(username=username, password=password)
    print(user)
    if user:
        login(request, user)
        userid = User.objects.get(username=username)
        userid = userid.id
        request.session['userid'] = userid
        return redirect('/dashboard')
    return redirect('/login')


@never_cache
def signup(request):
    if request.session.has_key('userid'):
        return redirect('/')
    if request.POST:
        user = request.POST.get('user')
        email = request.POST.get('email')
        password = request.POST.get('pass')

        is_user = User.objects.filter(Q(username=user) | Q(email=email))
        if is_user:
            messages.error(request, 'username or email already exists!')
            return redirect('login')

        user_created = User.objects.create_user(username=user, email=email, password=password)
        user = User.objects.get(username=user)
        userid = user.id
        login(request, user_created)
        request.session['userid'] = userid
        return redirect('/')


def redirect_to(request, key):
    if key is not None:
        is_valid = UrlList.objects.filter(key=key)
        if is_valid:
            row = UrlList.objects.get(key=key)
            url = row.url
            total_clicks = row.total_clicks + 1
            is_valid.update(total_clicks=total_clicks)
            Clicks.objects.create(key_id_id=row.id)
            return redirect(url)


@never_cache
@login_required(login_url='/login')
def user_dashboard(request):
    user = request.session['userid']
    query = UrlList.objects.filter(user_id=user)
    if query:
        return render(request, 'dashboard.html', {'urls': query})

    return render(request, 'dashboard.html')


def logout_now(request):
    logout(request)
    request.session.flush()
    return redirect('/')


def page_not_found(request, exception):
    return HttpResponse('<h1>404 page not found!</h1>')
