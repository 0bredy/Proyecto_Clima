## Laboratorio N3
## Bredy Guerra

import os
import sqlite3
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

# La base de datos vive en /data, sin importar desde donde se ejecute el script
CARPETA_PROYECTO = Path(__file__).resolve().parent.parent
CARPETA_DATOS = CARPETA_PROYECTO / "data"
NOMBRE_BD = os.getenv("NOMBRE_BD", "clima.db")
RUTA_BD = CARPETA_DATOS / NOMBRE_BD


def crear_base_datos():
    CARPETA_DATOS.mkdir(exist_ok=True)

    try:
        with sqlite3.connect(RUTA_BD) as conn:
            cursor = conn.cursor()

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS reportes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    ciudad TEXT NOT NULL,
                    temperatura REAL NOT NULL,
                    humedad REAL NOT NULL,
                    condicion TEXT,
                    fecha_consulta TEXT NOT NULL
                )
            """)

            print("Base de datos y tabla creadas correctamente.")

    except sqlite3.Error as e:
        print(f"Error: {e}")


def crear_reporte(ciudad, temperatura, humedad, condicion, fecha_consulta):
    try:
        with sqlite3.connect(RUTA_BD) as conn:
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO reportes
                (ciudad, temperatura, humedad, condicion, fecha_consulta)
                VALUES (?, ?, ?, ?, ?)
            """, (ciudad, temperatura, humedad, condicion, fecha_consulta))

            print("Reporte guardado correctamente.")

    except sqlite3.Error as e:
        print(f"Error: {e}")


def leer_reportes():
    try:
        with sqlite3.connect(RUTA_BD) as conn:
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM reportes")
            reportes = cursor.fetchall()

            for reporte in reportes:
                print(reporte)

            return reportes

    except sqlite3.Error as e:
        print(f"Error: {e}")
        return []


def actualizar_reporte(id_reporte, ciudad, temperatura, humedad, condicion, fecha_consulta):
    try:
        with sqlite3.connect(RUTA_BD) as conn:
            cursor = conn.cursor()

            cursor.execute("""
                UPDATE reportes
                SET ciudad = ?, temperatura = ?, humedad = ?,
                    condicion = ?, fecha_consulta = ?
                WHERE id = ?
            """, (ciudad, temperatura, humedad, condicion, fecha_consulta, id_reporte))

            print("Reporte actualizado correctamente.")

    except sqlite3.Error as e:
        print(f"Error: {e}")


def eliminar_reporte(id_reporte):
    try:
        with sqlite3.connect(RUTA_BD) as conn:
            cursor = conn.cursor()

            cursor.execute(
                "DELETE FROM reportes WHERE id = ?",
                (id_reporte,)
            )

            print("Reporte eliminado correctamente.")

    except sqlite3.Error as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    crear_base_datos()

    crear_reporte("David", 27.5, 85, "Nublado", "2026-09-01")
    crear_reporte("Panama", 30.2, 78, "Lluvia ligera", "2026-09-01")

    print("\nREPORTES:")
    leer_reportes()

    actualizar_reporte(1, "David", 26.8, 88, "Despejado", "2026-09-01")

    eliminar_reporte(2)

    print("\nREPORTES FINALES:")
    leer_reportes()
