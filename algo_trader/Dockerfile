ARG LIB_IMAGE
FROM ${LIB_IMAGE} as builder

FROM python:3.10.2

WORKDIR /usr/src/app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY --from=builder /usr/src/app /usr/src/app/algo_lib

# Set the PYTHONPATH to include the algo_lib directory
ENV PYTHONPATH="/usr/src/app/algo_lib:${PYTHONPATH}"

COPY . .

CMD ["python3", "main.py"]
