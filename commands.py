from newspaperapp.models import *

# Создать двух пользователей (с помощью метода User.objects.create_user):
user1 = User.objects.create_user(username='Pavel')
user2 = User.objects.create_user(username='Petr')

# Создать два объекта модели Author, связанные с пользователями:
author1 = Author.objects.create(authorUser=user1)
author2 = Author.objects.create(authorUser=user2)

# Добавить 4 категории в модель Category:
Category.objects.create(name='Technologies')
Category.objects.create(name='Cars')
Category.objects.create(name='Culture')
Category.objects.create(name='Science')

# Добавить 2 статьи и 1 новость:
post1 = Post.objects.create(author=author1, title='Заголовок статьи №1', text='Текст статьи №1')
post2 = Post.objects.create(author=author2, title='Заголовок статьи №2', text='Текст статьи №2')
post3 = Post.objects.create(author=author1, postType='NW', title='Заголовок новости №1', text='Текст новости №1')

# Присвоить им категории (как минимум в одной статье/новости должно быть не меньше 2 категорий):
post1.postCategory.add(Category.objects.get(name='Technologies'), Category.objects.get(name='Cars'))
post2.postCategory.add(Category.objects.get(name='Technologies'), Category.objects.get(name='Science'))
post3.postCategory.add(Category.objects.get(name='Culture'), Category.objects.get(name='Cars'))

# Создать как минимум 4 комментария к разным объектам модели Post
# (в каждом объекте должен быть как минимум один комментарий)
comment1 = Comment.objects.create(commentPost=post1, commentUser=user2, text='Текст комментария к статье №1')
comment2 = Comment.objects.create(commentPost=post2, commentUser=user1, text='Текст первого комментария к статье №2')
comment3 = Comment.objects.create(commentPost=post2, commentUser=user2, text='Текст второго комментария к статье №2')
comment4 = Comment.objects.create(commentPost=post3, commentUser=user2, text='Текст комментария к новости №1')
comment5 = Comment.objects.create(commentPost=post1, commentUser=user1, text='Текст еще одного комментария к статье №1')

# Применяя функции like() и dislike() к статьям/новостям и комментариям, скорректировать рейтинги этих объектов:
post1.like()
post1.like()
post1.like()
post1.like()
post1.like()
post1.like()
post1.dislike()

post2.like()
post2.like()
post2.like()

post3.like()
post3.like()
post3.dislike()

comment1.like()
comment2.like()
comment3.like()
comment4.like()
comment4.dislike()

# Обновить рейтинги пользователей:
Author.objects.get(authorUser=user1).update_rating()
Author.objects.get(authorUser=user2).update_rating()

# Вывести username и рейтинг лучшего пользователя (применяя сортировку и возвращая поля первого объекта):
bestAuthor = Author.objects.all().order_by('-ratingAuthor')[0]
print(f'Лучший пользователь: username - {bestAuthor.authorUser}, рейтинг - {bestAuthor.ratingAuthor}')

# Вывести дату добавления, username автора, рейтинг, заголовок и превью лучшей статьи,
# основываясь на лайках/дислайках к этой статье:
bestArPost = Post.objects.filter(postType='AR').order_by('-rating')[0]
print(f'{bestArPost.dateCreation.date()}, {bestArPost.author.authorUser}, {bestArPost.rating}, {bestArPost.title}, {bestArPost.preview()}')

# Вывести все комментарии (дата, пользователь, рейтинг, текст) к этой статье:
bestArPostComments = Comment.objects.filter(commentPost_id=bestArPost.id)
for comment in bestArPostComments:
    print(f'{comment.dateCreation.date()}, {comment.commentUser}, {comment.rating}, {comment.text}')
