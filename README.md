# Jedi Academy

Простое web app посвященное вселенной Звездных Войн, написано на python + Django.

## Описание

В главном окне программы есть две карточки - Кандидат и Джедай. При выборе кандидата, откроется окно для ввода данных
нового кандидата. После сохранения данных кандидата, произойдет переход на страницу тестирования кандидата. После 
прохождения тестирования произойдёт переход обратно в главное окно.

При выборе джедая, откроется окно со списком джедаев и кнопками перехода к каждому из них. Так же будет показано 
количество падаванов у каждого джедая. После перехода к конкретному джедаю будет показано окно с падаванами и 
кандидатами и их ответами на вопросы (). Понравившихся кандидатов можно взять, нажав на кнопку "Взять". Можно взять не 
более 3-х падаванов. При получении кандидатом статуса "падаван", ему на указанный при создании адрес будет послано 
письмо. При необходимости, можно изгнать падаванов и заменить их новыми.

Все ошибки кооректно отображаются, вместо неинформативного окна 404 будет выводиться краткая информаця о неполадке.

## Как это работает

* Склонить проект.
* Создать виртуальное окружение и войти в него.
* Установить `requirements`.
* Создать базу данных в PostgreSQL.
* Переименовать `settings.template.py` в `settings.py` (в папке jedi_academy), указать `secret key`, `allowed hosts` и 
настройки базы данных.
* Применить миграции `python manage.py migrate`
* Запустить - python manage.py runserver хост:порт

## Скриншоты

Главная страница

![Главная страница](screenshots/screenshot_main.png?raw=true "Главная страница")
![Создание кандидата](screenshots/screenshot_candidate.png?raw=true "Создание кандидата")
![Тестирование](screenshots/screenshot_testing.png?raw=true "Тестирование")
![Список джедаев](screenshots/screenshot_jedi.png?raw=true "Список джедаев")
![Кандидаты в падаваны](screenshots/screenshot_jedi_padawan.png?raw=true "Кандидаты в падаваны")