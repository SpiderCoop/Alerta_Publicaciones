import datetime as dt

from services.log_service import LogService


def test_log_service_creates_database_and_reports_delivery_state(tmp_path):
    # Arrange
    db_path = tmp_path / "nested" / "deliveries.db"
    service = LogService(str(db_path))
    publication_date = dt.date(2026, 11, 4)

    # Act
    before_delivery = service.check_delivery("New consultation", publication_date)
    service.log_delivery("New consultation", publication_date)
    after_delivery = service.check_delivery("New consultation", publication_date)

    # Assert
    assert db_path.exists()
    assert before_delivery is False
    assert after_delivery is True


def test_log_service_only_matches_the_requested_publication(tmp_path):
    # Arrange
    service = LogService(str(tmp_path / "deliveries.db"))
    publication_date = dt.date(2026, 11, 4)
    service.log_delivery("First consultation", publication_date)

    # Act
    result = service.check_delivery("Other consultation", publication_date)

    # Assert
    assert result is False


def test_log_service_only_matches_the_requested_publication_date(tmp_path):
    # Arrange
    service = LogService(str(tmp_path / "deliveries.db"))
    service.log_delivery("Same consultation", dt.date(2026, 11, 4))

    # Act
    result = service.check_delivery("Same consultation", dt.date(2026, 11, 5))

    # Assert
    assert result is False
