from django.test import TestCase
from gestionCarga.models import Camion, Carga, Caja, Packing, Bidon


class CamionTestCase(TestCase):
    def setUp(self):
        self.camion = Camion.objects.create(
            patente='ABC123', estado='Disponible', carga_maxima=1000)
        pass

    def test_obtener_cargas(self):
        # Agregar algunas cargas al camión
        carga1 = Carga.objects.create(
            contenido='Cnt 1', camion=self.camion)
        carga2 = Carga.objects.create(
            contenido='Cnt 2', camion=self.camion)
        carga3 = Carga.objects.create(
            contenido='Cnt 3', camion=self.camion)

        # Verificar que las cargas se han agregado correctamente
        self.assertEqual(list(self.camion.obtener_cargas()),
                         [carga1, carga2, carga3])

    def test_cantidad_cargas(self):
        # Agregar algunas cargas al camión
        carga1 = Carga.objects.create(
            contenido='Cnt 1', camion=self.camion)
        carga2 = Carga.objects.create(
            contenido='Cnt 2', camion=self.camion)
        carga3 = Carga.objects.create(
            contenido='Cnt 3', camion=self.camion)

        # Verificar que la cantidad de cargas es correcta
        self.assertEqual(self.camion.cantidad_cargas(), 3)
      
  
    def cleanUp(self):
        self.camion.delete()


class CargaTestCase(TestCase):

    def setUp(self):
        self.camion = Camion.objects.create(
            patente='ABC123', estado='Disponible', carga_maxima=1000)
        self.carga = Carga.objects.create(
            contenido='Cnt 1', camion=self.camion)
        
    def test_obtener_peso(self):
        # Agregar algunas cajas a la carga
        caja1 = Caja.objects.create(
            carga=self.carga, peso=10)
        caja2 = Caja.objects.create(
            carga=self.carga, peso=20)
        caja3 = Caja.objects.create(
            carga=self.carga, peso=30)

        # Agregar algunos packings a la carga
        packing1 = Packing.objects.create(
            carga=self.carga, peso_por_caja=10, cantidad=10, peso_estructura=10)
        packing2 = Packing.objects.create(
            carga=self.carga, peso_por_caja=20, cantidad=20, peso_estructura=20)
        packing3 = Packing.objects.create(
            carga=self.carga, peso_por_caja=30, cantidad=30, peso_estructura=30)

        # Agregar algunos bidones a la carga
        bidon1 = Bidon.objects.create(
            carga=self.carga, capacidad=10, densidad = 1)
        bidon2 = Bidon.objects.create(
            carga=self.carga, capacidad=20, densidad = 1)
        bidon3 = Bidon.objects.create(
            carga=self.carga, capacidad=30, densidad = 1)

        # Verificar que el peso total de la carga es correcto
        self.assertEqual(self.carga.obtener_peso(), 1580)
        