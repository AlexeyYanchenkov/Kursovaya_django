from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        user_group, _ = Group.objects.get_or_create(name="User")
        manager_group, _ = Group.objects.get_or_create(name="Manager")

        # Пользователь: доступ только к своим объектам — без глобальных разрешений
        # Менеджер: доступ к просмотру моделей, без изменения
        view_client = Permission.objects.get(codename="view_client")
        view_mailing = Permission.objects.get(codename="view_mailing")

        manager_group.permissions.add(view_client, view_mailing)

        self.stdout.write("Группы и разрешения созданы.")
