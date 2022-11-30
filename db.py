# The benefits of ORM, Object Relational Mapping, are:
# 1. Multi-threading support.
# 2. Table and columns creation handling automatically.
# 3. Easier DB migrations.
# 4. A more clean, short and elegant code.
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()  # Creates a SQLAlchemy object (which later can be linked to our Flask App)
