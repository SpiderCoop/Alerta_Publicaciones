from unittest.mock import patch

from services.keep_job_active import keep_job_active


def test_keep_job_active_writes_zero_when_random_value_is_not_above_threshold(tmp_path):
    # Arrange
    save_path = tmp_path / "state" / "keep_active.txt"

    # Act
    with patch("services.keep_job_active.random.random", return_value=0.8):
        keep_job_active(str(save_path))

    # Assert
    assert save_path.read_text() == "0"


def test_keep_job_active_writes_one_when_random_value_is_above_threshold(tmp_path):
    # Arrange
    save_path = tmp_path / "keep_active.txt"

    # Act
    with patch("services.keep_job_active.random.random", return_value=0.81):
        keep_job_active(str(save_path))

    # Assert
    assert save_path.read_text() == "1"


def test_keep_job_active_supports_a_filename_without_a_directory(tmp_path, monkeypatch):
    # Arrange
    monkeypatch.chdir(tmp_path)

    # Act
    with patch("services.keep_job_active.random.random", return_value=0.1):
        keep_job_active("keep_active.txt")

    # Assert
    assert (tmp_path / "keep_active.txt").read_text() == "0"
