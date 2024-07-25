from django.db import connection
from .models import *

#CONSULTAS A LA BDD

def obtener_registros():

    registros = list(Mediciones.objects.raw(
        """
        SELECT m.id, m.oxigeno, m.ph, m.salinidad, m.fecha, m.hora, p.nombre AS piscina_nombre
        FROM index_mediciones m
        JOIN index_piscinas p ON m.piscina_id = p.id
        ORDER BY m.fecha DESC
        """
    ))

    return registros

def obtener_parametros():
    return Parametros.objects.raw("SELECT * FROM index_parametros")

#INSERCCIONES A LA BDD

def registrar_piscina(data):
    with connection.cursor() as cursor:
        cursor.execute(
            """
            INSERT INTO index_piscinas (nombre, ubicacion) 
            VALUES (%s, %s)
            """, data
        )

def registrar_mediciones(data):
    with connection.cursor() as cursor:
        cursor.execute(
            """
            INSERT INTO index_mediciones (piscina_id, oxigeno, ph, salinidad, fecha, hora) 
            VALUES (%s, %s, %s, %s, %s, %s)
            """, data
        )

#ACTUALIZAR

def actualizar_registro(data):
    with connection.cursor() as cursor:
        cursor.execute(
            """
            UPDATE index_mediciones SET piscina_id = %s, oxigeno=%s, ph=%s, salinidad=%s,
            fecha=%s, hora=%s 
            WHERE id=%s
            """,data
        )

def eliminar_registro_consulta(pk):
    data = [pk]
    with connection.cursor() as cursor:
        cursor.execute(
            """
            DELETE FROM index_mediciones WHERE id = %s
            """, data
        )

def registros_fechas_consulta(data):
    registros = Mediciones.objects.raw(
        """
        SELECT m.id, m.oxigeno, m.ph, m.salinidad, m.fecha, m.hora, p.nombre AS piscina_nombre
        FROM index_mediciones m
        JOIN index_piscinas p ON m.piscina_id = p.id
        WHERE m.fecha >= %s AND m.fecha <= %s
        ORDER BY m.fecha DESC
        """, data
    )
    # print(registros)
    # registro_dict = []

    # for registro in registros:
    #     print(registro)
    #     print(1)
    #     registro_dict.append({
    #         "id": registro.id,
    #         "Piscina": registro.piscina_nombre,
    #         "Oxigeno": registro.oxigeno,
    #         "Ph": registro.ph,
    #         "Salinidad": registro.salinidad,
    #         "Fecha": registro.fecha,
    #         "Hora": registro.hora
    #     })
    # print(registro_dict)
    # response = {"data": registro_dict}
    return registros

def obtener_piscina_id(data):
    registros = Mediciones.objects.raw(
        """
        SELECT m.id, m.oxigeno, m.ph, m.salinidad, m.fecha, m.hora, p.nombre AS piscina_nombre
        FROM index_mediciones m
        JOIN index_piscinas p ON m.piscina_id = p.id
        WHERE m.piscina_id = %s
        ORDER BY m.fecha DESC
        """, data
    )
    return registros

def obtener_piscinas():
    piscinas = Piscinas.objects.raw(
        """
        SELECT * FROM index_piscinas
        """
    )

    return piscinas

def actualizar_piscina_consulta(data):
    with connection.cursor() as cursor:
        cursor.execute(
            """
            UPDATE index_piscinas SET nombre = %s, ubicacion = %s
            WHERE id=%s
            """,data
        )

def eliminar_piscina_consulta(pk):
    with connection.cursor() as cursor:
        cursor.execute(
            """
            DELETE FROM index_mediciones WHERE piscina_id = %s
            """, pk
        )
    
    with connection.cursor() as cursor:
        cursor.execute(
            """
            DELETE FROM index_piscinas WHERE id = %s
            """, pk
        )

def obtener_piscina_id_graficos(data):
    registros = Mediciones.objects.raw(
        """
        SELECT m.id, m.oxigeno, m.ph, m.salinidad, m.fecha, m.hora, p.nombre AS piscina_nombre
        FROM index_mediciones m
        JOIN index_piscinas p ON m.piscina_id = p.id
        WHERE m.piscina_id = %s
        ORDER BY m.fecha
        """, data
    )
    return registros