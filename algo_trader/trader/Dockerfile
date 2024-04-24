FROM python:3.10.2

WORKDIR /app

COPY . .

COPY ../lib /app/lib

RUN apt-get update && apt-get install -y \
    wget \
    && rm -rf /var/lib/apt/lists/*

RUN wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz && \
    tar -xzf ta-lib-0.4.0-src.tar.gz && \
    cd ta-lib && \
    ./configure && \
    make && \
    make install && \
    cd .. && \
    rm -rf ta-lib* && \
    pip install ta-lib

RUN pip install -r requirements.txt

ENV BOT_TOKEN="6575277104:AAGLL8gGGT65SU_gIX5KBdkV47fLVbTO9mI"

CMD ["python3","-u", "main.py"]
