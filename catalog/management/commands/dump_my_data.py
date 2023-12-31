import codecs
import os

from django.core.management import BaseCommand, call_command

from config import settings


class Command(BaseCommand):
    help = 'Добавляет данные с БД в фикстуру'

    def handle(self, *args, **kwargs):
        installed_apps = settings.INSTALLED_APPS
        for app in installed_apps:
            if '.apps.' in app:
                app_name = app.split('.', 1)[0]

                path_to_folder = os.path.join(settings.BASE_DIR, app_name, 'fixtures')
                if not os.path.exists(path_to_folder):
                    os.mkdir(path_to_folder)

                path_to_fixtures = os.path.join(path_to_folder, f'{app_name}_data.json')
                with codecs.open(path_to_fixtures, 'w', encoding='utf-8') as file:
                    call_command('dumpdata', app_name, indent=4, stdout=file)
