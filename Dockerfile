FROM python:3.11-bookworm
WORKDIR /app

COPY ./ /app/
RUN pip install scrapy --break-system-packages
CMD ['python3']
