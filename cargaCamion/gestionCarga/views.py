from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import *

# Create your views here.


def index(request):
    camiones = Camion.objects.all()  # Obtiene todos los camiones
    # Pasa los camiones al template
    return render(request, 'index.html', {'camiones': camiones})


# Vista de creacion de camiones
def crear_camion(request):
    if request.method == 'POST':
        patente = request.POST.get('patente')
        carga_maxima = request.POST.get('carga_maxima')
        estado = request.POST.get('estado')

        # print(f'patente: {patente}\n carga_maxima: {carga_maxima}\n estado: {estado}')

        # creamos el objeto camion
        camion = Camion(patente=patente,
                        carga_maxima=carga_maxima, estado=estado)

        # guardamos el objeto camion
        camion.save()

        return redirect('../')

    return render(request, './camiones/crear_camion.html')

# vista para ver los detalles de un camion
# el detalle del camion incluye los del camion en si y las cargas que tiene


def detalle_camion(request, patente):
    camion = get_object_or_404(Camion, patente=patente)
    return render(request, './camiones/detalle_camion.html', {'camion': camion,
                                                              'cajas': Caja.objects.filter(carga__camion=camion),
                                                              'packings': Packing.objects.filter(carga__camion=camion),
                                                              'bidones': Bidon.objects.filter(carga__camion=camion)})

# vistas para editar un camion


def editar_camion(request, id):
    camion = get_object_or_404(Camion, id=id)
    if request.method == 'POST':
        patente = request.POST.get('patente')
        carga_maxima = request.POST.get('carga_maxima')
        estado = request.POST.get('estado')

        # print(f'patente: {patente}\n carga_maxima: {carga_maxima}\n estado: {estado}')

        # nos traemos el objeto camion
        camion = get_object_or_404(Camion, patente=patente)
        # hacemos el cambio de los datos
        camion.patente = patente
        camion.carga_maxima = carga_maxima
        camion.estado = estado

        # guardamos el objeto camion
        camion.save()
        return redirect('/')

    return render(request, './camiones/editar_camion.html', {'camion': camion})

# Editar estado de un camion


def editar_estado_camion(request, patente):
    camion = get_object_or_404(Camion, patente=patente)
    if request.method == 'POST':
        estado = request.POST.get('estado')
        # print(f'patente: {patente}\n carga_maxima: {carga_maxima}\n estado: {estado}')

        # nos traemos el objeto camion
        camion = get_object_or_404(Camion, patente=patente)
        # hacemos el cambio de los datos
        match estado:
            case 'Disponible':
                if camion.estado == "Regresando" or camion.estado == "Reparacion":
                    camion.estado = "Disponible"
                    camion.save()
                else:
                    return HttpResponse("El camion se encuentra en viaje o ya esta disponible", 304)
            case 'En-viaje':
                if camion.listo_para_salir():
                    camion.en_viaje()
                else:
                    return HttpResponse("El camion no esta disponible", 304)
            case 'De-regreso':
                if camion.estado == 'Viaje':
                    camion.de_regreso()
                else:
                    return HttpResponse("El camion no se encuentra en viaje", 304)
            case 'En-reparacion':
                if camion.estado == "Disponible":
                    camion.a_reparacion()
                else:
                    return HttpResponse("El camion se encuentra en viaje o de regreso", 304)
            case _:
                return HttpResponseBadRequest('Estado no valido')

        # guardamos el objeto camion
        camion.save()
        return redirect('./')
    else:
        return HttpResponseBadRequest('Metodo no permitido')

# Funcion para eliminar un camion


def eliminar_camion(request, patente):
    camion = get_object_or_404(Camion, patente=patente)

    if camion.estado == 'Disponible':
        camion.delete()

    else:
        messages.error(request, 'El camion no esta disponible')
        return HttpResponseBadRequest('El camion no esta disponible')

    return redirect('/')

# funcion para ver todas las cargas


def ver_cargas(request):
    return render(request, './cargas/cargas.html', {'cajas': Caja.objects.all(), 'packings': Packing.objects.all(), 'bidones': Bidon.objects.all()})

# funcion para crear una carga


def crear_carga(request):
    camion_id = request.POST.get('camion')

    if request.method == 'POST':
        if camion_id != "null":
            if camion.estado == 'Viaje' or camion.estado == 'Regresando':
                messages.error(
                    request, 'El camion Ya esta listo para salir o se encuentra en viaje')
                return HttpResponse('El camion Ya esta listo para salir o se encuentra en viaje', 304)

        tipo = request.POST.get('tipo')
        match tipo:
            case 'Caja':
                response = crear_caja(request, camion_id)
            case 'Packing':
                response = crear_packing(request, camion_id)
            case 'Bidon':
                response = crear_bidon(request, camion_id)

        if response.status_code == 200:
            return redirect('./')
        else:
            return response

    return render(request, './cargas/crear_cargas.html', {'camiones': Camion.objects.all()})

# Funcion para eliminar una carga

def baja_carga(request, id):
    carga = get_object_or_404(Carga, pk=id)
    camion = carga.camion

    if camion.estado == 'Disponible':
        camion.bajar_carga(carga)

    else:
        messages.error(request, 'El camion no esta disponible')
        return HttpResponseBadRequest('El camion no esta disponible')

    return redirect('../')

def subir_carga(request, id):
    if request.method == 'POST':
        camion_id = request.POST.get('camion')
        print(camion_id)
        camion = get_object_or_404(Camion, patente=camion_id)
        # nos traemos la caja packin o bidon que queremos subir
        carga = get_object_or_404(Carga, pk=id)

        

        if camion.estado == 'Disponible' and camion.peso_cargas() + carga.obtener_peso() < camion.carga_maxima * 0.75:
            camion.subir_carga(carga)

        else:
            messages.error(request, 'El camion no esta disponible')
            return HttpResponseBadRequest('El camion no esta disponible')

        return redirect('../')
    return render(request, './cargas/subir_carga.html', {'camiones': Camion.objects.all()})

def eliminar_carga(request, id):
    carga = get_object_or_404(Carga, pk=id)
    camion = carga.camion

    if camion.estado == 'Disponible':
        camion.bajar_carga(carga)

    else:
        messages.error(request, 'El camion no esta disponible')
        return HttpResponseBadRequest('El camion no esta disponible')

    return redirect('../')

# funcion para crear una caja


def crear_caja(request, camion_id):
    # nos traemos los datos del formulario
    peso = request.POST.get('peso')
    contenido = request.POST.get('contenido')
    carga = None

    if camion_id != "null":
        camion = get_object_or_404(Camion, pk=camion_id)

        # creamos el objeto carga
        carga = Carga(contenido=contenido, camion=camion)

        caja = Caja(peso=peso, carga=carga)

        # comprobamos si el camion tiene margen de peso
        # si no tiene margen de peso, no se crea la carga
        if camion.peso_cargas() + caja.obtener_peso() > camion.carga_maxima * 0.75:
            print('no hay margen de peso')
            # si no tiene margen de peso, no se crea la carga
            return HttpResponseBadRequest('El camion no tiene margen de peso')

    else:
        carga = Carga(contenido=contenido)
        caja = Caja(peso=peso, carga=carga)

    carga.save()
    caja.save()
    # retornamos un mensaje de exito
    messages.success(request, 'Carga creada exitosamente')
    return HttpResponse('Carga creada exitosamente')

# funcion para crear un packing


def crear_packing(request, camion_id):
    # nos traemos los datos del formulario
    peso_por_caja = request.POST.get('peso_por_caja')
    cantidad = request.POST.get('cantidad')
    peso_estructura = request.POST.get('peso_estructura')
    contenido = request.POST.get('contenido')
    carga = None

    if camion_id != "null":
        camion = get_object_or_404(Camion, pk=camion_id)

        # creamos el objeto carga
        carga = Carga(contenido=contenido, camion=camion)

        # creamos el objeto packing
        packing = Packing(peso_por_caja=peso_por_caja, cantidad=cantidad,
                          peso_estructura=peso_estructura, carga=carga)

        if camion.peso_cargas() + packing.obtener_peso() > camion.carga_maxima * 0.75:
            # si no tiene margen de peso, no se crea la carga
            messages.error(request, 'El camion no tiene margen de peso')
            return HttpResponseBadRequest('El camion no tiene margen de peso')

    else:
        carga = Carga(contenido=contenido)
        # creamos el objeto packing
        packing = Packing(peso_por_caja=peso_por_caja, cantidad=cantidad,
                          peso_estructura=peso_estructura, carga=carga)

    # guardamos el objeto packing
    carga.save()
    packing.save()
    messages.success(request, 'Carga creada exitosamente')
    return HttpResponse('Carga creada exitosamente')

# funcion para crear un bidon


def crear_bidon(request, camion_id):
    # nos traemos los datos del formulario
    contenido = request.POST.get('contenido')
    capacidad = request.POST.get('capacidad')
    densidad = request.POST.get('densidad')
    carga = None

    # nos traemos el objeto camion
    if camion_id != "null":
        camion = get_object_or_404(Camion, pk=camion_id)

        # creamos el objeto carga
        carga = Carga(contenido=contenido, camion=camion)

        # creamos el objeto bidon
        bidon = Bidon(capacidad=capacidad, densidad=densidad,
                      carga=carga)

        if camion.peso_cargas() + bidon.obtener_peso() > camion.carga_maxima * 0.75:
            # si no tiene margen de peso, no se crea la carga
            messages.error(request, 'El camion no tiene margen de peso')
            return HttpResponseBadRequest('El camion no tiene margen de peso')
    else:
        carga = Carga(contenido=contenido)
        # creamos el objeto bidon
        bidon = Bidon(capacidad=capacidad, densidad=densidad,
                      carga=carga)

    # guardamos los objetos
    carga.save()
    bidon.save()
    messages.success(request, 'Carga creada exitosamente')
    return HttpResponse('Carga creada exitosamente')
