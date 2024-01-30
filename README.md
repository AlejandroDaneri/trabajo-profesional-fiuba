# Trabajo Profesional | Algo Trading

<img src="image.jpeg" />

# Algo Compose

Este es un proyecto de Docker Compose que consta de dos servicios: `lib` y `algo_api`. Estos servicios están diseñados para trabajar juntos y proporcionar una plataforma integral para ejecutar algoritmos.

## Servicios

### 1. lib

El servicio `lib` se encarga de la lógica del algoritmo. Está construido a partir del código fuente ubicado en el directorio `./lib`. El directorio se monta en el contenedor en el directorio `/app`, y el servicio trabaja en ese directorio.

#### Construcción y Ejecución del Servicio

```bash
# Construye el servicio lib
docker-compose build lib

# Ejecuta solo el servicio lib
docker-compose run lib
```

Volumen

    Host: ./lib
    Contenedor: /app

### 2. algo_api

El servicio algo_api proporciona una interfaz de programación de aplicaciones (API) para interactuar con el servicio lib. Se construye utilizando el código fuente ubicado en el directorio ./algo_api. Este directorio se monta en el contenedor en /go/src/app, y el servicio trabaja en ese directorio.

#### Construcción y Ejecución del Servicio

```bash
# Construye el servicio algo_api
docker-compose build algo_api

# Ejecuta solo el servicio algo_api
docker-compose run algo_api
```

Volumen

    Host: ./algo_api
    Contenedor: /go/src/app

### 3. couchdb

El servicio couchdb proporciona una base de datos NoSQL para almacenar datos necesarios para los algoritmos. Se construye utilizando el servicio CouchDB.

### Telegram

Para conectarse al servicio de alertas de telegram, se debe ingresar al siguiente link [SatoshiFiubaBot](https://t.me/SatoshiFiubaBot) y escribir `/start`. Para renovar las alertas, diariamente, se deberá iniciar la conversación con el bot.

#### Construcción y Ejecución del Servicio

```bash
# Construye el servicio couchdb
docker-compose build couchdb

# Ejecuta solo el servicio couchdb
docker-compose run couchdb
```

## Uso

Clona este repositorio:

```bash
git clone https://github.com/tu_usuario/tu_repositorio.git
```

Navega al directorio del repositorio:

```bash
cd tu_repositorio
```

Ejecuta el contenedor con ambos servicios:

```bash
docker-compose up
```

Esto iniciará los servicios lib y algo_api. Puedes acceder a la API a través de la interfaz proporcionada por algo_api para interactuar con los algoritmos proporcionados por lib.

## Licencia

Este proyecto está bajo la licencia MIT.
