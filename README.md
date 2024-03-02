<div id="header" align="center">
  <h1>Training System</h1>
  <img src="https://img.shields.io/badge/Python-3.7.9-F8F8FF?style=for-the-badge&logo=python&logoColor=20B2AA">
  <img src="https://img.shields.io/badge/DjangoRestFramework-3.14.0-F8F8FF?style=for-the-badge&logo=django&logoColor=20B2AA">
  <img src="https://img.shields.io/badge/Docker-555555?style=for-the-badge&logo=docker&logoColor=2496ED">
</div>

# Запуск проекта через докер:

- Клонируйте репозиторий и перейдите в него.
- Из корневой папки запустите docker-compose:
  ```
  ~$ docker-compose up -d --build
  ```
- В контейнере **backend** выполните миграции:
  ```
  ~$ docker-compose exec backend python manage.py migrate
  ```
- Можете создать суперпользователя, для админки:
  ```
  ~$ docker-compose exec backend python manage.py createsuperuser
  ```