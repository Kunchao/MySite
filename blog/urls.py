from django.conf.urls import url
from . import views
from blog.views import ArticleYearArchiveView

app_name='blog'

urlpatterns = [
	url(r'^(?:index/)?$', views.index, name='index'),
	url(r'^contact/$', views.contact, name='contact'),
	url(r'^index/(?P<page>\d+)/$', views.index, name='index-with-page'),
	# url(r'^index/(?P<page>\d+)/$', views.index, name='index-with-page'),

	url(r'^post/(?P<slug>[\w-]+)/$', views.post, name='post'),

	url(r'^tag/$',views.tag_index, name = 'tag'),
	url(r'^tag/(?P<slug>[\w-]+)/(?P<page>\d+)/$', views.tag, name = 'tag-with-page'),

	url(r'^category/$',views.category_index, name='category' ),
	url(r'^category/(?P<slug>[\w-]+)/(?P<page>\d+)/$',views.category, name='category-with-page' ),
	
	url(r'^archives/(?P<year>[0-9]{4})/$', ArticleYearArchiveView.as_view(), name='archive_year_archive'),
	url(r'^about/$', views.about, name='about')
	]

