from django.core.management.base import BaseCommand
from django.utils import timezone

from core.models import BusinessInfo
from menu.models import DailyMenu, DailyMenuItem, MenuCategory, MenuItem
from orders.models import Order
from sales.models import Sale
from tables.models import Table


class Command(BaseCommand):
    help = 'Populate database with sample data'

    def handle(self, *args, **options):
        # Clear existing data
        MenuCategory.objects.all().delete()
        MenuItem.objects.all().delete()
        DailyMenu.objects.all().delete()
        DailyMenuItem.objects.all().delete()
        Table.objects.all().delete()
        Order.objects.all().delete()
        Sale.objects.all().delete()

        # Restaurant Info
        BusinessInfo.objects.create(
            name='Mikuna Wasi',
            address='Urb. JLByR \n Cerro Colorado',
            phone='988142414',
            email='contact@gmail.com',
            opening_days='Monday - Saturday',
            opening_hours='5:30AM - 11:00AM',
            facebook_link='https://facebook.com',
            instagram_link='https://instagram.com',
            tiktok_link='https://tiktok.com',
        )

        # Categories
        categories = ['Entrees', 'Main Course', 'Desserts', 'Drinks']
        category_objs = {}

        for name in categories:
            obj = MenuCategory.objects.create(name=name)
            category_objs[name] = obj
            self.stdout.write(f'Created category: {name}')

        # Menu Items
        items = [
            ('Spring Rolls', 'Entrees', 5.99),
            ('Caesar Salad', 'Entrees', 6.49),
            ('Grilled Chicken', 'Main Course', 12.99),
            ('Pasta Alfredo', 'Main Course', 11.99),
            ('Chocolate Cake', 'Desserts', 4.99),
            ('Lemonade', 'Drinks', 2.49),
        ]
        item_objs = []

        for name, category_name, price in items:
            item = MenuItem.objects.create(
                name=name,
                category=category_objs[category_name],
                price=price,
                description=f'{name} - sample description.',
            )
            item_objs.append(item)
            self.stdout.write(f'Created menu item: {name}')

        # Daily Menu for today
        today = timezone.now().date()
        daily_menu = DailyMenu.objects.create(date=today)
        self.stdout.write(f'Created Daily Menu for {today}')

        for item in item_objs:
            DailyMenuItem.objects.create(
                daily_menu=daily_menu, menu_item=item, stock=10, is_available=True
            )
            self.stdout.write(f'Added "{item.name}" to daily menu with stock=10')

        # Create tables
        for i in range(1, 6):
            Table.objects.create(table_number=i, seats=4, status='available')
            self.stdout.write(f'Created Table {i}')

        self.stdout.write(self.style.SUCCESS('✅ Sample data populated successfully!'))
