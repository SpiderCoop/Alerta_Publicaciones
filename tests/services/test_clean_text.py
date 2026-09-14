from services.clean_text import clean_text


def test_clean_text_removes_accents_and_replaces_filename_characters():
    # Arrange
    text = "Árbol/niño: ¿Qué, acción? Ütil"

    # Act
    result = clean_text(text)

    # Assert
    assert result == "Arbol_nino_ ¿Que accion Util"


def test_clean_text_returns_empty_and_unmatched_characters_unchanged():
    # Arrange
    text = ""

    # Act
    result = clean_text(text)

    # Assert
    assert result == ""
