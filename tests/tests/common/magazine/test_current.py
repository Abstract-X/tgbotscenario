from tgbotscenario.common.magazine import Magazine


def test():

    magazine = Magazine(["InitialScene", "Scene"])

    assert magazine.current == "Scene"
