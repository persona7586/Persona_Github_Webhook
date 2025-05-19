from django.shortcuts import render
from blog.models import Post


"""
def 함수명(전달값):
    실행 문장
    return 반환값
"""

def landing(request):
    recent_posts = Post.objects.order_by('-pk')[:3]

    return render(
        request,
        'single_pages/landing.html',
        {
            'recent_posts': recent_posts,
        }
    )


def about_me(request):
    return render(
        request,
        'single_pages/about_me.html'
    )
