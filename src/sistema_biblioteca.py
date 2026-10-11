#===================================================================================================

"""Sistema de gestión de una biblioteca."""

"""integrantes: BLAS BALDEON VERONICA, JOSÉ MANUEL INCHUÑA RUIZ, y EBER VILLASANTE MAMANI """
"""Grupo: B"""

"""Asignatura: Lenguaje de Programación 1"""

#====================================================================================================

# ABC y abstractmethod permiten crear clases abstractas y definir
# métodos que las clases hijas están obligadas a implementar.
from abc import ABC, abstractmethod

# datetime registra fechas y horas; timedelta permite calcular
# las fechas límite de devolución sumando días.
from datetime import datetime, timedelta

from typing import List, Optional


# ============================================================
# MANEJO DE EXCEPCIONES
# Las excepciones personalizadas identifican errores concretos
# y permiten controlarlos sin cerrar inesperadamente el programa.
# ============================================================

class MaterialYaPrestadoError(Exception):
    """Error cuando no hay ejemplares disponibles o el préstamo se repite."""
    pass


class DatosInvalidosError(Exception):
    """Error cuando faltan datos o estos no son válidos."""
    pass


# ============================================================
# JERARQUÍA DE CLASES Y ABSTRACCIÓN
# MaterialBibliografico es la clase padre abstracta.
# Libro y Revista heredan de ella e implementan sus métodos.
# ============================================================

class MaterialBibliografico(ABC):

    @abstractmethod
    def prestar(self) -> bool:
        """Cada material define cómo descuenta su stock."""
        pass

    @abstractmethod
    def devolver(self) -> bool:
        """Cada material define cómo recupera un ejemplar."""
        pass

    @abstractmethod
    def esta_prestado(self) -> bool:
        """Cada material informa si no tiene ejemplares disponibles."""
        pass


# ============================================================
# CLASE LIBRO
# Representa un libro, sus datos y la disponibilidad de ejemplares.
# ============================================================

class Libro(MaterialBibliografico):

    def __init__(self, id: str, titulo: str, autor: str):
        # Valida los datos obligatorios antes de crear el objeto.
        if not all(
            isinstance(valor, str) and valor.strip()
            for valor in (id, titulo, autor)
        ):
            raise DatosInvalidosError(
                "El código, título y autor son obligatorios."
            )

        # El guion bajo indica atributos encapsulados.
        self._id = id.strip()
        self._titulo = titulo.strip()
        self._autor = autor.strip()
        self._prestado = False

        # Cada título dispone de tres ejemplares.
        self._stock_total = 3
        self._stock_disponible = 3

    # @property y @setter permiten consultar y modificar atributos
    # de forma controlada, aplicando el principio de encapsulación.

    @property
    def id(self) -> str:
        return self._id

    @id.setter
    def id(self, valor: str):
        if not isinstance(valor, str) or not valor.strip():
            raise DatosInvalidosError("El código no puede estar vacío.")
        self._id = valor.strip()

    @property
    def titulo(self) -> str:
        return self._titulo

    @titulo.setter
    def titulo(self, valor: str):
        if not isinstance(valor, str) or not valor.strip():
            raise DatosInvalidosError("El título no puede estar vacío.")
        self._titulo = valor.strip()

    @property
    def autor(self) -> str:
        return self._autor

    @autor.setter
    def autor(self, valor: str):
        if not isinstance(valor, str) or not valor.strip():
            raise DatosInvalidosError("El autor no puede estar vacío.")
        self._autor = valor.strip()

    @property
    def prestado(self) -> bool:
        return self._prestado

    @prestado.setter
    def prestado(self, valor: bool):
        if not isinstance(valor, bool):
            raise DatosInvalidosError(
                "El estado debe ser True o False."
            )

        self._prestado = valor
        self._stock_disponible = (
            0 if valor else self._stock_total
        )

    @property
    def stock_disponible(self) -> int:
        return self._stock_disponible

    @property
    def stock_total(self) -> int:
        return self._stock_total

    # Implementación del método abstracto prestar().
    # Reduce el stock y actualiza el estado del libro.
    def prestar(self) -> bool:
        if self._stock_disponible <= 0:
            self._prestado = True
            return False

        self._stock_disponible -= 1
        self._prestado = self._stock_disponible == 0
        return True

    # Implementación del método abstracto devolver().
    # Aumenta el stock sin superar el total de ejemplares.
    def devolver(self) -> bool:
        if self._stock_disponible >= self._stock_total:
            return False

        self._stock_disponible += 1
        self._prestado = self._stock_disponible == 0
        return True

    def esta_prestado(self) -> bool:
        return self._stock_disponible == 0

    # __str__ define la información que se muestra del libro.
    def __str__(self) -> str:
        estado = "Agotado" if self.esta_prestado() else "Disponible"

        return (
            f"ID: {self._id} | Título: {self._titulo} | "
            f"Autor: {self._autor} | "
            f"Stock: {self._stock_disponible}/{self._stock_total} | "
            f"Estado: {estado}"
        )


# ============================================================
# CLASE REVISTA
# Hereda de MaterialBibliografico e implementa los métodos
# abstractos con su propio control de stock.
# ============================================================

class Revista(MaterialBibliografico):

    # Constante que establece el plazo de préstamo de una revista.
    PLAZO_PRESTAMO_DIAS = 3

    def __init__(self, id: str, titulo: str, numero: str):
        if not all(
            isinstance(valor, str) and valor.strip()
            for valor in (id, titulo, numero)
        ):
            raise DatosInvalidosError(
                "El código, título y número son obligatorios."
            )

        self._id = id.strip()
        self._titulo = titulo.strip()
        self._numero = numero.strip()
        self._stock_total = 3
        self._stock_disponible = 3

    @property
    def id(self) -> str:
        return self._id

    @id.setter
    def id(self, valor: str):
        if not isinstance(valor, str) or not valor.strip():
            raise DatosInvalidosError("El código no puede estar vacío.")
        self._id = valor.strip()

    @property
    def titulo(self) -> str:
        return self._titulo

    @titulo.setter
    def titulo(self, valor: str):
        if not isinstance(valor, str) or not valor.strip():
            raise DatosInvalidosError("El título no puede estar vacío.")
        self._titulo = valor.strip()

    @property
    def numero(self) -> str:
        return self._numero

    @numero.setter
    def numero(self, valor: str):
        if not isinstance(valor, str) or not valor.strip():
            raise DatosInvalidosError("El número no puede estar vacío.")
        self._numero = valor.strip()

    @property
    def stock_disponible(self) -> int:
        return self._stock_disponible

    @property
    def stock_total(self) -> int:
        return self._stock_total

    # La revista implementa prestar() con su propia disponibilidad.
    def prestar(self) -> bool:
        if self._stock_disponible <= 0:
            return False

        self._stock_disponible -= 1
        return True

    # La revista implementa devolver() para recuperar el ejemplar.
    def devolver(self) -> bool:
        if self._stock_disponible >= self._stock_total:
            return False

        self._stock_disponible += 1
        return True

    def esta_prestado(self) -> bool:
        return self._stock_disponible == 0

    def __str__(self) -> str:
        estado = "Agotado" if self.esta_prestado() else "Disponible"

        return (
            f"ID: {self._id} | Revista: {self._titulo} | "
            f"Número: {self._numero} | "
            f"Stock: {self._stock_disponible}/{self._stock_total} | "
            f"Estado: {estado}"
        )


# ============================================================
# CLASE ESTUDIANTE
# Representa a la persona que solicita los materiales.
# Guarda el código, nombre y carrera exigidos por la consigna.
# ============================================================

class Estudiante:

    def __init__(self, id: str, nombre: str, carrera: str):
        if not all(
            isinstance(valor, str) and valor.strip()
            for valor in (id, nombre, carrera)
        ):
            raise DatosInvalidosError(
                "El código, nombre y carrera son obligatorios."
            )

        self._id = id.strip()
        self._nombre = nombre.strip()
        self._carrera = carrera.strip()

    # Propiedades para acceder a los datos de manera controlada.
    @property
    def id(self) -> str:
        return self._id

    @id.setter
    def id(self, valor: str):
        if not isinstance(valor, str) or not valor.strip():
            raise DatosInvalidosError("El código no puede estar vacío.")
        self._id = valor.strip()

    @property
    def nombre(self) -> str:
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str):
        if not isinstance(valor, str) or not valor.strip():
            raise DatosInvalidosError("El nombre no puede estar vacío.")
        self._nombre = valor.strip()

    @property
    def carrera(self) -> str:
        return self._carrera

    @carrera.setter
    def carrera(self, valor: str):
        if not isinstance(valor, str) or not valor.strip():
            raise DatosInvalidosError("La carrera no puede estar vacía.")
        self._carrera = valor.strip()

    def __str__(self) -> str:
        return (
            f"Código: {self._id} | Nombre: {self._nombre} | "
            f"Carrera: {self._carrera}"
        )


# ============================================================
# CLASE PRESTAMO
# Relaciona un material con un estudiante y registra las fechas.
# ============================================================

class Prestamo:

    def __init__(
        self,
        libro: MaterialBibliografico,
        estudiante: Estudiante
    ):
        # _libro puede referenciar un Libro o una Revista.
        self._libro = libro
        self._estudiante = estudiante

        # datetime.now() guarda la fecha y hora actuales.
        self._fecha_prestamo = datetime.now()

        # timedelta calcula la fecha límite sumando los días del plazo.
        # Se asignan tres días a revistas y siete a libros.
        plazo = (
            Revista.PLAZO_PRESTAMO_DIAS
            if isinstance(libro, Revista)
            else 7
        )

        self._fecha_devolucion = (
            self._fecha_prestamo + timedelta(days=plazo)
        )
        self._activo = True

    @property
    def libro(self) -> MaterialBibliografico:
        return self._libro

    @property
    def estudiante(self) -> Estudiante:
        return self._estudiante

    @property
    def fecha_prestamo(self) -> datetime:
        return self._fecha_prestamo

    @property
    def fecha_devolucion(self) -> datetime:
        return self._fecha_devolucion

    @property
    def activo(self) -> bool:
        return self._activo

    # Verifica los objetos y ejecuta el préstamo del material.
    def realizar_prestamo(self) -> bool:
        if self._libro is None or self._estudiante is None:
            raise DatosInvalidosError(
                "El material y el estudiante son obligatorios."
            )

        # Polimorfismo: se llama al método prestar() del objeto recibido.
        # Si es Libro, ejecuta Libro.prestar(); si es Revista,
        # ejecuta Revista.prestar().
        if not self._libro.prestar():
            raise MaterialYaPrestadoError(
                "No hay ejemplares disponibles."
            )

        return True

    def __str__(self) -> str:
        return (
            f"Material: {self._libro.titulo} | "
            f"Estudiante: {self._estudiante.nombre} | "
            f"Fecha: {self._fecha_prestamo:%d/%m/%Y %H:%M}"
        )


# ============================================================
# CLASE BIBLIOTECA
# Administra el catálogo, los préstamos y las devoluciones.
# ============================================================

class Biblioteca:

    def __init__(self):
        self._materiales: List[MaterialBibliografico] = []
        self._prestamos: List[Prestamo] = []

    @property
    def materiales(self) -> List[MaterialBibliografico]:
        return self._materiales.copy()

    @property
    def prestamos(self) -> List[Prestamo]:
        return self._prestamos.copy()

    def registrar_material(self, material: MaterialBibliografico):
        if material is None:
            raise DatosInvalidosError(
                "El material no puede estar vacío."
            )

        for existente in self._materiales:
            if existente.id.lower() == material.id.lower():
                raise DatosInvalidosError(
                    "Ya existe un material con ese código."
                )

        self._materiales.append(material)

    def procesar_prestamo(
        self,
        material: MaterialBibliografico,
        estudiante: Estudiante
    ) -> bool:
        if material is None or estudiante is None:
            raise DatosInvalidosError(
                "Debe indicar un material y un estudiante."
            )

        if material not in self._materiales:
            raise DatosInvalidosError(
                "El material no pertenece al catálogo."
            )

        # Evita que el mismo estudiante solicite nuevamente el mismo
        # material mientras mantenga un préstamo activo.
        for prestamo in self._prestamos:
            if (
                prestamo.activo
                and prestamo.estudiante.id == estudiante.id
                and prestamo.libro.id == material.id
            ):
                raise MaterialYaPrestadoError(
                    "Ya tienes prestado un ejemplar de este material."
                )

        # Polimorfismo: Biblioteca acepta cualquier material que
        # implemente MaterialBibliografico, sin duplicar la lógica.
        prestamo = Prestamo(material, estudiante)
        prestamo.realizar_prestamo()
        self._prestamos.append(prestamo)

        return True

    def devolver_material(
        self,
        numero: int,
        estudiante: Estudiante
    ) -> bool:
        if numero < 1 or numero > len(self._prestamos):
            raise DatosInvalidosError(
                "El número de préstamo no es válido."
            )

        prestamo = self._prestamos[numero - 1]

        if not prestamo.activo:
            raise DatosInvalidosError(
                "Este préstamo ya fue devuelto."
            )

        if prestamo.estudiante.id != estudiante.id:
            raise DatosInvalidosError(
                "Este préstamo no pertenece al estudiante registrado."
            )

        # El material aplica su propio método devolver().
        if not prestamo.libro.devolver():
            raise DatosInvalidosError(
                "No se pudo registrar la devolución."
            )

        prestamo._activo = False
        return True

    def prestamos_estudiante(self, estudiante: Estudiante):
        return [
            (i + 1, prestamo)
            for i, prestamo in enumerate(self._prestamos)
            if (
                prestamo.estudiante.id == estudiante.id
                and prestamo.activo
            )
        ]


# ============================================================
# CATÁLOGO INICIAL
# Registra materiales de ejemplo para probar el programa.
# ============================================================

def crear_biblioteca() -> Biblioteca:
    biblioteca = Biblioteca()

    biblioteca.registrar_material(
        Libro("L001", "Python desde cero", "Mark Lutz")
    )
    biblioteca.registrar_material(
        Libro(
            "L002",
            "Fundamentos de programación",
            "Luis Joyanes"
        )
    )
    biblioteca.registrar_material(
        Libro(
            "L003",
            "Ingeniería de software",
            "Ian Sommerville"
        )
    )
    biblioteca.registrar_material(
        Revista("R001", "Tecnología e innovación", "N.° 15")
    )
    biblioteca.registrar_material(
        Revista("R002", "Ciencia y computación", "N.° 08")
    )

    return biblioteca


# ============================================================
# FUNCIONES DE INTERACCIÓN
# Separan las entradas y salidas de la lógica de las clases.
# ============================================================

def solicitar_texto(mensaje: str) -> str:
    while True:
        dato = input(mensaje).strip()

        if dato:
            return dato

        print("Error: este campo no puede estar vacío.")


def registrar_estudiante() -> Estudiante:
    print("\n=== REGISTRO DEL ESTUDIANTE ===")

    while True:
        try:
            codigo = solicitar_texto("Código del estudiante: ")
            nombre = solicitar_texto("Nombre completo: ")
            carrera = solicitar_texto("Carrera universitaria: ")

            return Estudiante(codigo, nombre, carrera)

        except DatosInvalidosError as error:
            # try-except captura errores de validación y permite continuar.
            print(f"Error: {error}")


def mostrar_catalogo(biblioteca: Biblioteca):
    print("\n========== CATÁLOGO DE LA BIBLIOTECA ==========")

    for i, material in enumerate(biblioteca.materiales, start=1):
        tipo = "LIBRO" if isinstance(material, Libro) else "REVISTA"
        print(f"{i}. [{tipo}] {material}")

    print("================================================")


def elegir_material(
    biblioteca: Biblioteca
) -> Optional[MaterialBibliografico]:
    materiales = biblioteca.materiales

    if not materiales:
        print("No hay materiales registrados.")
        return None

    mostrar_catalogo(biblioteca)

    try:
        numero = int(
            input("Seleccione el número del material que desea: ")
        )

        if numero < 1 or numero > len(materiales):
            print("Opción inválida.")
            return None

        return materiales[numero - 1]

    except ValueError:
        # ValueError se produce si se escribe texto en lugar de un número.
        print("Debe ingresar un número válido.")
        return None


def solicitar_prestamo(
    biblioteca: Biblioteca,
    estudiante: Estudiante
):
    material = elegir_material(biblioteca)

    if material is None:
        return

    try:
        biblioteca.procesar_prestamo(material, estudiante)

        print("\n¡Préstamo registrado correctamente!")
        print(f"Estudiante: {estudiante.nombre}")
        print(f"Material: {material.titulo}")

        prestamos = biblioteca.prestamos_estudiante(estudiante)
        ultimo = prestamos[-1][1]

        print(
            "Fecha del préstamo: "
            f"{ultimo.fecha_prestamo:%d/%m/%Y %H:%M}"
        )
        print(
            "Fecha límite de devolución: "
            f"{ultimo.fecha_devolucion:%d/%m/%Y}"
        )
        print(f"Ejemplares restantes: {material.stock_disponible}")

    except (DatosInvalidosError, MaterialYaPrestadoError) as error:
        # Captura errores de negocio para mostrar un mensaje comprensible.
        print(f"\nNo se pudo completar el préstamo: {error}")


def mostrar_prestamos(
    biblioteca: Biblioteca,
    estudiante: Estudiante
):
    prestamos = biblioteca.prestamos_estudiante(estudiante)

    print("\n========== MIS PRÉSTAMOS ACTIVOS ==========")

    if not prestamos:
        print("No tienes préstamos activos.")
        return

    for numero, prestamo in prestamos:
        print(
            f"{numero}. {prestamo.libro.titulo} | "
            f"Préstamo: {prestamo.fecha_prestamo:%d/%m/%Y %H:%M} | "
            f"Devolución: {prestamo.fecha_devolucion:%d/%m/%Y}"
        )


def devolver_prestamo(
    biblioteca: Biblioteca,
    estudiante: Estudiante
):
    prestamos = biblioteca.prestamos_estudiante(estudiante)

    if not prestamos:
        print("\nNo tienes préstamos pendientes de devolución.")
        return

    mostrar_prestamos(biblioteca, estudiante)

    try:
        numero = int(
            input("Ingrese el número del préstamo a devolver: ")
        )

        biblioteca.devolver_material(numero, estudiante)
        print("Devolución realizada correctamente.")

    except ValueError:
        print("Debe ingresar un número válido.")

    except DatosInvalidosError as error:
        print(f"Error: {error}")


# ============================================================
# MENÚ DEL ESTUDIANTE
# Permite consultar, prestar, devolver y finalizar una sesión.
# ============================================================

def menu_estudiante(
    biblioteca: Biblioteca,
    estudiante: Estudiante
) -> bool:

    while True:
        print("\n========== SISTEMA DE BIBLIOTECA ==========")
        print(f"Estudiante: {estudiante.nombre}")
        print("1. Ver catálogo de libros y revistas")
        print("2. Solicitar un préstamo")
        print("3. Ver mis préstamos activos")
        print("4. Devolver un material")
        print("5. Terminar sesión y registrar otro estudiante")
        print("6. Salir del programa")
        print("===========================================")

        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            mostrar_catalogo(biblioteca)

        elif opcion == "2":
            solicitar_prestamo(biblioteca, estudiante)

            print("\n¿Qué desea hacer ahora?")
            print("1. Continuar utilizando el sistema")
            print("2. Finalizar sesión y registrar otro estudiante")
            print("3. Salir del programa")

            decision = input("Seleccione una opción: ").strip()

            if decision == "2":
                print("Sesión finalizada.")
                return True

            if decision == "3":
                print("Saliendo del programa...")
                return False

            continue

        elif opcion == "3":
            mostrar_prestamos(biblioteca, estudiante)

        elif opcion == "4":
            devolver_prestamo(biblioteca, estudiante)

        elif opcion == "5":
            print("Sesión finalizada.")
            return True

        elif opcion == "6":
            print("Saliendo del programa...")
            return False

        else:
            print("Opción inválida. Intente nuevamente.")


# ============================================================
# PROGRAMA PRINCIPAL
# Crea la biblioteca una sola vez para conservar el stock
# al finalizar una sesión y registrar a otro estudiante.
# ============================================================

def main():
    biblioteca = crear_biblioteca()

    print("===========================================")
    print(" SISTEMA DE GESTIÓN DE BIBLIOTECA UNIVERSITARIA")
    print("===========================================")

    continuar_programa = True

    while continuar_programa:
        estudiante = registrar_estudiante()

        print("\nRegistro completado correctamente.")
        print(estudiante)

        continuar_programa = menu_estudiante(
            biblioteca,
            estudiante
        )

    print("\nGracias por utilizar el sistema de biblioteca.")
    print("Programa finalizado.")


# Ejecuta main() únicamente cuando se inicia este archivo.
if __name__ == "__main__":
    main()
