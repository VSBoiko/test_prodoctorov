ПроДокторов

Тестовое задание - Junior Python разработчик (Django)

Есть API для получения списка задач и api для получения списка юзеров:
`https://json.medrating.org/todos`
`https://json.medrating.org/users`

Используя только эти API составить отчёты по всем юзерам в отдельных текстовых файлах.

После запуска скрипта, рядом должна появиться директория "tasks" с текстовыми файлами. 
Файл называть по username пользователя в формате "Antonette.txt". 
Внутри файла на первой строке записывать “Отчёт для ”, название компании, в которой работает юзер, в конце ставить точку. 
На второй строке писать полное имя, и рядом в < > записывать email. 
Через пробел от email записывать время составления отчёта в формате 23.09.2020 15:25. 
На третьей строке указывать общее количество задач: “Всего задач: 15”.
Четвёртая строка должна быть пустой.
На пятой строке "Завершённые задачи (N):", где N - это количество завершённых задач. 
Далее, список названий завершённых задач.
После завершённых задач через пустую строку записать "Оставшиеся задачи (M):", где M - количество оставшихся задач. И вывести стальные задачи.
Если название задачи больше 48 символов, то обрезать до 48 символов и добавить троеточие.


Пример файла:

```
Отчёт для Deckow-Crist.
Ervin Howell <Shanna@melissa.tv> 23.09.2020 15:25
Всего задач: 4

Завершённые задачи (2):
distinctio vitae autem nihil ut molestias quo
est ut voluptate quam dolor

Оставшиеся задачи (2):
suscipit repellat esse quibusdam voluptatem incu...
laborum aut in quam
```



Если файл для пользователя уже существует, то существующий файл переименовать, добавив в него время составления этого старого отчёта в формате "old_Antonette_2020-09-23T15:25.txt"
Таким образом, актуальный отчёт всегда будет без даты в названии. Старые отчёты не удаляются, а переименовываются.


Код должен быть чистым, без необоснованных повторений, с выделением функций, где это уместно, с говорящими именами.
Код сделать максимально эффективным, но не в ущерб читабельности. 
Подсказка: следует избегать частых записей на диск.
Предусмотреть возможные сбои в сети или при записи на диск. 
Не должно быть наполовину сформированных файлов. 
Либо файл есть и он целиком корректный, либо его нет.
Если по юзеру однажды был создан отчёт, то всегда должен существовать актуальный отчёт без даты в названии. 
Не должно быть такого, что из-за сбоя в сети или т.п. остались только файлы с датами в названиях.
Если какие-то моменты не обговорены в задаче, то продумайте плюсы и минусы возможных вариантов, и выберите наиболее подходящий на ваш взгляд, чтобы потом можно было обосновать своё решение.
Предусмотреть крайние случаи (у пользователя нет задач, и т.п.).

Код должен быть оформлен по pep8.

Использовать местное время.

Программа должна корректно работать на linux (Debian, Ubuntu).

Можно использовать любые библиотеки.