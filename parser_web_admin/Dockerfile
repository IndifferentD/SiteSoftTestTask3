FROM python:3.11-bookworm
WORKDIR /usr/src/parser_web_admin
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
RUN chmod +x wait-for-it.sh docker-entrypoint.sh
ENTRYPOINT ["/usr/src/parser_web_admin/docker-entrypoint.sh"]
CMD  ["python", "manage.py", "runserver", "0.0.0.0:8000"]
