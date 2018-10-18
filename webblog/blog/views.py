from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import get_object_or_404

from .forms import ArticleForm, RegisterForm, LoginForm, EditUserForm
from .models import User, Blog_Articles


# 首页
def index(request):
	if request.method == 'POST':
		form = ArticleForm(request.POST)
		if form.is_valid():
			user = User.objects.get(username=request.user)
			title = request.POST['title']
			body = request.POST['body']
			article = Blog_Articles(
				title=title, body=body, author=user
			)
			article.save()
			messages.add_message(request, messages.SUCCESS, '发布成功')
			return HttpResponseRedirect('/')
		else:
			messages.add_message(request, messages.WARNING, '不能为空')
	posts = Blog_Articles.objects.order_by('-create_time')
	paginator = Paginator(posts, 20)
	page = request.GET.get('page')
	try:
		contacts = paginator.page(page)
	except PageNotAnInteger:  # 如果page不是有一个有效的数字。则跳转到第一页
		contacts = paginator.page(1)
	except EmptyPage:		# 如果page超过了最大或者最小范围。则跳转到最后一页
		contacts = paginator.page(paginator.num_pages)
	form = ArticleForm()
	return render(request, 'blog/index.html', {'form': form, 'contacts': contacts})


# 个人资料页面
@login_required(login_url='login')
def user(request, username):
	user = User.objects.get(username=username)
	posts = Blog_Articles.objects.filter(author=user)
	return render(request, 'blog/user.html', {'user': user,'posts':posts})

# 注册视图
def new_register(request):
	if request.method == 'POST':
		form = RegisterForm(request.POST)
		if form.is_valid():
			username = form.cleaned_data['username']
			try:
				save_name = User.objects.get(username=username)
			except:
				save_name = None
			if save_name is None:
				password = form.cleaned_data['password']
				email = form.cleaned_data['email']
				user = User.objects.create_user(username, email, password)
				user.adder = request.POST['adder']
				user.phone = request.POST['phone']
				user.birthday = request.POST['birthday']
				user.gender = request.POST['gender']
				#user.first_name = first_name
				#user.last_name = last_name
				user.save()
				messages.add_message(request, messages.SUCCESS, '创建用户成功!')
				return HttpResponseRedirect('/') # 正常都是要跳转到登录
			else:
				messages.add_message(request, messages.ERROR, '用户名已存在!')
				return HttpResponseRedirect('register') # 正常都是要跳转到登录
		else:
			messages.add_message(request, messages.WARNING, '请检查一下各项的输入!')
			form = RegisterForm()
			return render(request, 'blog/register.html', {'form':form})
	else:
		form = RegisterForm()
		return render(request, 'blog/register.html', {'form':form})


# 登录视图
def new_login(request):
	if request.method == 'POST':
		form = LoginForm(request.POST)
		if form.is_valid():
			username = request.POST['username']
			password = request.POST['password']
			user = authenticate(request, username=username, password=password)
			if user is not None:
				login(request, user)
				messages.add_message(request, messages.SUCCESS, '登录成功！')
				return HttpResponseRedirect('/')
			else:
				messages.add_message(request, messages.ERROR, '账号或者密码错误请重新输入！')
				return render(request, 'blog/login.html', {'form':form})
		else:
			form = LoginForm()
			messages.add_message(request, messages.WARNING, '请检查一下各项的输入是否有误！')
			return render(request, 'blog/login.html', {'form':form})
	else:
		form = LoginForm()
		return render(request, 'blog/login.html', {'form':form})


# 注销视图
def new_logout(request):
	messages.add_message(request, messages.WARNING, '注销成功!')
	logout(request)
	return HttpResponseRedirect('/')

# 编辑个人资料
@login_required(login_url='login')
def edit_username(request, username):
	user = User.objects.get(username=username)
	if request.method == 'POST':
		if request.user == user.username or request.user.is_superuser:
			form = EditUserForm(request.POST)
			if form.is_valid():
				user.email = request.POST['email']
				user.adder = request.POST['adder']
				user.phone = request.POST['phone']
				user.birthday = request.POST['birthday']
				user.gender = request.POST['gender']
				user.save()
				messages.add_message(request, messages.SUCCESS, '修改成功！')
				return HttpResponseRedirect('/user/{}/'.format(user.username))
			else:
				messages.add_message(request, messages.WARNING, '请检查一下各项的输入！')
				return render(request, 'blog/edit.html', {'form':form})
		else:
			messages.add_message(request, messages.WARNING, '暂无权限修改此文章')
			return HttpResponseRedirect('/')
	else:
		form = EditUserForm()
		return render(request, 'blog/edit.html', {'form':form, 'user':user})


# 单文章页面
@login_required(login_url='login')
def post(request, id):
	try:
		post = get_object_or_404(Blog_Articles, id=id)
	except:
		messages.add_message(request, messages.ERROR, '文章不存在！')
		# raise Http404 等完善了404页面再用这个页面
		return HttpResponseRedirect('/')
	return render(request, 'blog/post.html', {'post':post})


# 自定义错误页面
def page_not_found(request):
	return render(request, 'blog/404.html')

def page_error(request):
	return render(request, 'blog/500.html')

def permission_denied(request):
	return render(request, 'blog/403.html')


# 编辑文章
@login_required(login_url='login')
def edit_post(request, id):
	try:
		post = get_object_or_404(Blog_Articles, id=id)
	except:
		messages.add_message(request, messages.ERROR, '文章不存在！')
	if request.user == post.author or request.user.is_superuser:
		if request.method == 'POST':
			form = ArticleForm(request.POST)
			if form.is_valid():
				post.title = request.POST['title']
				post.body = request.POST['body']
				post.save()
				messages.add_message(request, messages.SUCCESS, '修改成功！')
				return HttpResponseRedirect('/post/{}'.format(id))
			else:
				messages.add_message(request, messages.WARNING, '请检查一下各项的输入！')
				return render(request, 'blog/edit_post.html', {'form':form, 'post':post})
		else:
			form = ArticleForm()
			return render(request, 'blog/edit_post.html', {'form':form, 'post':post})
	else:
		messages.add_message(request, messages.WARNING, '暂无权限修改此文章')
		return HttpResponseRedirect('/')