FROM python:3.12.5-slim@sha256:59c7332a4a24373861c4a5f0eec2c92b87e3efeb8ddef011744ef9a751b1d11c

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ftk_pieces_api ftk_pieces_api

EXPOSE 8000
CMD ["uvicorn", "ftk_pieces_api.main:app", "--host", "0.0.0.0", "--port", "8000"]