import logging
from django.conf import settings
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.interval import IntervalTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from newspaperapp.models import Post, Subscriber
from django.template.loader import render_to_string
from django.utils import timezone
from apscheduler.triggers.cron import CronTrigger
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives, send_mail
logger = logging.getLogger(__name__)


def send_weekly_newsletter():
    subscribers = Subscriber.objects.all()

    for subscriber in subscribers:
        categories = subscriber.subscribed_categories.all()

        # Получить посты за последнюю неделю с выбранными категориями
        posts = Post.objects.filter(postCategory__in=categories, dateCreation__gte=timezone.now()-timezone.timedelta(weeks=1))

        if posts:
            subject = 'Еженедельная рассылка новостей'
            context = {
                'subscriber': subscriber,
                'categories': categories,
                'posts': posts
            }
            html_message = render_to_string('email/weekly_newsletter.html', context)
            text_message = strip_tags(html_message)
            email_message = EmailMultiAlternatives(subject, text_message, settings.DEFAULT_FROM_EMAIL, [subscriber.email])
            email_message.attach_alternative(html_message, 'text/html')
            email_message.send()
            logger.info(f"Sent weekly newsletter to {subscriber.email}")


def delete_old_job_executions(max_age=604_800):
    """This job deletes all apscheduler job executions older than `max_age` from the database."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")
        scheduler.add_job(
            send_weekly_newsletter,
            trigger=IntervalTrigger(seconds=10),
            id="send_weekly_newsletter",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'send_weekly_newsletter'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")

