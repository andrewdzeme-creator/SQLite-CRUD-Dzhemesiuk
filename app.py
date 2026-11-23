from flask import Flask, abort, redirect, render_template, request, url_for

from database_connector import (
    create_db_table,
    delete_item,
    get_all_items,
    get_item_by_id,
    insert_item,
    update_item,
)

STATUSES = {
    "planned": "Заплановано",
    "reading": "Читаю",
    "read": "Прочитано",
}


def validate_book(form):
    title = form.get("title", "").strip()
    author = form.get("author", "").strip()
    status = form.get("status", "")
    try:
        year = int(form.get("publication_year", ""))
    except ValueError:
        return None, "Введи рік видання числом."

    if not 1 <= len(title) <= 200:
        return None, "Назва має містити від 1 до 200 символів."
    if not 1 <= len(author) <= 120:
        return None, "Ім’я автора має містити від 1 до 120 символів."
    if not 1 <= year <= 9999:
        return None, "Рік видання має бути від 1 до 9999."
    if status not in STATUSES:
        return None, "Вибери статус зі списку."

    return dict(title=title, author=author, publication_year=year, status=status), None


def create_app(config=None):
    app = Flask(__name__)
    if config:
        app.config.from_mapping(config)

    with app.app_context():
        create_db_table()

    @app.get("/")
    def index():
        return render_template("index.html", books=get_all_items(), statuses=STATUSES)

    @app.route("/add", methods=["GET", "POST"])
    def add():
        if request.method == "POST":
            data, error = validate_book(request.form)
            if error:
                return render_template(
                    "form.html", heading="Нова книга", book=request.form,
                    statuses=STATUSES, error=error,
                ), 400
            insert_item(data)
            return redirect(url_for("index"), code=303)
        return render_template(
            "form.html", heading="Нова книга", book={}, statuses=STATUSES,
        )

    @app.route("/edit/<int:book_id>", methods=["GET", "POST"])
    def edit(book_id):
        book = get_item_by_id(book_id)
        if book is None:
            abort(404)
        if request.method == "POST":
            data, error = validate_book(request.form)
            if error:
                return render_template(
                    "form.html", heading="Редагування книги", book=request.form,
                    statuses=STATUSES, error=error,
                ), 400
            if not update_item(book_id, data):
                abort(404)
            return redirect(url_for("index"), code=303)
        return render_template(
            "form.html", heading="Редагування книги", book=dict(book), statuses=STATUSES,
        )

    @app.post("/delete/<int:book_id>")
    def delete(book_id):
        if not delete_item(book_id):
            abort(404)
        return redirect(url_for("index"), code=303)

    return app


if __name__ == "__main__":
    create_app().run()
