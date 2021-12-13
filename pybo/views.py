# from django.http import HttpResponse  # 삭제
import json
import requests

from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from django.utils import timezone
from .forms import QuestionForm, AnswerForm
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse




def index(request):
    """
    pybo 목록 출력
    """
    # 입력 파라미터
    page = request.GET.get('page', '1')  # 페이지
    # http://localhost:8000/pybo/?page=1 처럼 GET 방식으로 호출된 URL에서 page값을 가져올 때 사용
    # http://localhost:8000/pybo/ 처럼 page값 없이 호출된 경우에는 디폴트로 1이라는 값을 설정한다.

    # 조회
    question_list = Question.objects.order_by('-create_date')

    # 페이징 처리
    paginator = Paginator(question_list, 10)  # 페이지당 10개씩 보여주기
    # 첫 번째 파라미터 question_list는 게시물 전체를 의미하는 데이터이고 두번째 파라미터 10은 페이지당 보여줄 게시물의 개수이다.

    page_obj = paginator.get_page(page)
    #  paginator를 이용하여 요청된 페이지(page)에 해당되는 페이징 객체(page_obj)를 생성

    context = {'question_list': page_obj}


    # context = {'question_list': question_list}
    return render(request, 'pybo/question_list.html', context)


def detail(request, question_id):
    """
    pybo 내용 출력
    """
    question = get_object_or_404(Question, pk=question_id)
    context = {'question': question}
    return render(request, 'pybo/question_detail.html', context)


# 로그아웃 상태에서 @login_required 어노테이션이 적용된 함수가 호출되면 자동으로 로그인 화면으로 이동
# @login_required 어노테이션은 login_url='common:login' 처럼 로그인 URL을 지정할 수 있다.
@login_required(login_url='common:login')
def answer_create(request, question_id):
    """
    pybo 답변등록
    answer_create 함수의 매개변수 question_id는 URL 매핑에 의해 그 값이 전달된다.
    답변 등록시 텍스트창에 입력한 내용은 answer_create 함수의 첫번째 매개변수 request를 통해 읽을 수 있다.
    """

    # 이 부분은 http://localhost:8000/pybo/30/ 처럼 없는 데이터를 요청할 경우 404 페이지를 출력
    question = get_object_or_404(Question, pk=question_id)


    # 수정 전 코드
    # question.answer_set.create(content=request.POST.get('content'), create_date=timezone.now())
    # return redirect('pybo:detail', question_id=question.id)
    # request.POST.get('content')는 POST로 전송된 폼(form) 데이터 항목 중 content 값을 의미한다.
    # 답변을 생성하기 위해 question.asnswer_set.create 를 사용하였다.
    # question.answer_set은 질문의 답변을 의미한다
    # Question과 Answer 모델은 서로 ForeignKey 로 연결되어 있기때문에 이처럼 사용할 수 있다
    # 이것을 사용해도 동일하다
    # answer = Answer(question=question, content=request.POST.get('content'), create_date=timezone.now())
    # answer.save()

    # 수정 후 코드. question_create와 같은 방법으로 AnswerForm을 이용하도록 변경
    if request.method == "POST":
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = request.user  # author 속성에 로그인 계정 저장
            answer.create_date = timezone.now()
            answer.question = question
            answer.save()
            return redirect('pybo:detail', question_id=question.id)
    else:
        form = AnswerForm()
    context = {'question': question, 'form': form}
    return render(request, 'pybo/question_detail.html', context)




@login_required(login_url='common:login')
def question_create(request):
    """
    pybo 질문등록
     1. else 구문
     "질문 등록하기" 버튼을 클릭한 경우에는 /pybo/question/create/ 페이지가 GET 방식으로 요청되어 question_create 함수가 실행
      <a href="{% url 'pybo:question_create' %}" class="btn btn-primary">질문 등록하기</a>과 같이 링크를 통해 페이지를 요청할 경우에는 무조건 GET 방식이 사용
      request.method 값이 GET이 되어 if .. else .. 에서 else 구문을 타게 되어 결국 질문 등록 화면을 보여 줄 것이다.

    2. if 구문
    질문 등록 화면에서 subject, content 항목에 값을 기입하고 "저장하기" 버튼을 클릭하면 이번에는 동일한 /pybo/question/create/ 페이지가 POST방식으로 요청된다
     form 태그에 action 속성이 지정되지 않으면 현재 페이지가 디폴트 action으로 설정되기 때문
      "저장하기" 버튼을 클릭하면 question_create 함수가 실행되고 request.method 값은 POST가 되면서 if 구문이 실행된다.
    """
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        # POST 방식에서는 form = QuestionForm(request.POST) 처럼 request.POST를 인수로 생성
        # request.POST를 인수로 QuestionForm을 생성할 경우에는
        # request.POST에 담긴 subject, content 값이 QuestionForm의 subject, content 속성에 자동으로 저장되어 객체가 생성
        if form.is_valid():
            # form.is_valid()는 form이 유효한지를 검사
            # form에 저장된 subject, content의 값이 올바르지 않다면 form에는 오류 메시지가 저장되고 form.is_valid()가 실패하여 다시 질문 등록 화면으로 돌아갈 것
            # 이 때 form에 저장된 오류 메시지는 질문 등록 화면에 표시

            question = form.save(commit=False)
            # form이 유효하다면 if form.is_valid(): 이후의 문장이 수행되어 질문 데이터가 생성
            # question = form.save(commit=False)는 form으로 Question 데이터를 저장하기 위한 코드
            # commit=False는 임시 저장을 의미
            # 임시 저장을 한 후 question 객체를 리턴받아 create_date에 값을 설정한 후 question.save()로 실제 저장하는 것

            question.author = request.user  # author 속성에 로그인 계정 저장
            # QuestionForm이 Question 모델과 연결된 모델 폼이기 때문에 이와 같이 사용할 수 있다

            question.create_date = timezone.now()
            question.save()
            return redirect('pybo:index')
        # 저장이 완료되면 return redirect('pybo:index')를 호출하여 질문 목록 화면으로 이동
    else:
        form = QuestionForm() # GET 방식에서는 form = QuestionForm() 처럼 QuestionForm을 인수 없이 생성
    context = {'form': form}
    # 'form : form으로 질문 등록 화면 폼 엘리먼트 생성
    return render(request, 'pybo/question_form.html', context)

@login_required(login_url='common:login')
def question_modify(request, question_id):
    """
    pybo 질문수정

    """
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author:
        # question_modify 함수는 로그인한 사용자(request.user)와 수정하려는 질문의 글쓴이(question.author)가 다를 경우에는 "수정권한이 없습니다"라는 오류를 발생시킨다.
        messages.error(request, '수정권한이 없습니다') # 오류를 발생시키기 위해 messages 모듈을 이용
        # messages는 장고가 제공하는 모듈로 넌필드 오류(non-field error)를 발생시킬 경우에 사용
        return redirect('pybo:detail', question_id=question.id)

    if request.method == "POST":
        # 질문 수정 화면에서 "저장하기" 버튼을 클릭하면 http://localhost:8000/pybo/question/modify/2/ 페이지가 POST 방식으로 호출되어 데이터가 수정
        # POST 요청인 경우 수정된 내용을 반영해야 하는 케이스이므로 다음처럼 폼을 생성
        form = QuestionForm(request.POST, instance=question)
        # instance를 기준으로 QuestionForm을 생성하지만 request.POST의 값으로 덮어쓰라는 의미
        if form.is_valid():
            question = form.save(commit=False)
            question.modify_date = timezone.now()  # 수정일시 저장
            question.save()
            return redirect('pybo:detail', question_id=question.id)
    else:
        #  "수정" 버튼을 클릭하면 http://localhost:8000/pybo/question/modify/2/ 페이지가 GET 방식으로 호출되어 질문수정 화면이 보여짐
        # GET 요청인 경우 질문수정 화면에 조회된 질문의 제목과 내용이 반영될 수 있도록 다음과 같이 폼을 생성
        form = QuestionForm(instance=question)

        # instance 값을 지정하면 폼의 속성 값이 instance의 값으로 채워진다. 질문을 수정하는 화면에서 제목과 내용이 채워진 채로 보일 것이다
    context = {'form': form}
    return render(request, 'pybo/question_form.html', context)


def generate_random_data():
    url='https://newsapi.org/v2/top-headlines?country=us&category=business&apiKey=API_KEY'
    r=requests.get(url)
    payload = json.loads(r.text)
    count=1
    for data in payload.get('articles'):
        print(count)
        ElasticDemo.objects.create(
            title = data.get('title'),
            content = data.get('description')
        )

def index2(request):
    generate_random_data()
    return JsonResponse({'status : 200'})
