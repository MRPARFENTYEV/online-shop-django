# Вас приветствует онлайн магазин "Потный айтишник".
#### Клонируйте проект к себе на компьютер *git clone https://github.com/MRPARFENTYEV/online-shop-django.git*
#### Создайте миграции *python manage.py makemigrations*
#### Примените миграции *python manage.py migrate*
#### Запустите проект  *python manage.py runserver*
#### Создайте суперпользователя *python manage.py createsuperuser*
#### Заходите в админку *http://127.0.0.1:8000/admin/*
#### Создайте магазин, просто пропишите его название и слаг. (Предполагается, что онлай магазин "Потный айтишник" - это платформа, на которой размещаются продавцы)
#### Внесите товары в базу данных ( каритинки в media > products, записи можно взять в that_was_my_data), но на самом деле создать три, четыре товара будет легко, главное заполнить все поля внутри админки. Не забудьте прописать слаги, когда создаете товары и категории, по ним происходит много операций. Слаги товаров, потом автоматически дополнятся уникальными интендификаторами. Когда магазин заполнен, смотрите вверх вправо, там есть надпись - перейти на сайт, кликайте по ней.

## Как работать с сайтом?

#### В папке проекта that_was_my_data можно найти файлы, которыми я пользовался для тестирования. Если понадобятся.

### Всего предусмотрено 4 роли:
### 1- Админ.
#### Вы его зарегестрировали создав суперпользователя.
#### Админ в админке заполняет магазин товарами.  Может счелкать статусами товаров, может удалять вредных пользователей, и делать все доступное в рамках проекта.
#### *На главной страничке можно побаловаться, посмотреть товары, добавить их в избранное, даже оформить заказ, если адреса нет, то функция автоматически пошлет вас его заполнять*
#### ![изображение](https://github.com/MRPARFENTYEV/online-shop-django/assets/110676672/1a03c8a8-ddd6-45c5-8260-434674796c53)
#### *Можно посмотреть детали интересующего продукта*
#### ![изображение](https://github.com/MRPARFENTYEV/online-shop-django/assets/110676672/5fdc7070-05ba-45f0-9aea-0c32b267a042)
#### *Если нажать на ссылку продавца, то товары отсортируются по магазину*
#### ![изображение](https://github.com/MRPARFENTYEV/online-shop-django/assets/110676672/38de50fd-e63d-4f2a-abaf-c6ffd298384e)

### 2 - Менеджер. 
#### Регистрируется как пользователь, админ должен дать ему права быть менеджером. Я через dbeaver просто ставлю в user.is_admin галочку и надо прописать ему название магазина, например BigPig. Прописывается название магазина в user.store_name . 

#### *Менеджер может смотреть список покупок из магазина к которому он прикреплен. Логинитесь менеджером, заходите в профиль > менеджерам. Там можно посмотреть список покупок в магазине и обновить цены из excel файла. Тут важно: файл должен быть правильным. Я закинул две штуки в папку price_operations в проекте.* 
#### ![изображение](https://github.com/MRPARFENTYEV/online-shop-django/assets/110676672/098891c0-91ee-4109-81fd-08c2bc52b828)

#### *Можно делать товар доступным/недоступным . Тыкаете на домашнюю страницу и выбираете товар( при этом вы вошли за менеджера). Например решили выключить PigaphoneProXL.  Слева от картинки товара будет окошко. Если хотите, чтобы товар был виден ставьте голочку. Не хотите не ставьте галочку. Товар выключится из домашней странички, его нельзя будет добавить в корзину.*
#### ![изображение](https://github.com/MRPARFENTYEV/online-shop-django/assets/110676672/cc33fbf0-aafb-42e4-9075-dadb8acb4a31)

### 3 - Анонимный пользователь.
#### Эта роль только для того чтобы посчелкать на иконки, долго незарегистрированным анонимом вы не пробудите.

### 4 - Пользователь.
#### Становится таковым из анонимного пользователя после проходжения регистрации. Для регистрации идете на главной страничке во вкладку "Регистрация", она сверху справа.
Вводите имейл, введите действующий, имя, пароль. После того как нажмете 'Подтвердить', вам на почту отправится письмо
со сгенерированной ссылкой.
#### ![изображение](https://github.com/MRPARFENTYEV/online-shop-django/assets/110676672/a688be03-ba22-4993-9c0e-99028e658513)
#### ![изображение](https://github.com/MRPARFENTYEV/online-shop-django/assets/110676672/dbb5069f-1b51-4ac9-be47-dc32b8895319)
#### ![изображение](https://github.com/MRPARFENTYEV/online-shop-django/assets/110676672/8ba5a8ff-a832-479f-ac49-795c9981e685)
#### ![изображение](https://github.com/MRPARFENTYEV/online-shop-django/assets/110676672/b6d0f0cf-a067-478f-ac58-7f6937b37f89)
#### Служба безопасности найдет ее подозрительной, поищите в спаме. Если не приходит, посмотрите в файле online_shop > settings.py, EMAIL_HOST_USER. 

#### Перейдя по ссылке вы верифицируетесь. Теперь если товары доступны, вы можете добавлять их в избранное (сердечко сверху) и добавлять их в корзину (рядом с сердечком). При попытке сделать заказ может перебросить на заполнение адреса. Придется заполнить. Когда подтверждаете заказ, он создается, менеджеру магазина на почту идет письмо, что вы что-то заказали, и вам на почту идет письмо,что заказ создан. Потом автоматически задействуется функция ненастоящего платежа и после нее вам приходит письмо с деталями заказа. Посмотреть все заказы можно в профиле (справа сверху) там их для вас список.Пользователь может сменить пароль, имя, адрес.
#### ![изображение](https://github.com/MRPARFENTYEV/online-shop-django/assets/110676672/9d21fb9a-5b92-4277-aff2-19124e24ff16)
#### ![изображение](https://github.com/MRPARFENTYEV/online-shop-django/assets/110676672/94c9455a-8177-422b-ad4f-33bc14fb2d09)

#### Онлайн магазин - "Потный айтишник", с нами вы проведете время незабываемо.

#### Список исправлений:

#### https://pypi.org/project/django-bootstrap4/
#### Добавлены bootstrap4/crispy формы
Было: ![img.png](img.png)
Стало: ![img_1.png](img_1.png)

