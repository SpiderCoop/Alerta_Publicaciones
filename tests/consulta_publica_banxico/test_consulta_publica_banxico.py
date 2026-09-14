from unittest.mock import Mock, patch

import pandas as pd

from consulta_publica_banxico import consulta_publica_banxico as module


def test_enviar_consultas_banxico_does_nothing_when_there_are_no_current_publications():
    # Arrange
    log_service = Mock()
    empty_consultations = pd.DataFrame()

    # Act
    with (
        patch.object(module, "LogService", return_value=log_service),
        patch.object(
            module, "obtener_consultas_banxico", return_value=empty_consultations
        ) as get_consultations,
        patch.object(module, "email") as email,
    ):
        module.enviar_consultas_banxico()

    # Assert
    get_consultations.assert_called_once_with(vigentes=True)
    log_service.check_delivery.assert_not_called()
    email.send.assert_not_called()


def test_enviar_consultas_banxico_sends_new_publication_and_removes_downloads(
    publication_row, tmp_path
):
    # Arrange
    log_service = Mock()
    log_service.check_delivery.return_value = False
    publication_file = tmp_path / "publication.pdf"
    publication_file.write_bytes(b"content")
    consultations = pd.DataFrame([publication_row])

    # Act
    with (
        patch.object(module, "LogService", return_value=log_service),
        patch.object(module, "obtener_consultas_banxico", return_value=consultations),
        patch.object(
            module, "download_file", return_value=str(publication_file)
        ) as download,
        patch.object(
            module,
            "create_email_body",
            return_value=("Subject", "Body"),
        ),
        patch.object(module, "email") as email,
        patch.object(
            module, "RECIPIENTS", {"to": ["to@example.test"], "cc": [], "bcc": []}
        ),
    ):
        module.enviar_consultas_banxico()

    # Assert
    download.assert_called_once_with(
        "https://example.test/document.pdf",
        "Documento principal - Consulta de prueba - 31_12_2026.pdf",
        module.SAVE_DOWNLOAD_DIR_PATH,
    )
    email.send.assert_called_once_with(
        "Subject",
        "Body",
        ["to@example.test"],
        [],
        [],
        files=[str(publication_file)],
    )
    log_service.log_delivery.assert_called_once_with("Consulta de prueba - 31_12_2026")
    assert not publication_file.exists()


def test_enviar_consultas_banxico_skips_publication_already_delivered(publication_row):
    # Arrange
    log_service = Mock()
    log_service.check_delivery.return_value = True
    consultations = pd.DataFrame([publication_row])

    # Act
    with (
        patch.object(module, "LogService", return_value=log_service),
        patch.object(module, "obtener_consultas_banxico", return_value=consultations),
        patch.object(module, "download_file") as download,
        patch.object(module, "email") as email,
    ):
        module.enviar_consultas_banxico()

    # Assert
    download.assert_not_called()
    email.send.assert_not_called()
    log_service.log_delivery.assert_not_called()
