from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Create initial user roles and assign permissions'

    def handle(self, *args, **kwargs):
        # Define roles and their allowed models/actions
        roles_permissions = {
            'Owner': {
                'models': [
                    'menuitem',
                    'menucategory',
                    'dailymenu',
                    'dailymenuitem',
                    'table',
                    'order',
                    'sale',
                    'expense',
                ],
                'actions': ['add', 'change', 'delete', 'view'],
            },
            'Cashier': {
                'models': ['order', 'sale'],
                'actions': ['add', 'change', 'view'],
            },
        }

        for role_name, config in roles_permissions.items():
            group, created = Group.objects.get_or_create(name=role_name)
            if created:
                self.stdout.write(f"Created group '{role_name}'")
            else:
                self.stdout.write(f"Group '{role_name}' already exists")

            for model in config['models']:
                for action in config['actions']:
                    codename = f'{action}_{model}'
                    try:
                        perm = Permission.objects.get(codename=codename)
                        group.permissions.add(perm)
                    except Permission.DoesNotExist:
                        self.stdout.write(
                            self.style.WARNING(f'Permission {codename} not found')
                        )

        # Optional: Create an example user
        User = get_user_model()
        if not User.objects.filter(username='cashier').exists():
            cashier = User.objects.create_user(
                username='cashier', password='cashier123'
            )
            cashier.groups.add(Group.objects.get(name='Cashier'))
            self.stdout.write("Created user 'cashier' with Cashier role")

        if not User.objects.filter(username='owner').exists():
            owner = User.objects.create_user(username='owner', password='owner123')
            owner.groups.add(Group.objects.get(name='Owner'))
            self.stdout.write("Created user 'owner' with Owner role")
