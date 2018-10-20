from django.urls import path
from . import views
from django.conf.urls import handler403, handler404, handler500

# 定义错误跳转页面 settings中需修改DEBUG = False ALLOWED_HOSTS = ['127.0.0.1', 'localhost']或者ALLOWED_HOSTS = ['*']
handler403 = views.permission_denied
handler404 = views.page_not_found
handler500 = views.page_error

urlpatterns = [
	path('', views.index, name='index'),
	path('user/<str:username>/', views.user, name='user'), # 这个最好验证一下只有登录用户才能进的路由
	path('register', views.new_register, name='register'),
	path('login', views.new_login, name='login'),
	path('logout', views.new_logout, name='logout'),
	path('edit/<str:username>/', views.edit_username, name='edit'),
	path('post/<int:id>', views.post, name='post'),
	path('edit/<int:id>', views.edit_post, name='edit_post'),

	path('follow/<str:username>', views.follow, name='follow'),
	path('unfollow/<str:username>', views.unfollow, name='unfollow'),
	path('followers/<str:username>', views.followers, name='followers'),
	path('followed_by/<str:username>', views.followed, name='followed'),
]