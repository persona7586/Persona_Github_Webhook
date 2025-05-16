from django.test import TestCase, Client
from bs4 import BeautifulSoup
from .models import Post

class TestView(TestCase):
    def setUp(self):
        self.client = Client()

        def test_post_list(self):
            # 1-1 포스트 목록 페이지 가져오기
            response = self.client.get('/blog/')
            # 1-2 정상적인 페이지 로드
            self.assertEqual(response.status_code, 200)
            # 1-3 페이지 타이틀 Blog
            soup = BeautifulSoup(response.content, 'html.parser')
            self.assertEqual(soup.title.text, 'Blog')
            # 1-4 Navigation bar 확인
            navbar = soup.nav
            # 1-5 Navigation bar에 Blog, About Me 문구 존재
            self.assertIn('Blog', navbar.text)
            self.assertIn('About Me', navbar.text)

            # 2-1 포스트(게시물)가 하나도 없을 경우
            self.assertEqual(Post.objects.count(), 0)
            # 2-2 main area에 '아직 게시물이 없습니다' 문구 적용
            main_area = soup.find('div', id='main-area')
            self.assertIn('아직 게시물이 없습니다', main_area.text)

            # 3-1 포스트 2개
            post_001 = Post.objects.create(
                title='첫 번째 포스트입니다.',
                content='Hello World.',
            )
            post_002 = Post.objects.create(
                title='두 번째 포스트입니다.',
                content='We are the world.',
            )
            self.assertEqual(Post.objects.count(), 2)

            # 3-2 포스트 목록 페이지 새로고침
            response = self.client.get('/blog/')
            soup = BeautifulSoup(response.content, 'html.parser')
            self.assertEqual(response.status_code, 200)

            # 3-3 main area에 포스트 2개의 제목 존재
            main_area = soup.find('div', id='main-area')
            self.assertIn(post_001.title, main_area.text)
            self.assertIn(post_002.title, main_area.text)

            # 3-4 '아직 게시물이 없습니다' 문구 더 이상 나타나지 않는거 확인
            self.assertNotIn('아직 게시물이 없습니다', main_area.text)

        def test_post_detail(self):
            # 1-1 Post 하나
            post_001 = Post.objects.create(
                title='첫 번째 포스트입니다.',
                content='Hello World.',
            )
            # 1-2 Post url = '/blog/1/'
            self.assertEqual(post_001.get_absolute_url(), '/blog/1/')

            # 2-0 첫 번째 포스트의 상세 페이지 테스트
            # 2-1 첫 번째 포스트의 url 접근 정상 작동(status code: 200).
            respons = self.client.get(post_001.get_absolute_url())
            self.assertEqual(respons.status_code, 200)
            soup = BeautifulSoup(respons.content, 'html.parser')

            # 2-2 포스트 목록 페이지와 똑같은 Navigation bar
            navbar = soup.nav
            self.assertIn('Blog', navbar.text)
            slef.assertIn('About Me', navbar.text)

            # 2-3 첫 번째 포스트의 제목 웹 브라우저 탭 타이틀에 존재
            self.assertIn(post_001.title, soup.title.text)

            # 2-4 첫 번째 포스트의 제목 포스트 영역 존재
            main_area = soup.find('div', id='main-area')
            post_area = main_area.find('div', id='post-area')
            self.assertIn(post_001.title, post_area.text)

            # 2-5 첫 번째 포스트의 author 포스트 영역 존재

            # 2-6 첫 번째 포스트의 content 포스트 영역 존재
            self.assertIn(post_001.content, post_area.text)