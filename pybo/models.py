from django.db import models
from django.contrib.auth.models import User


# 모델을 변경한 후에는 반드시 makemigrations와 migrate를 통해 데이터베이스를 변경해 주어야 한다
# 장고는 모델(Model)을 이용하여 데이터베이스를 처리한다.

class Question(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    # on_delete=models.CASCADE는 계정이 삭제되면 이 계정이 작성한 질문을 모두 삭제하라는 의미. 속성에 null을 허용하려면 CASCADE 옆에 , null=True 적어주면 된다.
    # author 필드는 User 모델을 ForeignKey로 적용하여 선언
    # User 모델은 django.contrib.auth 앱이 제공하는 사용자 모델
    # author 속성에 저장해야 하는 사용자 객체는 로그인 후 request 객체를 통해 얻을 수 있다
    subject = models.CharField(max_length=200)
    content = models.TextField()
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)  # 수정 일시

    # null=True는 데이터베이스에서 modify_date 칼럼에 null을 허용한다는 의미
    # blank=True는 form.is_valid()를 통한 입력 데이터 검사 시 값이 없어도 된다는 의미
    # 즉, null=True, blank=True는 어떤 조건으로든 값을 비워둘 수 있음을 의미

    def __str__(self):
        # 장고 셸 사용시 아이디 대신 제목으로 값 출력해줌
        return self.subject


class Answer(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    content = models.TextField()
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)  # 수정 일시


