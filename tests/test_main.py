import runpy
from unittest.mock import patch


def test_main_runs_keep_alive_and_publication_workflows_once():
    # Arrange
    with (
        patch("config.FORCE_SEND", True),
        patch("services.keep_job_active.keep_job_active") as keep_job_active,
        patch(
            "publicaciones.consulta_publica_banxico.consulta_publica_banxico.enviar_consultas_banxico"
        ) as send_consultations,
        patch("publicaciones.dof.dof.enviar_publicaciones_dof") as send_dof,
    ):
        # Act
        runpy.run_module("main", run_name="__main__")

    # Assert
    keep_job_active.assert_called_once_with()
    send_consultations.assert_called_once_with(force_send=True)
    send_dof.assert_called_once_with(force_send=True)
