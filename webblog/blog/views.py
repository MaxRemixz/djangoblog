from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import get_object_or_404

from .forms import ArticleForm, RegisterForm, LoginForm, EditUserForm, CommentForm
from .models import User, Blog_Articles, FriendShip, Comment


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
	show_followed = False
	if request.user.is_authenticated:
		show_followed = bool(request.COOKIES.get('show_followed', ''))
	if show_followed:
		posts = request.user.followed_posts.order_by('-create_time')
	else:
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
	return render(request, 'blog/index.html', {'form': form, 'contacts': contacts, 'show_followed': show_followed})


# 个人资料页面
@login_required(login_url='login')
def user(request, username):
	user_datas = User.objects.get(username=username)
	posts = Blog_Articles.objects.filter(author=user_datas)
	return render(request, 'blog/user.html', {'user_datas': user_datas,'posts':posts})


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
	user_datas = User.objects.get(username=username)
	if request.method == 'POST':
		if request.user == user_datas.username or request.user.is_superuser:
			form = EditUserForm(request.POST)
			if form.is_valid():
				user_datas.email = request.POST['email']
				user_datas.adder = request.POST['adder']
				user_datas.phone = request.POST['phone']
				user_datas.birthday = request.POST['birthday']
				user_datas.gender = request.POST['gender']
				user_datas.save()
				messages.add_message(request, messages.SUCCESS, '修改成功！')
				return HttpResponseRedirect('/user/{}/'.format(user_datas.username))
			else:
				messages.add_message(request, messages.WARNING, '请检查一下各项的输入！')
				return render(request, 'blog/edit.html', {'form':form})
		else:
			messages.add_message(request, messages.WARNING, '暂无权限修改此文章')
			return HttpResponseRedirect('/')
	else:
		form = EditUserForm()
		return render(request, 'blog/edit.html', {'form':form, 'user_datas':user_datas})


# 单文章页面
@login_required(login_url='login')
def post(request, id):
	try:
		post = get_object_or_404(Blog_Articles, id=id)
	except:
		messages.add_message(request, messages.ERROR, '文章不存在！')
		# raise Http404 等完善了404页面再用这个页面
		return HttpResponseRedirect('/')
	form = CommentForm()
	if request.method == 'POST':
		form = CommentForm(request.POST)
		if form.is_valid():
			comment = Comment(body=request.POST['body'], author=request.user, post=post)
			comment.save()
			messages.add_message(request, messages.SUCCESS, '评论提交成功')
			return HttpResponseRedirect('/post/{}'.format(id))
		else:
			messages.add_message(request, messages.ERROR, '评论内容不能为空')
			return HttpResponseRedirect('/post/{}'.format(id))
	else:
		comments = Comment.objects.filter(post=post).order_by('-create_time')
		return render(request, 'blog/post.html', {'post': post, 'form': form, 'comments': comments})


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


# 点击关注之后的视图函数
@login_required(login_url='login')
def follow(request, username):
	try:
		user = User.objects.get(username=username)
	except:
		messages.add_message(request, messages.ERROR, '错误的用户')
		return HttpResponseRedirect('/')
	if request.user.is_following(user):
		messages.add_message(request, messages.WARNING, '您已经关注过此用户')
		return HttpResponseRedirect('/user/{}'.format(user.username))
	request.user.follow(user)
	messages.add_message(request, messages.SUCCESS, '您已经成功关注了用户{}'.format(user.username))
	return HttpResponseRedirect('/user/{}'.format(user.username))


# 点击取消关注的试图函数
@login_required(login_url='login')
def unfollow(request, username):
	try:
		user = User.objects.get(username=username)
	except:
		messages.add_message(request, messages.ERROR, '您所查看的用户不存在')
		return HttpResponseRedirect('/')
	if not request.user.is_following(user):
		messages.add_message(request, messages.WARNING, '取消无效。您并没有关注此用户')
		return HttpResponseRedirect('/user/{}'.format(user.username))
	request.user.unfollow(user)
	messages.add_message(request, messages.WARNING, '您已经取消关注了用户{}'.format(user.username))
	return HttpResponseRedirect('/user/{}'.format(user.username))


# 查看用户关注者的视图
def followers(request, username):
	try:
		user = User.objects.get(username=username)
	except:
		messages.add_message(request, messages.ERROR, '您所查看的用户不存在')
		return HttpResponseRedirect('/')
	followers = FriendShip.objects.filter(follower=user).order_by('-create_time')
	return render(request, 'blog/followers.html', {'followers': followers, 'user_fol': user})


# 查看用户粉丝的视图
def followed(request, username):
	try:
		user = User.objects.get(username=username)
	except:
		messages.add_message(request, messages.ERROR, '您所查看的用户不存在')
		return HttpResponseRedirect('/')
	followed  = FriendShip.objects.filter(followed=user).order_by('-create_time')
	return render(request, 'blog/followed.html', {'followed': followed, 'user_fol': user})


# 查看首页所有的文章
@login_required(login_url='login')
def show_all(request):
	resp = HttpResponseRedirect('/')
	resp.set_cookie('show_followed', '', max_age=30*24*60*60)
	return resp


# 查看所关注的文章
@login_required(login_url='login')
def show_followed(request):
	resp = HttpResponseRedirect('/')
	resp.set_cookie('show_followed', '1', max_age=30*24*60*60)
	return resp


# 管理评论是否显示
@login_required(login_url='login')
def moderate(request):
	comments = Comment.objects.all().order_by('-create_time')
	paginator = Paginator(comments, 20)
	page = request.GET.get('page')
	try:
		contacts = paginator.page(page)
	except PageNotAnInteger:  # 如果page不是有一个有效的数字。则跳转到第一页
		contacts = paginator.page(1)
	except EmptyPage:		# 如果page超过了最大或者最小范围。则跳转到最后一页
		contacts = paginator.page(paginator.num_pages)
	return render(request, 'blog/moderate.html', {'contacts': contacts})


# 让评论显示
@login_required(login_url='login')
def moderate_enable(request, id):
	comment = get_object_or_404(Comment, id=id)
	comment.disabled = False
	comment.save()
	return HttpResponseRedirect('/moderate')


# 让评论隐藏
@login_required(login_url='login')
def moderate_disable(request, id):
	comment = get_object_or_404(Comment, id=id)
	comment.disabled = True
	comment.save()
	return HttpResponseRedirect('/moderate')
