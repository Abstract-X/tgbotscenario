from tgbotscenario.common.magazine import Magazine


def test_item_not_in_magazine():

    magazine = Magazine(["InitialScene"])

    magazine.set("Scene")

    assert magazine == Magazine(["InitialScene", "Scene"])


def test_item_in_magazine():

    magazine = Magazine(["InitialScene", "Scene"])

    magazine.set("InitialScene")

    assert magazine == Magazine(["InitialScene"])
