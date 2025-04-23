# Project Roadmap: Restaurant Management System

**Goal:** To develop a comprehensive system for managing a restaurant's menu, inventory, orders, sales, expenses, and user roles, initially utilizing a customized Django Admin panel and eventually transitioning to a RESTful API with Django REST Framework and a potential light frontend.

**Technologies:** Django, Django REST Framework, Poetry, Git, Docker, PostgreSQL.

**Phases:**

**Phase 1: Core Data Models and Django Admin Interface**

1.  **Project Setup:**

    - Initialize a new Django project.
    - Set up Poetry for dependency management (`poetry init`, `poetry add django psycopg2`).
    - Create the necessary Django apps (e.g., `menu`, `inventory`, `orders`, `sales`, `expenses`, `users`).
    - Configure PostgreSQL as the database.
    - Set up Git for version control (`git init`).
    - Create a basic `.gitignore` file.

2.  **Define Core Models:**

    - In the respective apps, define the Django models based on the core functionalities:
      - `menu`: `Category`, `Dish` (with fields for name, description, price, image, availability, category).
      - `inventory`: `Ingredient` (with fields for name, unit, current stock), `DishIngredient` (through model for many-to-many relationship between `Dish` and `Ingredient` with quantity).
      - `orders`: `Order` (with fields for order time, table number/customer info, status), `OrderItem` (through model for many-to-many with `Dish` and quantity, price at the time of order).
      - `sales`: `Sale` (with fields for order, sale time, total amount).
      - `expenses`: `ExpenseCategory`, `Expense` (with fields for category, description, amount, date).
      - `users`: Leverage Django's built-in `User` model and potentially create a `UserProfile` for additional restaurant-specific information.

3.  **Customize Django Admin:**

    - Register your models with the Django Admin interface (`admin.py` in each app).
    - Customize the Admin views for each model to provide a user-friendly experience:
      - Use `list_display`, `list_filter`, `search_fields`, `ordering`.
      - Implement `inlines` for related models (e.g., `OrderItem` within `Order`, `DishIngredient` within `Dish`).
      - Customize forms for better data input.
      - Potentially create custom Admin actions for specific tasks (e.g., marking an order as "prepared").

4.  **Implement Basic User Roles and Permissions:**

    - Utilize Django's built-in permission system and potentially create custom permission groups (e.g., `manager`, `staff`).
    - Assign permissions to different user roles to control access to different parts of the Admin interface.

5.  **Basic Reporting via Django Admin:**
    - Explore the possibility of creating custom Admin views or using libraries like `django-admin-charts` to display basic sales and expense reports within the Admin panel.

**Phase 2: REST API Development with Django REST Framework**

1.  **Install Django REST Framework:**

    - `poetry add djangorestframework`

2.  **Create Serializers:**

    - Develop DRF serializers for all your core models to handle data serialization and deserialization. Consider using `ModelSerializer` where appropriate and customize fields as needed.

3.  **Build API Views:**

    - Create API endpoints using `ViewSet`s or `APIView`s for all the functionalities:
      - Menu listing and detail.
      - Creating, updating, and viewing orders.
      - Recording sales and expenses.
      - Managing inventory (initially read-only or with basic update options).
      - User management (carefully consider which operations to expose via the API).

4.  **Implement Authentication and Permissions:**

    - Set up JWT authentication using `djangorestframework-simplejwt` (`poetry add djangorestframework-simplejwt`).
    - Implement appropriate permission classes to control access to API endpoints based on user roles.

5.  **Implement Filtering and Pagination:**

    - Use `django-filter` (`poetry add django-filter`) and DRF's built-in filtering and pagination to allow for efficient data retrieval.

6.  **API Documentation:**
    - Integrate `drf-spectacular` (`poetry add drf-spectacular`) to automatically generate OpenAPI documentation for your API.

**Phase 3: Optional Light Frontend Integration**

1.  **Frontend Setup:**

    - Initialize a new frontend project using a lightweight framework like Vue.js or React.js (outside the Django project directory).

2.  **API Consumption:**

    - Develop the frontend to consume the DRF API endpoints for displaying data and performing actions (e.g., placing orders, viewing menu).

3.  **User Interface Development:**
    - Build user-friendly interfaces for different user roles based on the API capabilities.

**Phase 4: Dockerization and Deployment**

1.  **Create Dockerfile and docker-compose.yml:**

    - Define the Docker environment for your Django/DRF backend (and potentially the frontend and PostgreSQL).

2.  **Containerize Application:**

    - Build and run your application using Docker.

3.  **Deployment:**
    - Choose a deployment platform (e.g., Heroku, DigitalOcean, AWS) and deploy your containerized application.
    - Set up your PostgreSQL database in the deployment environment.

**Continuous Learning:**

- Throughout the project, continuously refer to the official documentation for Django, DRF, Poetry, Git, Docker, and PostgreSQL.
- Explore best practices for API design, security, and testing.
- Consider exploring related technologies like Celery for background tasks (e.g., generating reports) or WebSockets for real-time features in the future.
