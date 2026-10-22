# Gunicorn sozlamalari: ko'p o'quvchi bir vaqtda test ishlaganda server qotib qolmasligi uchun.
# Railway Variables orqali o'zgartirish mumkin: WEB_CONCURRENCY (jarayonlar), GUNICORN_THREADS (har biridagi oqimlar).
import os

bind = f"0.0.0.0:{os.getenv('PORT', '8000')}"

# gthread: har bir jarayon bir nechta so'rovni parallel bajaradi (bitta sekin so'rov boshqalarni to'sib qo'ymaydi).
worker_class = 'gthread'
workers = int(os.getenv('WEB_CONCURRENCY', '3'))
threads = int(os.getenv('GUNICORN_THREADS', '8'))

# Osilib qolgan so'rov butun serverni ushlab turmasin.
timeout = int(os.getenv('GUNICORN_TIMEOUT', '60'))
graceful_timeout = 30
keepalive = 5

# Xotira asta-sekin o'sib ketmasligi uchun jarayonlar vaqti-vaqti bilan yangilanadi (hammasi birdan emas).
max_requests = 2000
max_requests_jitter = 300

backlog = 2048
accesslog = None
errorlog = '-'
