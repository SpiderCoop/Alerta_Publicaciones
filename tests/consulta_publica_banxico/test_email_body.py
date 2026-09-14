from consulta_publica_banxico.email_body import create_email_body


def test_create_email_body_returns_subject_and_html_body():
    # Arrange
    consultation = "Consulta sobre regulación"
    deadline = "31/12/2026"

    # Act
    subject, body = create_email_body(consultation, deadline)

    # Assert
    assert subject == "Nueva Consulta Publica Banxico - Consulta sobre regulación"
    assert deadline in body
    assert "<br><br><b>" in body
    assert "correo enviado de forma automatizada" in body
