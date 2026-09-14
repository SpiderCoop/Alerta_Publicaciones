import runpy
from unittest.mock import patch


def test_main_runs_keep_alive_and_publication_workflow_once():
    # Arrange
    with (
        patch("services.keep_job_active.keep_job_active") as keep_job_active,
        patch(
            "consulta_publica_banxico.consulta_publica_banxico.enviar_consultas_banxico"
        ) as send_consultations,
    ):
        # Act
        runpy.run_module("main", run_name="__main__")

    # Assert
    keep_job_active.assert_called_once_with()
    send_consultations.assert_called_once_with()
