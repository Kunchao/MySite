from django.apps import AppConfig


class BlogConfig(AppConfig):
    name = 'blog'
    verbose_name = 'Blog'

    #Blog settings
    blog_settings = {
    	'name': 'Vapor',
    	'owner_name': 'Vapor',
    	'owner_sign': 'Thoughts, stories and ideas.',
    	'post_per_page': 5,
    	'self_infos': [
    		{'name': 'Github', 'url':'https://github.com/Kunchao'},
    		{'name': 'Zhihu', 'url': 'https://www.zhihu.com/people/jin-ke-92-35/activities'},
    		{'name': 'Weibo', 'url': 'http://weibo.com/u/5347681032/home?wvr=5'},
    		{'name': 'Email', 'url': '#'},
    	],
    }
