FROM python:3.10.2

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

# Instalar dependencias necesarias para TA-Lib
RUN apt-get update && apt-get install -y \
    build-essential \
    wget \
    tar

# Descargar e instalar TA-Lib
RUN wget https://anaconda.org/conda-forge/libta-lib/0.4.0/download/linux-64/libta-lib-0.4.0-h166bdaf_1.tar.bz2 && \
    mkdir -p /usr/lib/x86_64-linux-gnu/lib && \
    tar xjf libta-lib-0.4.0-h166bdaf_1.tar.bz2 -C /usr/lib/x86_64-linux-gnu/lib --strip-components=1 && \
    rm libta-lib-0.4.0-h166bdaf_1.tar.bz2

RUN wget https://anaconda.org/conda-forge/ta-lib/0.4.19/download/linux-64/ta-lib-0.4.19-py310hde88566_4.tar.bz2 && \
    mkdir -p /usr/local/lib/python3.10/dist-packages/talib && \
    tar xjf ta-lib-0.4.19-py310hde88566_4.tar.bz2 -C /usr/local/lib/python3.10/dist-packages/talib --strip-components=3 && \
    rm ta-lib-0.4.19-py310hde88566_4.tar.bz2

ENV BOT_TOKEN="6575277104:AAGLL8gGGT65SU_gIX5KBdkV47fLVbTO9mI"

CMD ["python3","-u", "main.py"]
