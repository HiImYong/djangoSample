from django.urls import path
from django.urls import include, path


from . import views

app_name = 'pybo' # 서로 다른 앱에서 동일한 URL 별칭을 사용하면 중복이 발생할 수 있으므로, app_name을 추가해줌. app name은 "네임스페이스"라고 지칭

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:question_id>/', views.detail, name='detail'),
    path('answer/create/<int:question_id>/', views.answer_create, name='answer_create'),
    # 페이지를 요청하면 views.answer_create 함수가 호출될 것이다.
    path('question/create/', views.question_create, name='question_create'),
    # url 'pybo:question_modify' question.id URL이 추가되었으므로 pybo/urls.py에 다음처럼 URL매핑을 추가한다.
    path('question/modify/<int:question_id>/', views.question_modify, name='question_modify'),
    path('index2/', views.index2, name='index2'),
    path('question/delete/<int:question_id>/', views.question_delete, name='question_delete'),
]


