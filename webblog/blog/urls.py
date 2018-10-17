from django.urls import path
from . import views

urlpatterns = [
	path('', views.index, name='index'),
	path('user/<str:username>/', views.user, name='user'), # 这个最好验证一下只有登录用户才能进的路由
	path('register', views.new_register, name='register'),
	path('login', views.new_login, name='login'),
	path('logout', views.new_logout, name='logout'),
	path('edit/<str:username>/', views.edit_username, name='edit'),
	path('post/<int:id>', views.post, name='post'),
]