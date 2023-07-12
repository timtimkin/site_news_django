from django.db import models
from django.utils.text import slugify
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.conf import settings
import logging
from django.contrib.auth.models import User
from django.db.models import Q
from .signals import notify_subscribers

# Создание объекта логгера
logger = logging.getLogger(__name__)
# Установка уровня логирования
logger.setLevel(logging.DEBUG)
# Создание обработчика для записи в файл
file_handler = logging.FileHandler('debug.log')
# Установка уровня логирования для обработчика
file_handler.setLevel(logging.DEBUG)
# Создание форматтера лога
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
# Установка форматтера для обработчика
file_handler.setFormatter(formatter)
# Добавление обработчика в логгер
logger.addHandler(file_handler)


class Author(models.Model):
    authorUser = models.OneToOneField("auth.User", on_delete=models.CASCADE, verbose_name='имя', related_name='author_profile')
    ratingAuthor = models.SmallIntegerField(default=0)

    def update_rating(self):
        postRat = self.post_set.all().aggregate(postRating=models.Sum('rating'))
        pRat = postRat.get('postRating') or 0

        commentRat = self.authorUser.comment_set.all().aggregate(commentRating=models.Sum('rating'))
        cRat = commentRat.get('commentRating') or 0

        self.ratingAuthor = pRat * 3 + cRat
        self.save()


class Category(models.Model):
    name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.name


class Subscriber(models.Model):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    subscribed_categories = models.ManyToManyField(Category, blank=True, related_name='subscribers')

    def __str__(self):
        return self.email

    def get_subscribed_categories(self):
        return self.subscribed_categories.values_list('name', flat=True)


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE, verbose_name='Автор')
    NEWS = 'NW'
    ARTICLE = 'AR'
    POST_CHOICES = (
        (NEWS, 'Новость'),
        (ARTICLE, 'Статья'),
    )
    postType = models.CharField(max_length=2, choices=POST_CHOICES, default=ARTICLE, verbose_name='Тип')
    dateCreation = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    title = models.CharField(max_length=128, verbose_name='Заголовок')
    text = models.TextField(default='Здесь будет текст статьи(новости)...', verbose_name='Текст')
    rating = models.SmallIntegerField(default=0)
    is_new = models.BooleanField(default=True)
    slug = models.SlugField(default='default-slug')
    postCategory = models.ManyToManyField(Category, through='PostCategory', verbose_name='Категория',
                                          related_name='posts')

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return self.text[0:123] + '...'

    def get_absolute_url(self):
        return str(self.id)

    def save(self, *args, **kwargs):
        # logger.debug("Post create")
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
        self.send_new_post_notification()

    def send_new_post_notification(self):
        author_user = self.author.authorUser
        author_profile = getattr(author_user, 'author_profile', None)
        if author_profile is None:
            return
        logger.debug('Checking subscribers')
        try:
            subscriber = Subscriber.objects.get(user=author_user)
            subscriber_categories = subscriber.subscribed_categories.all()
            logger.debug('Found a subscriber of the right category')
        except Subscriber.DoesNotExist:
            subscriber_categories = Category.objects.none()
            logger.debug('There are no subscribers to this category')

        category_ids = subscriber_categories.values_list('id', flat=True)

        post_categories = PostCategory.objects.filter(post=self)
        categories = Category.objects.filter(postcategory__in=post_categories)
        if categories.exists():
            logger.debug('Categories exist')
        else:
            logger.debug('No categories found')

        subscribers = Subscriber.objects.filter(
            Q(subscribed_categories__in=post_categories.values('category')) |
            Q(user=author_user)
        ).distinct()

        if subscribers.exists():
            subject = 'Опубликован новый пост'
            context = {'post': self}
            message = render_to_string('email/new_post_notification.html', context)
            recipient_emails = subscribers.values_list('email', flat=True)

            logger.debug('Sending new post notification to subscribers')

            try:
                send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_emails, html_message=message)

                logger.debug('New post notification sent successfully')
            except Exception as e:
                logger.exception('Failed to send new post notification: %s', str(e))

        logger.debug('Finished send_new_post_notification')


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    commentPost = models.ForeignKey(Post, on_delete=models.CASCADE)
    commentUser = models.ForeignKey("auth.User", on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    dateCreation = models.DateTimeField(auto_now_add=True)
    rating = models.SmallIntegerField(default=0)

    def __str__(self):
        return self.commentUser.username

    def like(self):
        pass




