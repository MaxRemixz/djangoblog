# -*- coding: utf-8 -*-
from random import randint
from django.db import IntegrityError
from faker import Faker
from .models import User, Blog_Articles
from django.db import IntegrityError, transaction

#用于生成测试用户
@transaction.atomic
def users(count=100):
	fake = Faker(locale='zh_CN')
	i = 0
	while i < count:
		u = User.objects.create_user(fake.user_name(), fake.email(), 'password')
		u.adder = fake.address() 
		u.phone = fake.phone_number()
		u.birthday = fake.date_object()
		try:
			u.save()
			i += 1
		except IntegrityError:
			handle_exception()

#用于生成测试文章
def posts(count=100):
	fake = Faker()
	user_count = User.objects.count()

	for i in range(count):
		u = User.objects.all()[randint(0, user_count-1)]
		p = Blog_Articles(title=fake.sentence(),
			body=fake.text(),
			author=u)
		p.save()
