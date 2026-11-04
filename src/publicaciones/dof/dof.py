"""
Description:   Funcion integradora para el envio de las publicaciones del Diario Oficial de la Federación (DOF)
Author:        David Jiménez Cooper - SpiderCoop
Date:          2026-08-29
"""

import datetime as dt
from zoneinfo import ZoneInfo

from config import RECIPIENTS, TIMEZONE
from publicaciones.dof.email_body import create_email_body
from publicaciones.dof.web_scrapper import obtener_publicaciones_dof
from services.email_manager import email
from services.log_service import LogService


def enviar_publicaciones_dof(date: dt.datetime | None = None, force_send: bool = False):
    """
    Función principal para enviar publicaciones vigentes del DOF por correo electrónico.
    Args:
        date (dt.datetime, optional): Fecha para la cual se desean obtener las publicaciones del DOF. Por defecto es la fecha actual.
    """

    if date is None:
        date = dt.datetime.now(ZoneInfo(TIMEZONE))

    # Inicializamos el servicio de log para llevar un registro de los envios
    log_service = LogService()

    # Obtener las consultas vigentes
    publicaciones = obtener_publicaciones_dof(date=date)

    # Iteramos sobre cada publicacion
    if not publicaciones.empty:
        publicaciones_a_enviar = []
        for _index, row in publicaciones.iterrows():
            nombre_publicacion = row["nombre_publicacion"]
            enlace = row["enlace"]

            # Verificamos si ya se ha enviado un correo para esta consulta (parametrizado por si se quiere enviar de todas maneras)
            if force_send:
                delivered = False
            else:
                delivered = log_service.check_delivery(nombre_publicacion, date.date())

            # -------------------------------------------------------------------------------
            # Aqui tambien estaria la comprobacion de si la publicacion es relevante para la banca
            # -------------------------------------------------------------------------------

            # Si no se ha enviado, agregamos la publicacion a la lista de archivos a enviar
            if not delivered:
                publicaciones_a_enviar.append(
                    {"nombre_publicacion": nombre_publicacion, "enlace": enlace}
                )

        # Se envia el correo con los docuemntos adjuntos
        if publicaciones_a_enviar:
            asunto, cuerpo_correo = create_email_body(publicaciones_a_enviar, date=date)
            email.send(
                asunto,
                cuerpo_correo,
                [],
                [],
                RECIPIENTS.get("bcc"),
            )

            # Una vez enviado, se guarda en el registro de envios para no volver a enviar el mismo archivo
            for archivo in publicaciones_a_enviar:
                nombre_publicacion = archivo["nombre_publicacion"]
                log_service.log_delivery(nombre_publicacion, date.date())

        else:
            print("No hay nuevas publicaciones del DOF para enviar.")

    else:
        print("No hay publicaciones vigentes en el DOF en este momento.")
