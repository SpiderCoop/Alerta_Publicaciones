"""
Description:   Funciones para crear el cuerpo del correo electrónico para notificar sobre nuevas publicaciones en el DOF.
Author:        David Jiménez Cooper - SpiderCoop
Date:          2026-08-29
"""

import datetime as dt


def create_email_body(archivos_enviar, date: dt.datetime):
    """
    Crea el cuerpo del correo electrónico para notificar sobre nuevas publicaciones en el Diario Oficial de la Federación.

    Args:
        archivos_enviar (list): Lista de diccionarios con 'nombre_publicacion' y 'enlace' de las publicaciones.
        date (dt.datetime): Fecha de las publicaciones.

    Returns:
        tuple: Asunto y cuerpo del correo electrónico.
    """

    asunto = f"Publicaciones relevantes en el DOF - {date.strftime('%Y-%m-%d')}"
    cuerpo_correo = """
    Se han detectado publicaciones relevantes en el Diario Oficial de la Federación.
    <br><br>
    """
    for archivo in archivos_enviar:
        nombre_publicacion = archivo["nombre_publicacion"]
        enlace = archivo["enlace"]
        cuerpo_correo += f'<b>{nombre_publicacion}</b><br><a href="{enlace}">Ver publicación</a><br><br>'
    cuerpo_correo += "<i>Este es un correo enviado de forma automatizada.</i>"

    return asunto, cuerpo_correo
