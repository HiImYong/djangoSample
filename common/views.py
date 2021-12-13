from django.shortcuts import render

# Create your views here.
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from common.forms import UserForm


def signup(request):
    """
    계정생성
    """
    if request.method == "POST":
        # POST 요청인 경우에는 화면에서 입력한 데이터로 사용자를 생성
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            # form.cleaned_data.get 함수는 입력값을 개별적으로 얻고 싶은 경우에 사용하는 함수
            # 여기서는 사용자명과 비밀번호를 얻기 위해 사용
            user = authenticate(username=username, password=raw_password)  # 사용자 인증
            # authenticate와 login함수는 django.contrib.auth 모듈의 함수로 사용자 인증과 로그인을 담당
            # authenticate 함수는 사용자명과 비밀번호가 정확한지 검증하는 함수
            login(request, user)  # 로그인
            return redirect('index')
    else:
        # GET 요청인 경우에는 계정생성 화면을 리턴한다
        form = UserForm()
    return render(request, 'common/signup.html', {'form': form})