from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from .models import *
from .forms import *
from django.db import connection
from .consultas import *
from random import randrange
# Create your views here.

response_dict = []

response_dict2 = []

series2 = [10, 20, 30, 40]
series3 = [5, 15, 25, 35]

fechas = []
oxigeno = []
ph = []
salinidad = []

def index(request):
    if request.method == "POST":
        form = RegistroParametrosForm(request.POST)

        if form.is_valid():
            data = list(form.cleaned_data.values())
            data[0] = data[0].id
            data[4] = data[4].isoformat()  # Para la fecha
            data[5] = data[5].strftime('%H:%M:%S')  # Para la hora


            registrar_mediciones(data)

            return HttpResponseRedirect("/")
        
    else:
        form = RegistroParametrosForm()

    return render(request, "index/index.html", {"form": form})

def registro_piscina(request):

    if request.method == "POST":
        post_data = request.POST.copy()

        if "nombre" in post_data:
            post_data["nombre"] = post_data["nombre"].upper()

        form = RegistroPiscinaForm(post_data)

        if form.is_valid():
            data = list(form.cleaned_data.values())
            registrar_piscina(data)
            
            return HttpResponseRedirect("registrar-piscina")

    else:
        form = RegistroPiscinaForm()

    context={"form": form}

    return render(request, "index/registro_piscina.html", context)

def registros_recientes(request):
    
    return render(request, "index/registros_recientes.html")

def lista_registros(request):
    registros = obtener_registros()

    parametros = obtener_parametros()

    parametros_dict = {param.nombre: param for param in parametros }

    registros_dict = []

    for registro in registros:
        oxigeno = parametros_dict["Oxigeno"].rango_min <= registro.oxigeno <= parametros_dict["Oxigeno"].rango_max
        ph = parametros_dict["Ph"].rango_min <= registro.ph <= parametros_dict["Ph"].rango_max
        salinidad = parametros_dict["Salinidad"].rango_min <= registro.salinidad <= parametros_dict["Salinidad"].rango_max

        if (oxigeno and ph and salinidad):
            control = 1
        else:
            control = 0

        registros_dict.append({
            "id": registro.id,
            "Piscina": registro.piscina_nombre,
            "Oxigeno": registro.oxigeno,
            "Ph": registro.ph,
            "Salinidad": registro.salinidad,
            "Fecha": registro.fecha,
            "Hora": registro.hora,
            "Control": control
        })
    
    data = {"data": registros_dict}

    return JsonResponse(data)

def registros_fuera_control(request):
    return render(request, "index/registros_fuera_control.html")

def lista_fuera_control(request):
    registros = obtener_registros()

    parametros = obtener_parametros()

    parametros_dict = {param.nombre: param for param in parametros }

    registros_dict = []

    for registro in registros:
        oxigeno = parametros_dict["Oxigeno"].rango_min <= registro.oxigeno <= parametros_dict["Oxigeno"].rango_max
        ph = parametros_dict["Ph"].rango_min <= registro.ph <= parametros_dict["Ph"].rango_max
        salinidad = parametros_dict["Salinidad"].rango_min <= registro.salinidad <= parametros_dict["Salinidad"].rango_max

        if (oxigeno and ph and salinidad) == False:
            registros_dict.append({
            "id": registro.id,
            "Piscina": registro.piscina_nombre,
            "Oxigeno": registro.oxigeno,
            "Ph": registro.ph,
            "Salinidad": registro.salinidad,
            "Fecha": registro.fecha,
            "Hora": registro.hora,
            })
    
    data = {"data": registros_dict}

    return JsonResponse(data)

def actualizar(request, pk):

    if request.method == "POST":
        form = RegistroParametrosForm(request.POST)

        if form.is_valid():
            data = list(form.cleaned_data.values())
            data[0] = data[0].id
            data[4] = data[4].isoformat()  # Para la fecha
            data[5] = data[5].strftime('%H:%M:%S')  # Para la hora
            data.append(pk)

            actualizar_registro(data)

            return HttpResponseRedirect(reverse("registros-recientes"))
        
    else:
        registro = Mediciones.objects.raw(
            f"SELECT * FROM index_mediciones WHERE id={pk}"
        )
        data = {
            "piscina": registro[0].piscina,
            "oxigeno": registro[0].oxigeno,
            "ph": registro[0].ph,
            "salinidad": registro[0].salinidad,
            "fecha": registro[0].fecha,
            "hora": registro[0].hora
        }
        form = RegistroParametrosForm(data)
    return render(request, "index/actualizar.html", {"form": form, "pk":pk})

def eliminar_registro(request, pk):

    if request.method == "POST":
        decision = request.POST.get('decision')

        if decision == 'yes':
            eliminar_registro_consulta(pk)
            return HttpResponseRedirect('/')
        else:
            return HttpResponseRedirect('/')
     
    return render(request, "index/eliminar_registro.html", {"pk": pk})

def lista_registros_fechas(request):
    dato = {}
    dato["data"] = response_dict
    print(dato)
    return JsonResponse(dato)


def registros_fecha(request):
    
    form = RegistrosFechaForm()
    return render(request, "index/registros_fechas.html", {"form": form})

def mostrar_lista_fechas(request):

    if request.method == 'POST':
        form = RegistrosFechaForm(request.POST)
        if form.is_valid():
            # Procesar los datos del formulario
            response_dict.clear()
            data = list(form.cleaned_data.values())
            data[0] = data[0].isoformat()
            data[1] = data[1].isoformat()

            response = registros_fechas_consulta(data)

            parametros = obtener_parametros()

            parametros_dict = {param.nombre: param for param in parametros }

            for registro in response:

                oxigeno = parametros_dict["Oxigeno"].rango_min <= registro.oxigeno <= parametros_dict["Oxigeno"].rango_max
                ph = parametros_dict["Ph"].rango_min <= registro.ph <= parametros_dict["Ph"].rango_max
                salinidad = parametros_dict["Salinidad"].rango_min <= registro.salinidad <= parametros_dict["Salinidad"].rango_max

                if (oxigeno and ph and salinidad):
                    control = 1
                else:
                    control = 0

                response_dict.append({
                "id": registro.id,
                "Piscina": registro.piscina_nombre,
                "Oxigeno": registro.oxigeno,
                "Ph": registro.ph,
                "Salinidad": registro.salinidad,
                "Fecha": registro.fecha,
                "Hora": registro.hora,
                "Control": control
                })
            print(response_dict)
            return render(request, "index/lista_fechas.html")
    return render(request, "index/lista_fechas.html")

def elegir_piscina(request):
    form = ElegirPiscinaForm()
    return render(request, "index/elegir_piscina.html", {"form": form})

def mostrar_lista_piscina(request):
    if request.method == 'POST':
        form = ElegirPiscinaForm(request.POST)
        print(1)
        if form.is_valid():
            print(2)
            # Procesar los datos del formulario
            response_dict2.clear()
            data = list(form.cleaned_data.values())
            data[0] = data[0].id

            response = obtener_piscina_id(data)
            print(response)

            

            for registro in response:
                print(registro)
                response_dict2.append({
                "id": registro.id,
                "Piscina": registro.piscina_nombre,
                "Oxigeno": registro.oxigeno,
                "Ph": registro.ph,
                "Salinidad": registro.salinidad,
                "Fecha": registro.fecha,
                "Hora": registro.hora,
                
                })
            # print(response_dict)
            return render(request, "index/lista_registro_piscina.html")
        else:
    
            return render(request, "index/elegir_piscina.html", {"form": form})

        
def lista_registros_piscina(request):
    dato = {}
    dato["data"] = response_dict2
    print(dato)
    return JsonResponse(dato)

def piscinas(request):
    return render(request, "index/lista_piscinas.html")

def lista_piscinas(request):
    piscinas = obtener_piscinas()

    piscinas_dict = []

    for piscina in piscinas:

        piscinas_dict.append({
            "id": piscina.id,
            "Nombre": piscina.nombre,
            "Ubicacion": piscina.ubicacion,
        })
    
    data = {"data": piscinas_dict}

    return JsonResponse(data)

def actualizar_piscina(request, pk):
    if request.method == "POST":

        post_data = request.POST.copy()

        if "nombre" in post_data:
            post_data["nombre"] = post_data["nombre"].upper()        

        form = RegistroPiscinaForm(post_data)
        piscina = Piscinas.objects.raw(
            f"SELECT * FROM index_piscinas WHERE id = {pk}" 
        )
        nombre = piscina[0].nombre.upper()
        nombre_request = request.POST.get("nombre")
        nombre_request = nombre_request.upper()

        if  nombre_request == nombre:
            ubicacion = request.POST.get("ubicacion")
            data = [nombre, ubicacion, pk]
            actualizar_piscina_consulta(data)
            return HttpResponseRedirect(reverse("registros-recientes"))
        else:
            if form.is_valid():
                print(2)
                data = list(form.cleaned_data.values())
                data[0] = data[0].upper()
                data.append(pk)
                actualizar_piscina_consulta(data)
                return HttpResponseRedirect(reverse("registros-recientes"))

    else:
        piscina = Piscinas.objects.raw(
            f"SELECT * FROM index_piscinas WHERE id = {pk}" 
        )
        data = {
                "nombre": piscina[0].nombre,
                "ubicacion": piscina[0].ubicacion
            }
        print(data)
        form = RegistroPiscinaForm(initial=data)
    return render(request, "index/actualizar_piscina.html", {"form":form, "pk": pk})

def eliminar_piscina(request, pk):
    data = [pk]
    if request.method == "POST":
        decision = request.POST.get('decision')

        if decision == 'yes':
            eliminar_piscina_consulta(data)
            return HttpResponseRedirect("/")
        else:
            return HttpResponseRedirect("/")
    else:

        piscina = Piscinas.objects.raw(
            """
            SELECT * FROM index_piscinas WHERE id = %s
            """, data
        )
        nombre = piscina[0].nombre
        return render(request, "index/eliminar_piscina.html", {"nombre": nombre, "pk":pk})

def graficos(request):
    graficos_bolean = False
    if request.method == 'POST':
        form = ElegirPiscinaForm(request.POST)
        if form.is_valid():
            # Procesar los datos del formulario
            data = list(form.cleaned_data.values())
            data[0] = data[0].id

            registros = obtener_piscina_id_graficos(data)
            print(registros)
            fechas.clear()
            oxigeno.clear()
            ph.clear()
            salinidad.clear()
            
            for registro in registros:
                print(registro)
                fechas.append(registro.fecha)
                oxigeno.append(registro.oxigeno)
                ph.append(registro.ph)
                salinidad.append(registro.salinidad)

            graficos_bolean = True
            print(graficos_bolean)
            return render(request, "index/graficos.html", {"form": form, "graficos": graficos_bolean})
            # print(response_dict)
        else:
            return render(request, "index/graficos.html", {"form": form, "graficos": graficos_bolean})
    else:
        form = ElegirPiscinaForm()
        return render(request, "index/graficos.html", {"form": form, "graficos": graficos_bolean})

def get_chart(request):
    colors = ["blue", "orange", "red", "black", "green", "magenta", "lightblue", "purple"]
    random_color = colors[randrange(0, (len(colors)-1))]
    
    chart1 = {
        "title": {
            "text": "Oxígeno"
        },
        "tooltip": {
            "show": True,
            "trigger": "axis",
            "triggerOn": "mousemove|click"
        },
        "xAxis":[
            {
                "type": "category",
                "data": fechas
            }
        ],
        "yAxis": [
            {
                "type": "value"
            }
        ],
        "series": [
            {
                "data": oxigeno,
                "type": "line",
                "itemStyle": {
                    "color": random_color 
                },
                "lineStyle": {
                    "color": random_color
                }
            }
        ]
    }

    chart2 = {
        "title": {
            "text": "Ph"
        },
        "tooltip": {
            "show": True,
            "trigger": "axis",
            "triggerOn": "mousemove|click"
        },
        "xAxis":[
            {
                "type": "category",
                "data": fechas
            }
        ],
        "yAxis": [
            {
                "type": "value",
                
            }
        ],
        "series": [
            {
                "data": ph,
                "type": "line",
                "itemStyle": {
                    "color": random_color 
                },
                "lineStyle": {
                    "color": random_color
                }
            }
        ]
    }

    chart3 = {
        "title": {
            "text": "Salinidad"
        },
        "tooltip": {
            "show": True,
            "trigger": "axis",
            "triggerOn": "mousemove|click"
        },
        "xAxis":[
            {
                "type": "category",
                "data": fechas
            }
        ],
        "yAxis": [
            {
                "type": "value",
                
            }
        ],
        "series": [
            {
                "data": salinidad,
                "type": "line",
                "itemStyle": {
                    "color": random_color 
                },
                "lineStyle": {
                    "color": random_color
                }
            }
        ]
    }

    chart_data = {
        "chart1": chart1,
        "chart2": chart2,
        "chart3": chart3
    }

    
    return JsonResponse(chart_data)