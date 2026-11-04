"""
Description:   Funcion para filtrar las publicaciones relevantes del DOF
Author:        David Jiménez Cooper - SpiderCoop
Date:          2026-08-29
"""

import re


def filtrar_publicaciones_dof(nombre_publicacion: str, enlace: str) -> bool:
    """
    Función principal para filtrar publicaciones relevantes del DOF.
    Args:
        nombre_publicacion (str): Nombre de la publicación del DOF.
        enlace (str): Enlace a la publicación del DOF.
    Returns:
        bool: True si la publicación es relevante, False en caso contrario.
    """

    # Establecemos como primer criterio de filtrado expresiones regulares que identifiquen publicaciones relevantes del DOF relacionadas con el sector financiero

    patron_institucion = re.compile(
        r"(banca|financiera|institución crediticia|instituciones de crédito)",
        re.IGNORECASE,
    )

    patron_regulacion = re.compile(r"(circular única de bancos)", re.IGNORECASE)

    patron_buen_fin = re.compile(r"(buen fin)", re.IGNORECASE)

    patron_otros = re.compile(r"(pagos electrónicos|pagos digitales)", re.IGNORECASE)

    # Evitamos Tasas de interés interbancarias de equilibrio. y Tasa de interés interbancaria de equilibrio de fondeo a un día hábil bancario.
    if re.search(
        r"(tasas de interés interbancarias de equilibrio|tasa de interés interbancaria de equilibrio de fondeo a un día hábil bancario)",
        nombre_publicacion,
        re.IGNORECASE,
    ):
        return False

    resultado = (
        patron_institucion.search(nombre_publicacion)
        or patron_regulacion.search(nombre_publicacion)
        or patron_buen_fin.search(nombre_publicacion)
        or patron_otros.search(nombre_publicacion)
    )

    return bool(resultado)
