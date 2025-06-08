from app import db , app1, JSONB

#описание схемы таблицы
class Names(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        array_of_names = db.Column(JSONB)

#cоздание таблицы
with app1.app_context(): # явное создание контекста приложения(без него flaskSQLAlchemy ругается)
        db.create_all()
        db.session.commit()

app1.run(host='0.0.0.0')
