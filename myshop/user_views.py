from django.shortcuts import render, redirect, HttpResponseRedirect
from django.http.response import JsonResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from myshop.forms import RegistrationForm, LoginForm

def register_user(request):
    form = RegistrationForm()
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login_user')
    return render(
        request=request,
        template_name='user/register.html',
        context={
            'form': form
        }
    )

def login_user(request):
    form = LoginForm()
    message = ""
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            # Hàm authenticate('username', 'password')
            # Xác thực khi username/password cung cấp là đúng -> trả về 1 object/instance từ class User
            user = authenticate(
                username = form.cleaned_data['username'],
                password = form.cleaned_data['password']
            )
            if user:
                # Xác thực thành công
                print('Bạn đã xác thực thành công') # Mới xác thực
                # Chưa có đăng nhập
                login(request=request, user=user) # Login/giữ trạng thái đăng nhập thành công
                if request.GET.get('next'):
                    return HttpResponseRedirect(request.GET['next'])
                return redirect('index')
            else:
                message = 'Vui lòng kiểm tra lại Username/Password'
    return render(
        request=request,
        template_name='user/login.html',
        context={
            'form': form,
            'message': message
        }
    )

# Hàm phía server nhận từ Javascript gửi lên
# JSON gửi từ JS <=> thì server cũng gửi lại JSON

def validate_username(request):
    if request.method == "POST":
        username = request.POST['username']
        try:
            User.objects.get(username=username)
            return JsonResponse({'message': f'{username} đã trùng'}, status=409) # 409 Conflict
        except User.DoesNotExist:
            return JsonResponse({'message': 'OK'}, status=200)
