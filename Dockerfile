FROM python:3.10-bookworm

WORKDIR /clientmanage

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY .  .

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]


# CMD ["gunicorn", "cm.wsgi:application", "--bind", "0.0.0.0:8000"]