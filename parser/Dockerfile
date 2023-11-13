FROM python:3.11-bookworm
WORKDIR /usr/src/habr_parser
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN chmod +x wait-for-it.sh docker-entrypoint.sh
ENTRYPOINT ["/usr/src/habr_parser/docker-entrypoint.sh"]
CMD [ "python", "main.py" ]
