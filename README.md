# Wildberries Analytics Platform

Аналитическая платформа для сбора, визуализации и анализа данных товаров с Wildberries. Проект позволяет пользователю просматривать товары по категориям, фильтровать и сортировать их, а также визуализировать ключевые метрики: цены, рейтинги, скидки и количество отзывов.

---

## ✨ Стек технологий

### Backend (Django):

* Python 3.11+
* Django 5+
* Django REST Framework
* PostgreSQL (для хранения данных в БД)
* Redis (для кэширования)

### Frontend (React):

* React 18+
* Axios
* Recharts (для визуализации)
* React Select, RC-Slider (фильтрация)

### DevOps:

* Docker + Docker Compose
* GitHub Actions (CI/CD)
* .env-конфигурация для гибкой настройки окружения

---

## 🚀 Запуск проекта

### 1. Клонирование репозитория

```bash
git clone https://github.com/your-username/WBAlytics.git
cd WBAlytics/infra
```

### 2. Конфигурация

Создайте файл `.env` в директории `infra/`, референс `.env.example`:

```env
# PostgreSQL
POSTGRES_DB=wb_db
POSTGRES_USER=wb_user
POSTGRES_PASSWORD=wb_pass
DB_HOST=db
DB_PORT=5432

# Django
DJANGO_SECRET_KEY=YourSecretKeyNeedTypeHere
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=*

# Redis
REDIS_URL=redis://redis:6379/1

# React
REACT_APP_API_URL=/api
```

### 3. Запуск через Docker Compose

```bash
sudo docker compose up --build
```

Проект будет доступен по адресу: `http://localhost` или `http://<ip_add_server>`

---

## 📊 Возможности платформы

### 1. Получение и отображение товаров по категориям

* Автоматический парсинг данных по категории
* Кэширование результатов в Redis, первая загрузка категории долго далее быстрее

### 2. Фильтрация по товарам

* Минимальная и максимальная цена (`min_price`, `max_price`)
* Рейтинг (`min_rating`, `max_rating`)
* Количество отзывов (`min_reviews`, `max_reviews`)

### 3. Сортировка

Поддерживаются поля:

* `price`
* `discounted_price`
* `rating`
* `review_count`
* `name`

Сортировка задается параметрами:

* `sort_by=field_name`
* `sort_dir=asc|desc`

### 4. Визуализация

* 🌀 Гистограмма цен (динамические интервалы)
* 📈 Линейный график: скидка против рейтинга
* 📉 График: стоимость против рейтинга

---

## 🔐 API

### ✈ GET `/api/products/?query=<CATEGORY>&...`

Получение отфильтрованного и отсортированного списка товаров из кэша (или после парсинга).

#### Примеры параметров:

```http
GET /api/products/?query=Смартфоны&min_price=10000&max_price=30000&min_rating=4.2&sort_by=price&sort_dir=asc
```

#### Ответ (JSON):

```json
[
  {
    "id": 123,
    "name": "Xiaomi Redmi Note 12",
    "price": 14999,
    "discounted_price": 12999,
    "rating": 4.5,
    "review_count": 1245
  },
  ...
]
```

---

## 🌟 Особенности реализации

* ✅ Используется кэш Redis, чтобы не перегружать парсинг
* ✅ Кастомная фильтрация и сортировка как по ORM, так и в кэше
* ✅ Автоматическая отрисовка React-компонентов при изменении фильтров
* ✅ Отображение загрузки при запросах
* ✅ Адаптивный дизайн таблиц и графиков
