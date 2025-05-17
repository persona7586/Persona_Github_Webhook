from django.test import TestCase, Client
from bs4 import BeautifulSoup
from django.contrib.auth.models import User
from .models import Post, Category

class TestView(TestCase):
    def setUp(self):
        self.client = Client()

        self.user_taemun1 = User.objects.create_user(username='taemun1', password='somepassword')
        self.user_taemun2 = User.objects.create_user(username='taemun2', password='somepassword')

        self.category_programming = Category.objects.create(name='programming', slug='programming')
        self.category_music = Category.objects.create(name='music', slug='music')

        self.post_001 = Post.objects.create(
            title='첫 번째 포스트입니다.',
            content='Hello World.',
            category=self.category_programming,
            author=self.user_taemun1,
        )

        self.post_002 = Post.objects.create(
            title='두 번째 포스트입니다.',
            content='We are the world.',
            category=self.category_music,
            author=self.user_taemun2,
        )

        self.post_003 = Post.objects.create(
            title='세 번째 포스트입니다.',
            content='category'
            author=self.user_taemun2,
        )

    def navbar_test(self, soup):
        navbar = soup.nav
        self.assertIn('Blog', navbar.text)
        self.assertIn('About Me', navbar.text)

        logo_btn = navbar.find('a', text='My Home') #navbar.html <a class="navbar-brand" href="/">My Home</a>
        self.assertEqual(logo_btn.attrs['href'],'/')

        home_btn = navbar.find('a', text='Home')
        self.assertEqual(home_btn.attrs['href'],'/')

        blog_btn = navbar.find('a', text='Blog')
        self.assertEqual(blog_btn.attrs['href'],'/blog/')

        about_me_btn = navbar.find('a', text='About Me')
        self.assertEqual(about_me_btn.attrs['href'],'/about_me/')

    def category_card_test(self, soup):
        categories_card = soup.find('div', id='categories_card')
        self.assertIn('Categories', categories_card.text)
        self.assertIn(f'{self.category_programming.name} ({self.category_programming.post_set.count()})', categories_card.text)
        self.assertIn(f'{self.category_music.name} ({self.category_music.post_set.count()})', categories_card.text)
        self.assertIn(f'미분류 (1)', categories_card.text)

    def test_post_list(self):
        # Post가 있는 경우
        self.assertEqual(Post.objects.count(), 3)

        response = self.client.get('/blog/')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')

        self.assertEqual(soup.title.text, 'Blog')

        self.navbar_test(soup)
        self.category_card_test(soup)

        main_area = soup.find('div', id='main-area')
        self.assertNotIn('아직 게시물이 없습니다', main_area.text)

        post_001_card = main_area.find('div', id='post-1')
        self.assertIn(self.post_001.title, post_001_card.text)
        self.assertIn(self.post_001.category.name, post_001_card.text)
        self.assertIn(self.post_001.author.username.upper(), post_001_card.text)
        self.assertIn(self.tag_hello.name, post_001_card.text)
        self.assertNotIn(self.tag_python.name, post_001_card.text)
        self.assertNotIn(self.tag_python_kor.name, post_001_card.text)

        post_002_card = main_area.find('div', id='post-2')
        self.assertIn(self.post_002.title, post_002_card.text)
        self.assertIn(self.post_002.category.name, post_002_card.text)
        self.assertIn(self.post_002.author.username.upper(), post_002_card.text)
        self.assertNotIn(self.tag_hello.name, post_002_card.text)
        self.assertNotIn(self.tag_python.name, post_002_card.text)
        self.assertNotIn(self.tag_python_kor.name, post_002_card.text)

        post_003_card = main_area.find('div', id='post-3')
        self.assertIn('미분류', post_003_card.text)
        self.assertIn(self.post_003.title, post_003_card.text)
        self.assertIn(self.post_003.author.username.upper(), post_003_card.text)
        self.assertNotIn(self.tag_hello.name, post_003_card.text)
        self.assertIn(self.tag_python.name, post_003_card.text)
        self.assertIn(self.tag_python_kor.name, post_003_card.text)

        # Post가 없는 경우
        Post.objects.all().delete()
        self.assertEqual(Post.objects.count(), 0)
        response = self.client.get('/blog/')
        soup = BeautifulSoup(response.content, 'html.parser')
        main_area = soup.find('div', id='main-area')
        self.assertIn('아직 게시물이 없습니다', main_area.text)

    def test_post_detail(self):
        # 1-1 Post 하나
        '''
        post_001 = Post.objects.create(
            title='첫 번째 포스트입니다.',
            content='Hello World.',
            author=self.user_taemun1,
        )
        '''
        # 1-2 Post url = '/blog/1/'
        self.assertEqual(self.post_001.get_absolute_url(), '/blog/1/')

        # 2-0 첫 번째 포스트의 상세 페이지 테스트
        # 2-1 첫 번째 포스트의 url 접근 정상 작동(status code: 200).
        respons = self.client.get(self.post_001.get_absolute_url())
        self.assertEqual(respons.status_code, 200)
        soup = BeautifulSoup(respons.content, 'html.parser')

        # 2-2 포스트 목록 페이지와 똑같은 Navigation bar
        #navbar = soup.nav
        #self.assertIn('Blog', navbar.text)
        #slef.assertIn('About Me', navbar.text)
        self.navbar_test(soup)
        self.category_card_test(soup)

        # 2-3 첫 번째 포스트의 제목 웹 브라우저 탭 타이틀에 존재
        self.assertIn(self.post_001.title, soup.title.text)

        # 2-4 첫 번째 포스트의 제목 포스트 영역 존재
        main_area = soup.find('div', id='main-area')
        post_area = main_area.find('div', id='post-area')
        self.assertIn(self.post_001.title, post_area.text)
        self.assertIn(self.category_programming.name, post_area.text)

        # 2-5 첫 번째 포스트의 author 포스트 영역 존재
        self.assertIn(self.user_taemun1.username.upper(), post_area.text)
        self.assertIn(self.post_001.content, post_area.text)

        # 2-6 첫 번째 포스트의 content 포스트 영역 존재
        self.assertIn(post_001.content, post_area.text)