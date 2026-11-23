# Каталог книг

Навчальний застосунок Flask і SQLite для лабораторної роботи №6–7.

## Запуск

```sh
python -m venv venv
. venv/bin/activate
python -m pip install -r requirements.txt
python app.py
```

Відкрий http://127.0.0.1:5000. У Windows середовище активується командою
`venv\Scripts\activate` у командному рядку. Файл `data.db` створюється автоматично.

| Маршрут | Дія |
| --- | --- |
| `GET /` | Список книг |
| `GET /add`, `POST /add` | Форма та створення книги |
| `GET /edit/<id>`, `POST /edit/<id>` | Завантаження форми й оновлення |
| `POST /delete/<id>` | Видалення та повернення до списку |

Локальна історія Git додається в архіві як `history.bundle`. Щоб відкрити проєкт
разом із цією історією, виконай `git clone history.bundle SQLite-CRUD-Dzhemesiuk-git`
із кореня розпакованого архіву.
