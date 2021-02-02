import calendar
from datetime import date, timedelta

from django.test import TestCase, Client

from users.models import User
from order.models import Post, Respond


today = date.today()
days = calendar.monthrange(today.year, today.month)[1]
next_month_date = today + timedelta(days=days)

class ProfileTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="sarah", email="connor.s@skynet.com", password="12345")
        self.user_two = User.objects.create_user(username="dj", email="dj.s@skynet.com", password="123456")
        self.client.login(username="sarah", password="12345")
        self.post = Post.objects.create(name='NAME', author=self.user, text="TEXT", price=1, expiration_date=next_month_date)

    def test_post(self):
        self.client.login(username="sarah", password="12345")

        response = self.client.get("/posts/")
        self.assertEqual(response.status_code, 200)

        response = self.client.post("/posts/", {"name": "test_name", "text": "tests_posting", "price": 1, "expiration_date": next_month_date})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Post.objects.filter(text="tests_posting", author=self.user).exists())
    
    def test_new_post_in_page(self):
        self.client.login(username="sarah", password="12345")

        response = self.client.get(f"/posts/{self.post.id}/")
        self.assertContains(response, self.post.text, status_code=200)
    
    def test_error404(self):
        response = self.client.get("/lsd/")
        self.assertEqual(response.status_code, 404)
    
    def test_post_with_file(self):
        self.client.login(username="sarah", password="12345")

        with open("./order/test_files/file.jpg", "rb") as img: 
            self.client.post("/posts/", {"name": "t_name", "text": "t_posting", "price": 1, "expiration_date": next_month_date, "file": img})
        
        response = self.client.get("/")
        self.assertContains(response, "<img", status_code=200)
 