
# SISTEMA INTEGRAL DE GESTIÓN - SOFTWARE FJ

## Universidad
Universidad Nacional Abierta y a Distancia - UNAD

## Curso
Programación

## Fase
Fase 4 - Componente práctico

## Descripción del proyecto

Software FJ es un sistema integral de gestión de clientes, servicios y reservas, desarrollado en Python mediante los principios de la programación orientada a objetos.

La aplicación permite registrar y validar clientes, administrar servicios de reserva de salas, alquiler de equipos y asesorías especializadas, y gestionar reservas mediante operaciones de creación, confirmación, cancelación y procesamiento.

El sistema utiliza objetos y listas internas para administrar la información, sin implementar bases de datos.

## Objetivo

Desarrollar una aplicación orientada a objetos que permita gestionar clientes, servicios y reservas, aplicando abstracción, herencia, polimorfismo, encapsulamiento y manejo de excepciones para garantizar un funcionamiento organizado y confiable.

## Tecnologías utilizadas

- Python 3
- Visual Studio Code
- Git y GitHub

## Estructura del proyecto

| Archivo | Descripción |
|---|---|
| `main.py` | Programa principal y ejecución de operaciones. |
| `entidades.py` | Clase abstracta Entidad y gestión de clientes. |
| `servicios.py` | Clases de servicios especializados y cálculo de costos. |
| `reservas.py` | Administración y gestión de reservas. |
| `excepciones.py` | Definición de excepciones personalizadas. |
| `logs.py` | Registro de eventos, advertencias y errores. |
| `eventos.log` | Archivo generado para almacenar los registros de ejecución. |
| `README.md` | Documentación general del proyecto. |

## Funcionalidades principales

1. Registro y validación de clientes.
2. Creación de servicios especializados.
3. Reserva de salas, alquiler de equipos y asesorías.
4. Creación, confirmación y cancelación de reservas.
5. Procesamiento de reservas y cálculo de costos.
6. Aplicación de descuentos e impuestos.
7. Control de disponibilidad de servicios.
8. Validación de datos y manejo de excepciones personalizadas.
9. Registro de eventos y errores mediante el módulo `logging`.
10. Consulta y listado de reservas registradas.

## Conceptos de programación orientada a objetos

En el desarrollo del proyecto se aplican los siguientes conceptos:

- **Abstracción:** mediante clases abstractas que establecen estructuras generales.
- **Herencia:** las clases especializadas heredan características de sus clases principales.
- **Polimorfismo:** los diferentes tipos de servicios implementan sus propios métodos de cálculo y descripción.
- **Encapsulamiento:** se utilizan atributos privados y propiedades para controlar el acceso a la información.
- **Manejo de excepciones:** se implementan excepciones personalizadas para controlar errores y validaciones.

## Requisitos para ejecutar el proyecto

- Tener instalado Python 3.
- Contar con un editor de código, preferiblemente Visual Studio Code.
- Disponer de los archivos del proyecto en una misma carpeta.

No se requieren bases de datos ni instalaciones de librerías externas.

## Instrucciones de ejecución

1. Descargar o clonar el repositorio.
2. Abrir la carpeta del proyecto en Visual Studio Code.
3. Abrir una terminal desde la carpeta principal.
4. Ejecutar el siguiente comando:

```bash
python main.py
```

5. Observar en la terminal los resultados de las operaciones y las validaciones realizadas.

## Almacenamiento y registros

El sistema no utiliza bases de datos. La información se administra mediante objetos y listas internas durante la ejecución del programa.

El módulo `logs.py` utiliza la biblioteca estándar `logging` de Python para registrar eventos y errores en el archivo `eventos.log`.

Este archivo se crea o actualiza automáticamente cuando se ejecuta el sistema.

## Autoría

Proyecto académico desarrollado para la Fase 4 del componente práctico del curso de Programación de la UNAD.
