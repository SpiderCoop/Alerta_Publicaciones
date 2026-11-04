import runpy
from unittest.mock import patch


def test_main_runs_publication_workflows_once():
    # Arrange
    with (
        patch("config.FORCE_SEND", True),
        patch(
            "publicaciones.consulta_publica_banxico.consulta_publica_banxico.enviar_consultas_banxico"
        ) as send_consultations,
        patch("publicaciones.dof.dof.enviar_publicaciones_dof") as send_dof,
    ):
        # Act
        runpy.run_module("main", run_name="__main__")

    # Assert
    send_consultations.assert_called_once_with(force_send=True)
    send_dof.assert_called_once_with(force_send=True)
