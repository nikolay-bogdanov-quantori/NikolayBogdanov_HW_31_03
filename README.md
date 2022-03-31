# NikolayBogdanov_HW_31_03
--- краткие описания таблиц. 
---
"heroes"
 -- содержит столбцы id, имя героя, его сторона, дата рождения и числовой показатель силы в бою
 относится:
 --- к самой себе как many-to-many, промежуточной таблицей в этом отношении служит таблица battles
 --- к таблице motos как one-to-many
 --- к таблице stories как one-to-one (обеспечивается констрейнтом UNIQUE для hero_id в таблице историй
 
"motos"
 -- содержит id, id героя, к которому принадлежит, порядковый номер девиза для соответсвующего героя, текст девиза
  
  "stories"
-- содержит id, id героя, к которому принадлежит, текст истории

--- примеры как запускать докер на разных стейджингах.
---
из корневой папки репозитория

для DEV:

docker-compose up -d --build

для PROD:

docker-compose -f docker-compose.prod.yml up -d --build

--- примеры как запускать python скрипты.
---
список аргументов для передачу в функцию для каждого <script_name> можно узнать так:

docker-compose run --entrypoint python --rm client scripts.py <script_name> -h

пример 

docker-compose run --entrypoint python --rm client scripts.py add_hero -h


**добавить героя**

docker-compose run --entrypoint python --rm client scripts.py add_hero -n "some hero name" -s "Imperium of Man" -p 9


**добавить битву между случайно выбранными героями с разных сторон**

docker-compose run --entrypoint python --rm client scripts.py add_battle

**добавить девиз для героя**

docker-compose run --entrypoint python --rm client scripts.py add_moto -hid 1 -moto "some another moto for hero with id == 9"

**добавить историю для героя, у которого ее еще нет**

docker-compose run --entrypoint python --rm client scripts.py add_story -hid 9 -s "some story"

**удалить героя**

docker-compose run --entrypoint python --rm client scripts.py del_hero -hid 4
