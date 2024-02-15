FROM python:3.9

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

RUN python initProdDatabase.py

EXPOSE 80

CMD ["gunicorn", "-k", "geventwebsocket.gunicorn.workers.GeventWebSocketWorker", "-w", "1", "serve:app", "--bind", "0.0.0.0:80"]