import sys
import tempfile
import unittest
from pathlib import Path

# Permite importar los modulos de /src desde la carpeta /tests
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

import db_manager


class TestDbManager(unittest.TestCase):

    def setUp(self):
        # Cada prueba corre contra una base de datos temporal, no contra clima.db
        self.carpeta_temporal = tempfile.TemporaryDirectory(ignore_cleanup_errors=True)
        db_manager.CARPETA_DATOS = Path(self.carpeta_temporal.name)
        db_manager.RUTA_BD = Path(self.carpeta_temporal.name) / "prueba.db"
        db_manager.crear_base_datos()

    def tearDown(self):
        self.carpeta_temporal.cleanup()

    def test_crear_y_leer(self):
        db_manager.crear_reporte("David", 27.5, 85, "Nublado", "2026-09-01")
        reportes = db_manager.leer_reportes()

        self.assertEqual(len(reportes), 1)
        self.assertEqual(reportes[0][1], "David")

    def test_actualizar(self):
        db_manager.crear_reporte("David", 27.5, 85, "Nublado", "2026-09-01")
        db_manager.actualizar_reporte(1, "David", 26.8, 88, "Despejado", "2026-09-01")

        reportes = db_manager.leer_reportes()
        self.assertEqual(reportes[0][2], 26.8)
        self.assertEqual(reportes[0][4], "Despejado")

    def test_eliminar(self):
        db_manager.crear_reporte("Panama", 30.2, 78, "Lluvia ligera", "2026-09-01")
        db_manager.eliminar_reporte(1)

        self.assertEqual(len(db_manager.leer_reportes()), 0)


if __name__ == "__main__":
    unittest.main()