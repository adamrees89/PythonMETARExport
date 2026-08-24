FROM python:3.12-slim AS build

WORKDIR /app
COPY requirements.txt ./
RUN pip install --prefix=/install --no-cache-dir -r requirements.txt

FROM python:3.12-slim
WORKDIR /app
COPY --from=build /install /usr/local
COPY . /app
EXPOSE 8000
CMD ["python", "metarGet.py"]
