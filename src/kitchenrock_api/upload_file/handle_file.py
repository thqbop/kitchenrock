from os.path import join, exists
from django.conf import settings
import os
from datetime import datetime
import random, string

def handle_upload(file_items, user_id, base_path='logo/', **kwargs):
    upload_full_path = join(settings.MEDIA_ROOT, base_path)
    saved = dict()
    if not exists(upload_full_path):
        os.makedirs(upload_full_path)

    for key, file in file_items:
        file_name = '{0}{1}_{2}'.format(id_generator(10), user_id, file.name)
        dest = open(os.path.join(upload_full_path, file_name), 'wb')
        for chunk in file.chunks():
            dest.write(chunk)
        dest.close()
        file_dir = join(base_path, file_name)
        saved.update({key: file_dir})
    return saved

def id_generator(size=6):
    return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(size))