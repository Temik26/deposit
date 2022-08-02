# Сервис для расчета депозита

## Cборка сервиса
```
docker build -t deposit .
```

## Запуск сервиса
```
docker run --name deposit -p 8000:8000 -d deposit
```

## Запуск тестов
```
docker exec deposit python manage.py test deposit_account
```



