from unittest.mock import Mock, patch

import pytest

from services.download_service import download_file


def test_download_file_creates_directory_and_writes_successful_response(tmp_path):
    # Arrange
    target_dir = tmp_path / "downloads"
    response = Mock(status_code=200, content=b"pdf content")

    # Act
    with patch("services.download_service.requests.get", return_value=response) as get:
        file_path = download_file(
            "https://example.test/file.pdf", "report.pdf", str(target_dir)
        )

    # Assert
    get.assert_called_once_with(
        "https://example.test/file.pdf", headers={"User-Agent": "Mozilla/5.0"}
    )
    assert target_dir.is_dir()
    assert file_path == str(target_dir / "report.pdf")
    assert (target_dir / "report.pdf").read_bytes() == b"pdf content"


def test_download_file_raises_for_unsuccessful_response(tmp_path):
    # Arrange
    response = Mock(status_code=404, content=b"")

    # Act and Assert
    with (
        patch("services.download_service.requests.get", return_value=response),
        pytest.raises(FileNotFoundError, match="Error al descargar"),
    ):
        download_file("https://example.test/missing.pdf", "missing.pdf", str(tmp_path))
