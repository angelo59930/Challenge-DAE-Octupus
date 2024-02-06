# Detalles del proyecto
Situación (dominio del problema):

Una empresa de transporte de cargas necesita un software que la ayude a organizarse con la carga de las camiones. La empresa puede recibir requerimiento para transportar packings, cajas sueltas y bidones que transportan líquido.

## Supuestos que se realizaron
- Se asume que una carga no puede ser transportada por mas de un camion

# Uso de la aplicacion
El uso de la aplicacion es bastante basico desde la pagina principal se puede acceder a las diferentes funcionalidades de la aplicacion, las cuales son:
- Crear un camion
- ver los camiones
- ver las cargas

si vemos las cargas podremos
- Crear una carga
- bajar una carga
- subir una carga
  
si vemos los camiones podremos
- ver la informacion de un camion
- editar un camion
- eliminar un camion

si vemos el detalle de un camion podremos
- ver las cargas que tiene un camion
- cambiar el estado del camion
- ver la informacion general del camion


# Ejecucion del proyecto

Para poder ejecutar el proyecto va a ser necesario seguir los siguientes pasos:
1. Configurar nuestro motor de bases de datos (Mysql)
2. Configurar el poryecto Django para que consuma la BD
3. Entrar a la pagina principal

## 1. Configuracion de nuestro motor de bases de datos

Primero tendremos que instalar nuestro gestor de bases de datos, en este caso usaremos mysql, para ello ejecutaremos los siguientes comandos:
```bash
docker pull mysql
docker run -d --name mysql-tecnico -e MYSQL_ROOT_PASSWORD=root -p 3306:3306 mysql:latest
```

Ya teniendo nuestro gestor de bases de datos corriendo, tendremos que crear nuestra base de datos, para ello ejecutaremos los siguientes comandos:
```bash
docker exec -it mysql-tecnico bash
mysql -u root -p root
```

Ya dentro de nuestro gestor de bases de datos, ejecutaremos los siguientes comandos:
```bash
CREATE DATABASE prueba;
```
Ya con la base de datos/schema creado podemos proseguir con la instalacion de la dependencia de python para la conexion a la base de datos
```bash
sudo apt-get install python3-dev default-libmysqlclient-dev build-essential pkg-config # para ubuntu
pip install mysqlclient
```

## 2. Configurar el poryecto Django para que consuma la BD
En este paso vamos a cambiar la configuracion de nuestro proyecto para que se conecte a la base de datos, para ello vamos a modificar el archivo `settings.py` que se encuentra en la carpeta tecnico, y vamos a modificar las siguientes lineas:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'prueba',
        'USER': 'root',
        'PASSWORD': 'root',
        'HOST': '172.17.0.2',
        'PORT': '3306',
    }
}
```
**Notar:** que el host es la ip de nuestro contenedor de docker, para saber cual es la ip ejecutamos el siguiente comando:
```bash
docker inspect mysql-tecnico | grep IPAddress
```
Una vez ya configurado nuestro proyecto para que se conecte a la base de datos, vamos a ejecutar los siguientes comandos para poder correr nuestro proyecto:
```bash
python manage.py makemigrations gestionCarga
python manage.py migrate
```

Y para poder correr nuestro proyecto ejecutamos el siguiente comando:
```bash
python manage.py runserver
```

## 3. Entrar a la pagina principal
Para poder acceder a nuestro proyecto y movernos por el debemos abrir el navegador
e dirigirnos a `localhost:8000/`

# tareas por completar del proyecto

- [x] Crear un camion
- [x] Crear una carga
- [x] si la carga sobrepasa el peso de camion no se crea
- [x] si la carga sobrpasa el 75% del camion no se crea
- [x] cambiar el estado del camion
- [x] Observar el estado de los camiones
- [x] Observar las cargas que tiene un camion
- [x] bajar una carga
- [x] subir una carga
- [x] editar un camion
- [x] eliminar un camion