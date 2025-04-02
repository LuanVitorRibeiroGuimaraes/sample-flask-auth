from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

#criar e verificar tabelas:
# with app.app_context():
#     db.create_all()
#     print(db.inspect(db.engine).get_table_names())
