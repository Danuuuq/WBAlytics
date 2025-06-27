# Wildberries Analytics Platform

Аналитическая платформа для сбора, визуализации и анализа данных товаров с Wildberries. Проект позволяет пользователю просматривать товары по категориям, фильтровать и сортировать их, а также визуализировать ключевые метрики: цены, рейтинги, скидки и количество отзывов.

---

## ✨ Стек технологий

### Backend (Django):

* Python 3.11+
* Django 5+
* Django REST Framework
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
git clone https://github.com/your-username/wb-analytics.git
cd wb-analytics
```

### 2. Конфигурация

Создайте файл `.env` в папке `infra/`:

```env
DJANGO_SECRET_KEY=your-secret
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
REDIS_HOST=redis
```

### 3. Запуск через Docker Compose

```bash
docker-compose up --build
```

Проект будет доступен по адресу: `http://localhost:8000`
Фронтенд: `http://localhost:3000`

---

## 🔧 CI/CD (GitHub Actions)

Пример `.github/workflows/main.yml` включает:

* Проверку PEP8 (flake8)
* Прогон тестов
* Сборку Docker-образа
* Возможное выкладывание на сервер

---

## 📊 Возможности платформы

### 1. Получение и отображение товаров по категориям

* Автоматический парсинг данных по категории
* Кэширование результатов на 1 час (в Redis)

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
* 📉 График: стоимость против количества отзывов

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
