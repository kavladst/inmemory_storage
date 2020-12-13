# Inmemory storage

## Запуск

Запуск приложения:
    
    docker-compose build
    docker-compose up

Запуск тестов:

    cd tests/functional
    docker-compose build
    docker-compose up 

## Использование

Чтобы подключиться к клиенту, можно использовать telnet:

    telnet localhost 8080

Для авторизации используюся команды:

1. **REGISTER** ***username password*** - регистрация в системе
2. **LOGIN** ***username password*** - вход в систему
3. **LOGOUT** - выход из системы

        REGISTER name password
        OK
        LOGOUT
        OK
        LOGIN name password
        OK

После авторизации можно использвать операторы (у каждого пользователя свое хранилище):

1. **SET** ***key*** ***value*** ***[EX seconds | PX milliseconds] [NX | XX]*** - устрановить значение по ключу с параметрами (EX - TTL в секундаъ, PX - TTL в милисекундах, NX - установить значение, если ключ не существует, XX - установить значение, если ключ существует)
2. **GET** ***key*** - получить значение по ключу
3. **DEL** ***key [key ...]*** - удалить все ключи из списка
4. **KEYS** - получить все ключи

        SET key value EX 10 NX
        OK
        KEYS
        ['key']
        GET key
        value

5. **HSET** ***key field value [field value ...]*** - установить словарь по ключу с задаными парами {*field*, *value*}
6. **HGET** ***key field*** - получить значение из словоря по ключу и полю

        HSET key field_1 value_1 field_2 value_2
        2
        HGET key field_1
        value_1
        HGET key field_2
        value_2
        DEL key
        1

7. **RPUSH** ***key element [element ...]*** - установить список по ключу со задаными елементами
8. **LSET** ***key index element*** - установить значение по ключу и индексу
9. **LGET** **key index**** - получить значение по ключу и индексу

        RPUSH key value_0 value_1 value_2
        3
        RPUSH key value_3
        4
        LGET key 0
        value_0
        LSET key 0 new_value_0
        OK
        LGET key 0
        new_value_0

10. **SAVE** - сохранить хранилище текущего пользователя на диск сервера

        SAVE
        OK

PS: Swagger REST доступен в корневом пути (http://localhost:8000/)