from django.db import models


class Camion(models.Model):
    patente = models.CharField(max_length=10)
    estado = models.CharField(max_length=50)
    carga_maxima = models.IntegerField()

    def __str__(self):
        return self.patente
    
    def obtener_cargas(self):
        return self.cargas.all()

    def cantidad_cargas(self):
        return self.cargas.count()

    def peso_cargas(self):
        peso = 0
        for carga in self.cargas.all():
            peso += carga.obtener_peso()
        return peso

    def bajar_carga(self, carga):
        self.cargas.remove(carga)
        return True
        
    def subir_carga(self, carga):
        self.cargas.add(carga)
        return True

    def a_reparacion(self):
        self.estado = "Reparacion"
        self.save()
        return True

    def sale_reparado(self):
        self.estado = "Disponible"
        self.save()
        return True

    def en_viaje(self):
        self.estado = "Viaje"
        self.save()
        return True

    def de_regreso(self):
        self.estado = "Regresando"
        self.save()
        return True

    def listo_para_salir(self):
        if self.estado == "Disponible":
            return True
        else:
            return False

    

class Carga(models.Model):
    contenido = models.CharField(max_length=10)
    camion = models.ForeignKey(
        Camion, on_delete=models.CASCADE, related_name='cargas', null=True)

    def __str__(self):
        return self.contenido

    def obtener_peso(self):
        peso = 0
        for caja in self.cajas.all():
            peso += caja.obtener_peso()
        for packing in self.packings.all():
            peso += packing.obtener_peso()
        for bidon in self.bidones.all():
            peso += bidon.obtener_peso()
        return peso


class Caja(models.Model):
    carga = models.ForeignKey(
        Carga, on_delete=models.CASCADE, related_name='cajas')
    peso = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.contenido + " " + str(self.peso)

    def obtener_peso(self):
        return float(self.peso)


class Packing(models.Model):
    carga = models.ForeignKey(
        Carga, on_delete=models.CASCADE, related_name='packings')
    peso_por_caja = models.DecimalField(max_digits=5, decimal_places=2)
    cantidad = models.IntegerField()
    peso_estructura = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.contenido + " " + str(self.peso_por_caja) + " " + str(self.cantidad) + " " + str(self.peso_estructura)

    def obtener_peso(self):
        return float(self.peso_por_caja) * float(self.cantidad) + float(self.peso_estructura)


class Bidon(models.Model):
    carga = models.ForeignKey(
        Carga, on_delete=models.CASCADE, related_name='bidones')
    capacidad = models.DecimalField(max_digits=5, decimal_places=2)
    densidad = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.contenido + " " + str(self.capacidad) + " " + str(self.densidad)

    def obtener_peso(self):
        return float(self.capacidad) * float(self.densidad)
