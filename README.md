### [Russian documentation](#Интернет магазин с использованием FastAPI)

### [English documentation](#E-commerce with FastAPI)

# E-commerce with FastAPI

This project is an educational application developed using FastAPI.
The Ecommerce is created to demonstrate the principles of building APIs,
handling requests, and working with databases. The main goal of the project
is to provide learning opportunities and practice in developing web applications
using modern technologies.

## Key Features

1. **User Management**: Users can register, log in, update their profiles, and
   manage their accounts.
2. **User Profiles**: Users can upload profile pictures and provide a bio to
   personalize their accounts.
3. **Address Management**: Users can add, update, and delete their delivery
   addresses, and set a default address for shipping.
4. **Payment Methods**: Users can add, update, and delete their payment methods,
   including credit/debit cards, and set a default payment method for checkout.
5. **Product Management**: Admins can manage product categories, add new
   products, update product information, and manage product inventory.
6. **Shopping Cart**: Users can add products to their shopping cart, update
   quantities, remove items, and proceed to checkout.
7. **Checkout Process**: Users can review their orders, select a shipping
   method, and make payments securely.
8. **Order Management**: Admins can view and manage orders, update order
   statuses, and track order fulfillment.
9. **Product Reviews**: Users can leave reviews and ratings for products they
   have purchased.

## Database

![Database](src/static/images/readme/E-commerce%20Database.png)

### Tables:

1. **Users (users):** Stores information about system users, including their
   identifiers, email addresses, passwords, names, surnames, roles, and activity
   statuses.
2. **Roles (roles):** Contains a list of user roles used to manage access within
   the system.
3. **User Profiles (user_profiles):** Contains additional information about user
   profiles, such as photos and biographies.
4. **Addresses (addresses):** Stores information about delivery addresses,
   including street, house number, city, region, postal code, and country.
5. **Address User Relationship (address_user):** Establishes the relationship
   between users and their delivery addresses.
6. **Countries (countries):** Contains a list of countries for organizing
   delivery addresses.
7. **Payment Types (payment_types):** Holds a list of payment types for
   classifying payment methods.
8. **Payment Methods (payment_methods):** Stores information about payment
   methods, including type, provider, and account number.
9. **Product Categories (product_categories):** Stores information about product
   categories for organizing the catalog.
10. **Products (products):** Contains information about products, including
    their names, descriptions, and images.
11. **Product Items (product_items):** Stores information about specific items,
    their prices, and stock levels.
12. **Variations (variations):** Contains information about various product
    variations, such as sizes or colors.
13. **Variation Options (variation_options):** Stores available options for
    product variations.
14. **Product Configurations (product_configurations):** Establishes
    relationships between products and their variations.
15. **Shopping Carts (shopping_carts):** Stores information about user shopping
    carts.
16. **Shopping Cart Items (shopping_cart_items):** Contains information about
    items added to shopping carts.
17. **Shipping Methods (shipping_methods):** Holds information about delivery
    methods available for selection during checkout.
18. **Order Statuses (order_statuses):** Contains a list of order statuses for
    tracking their progress.
19. **Orders (orders):** Stores information about orders placed by users.
20. **Order Lines (order_lines):** Contains information about products ordered
    by users.
21. **User Reviews (user_reviews):** Stores user reviews about ordered products.

## Project structure

```
project/
│
├── docker/
│   ├── app.sh
│   └── celery.sh
│
├── requirements/
│   ├── base.txt
│   ├── dev.txt
│   └── prod.txt
│
├── src/
│   ├── addresses/
│   ├── auth/
│   ├── countries/
│   ├── images/
│   ├── migrations/
│   ├── orders/
│   ├── payments/
│   ├── products/
│   ├── shipping_methods/
│   ├── shopping_carts/
│   ├── static/
│   ├── tasks/
│   ├── tests/
│   ├── users/
│   ├── utils/
│   ├── variations/
│   ├── app.py
│   ├── config.py 
│   ├── conftest.py
│   ├── dao.py
│   ├── database.py
│   ├── examples.py
│   ├── exceptions.py
│   ├── logger.py
│   ├── main.py
│   ├── models.py
│   ├── patterns.py
│   ├── permissions.py
│   └── responses.py
│
├── .black
├── .env-example
├── .flake8
├── .gitignore
├── .isort.cfg
├── .pre-commit-config.yaml
├── Dockerfile
├── alembic.ini
├── docker-compose.yml
├── grafana-dashboard.json
├── prometheus.yml
├── pytest.ini
└── README.md
```

- **docker/:** Directory containing scripts and configurations related to
  Docker.
    - **app.sh:** Shell script for running the Docker application.
    - **celery.sh:** Shell script for managing Celery tasks within Docker.

- **requirements/:** Directory containing dependency files for different
  environments.
    - **base.txt:** Base dependencies for the project.
    - **dev.txt:** Development-specific dependencies.
    - **prod.txt:** Production-specific dependencies.

- **src/:** Directory containing the source code of the project.
    - **addresses/:** Module for handling address-related functionalities.
    - **auth/:** Module for authentication functionalities.
    - **countries/:** Module for managing country data.
    - **images/:** Module for handling image-related functionalities.
    - **migrations/:** Directory for database migration scripts.
    - **orders/:** Module for managing order-related functionalities.
    - **payments/:** Module for handling payment-related functionalities.
    - **products/:** Module for managing product-related functionalities.
    - **shipping_methods/:** Module for managing shipping method
      functionalities.
    - **shopping_carts/:** Module for managing shopping cart functionalities.
    - **static/:** Directory for static files used in the project.
    - **tasks/:** Module for defining background tasks.
    - **tests/:** Directory for storing test modules.
    - **users/:** Module for managing user-related functionalities.
    - **utils/:** Directory for utility modules.
    - **variations/:** Module for managing product variation functionalities.
    - **app.py:** Main application file.
    - **config.py:** Configuration module for the project.
    - **conftest.py:** Configuration for pytest.
    - **dao.py:** Data access object module.
    - **database.py:** Database configuration and connection module.
    - **examples.py:** Module containing example code snippets.
    - **exceptions.py:** Module for defining custom exceptions.
    - **logger.py:** Module for logging functionalities.
    - **main.py:** Main entry point for the application.
    - **models.py:** Module containing data models for the project.
    - **patterns.py:** Module containing design patterns implementations.
    - **permissions.py:** Module for defining user permissions.
    - **responses.py:** Module for defining API response structures.

- **.black:** Configuration file for the Black code formatter tool.
- **.env-example:** Example file with environment variables.
- **.flake8:** Configuration file for the Flake8 code style checking tool.
- **.gitignore:** File specifying patterns to ignore in Git version control.
- **.isort.cfg:** Configuration file for the isort import sorting tool.
- **.pre-commit-config.yaml:** Configuration file for using pre-commit hooks.
- **Dockerfile:** Dockerfile for building a Docker image.
- **alembic.ini:** Configuration file for Alembic, a database migration tool for
  Python.
- **docker-compose.yml:** Docker Compose configuration file for running multiple
  Docker containers.
- **grafana-dashboard.json:** Configuration file for Grafana monitoring
  dashboard in JSON format.
- **prometheus.yml:** Configuration file for the Prometheus monitoring system.
- **pytest.ini:** Configuration file for testing using pytest.
- **README.md:** File containing the project's description.

## Installation and Running

### Installation:

1. Clone the project repository from GitHub:
   ```bash
   git clone https://github.com/kolenkoal/fastapi_ecommerce_api.git
   ```

2. Navigate into the project directory:
   ```bash
   cd fastapi_ecommerce_api
   ```

3. Rename the `.env-example` file to `.env`:
   ```bash
   mv .env-example .env
   ```

4. To configure your application, open the `.env` file in a text editor and fill
   in the appropriate values for each variable based on your environment. Make
   sure to provide valid credentials and configurations, especially for database
   connections, SMTP, and JWT secret key. Once configured, these variables will
   be loaded into your application's environment during runtime.

- **MODE:** Set the mode of your application. You can choose from "DEV", "
  PROD", or "TEST".

- **LOG_LEVEL:** Set the logging level for your application (e.g., "DEBUG", "
  INFO", "WARNING", "ERROR", "CRITICAL").

- **Database Configuration:**
    - **DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME:** Configuration for the
      main database.
    - **POSTGRES_DB, POSTGRES_USER, POSTGRES_PASSWORD:** Configuration for the
      PostgreSQL database (should be the same as DB_NAME, DB_USER and
      DB_PASSWORD respectively).
    - **TEST_DB_HOST, TEST_DB_PORT, TEST_DB_USER, TEST_DB_PASS, TEST_DB_NAME:**
      Configuration for the test database.

- **Redis Configuration:**
    - **REDIS_HOST, REDIS_PORT:** Configuration for the Redis server.

- **SMTP Configuration for sending emails (optional):**
    - **SMTP_HOST, SMTP_PORT:** Configuration for the SMTP server used for
      sending emails.
    - **EMAIL_SENDER_USERNAME, EMAIL_SENDER_PASSWORD:** Credentials for the
      email sender.

- **JWT Secret Key:** Secret key used for JWT (JSON Web Token) authentication.
  You can set your own or peek random secret key
  from https://www.grc.com/passwords.htm

- **Default User Passwords:**
    - **ADMIN_PASSWORD:** Default password for admin users
      (use it for logging as admin. Login: admin@admin.com, password: your
      password for ADMIN_PASSWORD)
    - **USER_PASSWORD:** Default password for regular users.

- **Sentry Configuration:**
    - **SENTRY_URL_NUMBER, SENTRY_PROJECT_NUMBER:** Configuration for
      integrating with Sentry for error tracking. In the `app.py` there
      is `sentry_sdk.init` function to start sentry. Find how to set up your
      sentry project and insert DSN parts of the link to the project to these
      fields. The link will look like:
      https://XXXXXXXXXXXXXXXXXXXXXXXX.ingest.us.sentry.io/XXXXXXXXX

### Running:

To start the project:

1. Make sure Docker and Docker Compose are installed on your system.

2. Run the following command to start the project:
   ```bash
   docker-compose up
   ```

3. Once the containers are up and running, access the Swagger documentation
   at [http://0.0.0.0:8000/docs](http://0.0.0.0:8000/docs) to interact with the
   API.

To stop the project:

1. Press `Ctrl + C` in the terminal to stop the running Docker containers.

2. Run the following command to bring down the Docker containers:
   ```bash
   docker-compose down
   ```

### Running Tests:

If you want to run tests:

To set up the testing environment, you'll need to create a local database and
configure the following variables in your `.env` file:

- **TEST_DB_HOST:** The host address of your local test database.
- **TEST_DB_PORT:** The port number of your local test database.
- **TEST_DB_USER:** The username for accessing your local test database.
- **TEST_DB_PASS:** The password for accessing your local test database.
- **TEST_DB_NAME:** The name of your local test database.

1. Set up and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

2. Install the required packages:
   ```bash
   pip3 install -r requirements/dev.txt && pip3 install -r requirements/base.txt
   ```

3. Run the tests using pytest:
   ```bash
   pytest
   ```

---

## Usage

Once the application is running, you can access the Swagger documentation by
navigating to http://0.0.0.0:8000/docs in your web browser. Use the Swagger UI
to test the API endpoints and explore the available functionality.

Prometheus and Grafana are automatically started along with the application. If
you want to use it, you need to set it up:

1. Navigate to http://0.0.0.0:9090/targets?search= and verify that both
   prometheus and ecommerce are up:
   ![Database](src/static/images/readme/prometheus.png)
2. You can access Grafana by navigating to http://0.0.0.0:3000 in your web
   browser. Log in to Grafana with the default credentials (username: admin,
   password:
   admin), and configure Prometheus as a data source to start visualizing your
   application metrics.
3. Go to http://0.0.0.0:3000/datasources. Click `Add new data source`.
   Choose
   Prometheus. In HTTP -> URL type `http://prometheus:9090`.
   Click `Save & test.` If you see `Data source is working`, everything
   okay.
4. Find `grafana-dashboard.json` in the root of the project. Replace
   all `POarCC0Ik` with id of your prometheus data source, which is shown in the
   URL of the
   page.
   ![Database](src/static/images/readme/grafana.png)
5. Go to http://0.0.0.0:3000/dashboards. New -> Import and insert
   updated `grafana-dashboard.json` in `Import via panel json`. Everything
   should work after that

## Feedback

If you have any feedback, questions, or suggestions regarding this project, feel
free to reach out to me on Telegram. You can write
me [here](https://t.me/kolenkoa). I'd be happy to assist you
further!

# Интернет магазин с использованием FastAPI

Этот проект - личное приложение, разработанное с использованием
FastAPI.
Интернет магазин создана для демонстрации принципов построения API,
обработки запросов и работы с базами данных. Основная цель проекта -
показать навыки в разработке веб-приложений с использованием современных
технологий.

## Основные функции

1. **Управление пользователями**: Пользователи могут регистрироваться, входить в
   систему, обновлять свои профили и
   управлять своими аккаунтами.
2. **Профили пользователей**: Пользователи могут загружать аватары и добавлять
   биографию для
   персонализации своих аккаунтов.
3. **Управление адресами**: Пользователи могут добавлять, обновлять и удалять
   свои адреса доставки, а также
   устанавливать адрес по умолчанию для доставки.
4. **Способы оплаты**: Пользователи могут добавлять, обновлять и удалять свои
   способы оплаты,
   включая кредитные/дебетовые карты, а также устанавливать способ оплаты по
   умолчанию для оформления заказа.
5. **Управление товарами**: Администраторы могут управлять категориями товаров,
   добавлять новые
   товары, обновлять информацию о товарах и управлять запасами товаров.
6. **Корзина покупок**: Пользователи могут добавлять товары в корзину, обновлять
   количество, удалять товары и переходить к оформлению заказа.
7. **Процесс оформления заказа**: Пользователи могут просматривать свои заказы,
   выбирать метод доставки и
   производить оплату безопасно.
8. **Управление заказами**: Администраторы могут просматривать и управлять
   заказами, обновлять статусы заказов и
   отслеживать выполнение заказов.
9. **Отзывы о товарах**: Пользователи могут оставлять отзывы и оценки для
   товаров, которые
   они приобрели.

## База данных

![Database](src/static/images/readme/E-commerce%20Database.png)

### Таблицы:

1. **Пользователи (users):** Содержит информацию о пользователях системы,
   включая их
   идентификаторы, адреса электронной почты, пароли, имена, фамилии, роли и
   статусы активности.
2. **Роли (roles):** Содержит список ролей пользователей, используемых для
   управления доступом в системе.
3. **Профили пользователей (user_profiles):** Содержит дополнительную информацию
   о профилях пользователей,
   такую как фотографии и биографии.
4. **Адреса (addresses):** Содержит информацию об адресах доставки, включая
   улицу, дом, город, регион, почтовый индекс и страну.
5. **Связь пользователь-адрес (address_user):** Устанавливает связь между
   пользователями и их адресами доставки.
6. **Страны (countries):** Содержит список стран для организации адресов
   доставки.
7. **Типы оплаты (payment_types):** Содержит список типов оплаты для
   классификации способов оплаты.
8. **Способы оплаты (payment_methods):** Содержит информацию о способах оплаты,
   включая тип, провайдера и номер счета.
9. **Категории товаров (product_categories):** Содержит информацию о категориях
   товаров для организации каталога.
10. **Товары (products):** Содержит информацию о товарах, включая их названия,
    описания и изображения.
11. **Элементы товаров (product_items):** Содержит информацию о конкретных
    товарах, их ценах и уровнях запасов.
12. **Вариации (variations):** Содержит информацию о различных вариантах
    товаров, таких как размеры или цвета.
13. **Опции вариаций (variation_options):** Содержит доступные варианты для
    вариаций товаров.
14. **Конфигурации товаров (product_configurations):** Устанавливает отношения
    между товарами и их вариациями.
15. **Корзины покупок (shopping_carts):** Содержит информацию о корзинах покупок
    пользователей.
16. **Элементы корзины покупок (shopping_cart_items):** Содержит информацию об
    элементах, добавленных в корзины покупок.
17. **Методы доставки (shipping_methods):** Содержит информацию о доступных
    методах доставки для выбора при оформлении заказа.
18. **Статусы заказов (order_statuses):** Содержит список статусов заказов для
    отслеживания их состояния.
19. **Заказы (orders):** Содержит информацию о заказах, размещенных
    пользователями.
20. **Линии заказов (order_lines):** Содержит информацию о товарах, заказанных
    пользователями.
21. **Отзывы о товарах(user_reviews):** Содержит отзывы пользователей о
    заказанных товарах.

## Структура проекта

```
project/
│
├── docker/
│   ├── app.sh
│   └── celery.sh
│
├── requirements/
│   ├── base.txt
│   ├── dev.txt
│   └── prod.txt
│
├── src/
│   ├── addresses/
│   ├── auth/
│   ├── countries/
│   ├── images/
│   ├── migrations/
│   ├── orders/
│   ├── payments/
│   ├── products/
│   ├── shipping_methods/
│   ├── shopping_carts/
│   ├── static/
│   ├── tasks/
│   ├── tests/
│   ├── users/
│   ├── utils/
│   ├── variations/
│   ├── app.py
│   ├── config.py 
│   ├── conftest.py
│   ├── dao.py
│   ├── database.py
│   ├── examples.py
│   ├── exceptions.py
│   ├── logger.py
│   ├── main.py
│   ├── models.py
│   ├── patterns.py
│   ├── permissions.py
│   └── responses.py
│
├── .black
├── .env-example
├── .flake8
├── .gitignore
├── .isort.cfg
├── .pre-commit-config.yaml
├── Dockerfile
├── alembic.ini
├── docker-compose.yml
├── grafana-dashboard.json
├── prometheus.yml
├── pytest.ini
└── README.md
```

- **docker/:** Каталог, содержащий скрипты и конфигурации, связанные с
  Docker.
    - **app.sh:** Shell-скрипт для запуска приложения Docker.
    - **celery.sh:** Shell-скрипт для управления задачами Celery внутри Docker.

- **requirements/:** Каталог, содержащий файлы зависимостей для разных
  сред.
    - **base.txt:** Основные зависимости для проекта.
    - **dev.txt:** Зависимости для разработки.
    - **prod.txt:** Зависимости для продуктовой среды.

- **src/:** Каталог, содержащий исходный код проекта.
    - **addresses/:** Модуль для работы с функциями, связанными с адресами.
    - **auth/:** Модуль для функций аутентификации.
    - **countries/:** Модуль для управления данными о странах.
    - **images/:** Модуль для работы с функциями, связанными с изображениями.
    - **migrations/:** Каталог для скриптов миграции базы данных.
    - **orders/:** Модуль для управления функциями, связанными с заказами.
    - **payments/:** Модуль для работы с функциями, связанными с оплатой.
    - **products/:** Модуль для управления функциями, связанными с товарами.
    - **shipping_methods/:** Модуль для управления функциями, связанными с
      методами доставки.
    - **shopping_carts/:** Модуль для управления функциями, связанными с
      корзинами покупок.
    - **static/:** Каталог для статических файлов, используемых в проекте.
    - **tasks/:** Модуль для определения фоновых задач.
    - **tests/:** Каталог для хранения модулей тестирования.
    - **users/:** Модуль для управления функциями, связанными с пользователями.
    - **utils/:** Каталог для утилитарных модулей.
    - **variations/:** Модуль для управления функциями, связанными с вариациями
      товаров.
    - **app.py:** Основной файл приложения.
    - **config.py:** Модуль конфигурации проекта.
    - **conftest.py:** Конфигурация для pytest.
    - **dao.py:** Модуль объекта доступа к данным.
    - **database.py:** Модуль конфигурации и соединения с базой данных.
    - **examples.py:** Модуль, содержащий примеры кода.
    - **exceptions.py:** Модуль для определения пользовательских исключений.
    - **logger.py:** Модуль для функций логгирования.
    - **main.py:** Основная точка входа в приложение.
    - **models.py:** Модуль, содержащий модели данных для проекта.
    - **patterns.py:** Модуль, содержащий реализации шаблонов проектирования.
    - **permissions.py:** Модуль для определения прав доступа пользователей.
    - **responses.py:** Модуль для определения структур ответов API.

- **.black:** Файл конфигурации для инструмента форматирования кода Black.
- **.env-example:** Пример файла с переменными окружения.
- **.flake8:** Файл конфигурации для инструмента проверки стиля кода Flake8.
- **.gitignore:** Файл, определяющий шаблоны для игнорирования в системе
  контроля версий Git.
- **.isort.cfg:** Файл конфигурации для инструмента сортировки импортов isort.
- **.pre-commit-config.yaml:** Файл конфигурации для использования
  pre-commit-хуков.
- **Dockerfile:** Dockerfile для сборки Docker-образа.
- **alembic.ini:** Файл конфигурации для Alembic, инструмента миграции базы
  данных для Python.
- **docker-compose.yml:** Файл конфигурации Docker Compose для запуска
  нескольких контейнеров Docker.
- **grafana-dashboard.json:** Файл конфигурации для панели мониторинга Grafana в
  формате JSON
- **prometheus.yml:** Файл конфигурации для системы мониторинга Prometheus.
- **pytest.ini:** Файл конфигурации для тестирования с использованием pytest.
- **README.md:** Файл, содержащий описание проекта.

## Установка и запуск

### Установка:

1. Склонируйте репозиторий проекта из GitHub:
   ```bash
   git clone https://github.com/kolenkoal/fastapi_ecommerce_api.git
   ```

2. Перейдите в каталог проекта:
   ```bash
   cd fastapi_ecommerce_api
   ```

3. Переименуйте файл `.env-example` в `.env`:
   ```bash
   mv .env-example .env
   ```

4. Для настройки вашего приложения откройте файл `.env` в текстовом редакторе и
   заполните
   соответствующие значения для каждой переменной в зависимости от вашей среды.
   Обязательно
   предоставьте действительные учетные данные и конфигурации, особенно для
   подключения к базе
   данных, SMTP и секретного ключа JWT. После настройки эти переменные будут
   загружены в
   окружение вашего приложения во время его выполнения.

- **MODE:** Установите режим вашего приложения. Вы можете выбрать "DEV", "PROD"
  или "TEST".

- **LOG_LEVEL:** Установите уровень логгирования для вашего приложения (
  например, "DEBUG", "
  INFO", "WARNING", "ERROR", "CRITICAL").

- **Настройки базы данных:**
    - **DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME:** Конфигурация для
      основной базы данных.
    - **POSTGRES_DB, POSTGRES_USER, POSTGRES_PASSWORD:** Конфигурация для
      базы данных PostgreSQL (должна совпадать с DB_NAME, DB_USER и
      DB_PASSWORD соответственно).
    - **TEST_DB_HOST, TEST_DB_PORT, TEST_DB_USER, TEST_DB_PASS, TEST_DB_NAME:**
      Конфигурация для тестовой базы данных.

- **Настройки Redis:**
    - **REDIS_HOST, REDIS_PORT:** Конфигурация для сервера Redis.

- **Настройки SMTP для отправки электронных писем (необязательно):**
    - **SMTP_HOST, SMTP_PORT:** Конфигурация для SMTP-сервера, используемого для
      отправки электронных писем.
    - **EMAIL_SENDER_USERNAME, EMAIL_SENDER_PASSWORD:** Учетные данные для
      отправителя электронных писем.

- **Секретный ключ JWT:** Секретный ключ, используемый для аутентификации
  JWT (JSON Web Token).
  Вы можете установить свой собственный или сгенерировать случайный секретный
  ключ
  на сайте https://www.grc.com/passwords.htm

- **Пароли пользователей по умолчанию:**
    - **ADMIN_PASSWORD:** Пароль по умолчанию для администраторов
      (используйте его для входа в систему как администратор. Логин:
      admin@admin.com, пароль: ваш
      пароль для ADMIN_PASSWORD)
    - **USER_PASSWORD:** Пароль по умолчанию для обычных пользователей.

- **Настройки Sentry:**
    - **SENTRY_URL_NUMBER, SENTRY_PROJECT_NUMBER:** Конфигурация для
      интеграции с Sentry для отслеживания ошибок. В файле `app.py` есть
      функция `sentry_sdk.init`,
      чтобы начать работу с Sentry. Настройте свой Sentry проект и вставьте DSN
      части ссылки
      на проект в эти поля. Ссылка будет выглядеть примерно так:
      https://XXXXXXXXXXXXXXXXXXXXXXXX.ingest.us.sentry.io/XXXXXXXXX

### Запуск:

Для запуска проекта:

1. Убедитесь, что Docker и Docker Compose установлены на вашей системе.

2. Запустите следующую команду для запуска проекта:
   ```bash
   docker-compose up
   ```

3. После запуска контейнеров перейдите к документации Swagger
   по адресу [http://0.0.0.0:8000/docs](http://0.0.0.0:8000/docs), чтобы
   взаимодействовать с
   API.

Для остановки проекта:

1. Нажмите `Ctrl + C` в терминале, чтобы остановить запущенные контейнеры
   Docker.

2. Запустите следующую команду, чтобы остановить контейнеры Docker:
   ```bash
   docker-compose down
   ```

### Запуск тестов:

Если вы хотите запустить тесты:

Для настройки среды тестирования вам необходимо создать локальную базу данных и
настроить следующие переменные в вашем файле `.env`:

- **TEST_DB_HOST:** Адрес хоста вашей локальной тестовой базы данных.
- **TEST_DB_PORT:** Номер порта вашей локальной тестовой базы данных.
- **TEST_DB_USER:** Имя пользователя для доступа к вашей локальной тестовой базе
  данных.
- **TEST_DB_PASS:** Пароль для доступа к вашей локальной тестовой базе данных.
- **TEST_DB_NAME:** Имя вашей локальной тестовой базы данных.

1. Создайте и активируйте виртуальное окружение:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

2. Установите необходимые пакеты:
   ```bash
   pip3 install -r requirements/dev.txt && pip3 install -r requirements/base.txt
   ```

3. Запустите тесты:

   ```bash
   pytest src/tests
   ```

## Дополнительные настройки

- **Настройка Celery:** Перейдите к файлу `.env` и установите необходимые
  переменные окружения для настройки брокера сообщений (например, Redis) и
  задачи периодической очистки.

- **Настройка мониторинга:** Приложение включает файлы конфигурации для
  мониторинга с использованием Prometheus и Grafana. Вы можете настроить их
  по вашему усмотрению.

## Вклад

Если вы нашли ошибку, у вас есть предложения по улучшению или хотите добавить
новые
функции, не стесняйтесь создавать запросы на включение изменений (pull
requests). Я всегда
рад вносить улучшения в проект.

## Лицензия

Этот проект лицензирован в соответствии с условиями лицензии MIT.