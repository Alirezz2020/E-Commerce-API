# EcommerceAPI

This project is a full-featured ecommerce API built with Django and Django REST Framework. It provides a robust backend for managing products, orders, reviews, and categories while also featuring a modern landing page with search, filtering, and pagination. Additionally, the project supports user authentication with an accounts app and offers a comprehensive admin panel for superusers to manage all aspects of the store—including adding product images.

## Features

- **Shop App:**
  - Product management with images.
  - Category organization.
  - Reviews for product feedback.
  - Orders with automated total calculations and inventory management.
- **Home App:**
  - A modern landing page built with a class-based view.
  - Search, filtering, and ordering options.
  - Pagination for product listings.
- **Accounts App:**
  - User registration, login, and logout using Django's built-in authentication.
- **Admin Panel:**
  - Full control over products, categories, orders, reviews, and order items.
  - Superusers can add and preview product images directly from the admin.
- **Modern UI:**
  - Custom CSS using Flexbox and Grid.
  - Smooth JavaScript for enhanced UX (e.g., smooth scrolling).

## Installation

1. **Clone the repository:**

   ```sh
   git clone https://github.com/Alirezz2020/E-Commerce-API.git
   cd E-Commerce-API
2. **Set Up a Virtual Environment:**
    ```sh
   python -m venv venv
   source venv/bin/activate  # For Windows: venv\Scripts\activate
3. **Install Dependencies:**
   ```sh
    pip install -r requirements.txt

4. **Apply Migrations:**
    ```sh
    python manage.py migrate
5. **Create a Superuser:**
    ```sh
   python manage.py createsuperuser
6. **Run the Development Server:**
    ```sh
   python manage.py runserver
7. **Access the Application:**

    Visit http://127.0.0.1:8000/ in your browser to start exploring the platform.

## Contributing
Contributions are welcome! Please fork the repository and create a pull request with your changes. Make sure to include tests and follow the project’s coding standards.

## License
This project is licensed under the MIT License.

