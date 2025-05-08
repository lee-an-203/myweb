from django.shortcuts import render, redirect, HttpResponseRedirect
from django.http.response import JsonResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from myshop.forms import RegistrationForm, LoginForm
from django.contrib.auth.decorators import login_required

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
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            # Xác thực người dùng
            user = authenticate(username=username, password=password)
            
            if user is not None:
                # Đăng nhập thành công
                login(request=request, user=user)
                print('Bạn đã xác thực thành công')
                
                # Kiểm tra nếu có tham số 'next' trong URL
                next_url = request.GET.get('next')
                if next_url:
                    return HttpResponseRedirect(next_url)
                
                # Nếu không có 'next', chuyển hướng về trang chính
                return redirect('index')
            else:
                # Xác thực thất bại
                message = "Tên đăng nhập hoặc mật khẩu không đúng."
        else:
            # Form không hợp lệ
            message = "Vui lòng nhập tài khoản, mật khẩu."
    else:
        # GET request: hiển thị form đăng nhập
        message = ""

    return render(
        request=request,
        template_name='user/login.html',
        context={
            'form': form,
            'message': message
        }
    )


def validate_username(request):
    if request.method == "POST":
        username = request.POST['username']
        try:
            User.objects.get(username=username)
            return JsonResponse({'message': f'{username} đã tồn tại'}, status=409)
        except User.DoesNotExist:
            return JsonResponse({'message': 'Tên người dùng hợp lệ'}, status=200)

