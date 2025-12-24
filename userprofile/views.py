from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from .models import Profile
from .forms import UserLoginForm, UserRegisterForm, ProfileForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required



# Create your views here.


def user_login(request):
    if request.method == 'POST':
        user_login_form = UserLoginForm(data=request.POST)
        if user_login_form.is_valid():
            data = user_login_form.cleaned_data
            user = authenticate(request, username=data['username'], password=data['password'])
            if user:
                login(request, user)
                return redirect('home')
            else:
                return HttpResponse('用户名或密码错误')
        else:
            return HttpResponse('账号或密码输入不合法')
    elif request.method == 'GET':
        user_login_form = UserLoginForm()
        context = {
            'form': user_login_form
        }
        return render(request, 'userprofile/login.html', context)
    else:
        return HttpResponse('请使用GET或POST请求数据')


def user_logout(request):
    logout(request)
    return redirect('home')


def user_register(request):
    if request.method == 'POST':
        user_register_form = UserRegisterForm(data=request.POST)
        if user_register_form.is_valid():
            new_user = user_register_form.save(commit=False)
            new_user.set_password(user_register_form.cleaned_data['password'])
            new_user.save()
            login(request, new_user)
            return redirect('home')
        else:
            return HttpResponse('注册表单输入有误。请重新输入~')
    elif request.method == 'GET':
        user_register_form = UserRegisterForm()
        context = {
            'form': user_register_form
        }
        return render(request, 'userprofile/register.html', context)
    else:
        return HttpResponse('请使用GET或POST请求数据')


@login_required(login_url='/userprofile/login/')
def user_delete(request, id):
    if request.method == 'POST':
        user = User.objects.get(id=id)
        if request.user == user:
            logout(request)
            user.delete()
            return redirect('home')
        else:
            return HttpResponse('您没有权限删除该用户')
    else:
        return HttpResponse('请使用POST请求删除用户')

@login_required(login_url='/userprofile/login/')
def profile_edit(request, id):
    user = User.objects.get(id=id)
    if Profile.objects.filter(user_id=id).exists():
        profile = Profile.objects.get(user_id=id)
    else:
        profile = Profile(user_id=id)

    if request.method == 'POST':
        if request.user != user:
            return HttpResponse('您没有权限编辑该用户的个人信息')
        profile_form = ProfileForm(request.POST, request.FILES, instance=profile)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, '个人资料已更新')
            return redirect("userprofile:edit", id=id)
        else:
            return HttpResponse('个人信息更新失败')
        
    elif request.method == 'GET':
        profile_form = ProfileForm(instance=profile)
        context = {
            'form': profile_form,
            'profile': profile,
            'user': user,
        }
        return render(request, 'userprofile/edit.html', context)
    else:
        return HttpResponse('请使用GET或POST请求数据')



