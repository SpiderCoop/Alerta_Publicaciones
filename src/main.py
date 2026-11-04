"""
Description:   Funcion principal para enviar publicaciones.
Author:        David Jiménez Cooper - SpiderCoop
Date:          2026-08-29
"""

from config import FORCE_SEND
from publicaciones.consulta_publica_banxico.consulta_publica_banxico import (
    enviar_consultas_banxico,
)
from publicaciones.dof.dof import enviar_publicaciones_dof

enviar_consultas_banxico(
    force_send=FORCE_SEND
)  # funcion principal para enviar consultas vigentes de Banxico por correo electrónico
enviar_publicaciones_dof(
    force_send=FORCE_SEND
)  # funcion principal para enviar publicaciones del DOF por correo electrónico
