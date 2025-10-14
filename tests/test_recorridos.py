import unittest
import json
import os
from src.RecorridoBuses import CreadorRecorridosBuses

class TestCreadorRecorridosBuses(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test_file = 'data/test_datos_buses.json'
        cls.app = CreadorRecorridosBuses(None)
        cls.app.archivo_datos = cls.test_file
        cls.app.rutas = {}
        cls.app.buses = {}

    @classmethod
    def tearDownClass(cls):
        if os.path.exists(cls.test_file):
            os.remove(cls.test_file)

    def test_guardar_y_cargar_datos(self):
        self.app.rutas = {'Ruta 1': ['Parada A', 'Parada B']}
        self.app.buses = {'Bus 1': {'ruta': 'Ruta 1', 'capacidad': 40, 'estado': 'Disponible'}}
        self.app.guardar_datos()

        self.app.rutas = {}
        self.app.buses = {}
        self.app.cargar_datos()

        self.assertIn('Ruta 1', self.app.rutas)
        self.assertIn('Bus 1', self.app.buses)

    def test_crear_ruta(self):
        self.app.rutas = {}
        self.app.crear_ruta('Ruta 2', ['Parada C', 'Parada D'])
        self.assertIn('Ruta 2', self.app.rutas)

    def test_eliminar_ruta(self):
        self.app.rutas = {'Ruta 3': ['Parada E', 'Parada F']}
        del self.app.rutas['Ruta 3']
        self.assertNotIn('Ruta 3', self.app.rutas)

    def test_agregar_bus(self):
        self.app.buses = {}
        self.app.agregar_bus('Bus 2', 'Ruta 1', 40)
        self.assertIn('Bus 2', self.app.buses)

    def test_eliminar_bus(self):
        self.app.buses = {'Bus 3': {'ruta': 'Ruta 1', 'capacidad': 40, 'estado': 'Disponible'}}
        del self.app.buses['Bus 3']
        self.assertNotIn('Bus 3', self.app.buses)

if __name__ == '__main__':
    unittest.main()