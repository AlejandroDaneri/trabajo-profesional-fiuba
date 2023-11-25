# Trabajo Profesional | Algo Trading

<img src="image.jpeg" />

# Algo Compose

Este es un proyecto de Docker Compose que consta de dos servicios: `algo_lib` y `algo_api`. Estos servicios están diseñados para trabajar juntos y proporcionar una plataforma integral para ejecutar algoritmos.

## Servicios

### 1. algo_lib

El servicio `algo_lib` se encarga de la lógica del algoritmo. Está construido a partir del código fuente ubicado en el directorio `./algo_lib`. El directorio se monta en el contenedor en el directorio `/app`, y el servicio trabaja en ese directorio.

#### Construcción y Ejecución del Servicio

```bash
# Construye el servicio algo_lib
docker-compose build algo_lib

# Ejecuta solo el servicio algo_lib
docker-compose run algo_lib
```

Volumen

    Host: ./algo_lib
    Contenedor: /app

### 2. algo_api

El servicio algo_api proporciona una interfaz de programación de aplicaciones (API) para interactuar con el servicio algo_lib. Se construye utilizando el código fuente ubicado en el directorio ./algo_api. Este directorio se monta en el contenedor en /go/src/app, y el servicio trabaja en ese directorio.

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

Esto iniciará los servicios algo_lib y algo_api. Puedes acceder a la API a través de la interfaz proporcionada por algo_api para interactuar con los algoritmos proporcionados por algo_lib.

## Licencia

Este proyecto está bajo la licencia MIT.
