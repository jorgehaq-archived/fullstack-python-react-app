# Backend - Aplicación Fullstack con Arquitectura Limpia

Este es el backend de la aplicación, implementado con FastAPI siguiendo los principios de Clean Architecture (Arquitectura Limpia) y SOLID.

## Características

- Framework FastAPI para alto rendimiento
- GraphQL con Strawberry para consultas flexibles
- Arquitectura limpia con capas de dominio bien definidas
- Implementación de los principios SOLID
- SQLAlchemy y Alembic para ORM y migraciones
- PostgreSQL como base de datos
- Docker para desarrollo y producción

## Estructura del Proyecto



backend/ ├── alembic/ # Migraciones de base de datos ├── app/ │ ├── api/ # Capa de API (GraphQL, REST) │ ├── core/ # Configuración y utilidades core │ ├── domain/ # Capa de dominio (entidades, servicios, interfaces) │ ├── infrastructure/ # Implementaciones concretas y dependencias externas │ └── main.py # Punto de entrada de la aplicación ├── scripts/ # Scripts de utilidad └── tests/ # Pruebas



## Requisitos

- Python 3.11+
- Poetry (para gestión de dependencias)
- PostgreSQL
- Docker (opcional)

## Instalación y Configuración

### Usando Poetry

1. Clonar el repositorio


git clone https://github.com/tuusuario/fullstack-app.git cd fullstack-app/backend



2. Instalar dependencias con Poetry


poetry install


3. Activar el entorno virtual


poetry shell



4. Configurar variables de entorno


cp .env.example .env

# Editar .env con tus configuraciones



5. Crear y aplicar migraciones


python scripts/create_initial_migration.py alembic upgrade head



6. Inicializar datos


python scripts/seed_initial_data.py



7. Ejecutar la aplicación


uvicorn app.main:app --reload



### Usando Docker

1. Asegúrate de estar en la raíz del proyecto


cd fullstack-app



2. Ejecutar con docker-compose


docker-compose up -d



## Desarrollo

### Ejecutar Pruebas



pytest



### Crear una Nueva Migración

Después de modificar modelos:



alembic revision --autogenerate -m "descripción del cambio" alembic upgrade head



### Acceder al API

- GraphQL: http://localhost:8000/graphql
- Documentación API (Swagger): http://localhost:8000/docs

## Principios SOLID Aplicados

1. **Principio de Responsabilidad Única (SRP)**
   - Cada módulo, clase y función tiene una única responsabilidad
   - Servicios de dominio enfocados en operaciones específicas

2. **Principio Abierto/Cerrado (OCP)**
   - Las entidades están abiertas para extensión pero cerradas para modificación
   - Usamos interfaces y patrones para extender funcionalidad

3. **Principio de Sustitución de Liskov (LSP)**
   - Las implementaciones concretas pueden ser sustituidas por sus abstracciones
   - Pruebas con mocks demuestran este principio

4. **Principio de Segregación de Interfaces (ISP)**
   - Interfaces pequeñas y específicas en lugar de una grande
   - Repositorios y servicios con interfaces bien definidas

5. **Principio de Inversión de Dependencias (DIP)**
   - Las capas de alto nivel no dependen de implementaciones de bajo nivel
   - Dependencias inyectadas a través de constructores

## Contribuir

1. Crea un feature branch desde `develop`
2. Implementa tus cambios siguiendo las convenciones
3. Asegúrate de que las pruebas pasen
4. Envía un pull request a `develop`