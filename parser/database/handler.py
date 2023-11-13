from peewee import PostgresqlDatabase

credentials={
  "host": "parser_db",
  "port": "5432",
  "user": "parser",
  "database": "habr"
}

database_handler = PostgresqlDatabase(**credentials)
