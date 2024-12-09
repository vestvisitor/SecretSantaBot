from celery import Celery

app = Celery('src',
             broker='redis://',
             backend='db+sqlite:///src/celery_backend.db',
             include=['src.utils']
             )

app.conf.update(
    result_expires=3600,
)
