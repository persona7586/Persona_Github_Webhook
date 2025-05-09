from django.shortcuts import render


"""
def 함수명(전달값):
    실행 문장
    return 반환값
"""

def landing(request):
    return render(
        request,
        'single_pages/landing.html'
    )

def about_me(request):
    return render(
        request,
        'single_pages/about_me.html'
    )
