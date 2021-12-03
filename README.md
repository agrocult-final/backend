<p align="center">
    <h1 align="center">PROJECT</h1>
</p>

<h4>Реализованная функциональность</h4>

<h4>Особенность проекта в будущем:</h4>

<h4>Основной стек технологий:</h4>
<ul>
    <li>Python</li>
	<li>Бэкенд: FastAPI, TortoiseORM, RQ, APScheduler, aioboto3</li>
	<li>Инфраструктура: S3 (совместимый) сервер, PostgreSQL, Redis</li>
	<li>Git.</li>
	<li>Docker.</li>

 </ul>
<h4>Демо</h4>
<p>Демо-api сервиса доступно по адресу: https://agroatom.egnod.dev/api/docs </p>


СРЕДА ЗАПУСКА
------------
1) развертывание сервиса производится на debian-like linux (debian 9+);
2) требуется установленный docker и docker-compose
3) S3-совместимый сервер (self-hosted или нет - неважно)

УСТАНОВКА
------------
### Установка Docker/Docker-compose

Выполните
~~~
sudo apt-get update
sudo apt-get upgrade
sudo apt-get install docker.io docker-compose

git clone https://github.com/agrocult-final/backend agroatom
cd agroatom
~~~
### База данных и Выполнение миграций

При первом запуске docker-compose, после того как поднимется БД, сервис migrator выполнит необходимые миграции, в предпоследней из которых будут базовый данные справочника сортов.

### Файлы среды

~~~
cp deploy/examples/envs/.env.workers_dashboard .
cp deploy/examples/envs/.env .
cp deploy/examples/envs/.env.db .
~~~

Для старта потребуется только заполнить параметры для S3 подключения в .env:
- AGROATOM_S3_URL
- AGROATOM_S3_ACCESS_KEY
- AGROATOM_S3_SECRET_KEY

Остальное для тестирования менять необязательно.

### Сборка и запуск

Сборка:
~~~
docker-compose -f deploy/docker-compose.yml --project-directory . build api
~~~

Запуск с двумя воркерами обработки изображений (параллельно будут обрабатываться 2 изображения, можно больше):
~~~
docker-compose -f deploy/docker-compose.yml --project-directory . up -d --scale tasks-actors-ycc=2
~~~
