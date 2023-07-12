import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "newspaperproject.settings")
django.setup()

from newspaperapp.models import Category, Subscriber

# Проверка наличия категорий
categories = Category.objects.all()
if categories.exists():
    print("Categories exist")
else:
    print("No categories found")

# Проверка связей подписчиков с категориями
subscribers = Subscriber.objects.all()
for subscriber in subscribers:
    subscribed_categories = subscriber.subscribed_categories.all()
    if subscribed_categories.exists():
        print(f"Subscriber {subscriber.email} has subscribed categories: {', '.join(subscribed_categories.values_list('name', flat=True))}")
    else:
        print(f"Subscriber {subscriber.email} has no subscribed categories")
