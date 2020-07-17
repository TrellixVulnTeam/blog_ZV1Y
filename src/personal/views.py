from django.shortcuts import render
from operator import attrgetter
from blog.models import BlogPost
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from blog.views import get_blog_queryset

BLOGS_POSTS_PER_PAGE = 3
# Create your views here.
def home_screen_view(request):
    context = {}

    query = ""
    if request.GET:
        query = request.GET.get('q', '')
        context['query'] = str(query)

    blog_posts = sorted(get_blog_queryset(query), key=attrgetter('date_updated'), reverse=True) 

    page = request.GET.get('page', 1)
    blog_posts_paginator = Paginator(blog_posts, BLOGS_POSTS_PER_PAGE)
    try:
        blog_posts = blog_posts_paginator.page(page)
    except PageNotAnInteger:
        blog_posts = blog_posts_paginator(BLOGS_POSTS_PER_PAGE)

    except EmptyPage:
        blog_posts = blog_posts_paginator(blog_posts.paginator.num_pages)

    context['blog_posts'] = blog_posts
    
    return render(request, "personal/home.html", context)