# Football League API

**Тема проекта:** разработка и развертывание REST API-сервиса для учета футбольных команд и матчей.

**Сделал:** 77Lev77

---

## 1. Назначение проекта

Football League API — это учебный REST API-сервис на Flask для учета футбольных команд и матчей. Сервис позволяет хранить информацию о командах, тренерах, стадионах, расписании матчей, статусах игр и счете завершенных встреч.

Проект выполнен в рамках университетского задания, включающего полный цикл подготовки веб-сервиса: создание репозитория GitHub, разработка Flask-приложения, упаковка в Docker, загрузка Docker-образа в Docker Hub, подготовка Terraform-конфигурации для Yandex Cloud, развертывание в Minikube через Kubernetes и оформление README-документации.

---

## 2. Выполненные пункты задания

| № | Пункт задания | Реализация |
|---|---|---|
| 1 | Репозиторий GitHub | Проект подготовлен для загрузки в `https://github.com/77Lev77/football-league-api` |
| 2 | Сервис Flask/FastAPI | Реализован REST API-сервис на Flask |
| 3 | Упаковка сервиса в Docker | Добавлен `Dockerfile` |
| 4 | Загрузка образа в Docker Hub | Образ предусмотрен как `77lev77/football-league-api:latest` |
| 5 | Развертка в Yandex Cloud через Terraform | Подготовлены файлы в `infra/terraform/` |
| 6 | Развертка в Minikube через k8s | Подготовлены Kubernetes-манифесты в `kubernetes/` |
| 7 | README | Подготовлен подробный `README.md` |

---

## 3. Используемые технологии

- Python 3.11;
- Flask;
- Gunicorn;
- JSON-файлы как простое хранилище данных;
- Docker;
- Docker Compose;
- Docker Hub;
- Kubernetes;
- Minikube;
- Terraform;
- Yandex Cloud;
- Git и GitHub;
- pytest.

---

## 4. Структура проекта

```text
football-league-api/
├── src/
│   ├── app.py              # основной Flask-сервис
│   └── storage.py          # функции для чтения и записи JSON-данных
│
├── data/
│   ├── teams.json          # список футбольных команд
│   └── matches.json        # список футбольных матчей
│
├── kubernetes/
│   ├── namespace.yaml      # namespace для Kubernetes
│   ├── deployment.yaml     # описание Deployment
│   └── service.yaml        # описание Service
│
├── infra/
│   └── terraform/
│       ├── main.tf         # основная Terraform-конфигурация
│       ├── variables.tf    # переменные Terraform
│       └── outputs.tf      # вывод внешнего IP и URL
│
├── tests/
│   └── test_api.py         # базовые тесты API
│
├── Dockerfile              # сборка Docker-образа
├── docker-compose.yml      # запуск через Docker Compose
├── requirements.txt        # Python-зависимости
├── README.md               # документация проекта
├── .gitignore
└── .dockerignore
```

---

## 5. API-эндпоинты

### Общие эндпоинты

| Метод | URL | Назначение |
|---|---|---|
| GET | `/` | Информация о сервисе |
| GET | `/health` | Проверка работоспособности |

### Команды

| Метод | URL | Назначение |
|---|---|---|
| GET | `/teams` | Получить список команд |
| GET | `/teams?city=Москва` | Фильтр команд по городу |
| GET | `/teams/<id>` | Получить команду по ID |
| POST | `/teams` | Создать команду |
| PUT | `/teams/<id>` | Изменить команду |
| DELETE | `/teams/<id>` | Удалить команду |

### Матчи

| Метод | URL | Назначение |
|---|---|---|
| GET | `/matches` | Получить список матчей |
| GET | `/matches?status=scheduled` | Фильтр матчей по статусу |
| GET | `/matches?team=Зенит` | Фильтр матчей по команде |
| GET | `/matches/<id>` | Получить матч по ID |
| GET | `/matches/team/<team_name>` | Получить матчи конкретной команды |
| GET | `/matches/status/<status>` | Получить матчи по статусу |
| POST | `/matches` | Создать матч |
| PUT | `/matches/<id>` | Изменить матч |
| PATCH | `/matches/<id>/score` | Изменить счет матча |
| DELETE | `/matches/<id>` | Удалить матч |

---

## 6. Локальный запуск на Windows

Перейти в папку проекта:

```cmd
cd /d F:\football-league-api
```

Создать виртуальное окружение:

```cmd
python -m venv venv
```

Активировать окружение:

```cmd
venv\Scripts\activate
```

Установить зависимости:

```cmd
pip install -r requirements.txt
```

Запустить Flask-сервис:

```cmd
python src\app.py
```

После запуска сервис будет доступен по адресу:

```text
http://127.0.0.1:8000
```

Проверка API:

```text
http://127.0.0.1:8000/health
http://127.0.0.1:8000/teams
http://127.0.0.1:8000/matches
```

---

## 7. Локальный запуск на Linux/macOS

```bash
cd football-league-api
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python src/app.py
```

---

## 8. Примеры запросов

### Получение всех команд

```bash
curl http://127.0.0.1:8000/teams
```

### Создание команды

```bash
curl -X POST http://127.0.0.1:8000/teams \
-H "Content-Type: application/json" \
-d '{"name":"Динамо","city":"Москва","coach":"Марцел Личка","founded":1923,"stadium":"ВТБ Арена"}'
```

### Получение всех матчей

```bash
curl http://127.0.0.1:8000/matches
```

### Создание матча

```bash
curl -X POST http://127.0.0.1:8000/matches \
-H "Content-Type: application/json" \
-d '{"home_team":"Динамо","away_team":"Краснодар","date":"2026-07-10","stadium":"ВТБ Арена","status":"scheduled"}'
```

### Изменение счета матча

```bash
curl -X PATCH http://127.0.0.1:8000/matches/1/score \
-H "Content-Type: application/json" \
-d '{"home_score":2,"away_score":2,"status":"finished"}'
```

---

## 9. Запуск через Docker

Сборка Docker-образа:

```cmd
cd /d F:\football-league-api
docker build -t football-league-api .
```

Запуск контейнера:

```cmd
docker run --name football-league-api -p 8000:8000 football-league-api
```

Проверка:

```text
http://localhost:8000/health
http://localhost:8000/teams
http://localhost:8000/matches
```

Остановка и удаление контейнера:

```cmd
docker stop football-league-api
docker rm football-league-api
```

---

## 10. Запуск через Docker Compose

```cmd
cd /d F:\football-league-api
docker compose up --build
```

Остановка:

```cmd
docker compose down
```

---

## 11. Загрузка Docker-образа в Docker Hub

Авторизация:

```cmd
docker login -u 77lev77
```

Сборка образа:

```cmd
docker build -t football-league-api .
```

Назначение тега Docker Hub:

```cmd
docker tag football-league-api 77lev77/football-league-api:latest
```

Загрузка образа:

```cmd
docker push 77lev77/football-league-api:latest
```

Проверка запуска образа из Docker Hub:

```cmd
docker run --name football-league-api-hub -p 8001:8000 77lev77/football-league-api:latest
```

Проверка в браузере:

```text
http://localhost:8001/health
```

---

## 12. Развертывание в Minikube через Kubernetes

Запуск Minikube:

```cmd
minikube start
```

Применение манифестов:

```cmd
cd /d F:\football-league-api
kubectl apply -f kubernetes
```

Проверка namespace:

```cmd
kubectl get ns
```

Проверка pod'ов:

```cmd
kubectl get pods -n football
```

Проверка deployment:

```cmd
kubectl get deployment -n football
```

Проверка service:

```cmd
kubectl get svc -n football
```

Открытие сервиса:

```cmd
minikube service football-league-api-service -n football
```

---

## 13. Развертывание в Yandex Cloud через Terraform

Terraform-конфигурация находится в директории:

```text
infra/terraform/
```

Перед запуском необходимо подготовить аккаунт Yandex Cloud, создать cloud/folder, настроить доступы и SSH-ключ.

Переход в директорию Terraform:

```cmd
cd /d F:\football-league-api\infra\terraform
```

Инициализация:

```cmd
terraform init
```

Проверка конфигурации:

```cmd
terraform validate
```

Планирование:

```cmd
terraform plan
```

Применение конфигурации:

```cmd
terraform apply
```

После выполнения Terraform создаст виртуальную машину, установит Docker и запустит контейнер:

```text
77lev77/football-league-api:latest
```

Ссылка на приложение будет выведена в output `application_url`.

---

## 14. Загрузка проекта на GitHub

Перед загрузкой желательно указать локального автора коммитов для данного проекта:

```cmd
git config user.name "77Lev77"
git config user.email "EMAIL_АККАУНТА_77LEV77"
```

Инициализация и первый коммит:

```cmd
cd /d F:\football-league-api
git init
git add .
git commit -m "Initial commit"
git branch -M main
```

Привязка удаленного репозитория:

```cmd
git remote add origin https://github.com/77Lev77/football-league-api.git
```

Загрузка на GitHub:

```cmd
git push -u origin main
```

Если `origin` уже существует:

```cmd
git remote set-url origin https://github.com/77Lev77/football-league-api.git
git push -u origin main
```

---

## 15. Тестирование

Запуск тестов:

```cmd
pytest
```

Тесты проверяют базовые эндпоинты:

- `/health`;
- `/teams`;
- `/matches`.

---

## 16. Что можно объяснить на защите

Проект представляет собой Flask-приложение, в котором реализованы REST-эндпоинты для работы с футбольными командами и матчами. Данные хранятся в JSON-файлах, что удобно для учебного проекта и не требует установки отдельной базы данных. В файле `storage.py` вынесена логика чтения и записи данных, а в `app.py` находятся маршруты API.

Dockerfile позволяет собрать приложение в изолированный контейнер, который запускается одинаково на разных компьютерах. Docker Hub используется для хранения готового образа, чтобы Kubernetes или виртуальная машина в Yandex Cloud могли скачать и запустить приложение без копирования исходного кода.

Kubernetes-манифесты описывают namespace, deployment и service. Deployment отвечает за запуск pod'ов с приложением, а service открывает доступ к приложению внутри Minikube. Terraform-файлы нужны для автоматического создания инфраструктуры в Yandex Cloud.

---

## 17. Итог

В результате выполнения работы был разработан REST API-сервис на Flask по теме футбола. Приложение поддерживает учет команд и матчей, CRUD-операции, фильтрацию по статусу, городу и команде. Проект подготовлен к запуску локально, через Docker, Docker Compose, Docker Hub, Kubernetes/Minikube и Terraform/Yandex Cloud.
