# PriceHelper
# Техническое задание по базам данных
## Описание
### Краткое описание
PriceHelper - веб-сайт для хранения пользователями цен на продукты
в различных магазинах. Пользователь сам для себя выбирает нужные ему
продукты, подходящие ему магазины, указать для себя сложность в
доступности того или иного магазина и выставить цены (либо 
экспортировать готовую таблицу цен у других пользователей). 
Помимо прочего, пользователь может добавить продукты в так называемую
корзину и получить исходя из определяемой сложности
оптимальный выбор магазинов, при котором
пользователь потратит меньше всего средств.

### Предметная область
Предметная область включает в себя следующие сущности:
* Пользователь 
* Город
* Продукт
* Категория продукта
* Магазин
* Цена

## Данные 
### Пользователь
В базе данных о пользователе хранятся следующие данные:
* Уникальное имя пользователя 
* Имя
* Фамилия
* Город
* Уникальный e-mail
* Пароль
* Аватар
* Приватный/публичный аккаунт (приватный аккаунт не могут просматривать
другие пользователи)
* Является ли пользователь администратором

Для регистрации необходимо ввести имя, фамилию, имя пользователя,
адрес почты и пароль. Остальные поля указываются в личном кабинете
по желанию. 

### Город
Для конкретизирования информации о ценах, пользователь может указать
свой город. В базе изначально содержится таблица городов,
пользователь может просто указать "Другой город", если его там нет,
это опциональная характеристика. Города добавляются администратором
на этапе развертывания.

* Название города

### Категория продуктов
Для удобства классификации продуктов в базе данных хранятся
категории продуктов

* Уникальное азвание категории

Категории также изначально хранятся в соответствующей таблице,
если нужной категории не имеется, можно просто указать "Разное",
также добавляются администратором на этапе развертывания

### Продукт
В базе данных хранится множество продуктов, но пользователь
может для себя создать новый продукт и использователь его в своих
целях, тогда другие пользователи этот продукт в общем списке видеть
не будут, итого каждый пользователь в общем списке видит 
изначальный продукте и добавленные им же

* Название продукта
* Категория продукта
* Иконка (фото) продукта
* Автор (если продукт изначальный (создан администратором), 
то такой продукт автора не имеет)

### Магазин
* Название магазина
* Иконка (фото) магазина
* Автор (аналогично продуктам)

Пользователь выбирает из общего списка продукты и магазины для себя,
и при связи пользователя и магазина пользователь также устанавливает
сложность в доступности этого магазина от 1 до 5(пользователь
сам определяет в какой магазин ему легче идти, а в какой вызывает
трудности)

### Магазин пользователя
* Пользователь
* Магазин
* Сложность

### Продукт пользователя (имеется в виду продукт, который пользователь добавляет к себе в таблицу, это может быть как оригинальный продукт, так и его собственный)
* Пользователь
* Продукт
* Находится ли продукт у пользователя в корзине

Во вкладке "Корзина" пользователь выбирает из добавленных им продукты,
которые он собирается купить

### Цена
* Магазин пользователя
* Продукт пользователя
* Цена (десятичное число)
* Комментарий

## Роли пользователей
### Неавторизированный пользователь
Неавторизированный пользователь может зарегистрироваться или войти
в существующий аккаунт
### Авторизованный пользователь
Может редактировать свою собственную таблицу, создавать свои
собственные продукты, которые в общем списке видны только ему
### Администратор
Администратор может добавлять продукты, которые попадают в базу данных
как оригинальные (то есть без автора), 
в общем списке их могут видеть все пользователи
 
## UI / API
Проект реализовывается в виде веб-сайта

Архитектура, диаграммы и некоторые пользовательские сценарии:
https://miro.com/app/board/uXjVNOVcT6c=/?share_link_id=679770638265

## Технологии разработки
### Языки программирования
* Python Django
* JS
### СУБД
* PostgreSQL

## Тестирование
* Тестирование пользовательского интерфейса - проверка на корректность
отображения интерфейса и его элементов
* Тестирование пользовательских сценариев - создание некоторых
сценариев, основанных на типичных действиях пользователей,
проверка на корректность работы сайта при них
* Модульное тестирование - проверка входных и выходных данных для
каждой функции приложения, проверка работы отдельных функций, таких как
добавление продуктов, магазинов, цен, а также расчет оптимального
выбора магазинов
* Тестирование импорта данных - проверка корректности импорта
таблицы цен для других пользователей

## Структура БД
https://lucid.app/lucidchart/76d604a4-8063-4ed8-876e-46c6e4a8587f/edit?invitationId=inv_508c6e08-cf5c-4622-988a-78ded2984e8b
