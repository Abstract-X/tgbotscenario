from tgbotscenario.common.magazine import Magazine


def test_item_not_exists():

    magazine = Magazine(["InitialScene", "Scene"])

    assert magazine.previous == "InitialScene"


def test_item_exists():

    magazine = Magazine(["InitialScene"])

    assert magazine.previous is None
