FROM python:3.10.2

WORKDIR /app

COPY trader .

COPY lib /app/lib

RUN pip install -r requirements.txt

ENV BOT_TOKEN="6575277104:AAGLL8gGGT65SU_gIX5KBdkV47fLVbTO9mI"

CMD ["python3","-u", "main.py"]
