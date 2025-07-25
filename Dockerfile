FROM node:18 as frontend-build
WORKDIR /frontend
COPY frontend/ .
RUN npm install
RUN npm run build

FROM python:3.10-slim
WORKDIR /backend
COPY backend/ .
RUN pip install flask pymupdf sentence-transformers torch

COPY --from=frontend-build /frontend/build /backend/static

EXPOSE 5000
CMD ["python", "app.py"]
