from unittest.mock import Mock, patch

import pytest
from selenium.common.exceptions import NoSuchElementException

from consulta_publica_banxico.web_scrapper import obtener_consultas_banxico


class FakeElement:
    def __init__(self, text="", by_selector=None, elements=None):
        self.text = text
        self.by_selector = by_selector or {}
        self.elements = elements or {}
        self.clicked = False

    def find_element(self, _by, selector):
        return self.by_selector[selector]

    def find_elements(self, _by, selector):
        return self.elements.get(selector, [])

    def click(self):
        self.clicked = True

    def get_attribute(self, name):
        return self.by_selector.get(name)


def test_obtener_consultas_banxico_returns_valid_rows_and_quits_driver():
    # Arrange
    link = FakeElement(
        text="Documento", by_selector={"href": "https://example.test/doc.pdf"}
    )
    item = FakeElement(
        text="Consulta pública\nInformación adicional",
        by_selector={"span": FakeElement(text="31/12/2026")},
        elements={"a.button": [link]},
    )
    tab = FakeElement()
    tab_list = FakeElement(by_selector={'li[aria-controls="vigentes"]': tab})
    tabs = FakeElement(by_selector={'ul[role="tablist"]': tab_list})
    content = FakeElement(elements={"li": [item]})
    driver = Mock()
    wait_results = iter([tabs, content])

    # Act
    with (
        patch(
            "consulta_publica_banxico.web_scrapper.driver_configuration",
            return_value=driver,
        ),
        patch(
            "consulta_publica_banxico.web_scrapper.WebDriverWait.until",
            side_effect=lambda _condition: next(wait_results),
        ),
    ):
        result = obtener_consultas_banxico()

    # Assert
    assert result.to_dict("records") == [
        {
            "nombre": "Consulta pública",
            "fecha_limite": "31/12/2026",
            "enlaces": {"Documento": "https://example.test/doc.pdf"},
        }
    ]
    assert tab.clicked is True
    driver.get.assert_called_once_with(
        "https://www.banxico.org.mx/ConsultaRegulacionWeb/"
    )
    driver.quit.assert_called_once()


def test_obtener_consultas_banxico_uses_historical_tab_when_requested():
    # Arrange
    historical_tab = FakeElement()
    tab_list = FakeElement(
        by_selector={'li[aria-controls="historicas"]': historical_tab}
    )
    tabs = FakeElement(by_selector={'ul[role="tablist"]': tab_list})
    content = FakeElement(elements={"li": []})
    driver = Mock()
    wait_results = iter([tabs, content])

    # Act
    with (
        patch(
            "consulta_publica_banxico.web_scrapper.driver_configuration",
            return_value=driver,
        ),
        patch(
            "consulta_publica_banxico.web_scrapper.WebDriverWait.until",
            side_effect=lambda _condition: next(wait_results),
        ),
    ):
        result = obtener_consultas_banxico(vigentes=False)

    # Assert
    assert result.empty
    assert historical_tab.clicked is True
    driver.quit.assert_called_once()


def test_obtener_consultas_banxico_wraps_tab_errors_and_quits_driver():
    # Arrange
    driver = Mock()
    with (
        patch(
            "consulta_publica_banxico.web_scrapper.driver_configuration",
            return_value=driver,
        ),
        patch(
            "consulta_publica_banxico.web_scrapper.WebDriverWait.until",
            side_effect=RuntimeError("timeout"),
        ),
        pytest.raises(ValueError, match="Error al hacer click en la tab"),
    ):
        # Act and Assert
        obtener_consultas_banxico()

    driver.quit.assert_called_once()


def test_obtener_consultas_banxico_wraps_content_errors_and_quits_driver():
    # Arrange
    driver = Mock()
    tabs = FakeElement(
        by_selector={
            'ul[role="tablist"]': FakeElement(
                by_selector={'li[aria-controls="vigentes"]': FakeElement()}
            )
        }
    )
    wait_results = iter([tabs, RuntimeError("content timeout")])

    def wait_until(_condition):
        result = next(wait_results)
        if isinstance(result, Exception):
            raise result
        return result

    # Act and Assert
    with (
        patch(
            "consulta_publica_banxico.web_scrapper.driver_configuration",
            return_value=driver,
        ),
        patch(
            "consulta_publica_banxico.web_scrapper.WebDriverWait.until",
            side_effect=wait_until,
        ),
        pytest.raises(ValueError, match="Error al buscar los elementos"),
    ):
        obtener_consultas_banxico()

    driver.quit.assert_called_once()


def test_obtener_consultas_banxico_ignores_items_without_required_fields():
    # Arrange
    incomplete_item = FakeElement(
        text="Incomplete consultation",
        by_selector={
            "span": NoSuchElementException("missing date"),
        },
    )

    def find_missing(_by, selector):
        error = incomplete_item.by_selector.get(selector)
        if isinstance(error, Exception):
            raise error
        return error

    incomplete_item.find_element = find_missing
    missing_links_item = FakeElement(
        text="Missing links",
        by_selector={"span": FakeElement(text="31/12/2026")},
    )
    missing_links_item.find_elements = Mock(
        side_effect=NoSuchElementException("missing links")
    )

    class MissingNameElement(FakeElement):
        def __init__(self, by_selector=None, elements=None):
            self.by_selector = by_selector or {}
            self.elements = elements or {}
            self.clicked = False

        @property
        def text(self):
            raise NoSuchElementException("missing name")

    missing_name_item = MissingNameElement(
        by_selector={"span": FakeElement(text="31/12/2026")},
        elements={"a.button": []},
    )
    tab = FakeElement()
    tabs = FakeElement(
        by_selector={
            'ul[role="tablist"]': FakeElement(
                by_selector={'li[aria-controls="vigentes"]': tab}
            )
        }
    )
    content = FakeElement(
        elements={"li": [incomplete_item, missing_links_item, missing_name_item]}
    )
    driver = Mock()
    wait_results = iter([tabs, content])

    # Act
    with (
        patch(
            "consulta_publica_banxico.web_scrapper.driver_configuration",
            return_value=driver,
        ),
        patch(
            "consulta_publica_banxico.web_scrapper.WebDriverWait.until",
            side_effect=lambda _condition: next(wait_results),
        ),
    ):
        result = obtener_consultas_banxico()

    # Assert
    assert result.empty
    driver.quit.assert_called_once()
