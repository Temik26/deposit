# Сервис для расчета депозита

## Cборка сервиса
```
docker build -t deposit .
```

## Запуск сервиса
```
docker run --name deposit -p 8000:8000 -d deposit
```

## Проведение миграций
```
docker exec deposit python manage.py migrate
```

## Запуск тестов
```
docker exec deposit python manage.py test deposit_account
```
## Отчет о покрытии кода тестами находится в htmlcov/index.html