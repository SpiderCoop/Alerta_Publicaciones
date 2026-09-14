from services.log_service import LogService


def test_log_service_creates_database_and_reports_delivery_state(tmp_path):
    # Arrange
    db_path = tmp_path / "nested" / "deliveries.db"
    service = LogService(str(db_path))

    # Act
    before_delivery = service.check_delivery("New consultation")
    service.log_delivery("New consultation")
    after_delivery = service.check_delivery("New consultation")

    # Assert
    assert db_path.exists()
    assert before_delivery is False
    assert after_delivery is True


def test_log_service_only_matches_the_requested_publication(tmp_path):
    # Arrange
    service = LogService(str(tmp_path / "deliveries.db"))
    service.log_delivery("First consultation")

    # Act
    result = service.check_delivery("Other consultation")

    # Assert
    assert result is False
