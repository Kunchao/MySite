from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib import admin



TAG_MAX_LENGTH=20
CATEGORY_MAX_LENGTH=40
TITLE_MAX_LENGTH=50
NICKNAME_MAX_LENGTH=40

CN_TO_EN_RADIO=2
# Create your models here.
class Tag(models.Model):
	name = models.CharField(max_length=TAG_MAX_LENGTH)
	slug = models.SlugField(max_length=TAG_MAX_LENGTH*CN_TO_EN_RADIO)

	def __str__(self):
		return self.name

class Category(models.Model):
	name = models.CharField(max_length=CATEGORY_MAX_LENGTH)
	slug = models.SlugField(max_length=CATEGORY_MAX_LENGTH*CN_TO_EN_RADIO)

	def __str__(self):
		return self.name

class Author(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	nickname = models.CharField(max_length=NICKNAME_MAX_LENGTH)
	sign = models.TextField()

	def __str__(self):
		return "{self.nickname}({self.id})".format(self=self)


class Post(models.Model):
	title = models.CharField(max_length=TITLE_MAX_LENGTH)
	slug = models.SlugField(max_length=TITLE_MAX_LENGTH*CN_TO_EN_RADIO)
	author = models.ForeignKey(Author, on_delete=models.CASCADE)
	content = models.TextField()
	tags = models.ManyToManyField(Tag, blank=True)
	category = models.ForeignKey(Category, on_delete=models.CASCADE)
	pub_date = models.DateTimeField('publish date',auto_now_add=True)
	last_mod = models.DateTimeField('last modify date', auto_now=True)
	isDraft = models.BooleanField(default=False)

	view_times = models.IntegerField(default=0)
	share_time = models.IntegerField(default=0)

	def __str__(self):
		return "{self.title} - {self.author.nickname}".format(self=self)


class Comment(models.Model):
	nickname = models.CharField(max_length=NICKNAME_MAX_LENGTH)
	email = models.EmailField()
	content = models.TextField()
	post = models.ForeignKey(Post, on_delete=models.CASCADE)
	parent = models.ForeignKey('self',on_delete=models.SET_NULL,
								null=True, default=None,blank=True)
	user = models.ForeignKey(Author, on_delete=models.SET_NULL,
								null=True,default=None, blank=True)
	time = models.DateTimeField(default=timezone.now)
	floor = models.IntegerField(default=0)

	def __str__(self):
		return "{self.nickname}: {self.content}".format(self=self)

class GithubHookSecret(models.Model):
	secret = models.CharField(max_length=255)



# admin.site.register(Post)