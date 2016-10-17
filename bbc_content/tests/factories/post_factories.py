__author__ = 'Bertrand'
import factory

from mezzanine.blog.models import BlogPost
from bbc_user.tests.factories.user_factory import UserFactory
from datetime import datetime,timedelta
from factory.django import DjangoModelFactory

class FakeBlogPostFactory(DjangoModelFactory):
    class Meta:
        model = BlogPost

    title = factory.Faker('title')
    description = factory.Faker('description')
    status = factory.Faker('status')
    content = factory.Faker('content')
    allow_comments = factory.Faker('allow_comment')
    user = factory.SubFactory(UserFactory)

class BlogPostFactory(DjangoModelFactory):
    class Meta:
        model = BlogPost

    title = 'test title'
    description = 'test desc'
    status = 2
    content = 'lorem ipsum dolor sit amet'
    allow_comments = True

    publish_date = factory.LazyFunction(datetime.now)
    expiry_date = factory.LazyFunction(lambda : datetime.now() + timedelta(days=2))
    user = factory.SubFactory(UserFactory)


