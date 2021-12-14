from django.conf import settings
from django.contrib import admin
from django.urls import include, path

from pybo import views

# from pybo import views  # 더 이상 필요하지 않으므로 삭제


urlpatterns = [
    path('admin/', admin.site.urls),
    path('pybo/', include('pybo.urls')),  # pybo 앱의 urls.py 파일을 사용
    path('common/', include('common.urls')),  # common 앱의 urls.py 파일을 사용
    path('', views.index, name='index'),  # '/' 에 해당되는 path. / 다음에 아무것도 없으면 pybo/views.py 파일의 index 함수가 실행된다

]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]