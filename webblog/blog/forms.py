from django import forms


class ArticleForm(forms.Form):
    title = forms.CharField(max_length=80, required=True, label='标题')
    body = forms.Textarea()


gender_choices = (
        (1, '男'),
        (2, '女'),
    )


class RegisterForm(forms.Form):
    username = forms.CharField(max_length=50, required=True)
    password = forms.CharField(max_length=50, required=True)
    email = forms.EmailField()
    adder = forms.CharField(max_length=50)
    phone = forms.CharField(max_length=11)
    birthday = forms.DateField()
    gender = forms.ChoiceField(widget=forms.RadioSelect, choices=gender_choices, label="性别")


# 登录表单
class LoginForm(forms.Form):
    username = forms.CharField(max_length=50, required=True)
    password = forms.CharField(max_length=50, required=True)


# 编辑资料表单
class EditUserForm(forms.Form):
    email = forms.EmailField()
    adder = forms.CharField(max_length=50)
    phone = forms.CharField(max_length=11)
    birthday = forms.DateField()
    gender = forms.ChoiceField(widget=forms.RadioSelect, choices=gender_choices, label="性别")


# 评论输入表单
class CommentForm(forms.Form):
    body = forms.CharField(max_length=500, required=True)
