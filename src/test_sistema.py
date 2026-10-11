#============================================================
"""
SISTEMA DE GESTIÓN PARA BIBLIOTECA UNIVERSITARIA

Integrantes: BLAS VERONICA, EBER VILLASANTE y JOSÉ INCHUÑA 

Grupo: B
Asignatura: Lenguaje de Programación 1
"""
#=============================================================


"""Este programa aplica programación orientada a objetos mediante
clases, encapsulamiento, herencia, polimorfismo y excepciones.
"""

from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from typing import Dict, List, Optional


# ============================================================
# 1. EXCEPCIONES PERSONALIZADAS
# ============================================================

# Se crean excepciones propias para identificar errores específicos
# del sistema y diferenciarlos de otros errores de Python.

class MaterialYaPrestadoError(Exception):
    """Error al intentar prestar un material que ya está prestado."""
    pass


class DatosInvalidosError(Exception):
    """Error cuando los datos obligatorios no son válidos."""
    pass


# ============================================================
# 2. CLASE ABSTRACTA MATERIALBIBLIOGRAFICO
# ============================================================

# ABC permite definir una clase abstracta.
# Se utiliza porque los libros y las revistas comparten operaciones,
# aunque cada tipo de material puede implementar su comportamiento.

class MaterialBibliografico(ABC):

    @abstractmethod
    def prestar(self) -> bool:
        """Presta el material si está disponible."""
        pass

    @abstractmethod
    def devolver(self) -> bool:
        """Devuelve el material si está prestado."""
        pass

    @abstractmethod
    def esta_prestado(self) -> bool:
        """Indica si el material está prestado."""
        pass


# ============================================================
# 3. CLASE LIBRO
# ============================================================

# Libro hereda de MaterialBibliografico para implementar las
# operaciones obligatorias de préstamo, devolución y consulta.
# Sus atributos privados protegen los datos del objeto.

class Libro(MaterialBibliografico):

    def __init__(self, id: str, titulo: str, autor: str) -> None:
        self.id = id
        self.titulo = titulo
        self.autor = autor
        self._prestado = False

    # @property permite consultar los atributos de forma controlada.
    # Los setters validan los datos antes de guardarlos.

    @property
    def id(self) -> str:
        return self._id

    @id.setter
    def id(self, valor: str) -> None:
        if not isinstance(valor, str) or not valor.strip():
            raise DatosInvalidosError(
                "El ID del libro no puede estar vacío."
            )
        self._id = valor.strip()

    @property
    def titulo(self) -> str:
        return self._titulo

    @titulo.setter
    def titulo(self, valor: str) -> None:
        if not isinstance(valor, str) or not valor.strip():
            raise DatosInvalidosError("El título no puede estar vacío.")
        self._titulo = valor.strip()

    @property
    def autor(self) -> str:
        return self._autor

    @autor.setter
    def autor(self, valor: str) -> None:
        if not isinstance(valor, str) or not valor.strip():
            raise DatosInvalidosError("El autor no puede estar vacío.")
        self._autor = valor.strip()

    @property
    def prestado(self) -> bool:
        # Se permite consultar el estado sin modificarlo directamente.
        return self._prestado

    def prestar(self) -> bool:
        """Cambia el estado del libro a prestado."""
        if self._prestado:
            return False

        self._prestado = True
        return True

    def devolver(self) -> bool:
        """Cambia el estado del libro a disponible."""
        if not self._prestado:
            return False

        self._prestado = False
        return True

    def esta_prestado(self) -> bool:
        return self._prestado

    def __str__(self) -> str:
        # __str__ facilita mostrar los datos del libro al usuario.
        estado = "Prestado" if self._prestado else "Disponible"
        return (
            f"ID: {self._id} | Título: {self._titulo} | "
            f"Autor: {self._autor} | Estado: {estado}"
        )


# ============================================================
# 4. CLASE ESTUDIANTE
# ============================================================

# Esta clase representa al estudiante que solicita materiales.
# Las propiedades permiten validar y controlar sus datos.

class Estudiante:

    def __init__(self, id: str, nombre: str, carrera: str) -> None:
        self.id = id
        self.nombre = nombre
        self.carrera = carrera

    @property
    def id(self) -> str:
        return self._id

    @id.setter
    def id(self, valor: str) -> None:
        if not isinstance(valor, str) or not valor.strip():
            raise DatosInvalidosError(
                "El ID del estudiante no puede estar vacío."
            )
        self._id = valor.strip()

    @property
    def nombre(self) -> str:
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        if not isinstance(valor, str) or not valor.strip():
            raise DatosInvalidosError(
                "El nombre del estudiante no puede estar vacío."
            )
        self._nombre = valor.strip()

    @property
    def carrera(self) -> str:
        return self._carrera

    @carrera.setter
    def carrera(self, valor: str) -> None:
        if not isinstance(valor, str) or not valor.strip():
            raise DatosInvalidosError(
                "La carrera del estudiante no puede estar vacía."
            )
        self._carrera = valor.strip()

    def __str__(self) -> str:
        # Devuelve una representación legible del estudiante.
        return (
            f"ID: {self._id} | Nombre: {self._nombre} | "
            f"Carrera: {self._carrera}"
        )


# ============================================================
# 5. CLASE PRESTAMO
# ============================================================

# Prestamo relaciona un libro con un estudiante y registra
# la fecha y hora en que se realiza la operación.
# datetime permite guardar la fecha real del préstamo.

class Prestamo:

    def __init__(self, libro: Libro, estudiante: Estudiante) -> None:
        if not isinstance(libro, Libro):
            raise DatosInvalidosError("Se requiere un libro válido.")

        if not isinstance(estudiante, Estudiante):
            raise DatosInvalidosError(
                "Se requiere un estudiante válido."
            )

        self._libro = libro
        self._estudiante = estudiante
        self._fecha_prestamo: Optional[datetime] = None

    @property
    def libro(self) -> Libro:
        return self._libro

    @property
    def estudiante(self) -> Estudiante:
        return self._estudiante

    @property
    def fecha_prestamo(self) -> Optional[datetime]:
        return self._fecha_prestamo

    def realizar_prestamo(self) -> bool:
        # Antes de prestar, se verifica que el libro esté disponible.
        # Así se evita registrar un préstamo duplicado.
        if self._libro.esta_prestado():
            return False

        if self._libro.prestar():
            self._fecha_prestamo = datetime.now()
            return True

        return False


# ============================================================
# 6. CLASE REVISTA
# ============================================================

# Revista también hereda de MaterialBibliografico.
# Su plazo de préstamo es de tres días, como solicita la consigna.
# timedelta permite calcular la fecha límite de devolución.

class Revista(MaterialBibliografico):

    PLAZO_PRESTAMO_DIAS = 3

    def __init__(self, id: str, titulo: str) -> None:
        self.id = id
        self.titulo = titulo
        self._prestado = False
        self._fecha_prestamo: Optional[datetime] = None
        self._fecha_limite: Optional[datetime] = None

    @property
    def id(self) -> str:
        return self._id

    @id.setter
    def id(self, valor: str) -> None:
        if not isinstance(valor, str) or not valor.strip():
            raise DatosInvalidosError(
                "El ID de la revista no puede estar vacío."
            )
        self._id = valor.strip()

    @property
    def titulo(self) -> str:
        return self._titulo

    @titulo.setter
    def titulo(self, valor: str) -> None:
        if not isinstance(valor, str) or not valor.strip():
            raise DatosInvalidosError(
                "El título de la revista no puede estar vacío."
            )
        self._titulo = valor.strip()

    @property
    def prestado(self) -> bool:
        return self._prestado

    @property
    def plazo_prestamo_dias(self) -> int:
        return self.PLAZO_PRESTAMO_DIAS

    @property
    def fecha_prestamo(self) -> Optional[datetime]:
        return self._fecha_prestamo

    @property
    def fecha_limite_devolucion(self) -> Optional[datetime]:
        return self._fecha_limite

    def prestar(self) -> bool:
        # La revista guarda la fecha del préstamo y calcula el plazo.
        if self._prestado:
            return False

        self._prestado = True
        self._fecha_prestamo = datetime.now()
        self._fecha_limite = (
            self._fecha_prestamo
            + timedelta(days=self.PLAZO_PRESTAMO_DIAS)
        )
        return True

    def devolver(self) -> bool:
        # Al devolverla, queda disponible y se limpian las fechas
        # del préstamo anterior.
        if not self._prestado:
            return False

        self._prestado = False
        self._fecha_prestamo = None
        self._fecha_limite = None
        return True

    def esta_prestado(self) -> bool:
        return self._prestado

    def __str__(self) -> str:
        estado = "Prestada" if self._prestado else "Disponible"

        mensaje = (
            f"ID: {self._id} | Título: {self._titulo} | "
            f"Estado: {estado} | "
            f"Plazo de préstamo: {self.PLAZO_PRESTAMO_DIAS} días"
        )

        if self._fecha_limite is not None:
            mensaje += (
                " | Fecha límite de devolución: "
                f"{self._fecha_limite.strftime('%d/%m/%Y %H:%M:%S')}"
            )

        return mensaje


# ============================================================
# 7. CLASE BIBLIOTECA
# ============================================================

# Biblioteca centraliza el procesamiento de los préstamos.
# El polimorfismo permite usar el mismo método con Libro y Revista:
# ambos implementan las operaciones de MaterialBibliografico.

class Biblioteca:

    def __init__(self) -> None:
        # La lista conserva un registro de los préstamos realizados.
        self._registro_prestamos: List[Dict[str, object]] = []

    @property
    def registro_prestamos(self) -> List[Dict[str, object]]:
        # Se devuelve una copia para evitar modificar directamente
        # la lista interna del registro.
        return [
            registro.copy()
            for registro in self._registro_prestamos
        ]

    def procesar_prestamo(
        self,
        material: MaterialBibliografico,
        estudiante: Estudiante
    ) -> bool:
        # Se validan los argumentos para evitar procesar datos inválidos.
        if material is None:
            raise DatosInvalidosError("El material es obligatorio.")

        if estudiante is None:
            raise DatosInvalidosError("El estudiante es obligatorio.")

        if not isinstance(material, MaterialBibliografico):
            raise DatosInvalidosError(
                "El material debe ser un material bibliográfico válido."
            )

        if not isinstance(estudiante, Estudiante):
            raise DatosInvalidosError("El estudiante debe ser válido.")

        # La excepción personalizada informa que el material ya está ocupado.
        if material.esta_prestado():
            raise MaterialYaPrestadoError(
                "No se puede prestar: el material ya está prestado."
            )

        # Se llama al mismo método prestar() independientemente
        # de que el material sea un libro o una revista.
        if material.prestar():
            registro = {
                "material": material,
                "estudiante": estudiante,
                "fecha_prestamo": datetime.now()
            }
            self._registro_prestamos.append(registro)
            return True

        return False


# ============================================================
# 8. PRUEBAS DE FUNCIONAMIENTO
# ============================================================

# Estas pruebas permiten observar las operaciones principales,
# verificar los errores controlados y demostrar el polimorfismo.

def main() -> None:
    biblioteca = Biblioteca()

    print("=== SISTEMA DE GESTIÓN DE BIBLIOTECA ===")

    try:
        estudiante = Estudiante(
            "E001",
            "Marco Antonio",
            "Ingeniería de Software"
        )

        libro = Libro(
            "L001",
            "Python para principiantes",
            "Ana Perez"
        )

        revista = Revista(
            "R001",
            "Revista de Ciencia y Tecnología"
        )

        print("\n=== ESTUDIANTE ===")
        print(estudiante)

        print("\n=== LIBRO ===")
        print(libro)

        print("\n=== PRIMER PRÉSTAMO DE LIBRO ===")
        prestamo = Prestamo(libro, estudiante)

        if prestamo.realizar_prestamo():
            print("Préstamo realizado correctamente.")
            print(
                "Fecha del préstamo:",
                prestamo.fecha_prestamo.strftime("%d/%m/%Y %H:%M:%S")
            )
        else:
            print("El libro ya está prestado.")

        print(libro)

        print("\n=== INTENTO DE PRÉSTAMO DUPLICADO ===")
        try:
            biblioteca.procesar_prestamo(libro, estudiante)
        except MaterialYaPrestadoError as error:
            print("Error controlado:", error)

        print("\n=== DEVOLUCIÓN DEL LIBRO ===")
        if libro.devolver():
            print("Libro devuelto correctamente.")
        print(libro)

        print("\n=== PRÉSTAMO DE LIBRO EN BIBLIOTECA ===")
        if biblioteca.procesar_prestamo(libro, estudiante):
            print("Préstamo registrado correctamente.")

        print("\n=== PRÉSTAMO DE REVISTA ===")
        if biblioteca.procesar_prestamo(revista, estudiante):
            print("Préstamo de revista registrado correctamente.")
        print(revista)

        print("\n=== INTENTO DE PRÉSTAMO DUPLICADO DE REVISTA ===")
        try:
            biblioteca.procesar_prestamo(revista, estudiante)
        except MaterialYaPrestadoError as error:
            print("Error controlado:", error)

        print("\n=== DEVOLUCIÓN DE REVISTA ===")
        if revista.devolver():
            print("Revista devuelta correctamente.")
        print(revista)

        print("\n=== VALIDACIÓN DE DATOS ===")
        try:
            Libro("L002", "", "Autor de prueba")
        except DatosInvalidosError as error:
            print("Error controlado:", error)

        print("\n=== MATERIAL NONE ===")
        try:
            biblioteca.procesar_prestamo(None, estudiante)
        except DatosInvalidosError as error:
            print("Error controlado:", error)

        print("\n=== ESTUDIANTE NONE ===")
        try:
            biblioteca.procesar_prestamo(libro, None)
        except DatosInvalidosError as error:
            print("Error controlado:", error)

        print("\n=== RESUMEN ===")
        print(
            "Total de préstamos registrados:",
            len(biblioteca.registro_prestamos)
        )

    except (DatosInvalidosError, MaterialYaPrestadoError) as error:
        print("Error controlado:", error)


# Este condicional ejecuta las pruebas solamente cuando el archivo
# se ejecuta directamente, no cuando se importa desde otro módulo.
if __name__ == "__main__":
    main()
