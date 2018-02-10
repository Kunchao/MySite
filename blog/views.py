import math
import numpy

from django.shortcuts import render,get_object_or_404, redirect
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpRequest, Http404
from django.template import loader,Context
from django.db.models import Q,F
from django.views.generic.dates import YearArchiveView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# from django.template
from .apps import BlogConfig
from .models import Post, Tag, Category, Comment
from .forms import ContactForm
from django.core.mail import send_mail
# Create your views here.

Conf = BlogConfig.blog_settings

def get_item_in_page_or_404(the_list: list, page: str):
	try:
		page= int(page)
	except ValueError:
		raise Http404()

	if page <= 0:
		raise Http404()

	the_length= len(the_list)
	max_page_number=math.ceil(the_length / Conf['post_per_page'])

	if page>max_page_number:
		raise Http404()

	post_start=Conf['post_per_page']*(page-1)
	post_end=Conf['post_per_page']*page

	return the_list.order_by('-pub_date')[post_start:post_end],page,max_page_number

def get_next_or_404(the_list: list, post_num: str):
	try:
		post_num = int(post_num)
	except ValueError:
		raise Http404()

	if post_num<=0:
		raise Http404()

	max_num = len(the_list)
	pre_post_num = post_num-1
	next_post_num = post_num+1
	if pre_post_num > 0:
		# pre_post_slug = the_list.filter(id='pre_post_number').values('slug')[0].get('slug')
		# pre_post_num = str(pre_post_num)
		# pre_post_slug = the_list[pre_post_num].values()
		pre_post_slug = the_list[pre_post_num-1]['slug']
	else:
		pre_post_slug = None

	if next_post_num <= max_num:
		# next_post_slug = the_list.filter(id='next_post_number').values('slug')[0].get('slug')
		# next_post_num = str(next_post_num)
		# next_post_slug = the_list[next_post_num].values('slug')
		next_post_slug = the_list[next_post_num-1]['slug']
	else:
		next_post_slug = None
	

	return pre_post_slug,next_post_slug

# def get_len_in_each_item(the_list: list, )

def filter_post_list_by_user(the_list, user):
	if user.is_authenticated():
		if user.is_superuser:
			return the_list
		elif user.author:
			return the_list.exclude(Q(isDraft=True),~Q(author=user.author))
		else:
			return the_list.exclude(isDraft=True)
	else:
		return the_list.exclude(isDraft=True)

def has_permission_acess_not(user, the_post):
	if not the_post.isDraft:
		return True
	if user.is_authenticated():
		if user.is_superuser:
			return True
	if user in the_post.author:
				return True
	return False

# def post(request):
# def post(req: HttpRequest, slug: str) -> HttpResponse:
# 	the_post = get_object_or_404(Post, slug=slug)
# 	return render(req,'blog/base_site.html',{'post':'the_post',})
# def index(req:HttpRequest, page: str = '1'):
# 	post_list = filter_post_list_by_user(Post.objects.all(), req.user)
# 	post_list, page, max_page =get_item_in_page_or_404(post_list, page)
# 	# the_post = get_object_or_404(Post, slug=slug)
# 	# tags = the_post.tags.objects.all()
# 	form,result = contact(req)
# 	return render(req, 'blog/index.html',{
# 		'page':page,
# 		'max_page':max_page,
# 		'posts':post_list,
# 		'form':ContactForm(),
# 		'result':result,
# 		})
def contact(form):
	if form.is_valid():
			subject = form.cleaned_data['subject']
			message = form.cleaned_data['message']
			name = form.cleaned_data['name']
			sender = form.cleaned_data['sender']
			cc_myself = form.cleaned_data['cc_myself']

			recipients = ['739136321@qq.com']
			# if cc_myself:
			# 	recipients.append(sender)

			send_mail( message, name, sender, recipients,subject,)
			result ='makeit'

			return result


def index(req:HttpRequest, page: str='1'):
	post_list = filter_post_list_by_user(Post.objects.all(), req.user)
	post_list, page, max_page =get_item_in_page_or_404(post_list, page)
	result='send'
	if req.method == 'POST':
		form = ContactForm(req.POST)
		result = contact(form)

		return render(req, 'blog/index.html',{
						'page':page,
						'max_page':max_page,
						'posts':post_list,
						'form':form,
						'result':result,
				})
	else:
		form=ContactForm()

	
	return render(req, 'blog/index.html',{
						'page':page,
						'max_page':max_page,
						'posts':post_list,
						'form':form,
						'result':result,
				})

def post(req: HttpRequest,slug: str):
	post_list = Post.objects.all()
	post_list = list(post_list.order_by('-pub_date'))
	# the_post = post_list.filter(slug=slug)
	the_post = get_object_or_404(Post, slug=slug)
	post_num = post_list.index(the_post)+1
	post_list = list(Post.objects.all().values())
	pre_post_slug,next_post_slug = get_next_or_404(post_list,post_num)
	# the_post = get_object_or_404(Post, slug=slug)
	user = req.user

	if has_permission_acess_not(user, the_post):
		the_post.view_times = F('view_times')+1
		the_post.save()
		the_post.refresh_from_db()

	result='send'
	if req.method == 'POST':
		form = ContactForm(req.POST)
		result = contact(form)
		
		return render(req,'blog/post.html',{
		'post':the_post,
		'pre_post_slug':pre_post_slug,
		'next_post_slug':next_post_slug,
		'post_num':post_num,
		'form':form,
		'result':result,
		 })
	else:
		form=ContactForm()

	return render(req,'blog/post.html',{
		'post':the_post,
		'pre_post_slug':pre_post_slug,
		'next_post_slug':next_post_slug,
		'post_num':post_num,
		'form':form,
		'result':result,
		 })

	# posts = Post.objects.all()
	# t = loader.get_template("blog/base_site.html")
	# c = Context({'posts':posts,})
	# return HttpResponse(t.render(c))
def tag_index(req: HttpRequest):
	tags = Tag.objects.all()
	tags_num = len(tags)

	result='send'
	if req.method == 'POST':
		form = ContactForm(req.POST)
		result = contact(form)

		return render(req, 'blog/tag_index.html', {
				'tags':tags,
				'tags_num':tags_num,
				'form':form,
				'result':result,
			})
	else:
		form=ContactForm()

	return render(req, 'blog/tag_index.html', {
				'tags':tags,
				'tags_num':tags_num,
				'form':form,
				'result':result,
			})



def tag(req: HttpRequest, slug: str, page: str='1' )-> HttpResponse:
	the_tag = get_object_or_404(Tag, slug=slug)


	post_list = Post.objects.filter(tags__slug__contains=slug)
	post_list, page, max_page = get_item_in_page_or_404(post_list, page)

	tags = Tag.objects.all()
	tags_num = len(tags)

	# post_tags =  Tag.objects.filter(Post__tags__slug__contains=slug)
	result='send'
	if req.method == 'POST':
		form = ContactForm(req.POST)
		result = contact(form)

		return render(req, 'blog/tag.html', {
			'tags':tags,
			'tag':the_tag,
			'tags_num':tags_num,
			'posts':post_list,
			'page':page,
			'max_page':max_page,
			'form':form,
			'result':result,
			})
	else:
		form=ContactForm()

	return render(req, 'blog/tag.html', {
			'tags':tags,
			'tag':the_tag,
			'tags_num':tags_num,
			'posts':post_list,
			'page':page,
			'max_page':max_page,
			'form':form,
			'result':result,
			})


def category(req : HttpResponse, slug : str, page: str='1')-> HttpResponse:
	the_category = get_object_or_404(Category, slug=slug)

	post_list = filter_post_list_by_user(
		Post.objects.filter(category__slug=slug), req.user)
	post_list, page, max_page = get_item_in_page_or_404(post_list, page)

	tags = Tag.objects.all()
	tags_num = len(tags)

	result='send'
	if req.method == 'POST':
		form = ContactForm(req.POST)
		result = contact(form)

		return render(req, 'blog/category.html', {
			'category': the_category,
			'posts': post_list,
			'page': page,
			'max_page': max_page,
			'tags': Tag.objects.all(),
			'form':form,
			'result':result,
			})
	else:
		form=ContactForm()

	return render(req, 'blog/category.html', {
			'category': the_category,
			'posts': post_list,
			'page': page,
			'max_page': max_page,
			'tags': Tag.objects.all(),
			'form':form,
			'result':result,
			})


def category_index(req: HttpResponse)-> HttpResponse:
	post_list = Post.objects.all()
	categorys = list(Category.objects.all().values())
	cate_num = len(categorys)
	category_len_list = []
	
	for i in range(1,cate_num+1):
		category_len = {}
		category_len['len']=len(post_list.filter(category_id=i))
		category_len['name'] = categorys[i-1]['name']
		category_len_list.append(category_len)
		

	result='send'
	if req.method == 'POST':
		form = ContactForm(req.POST)
		result = contact(form)

		return render(req, 'blog/category_index.html', {
				'categorys':Category.objects.all(),
				'cate_num':cate_num,
				'category_len_list':category_len_list,
				'form':form,
				'result':result,
			})
	else:
		form=ContactForm()
		return render(req, 'blog/category_index.html', {
				'categorys':Category.objects.all(),
				'cate_num':cate_num,
				'category_len_list':category_len_list,
				'form':form,
				'result':result,
			})

class ArticleYearArchiveView(YearArchiveView):
	post_list =Post.objects.all()
	date_field = "pub_date"
	make_object_list = True
	allow_future = True

	model = Post
	template_name = 'blog/archives.html'


def about(req:HttpRequest):
	result='send'
	if req.method == 'POST':
		form = ContactForm(req.POST)
		result = contact(form)
		return render(req, 'blog/about.html',{
				'form':form,
				'result':result,
			})
	else:
		form=ContactForm()
	return render(req, 'blog/about.html',{
				'form':form,
				'result':result,})