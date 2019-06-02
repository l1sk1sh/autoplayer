from abc import ABC, abstractmethod


class AbstractFaction(ABC):

    okw_name = "okw"
    ussr_name = "rus"
    wehrmacht_name = "ger"
    british = "bri"
    usa_name = "usa"

    def __init__(self):
        super().__init__()

    @abstractmethod
    def get_faction_name(self):
        pass

    @abstractmethod
    def get_faction_symbol_path(self):
        pass

    @abstractmethod
    def get_match_config_path(self):
        pass

    @abstractmethod
    def get_base_unit_button(self):
        pass
