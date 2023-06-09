# Проект NewsProject
### Учебный проект "Новостной портал" в рамках обучения на платформе SkillFactory по курсу Fullstack разработчик на Python.

Новостной портал — это сайт, разворачиваемый в оболочке фреймворка Django. 
1.	При авторизации на сайте, реализованной при помощи Allauth, пользователю даётся возможность стать автором и после этого - написать статью или новость. Каждой публикации присваивается категория (новость, статья), а также категория новости (спорт, экономика и пр.). При добавлении новой публикации необходимо указать параметры категории. У каждого автора добавлен рейтинг по умолчанию равный 0.
2.	На главной странице реализована возможность подписки на категорию новостей. При нажатии на название категории происходит переход на страницу со списком новостей выбранной категории и возможностью подписаться на неё. 
3.	При подписке на определённую категорию на почту подписчика приходит письмо об этом. Реализована рассылка на почту подписчика со списком публикаций за неделю.
4.	На главной странице находится список новостей. При переходе на каждую новость открывается подробная информация с полным текстом, автором и возможностью редактировать и удалять новость. 
5.	Реализована возможность поиска публикаций по названию, категории поста и дате. При выборе критериев поиска формируется и выводится список публикаций.
6.	Выдача прав на определённые действия (редактирование, удаление публикаций) реализована через панель администратора. Созданы группы пользователей. У группы "Авторы" расширенные права. У простого пользователя (не автора) возможности ограничены только просмотром новостей и подпиской на них.
7.	При регистрации нового пользователя к нему на почту, указанной при регистрации, приходит письмо с подтверждением и ссылкой на сайт. Также администратору сайта приходит уведомление о новом пользователе.


В процессе обучения в конце каждого модуля даётся определённое задание по добавлению функционала в проект.

Итоговое задание 13.4
Настоящие системы логирования очень распределенные и орудуют большим количеством связанных компонентов. Давайте попробуем создать подобный механизм. Ваши настройки логирования должны выполнять следующее:

В консоль должны выводиться все сообщения уровня DEBUG и выше, включающие время, уровень сообщения, сообщения. Для сообщений WARNING и выше дополнительно должен выводиться путь к источнику события (используется аргумент pathname в форматировании). А для сообщений ERROR и CRITICAL еще должен выводить стэк ошибки (аргумент exc_info). Сюда должны попадать все сообщения с основного логгера django.
В файл general.log должны выводиться сообщения уровня INFO и выше только с указанием времени, уровня логирования, модуля, в котором возникло сообщение (аргумент module) и само сообщение. Сюда также попадают сообщения с регистратора django.
В файл errors.log должны выводиться сообщения только уровня ERROR и CRITICAL. В сообщении указывается время, уровень логирования, само сообщение, путь к источнику сообщения и стэк ошибки. В этот файл должны попадать сообщения только из логгеров django.request, django.server, django.template, django.db.backends.
В файл security.log должны попадать только сообщения, связанные с безопасностью, а значит только из логгера django.security. Формат вывода предполагает время, уровень логирования, модуль и сообщение.
На почту должны отправляться сообщения уровней ERROR и выше из django.request и django.server по формату, как в errors.log, но без стэка ошибок.
Более того, при помощи фильтров нужно указать, что в консоль сообщения отправляются только при DEBUG = True, а на почту и в файл general.log — только при DEBUG = False.

