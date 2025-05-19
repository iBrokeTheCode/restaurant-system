# Restaurant Management System

## Overview

This project is a Restaurant Management System developed to streamline daily operations. It offers a comprehensive suite of features for efficient menu management, order processing (dine-in and takeaway), automated sales tracking and invoicing, detailed expenditure recording, and insightful business reporting. The system also includes functionalities for managing restaurant tables and controlling staff access through user roles.

## Key Features

- **Menu Management:** Easily manage your restaurant's menu, including dish details, categories, pricing, and daily availability.
- **Order Management:** Take and track customer orders for both dine-in and takeaway services with ease.
- **Sales and Invoicing:** Automatically generate invoices upon payment and keep track of various payment methods.
- **Expenditure Tracking:** Record and categorize your restaurant's expenses, such as ingredients and supplies, for better financial oversight.
- **Reporting:** Gain valuable insights into your business performance with reports on daily, weekly, and monthly sales, best-selling items, and profit versus expenses.
- **Table Management:** Efficiently manage your restaurant's tables, including their capacity and current status.
- **User Management:** Implement staff access control through different user roles.

## Technology Stack

**Core**

- [Django](https://docs.djangoproject.com/en/5.2/)
- [Poetry](https://python-poetry.org)
- [SQLite](https://sqlite.org/index.html)
- [Bootstrap](https://getbootstrap.com/docs/5.0/getting-started/introduction/) / [Journal Theme from Bootswatch](https://bootswatch.com/journal/)

**Packages**

- [django-crispy-forms](https://django-crispy-forms.readthedocs.io/en/latest/)
- [crispy-bootstrap5](https://github.com/django-crispy-forms/crispy-bootstrap5)
- [django_extensions](https://django-extensions.readthedocs.io/en/latest/)
- [debug_toolbar](https://django-debug-toolbar.readthedocs.io/en/latest/)
- [djLint](https://djlint.com)
- [ruff](https://docs.astral.sh/ruff/)

## Screenshots

### Home

![image](https://github.com/user-attachments/assets/73b87863-0dfd-4506-82b2-64de94542831)

### Menu

![image](https://github.com/user-attachments/assets/c43c8e48-3d98-4ac5-9c20-17e8406c20e9)

### Tables

![image](https://github.com/user-attachments/assets/cf620b6e-d33c-42a3-9e32-31cebb6acaab)

---

### Cashier Dashboard

![image](https://github.com/user-attachments/assets/d744a196-4a52-4904-a236-2cf4e88a100e)

### Owner Dashboard

![image](https://github.com/user-attachments/assets/bc1ec2df-e571-45ca-831d-555da775b36b)

### Order CRUD

![image](https://github.com/user-attachments/assets/5e2a0892-af76-43bb-8179-ec52f2fb3f70)

- Includes CRUD operations for owner role. Also pagination and filtering.
- Cashier role can only read and register/update orders and sales.
- (*) Same interface for other modules/models.

### Reports

![image](https://github.com/user-attachments/assets/1fbdaee2-597c-42a4-b9af-415d4175b5ee)
