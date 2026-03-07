# Глоссарий терминов ВКР

### Установка зависимостей

```
pip install -r requirements.txt
```

### Запуск


Для запуска необходимо воспользоваться следующей командой
```
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```


### Сборка Docker-контейнера

```
docker buildx build --platform linux/amd64,linux/arm64 -t skoptenco/glossary-web:latest --push .
```
