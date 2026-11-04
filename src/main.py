"""
Description:   Funcion principal para enviar publicaciones.
Author:        David Jiménez Cooper - SpiderCoop
Date:          2026-08-29
"""

import datetime as dt
from zoneinfo import ZoneInfo

from config import DATE, FORCE_SEND, TIMEZONE
from publicaciones.consulta_publica_banxico.consulta_publica_banxico import (
    enviar_consultas_banxico,
)
from publicaciones.dof.dof import enviar_publicaciones_dof

if not DATE:
    DATE = dt.datetime.now(tz=ZoneInfo(TIMEZONE))
else:
    DATE = dt.datetime.strptime(DATE, "%Y-%m-%d").astimezone(ZoneInfo(TIMEZONE))

# Enviamos las consultas publicas de Banxico
enviar_consultas_banxico(force_send=FORCE_SEND)

# Enviamos las publicaciones del Diario Oficial de la Federación (DOF)
enviar_publicaciones_dof(DATE, force_send=FORCE_SEND)
