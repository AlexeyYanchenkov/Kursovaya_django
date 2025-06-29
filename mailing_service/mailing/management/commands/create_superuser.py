from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):
    help = 'Создаёт суперпользователя с заданным email и паролем'

    def add_arguments(self, parser):
        parser.add_argument('--email', type=str, required=True, help='Email суперпользователя')
        parser.add_argument('--password', type=str, required=True, help='Пароль суперпользователя')

    def handle(self, *args, **options):
        email = options['email']
        password = options['password']

        if User.objects.filter(email=email).exists():
            self.stdout.write(self.style.WARNING(f'Пользователь с email {email} уже существует.'))
            return

        user = User.objects.create_superuser(email=email, password=password)
        self.stdout.write(self.style.SUCCESS(f'Суперпользователь {email} создан успешно.'))
