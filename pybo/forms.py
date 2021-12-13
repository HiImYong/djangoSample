from django import forms
from pybo.models import Question, Answer


class QuestionForm(forms.ModelForm):
    class Meta:
        # 메타클래스가 있어야 모델폼이 사용이 가능하다.
        model = Question  # 사용할 모델
        # 장고에는 모델폼과 일반폼이 있다.
        # 모델 폼은 모델(Model)과 연결된 폼으로 폼을 저장하면 연결된 모델의 데이터를 저장할수 있는 폼이다
        fields = ['subject', 'content']  # QuestionForm에서 사용할 Question 모델의 속성

        # 질문 등록화면을 수정해주는 위젯이다.
        # {{ form.as_p }} 태그는 HTML 코드를 자동으로 생성하기 때문에 부트스트랩을 적용할 수가 없기 때문에,
        # Meta 클래스의 widgets 속성을 지정하면 입력 필드에 form-control과 같은 부트스트랩 클래스를 추가할 수 있다
        #widgets = {
        #    'subject': forms.TextInput(attrs={'class': 'form-control'}),
        #    'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 10}),
        #}
        labels = {
            #Subject 와 content를 영문이 아니라 한글로 표현한다.
            'subject': '제목',
            'content': '내용',
        }



class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['content']
        labels = {
            'content': '답변내용',
        }