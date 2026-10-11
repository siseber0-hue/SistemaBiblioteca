<div align="center">

# 📚 Sistema de Gestión para Biblioteca Universitaria

**Proyecto académico desarrollado en Python con Programación Orientada a Objetos**

[![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Estado](https://img.shields.io/badge/Estado-Acad%C3%A9mico-blue)]()
[![Asignatura](https://img.shields.io/badge/Asignatura-Lenguaje%20de%20Programaci%C3%B3n%201-2E8B57)]()

</div>

---

## 📝 Descripción

Este proyecto consiste en un sistema básico para gestionar una biblioteca universitaria. Permite representar materiales bibliográficos y estudiantes, así como controlar las operaciones de préstamo y devolución.

El proyecto se desarrolla como parte de la asignatura **Lenguaje de Programación 1** y aplica conceptos de programación orientada a objetos en Python.

## 🎯 Objetivos

- Modelar libros, revistas, estudiantes y préstamos mediante clases.
- Consultar la disponibilidad de los materiales bibliográficos.
- Registrar préstamos relacionando un material con un estudiante.
- Gestionar devoluciones y actualizar la disponibilidad.
- Aplicar encapsulación, abstracción, herencia y polimorfismo.
- Validar operaciones y manejar errores mediante excepciones.

## ⚙️ Funcionalidades principales

- 📖 Consulta del catálogo de libros y revistas.
- 👤 Registro de los datos esenciales del estudiante durante el flujo de préstamo.
- 📥 Registro de préstamos de materiales disponibles.
- 📤 Registro de devoluciones.
- 🔎 Consulta de préstamos activos del estudiante.
- 🛡️ Validación de datos y prevención de préstamos incompatibles.

> **Nota:** las opciones disponibles pueden depender de la versión final del código entregado.

## 🧱 Diseño orientado a objetos

| Clase | Responsabilidad |
|---|---|
| `MaterialBibliografico` | Clase abstracta que define las operaciones comunes de préstamo, devolución y consulta del estado. |
| `Libro` | Representa un libro y administra sus datos y disponibilidad. |
| `Revista` | Representa una revista como otro tipo de material bibliográfico. |
| `Estudiante` | Almacena el identificador, nombre y carrera del estudiante. |
| `Prestamo` | Relaciona un material bibliográfico con un estudiante y registra la fecha del préstamo. |
| `Biblioteca` | Administra el catálogo y coordina los préstamos y las devoluciones. |

### Conceptos aplicados

- **Encapsulación:** los atributos se manejan como atributos internos y se exponen mediante propiedades cuando corresponde.
- **Abstracción:** `MaterialBibliografico` establece un contrato común para los materiales.
- **Herencia:** `Libro` y `Revista` derivan de `MaterialBibliografico`.
- **Polimorfismo:** la biblioteca puede procesar diferentes tipos de materiales mediante operaciones comunes.
- **Excepciones personalizadas:** se utilizan para representar errores de datos u operaciones de préstamo no permitidas.

## 🛠️ Tecnologías y requisitos

- **Python 3.8 o superior**
- Editor de código, por ejemplo Visual Studio Code.
- No se requieren paquetes externos si el código utiliza únicamente la biblioteca estándar de Python.

## ▶️ Cómo ejecutar el programa

1. Descarga o clona este repositorio.
2. Abre una terminal en la carpeta raíz del proyecto.
3. Ejecuta:

```bash
python src/sistema_biblioteca.py
```

En algunos equipos, el comando puede ser:

```bash
python3 src/sistema_biblioteca.py
```

Si el archivo principal tiene un nombre diferente en la versión final, utiliza ese nombre en el comando.

## 📁 Estructura del proyecto

```text
SistemaBiblioteca/
├── src/
│   └── sistema_biblioteca.py
├── docs/
│   ├── analisis_requerimientos.pdf
│   └── diagrama_clases.png
└── README.md
```

- `src/`: contiene el código fuente del sistema.
- `docs/`: contiene el análisis de requerimientos y el diagrama de clases.
- `README.md`: presenta el proyecto y explica cómo ejecutarlo.

## 📄 Documentación

En la carpeta `docs/` se incluye el documento de análisis y diseño, que contempla:

- Planteamiento del problema.
- Cinco requerimientos funcionales.
- Tres restricciones del sistema.
- Diagrama de clases UML.
- Responsabilidades y justificación de las clases.

## ⚠️ Alcance y limitaciones

El sistema es una implementación académica básica. Si la información se almacena en estructuras en memoria, los registros no se conservan después de cerrar el programa. El proyecto no contempla, salvo que se añada posteriormente, una base de datos permanente, autenticación de usuarios, multas, reservas ni una interfaz gráfica.

## 👥 Integrantes

- **MARCO ANTONIO**
- **ARMANDO TORRES**
- **FERNANDA VILLEGAS**

**Grupo:** B  
**Asignatura:** Lenguaje de Programación 1

---

<div align="center">

Desarrollado con 🐍 Python para el aprendizaje de programación orientada a objetos.

</div>
