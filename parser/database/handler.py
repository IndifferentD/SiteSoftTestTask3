from peewee import PostgresqlDatabase

credentials={
  # "host": "192.168.180.147",
  # "port": "5435",
  "host": "parser_db",
  "port": "5432",
  "user": "parser",
  "database": "habr"
}



database_handler = PostgresqlDatabase(**credentials)
