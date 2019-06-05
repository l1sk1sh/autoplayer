from autoplayer.model.faction.abstract_faction import AbstractFaction


class RUSFaction(AbstractFaction):

    _symbol_path = "./resources/faction/rus_symbol_setup.png"
    _name = AbstractFaction.ussr_name
    _base_unit_order_time = 28

    def __init__(self):
        AbstractFaction.__init__(self)

    def get_faction_name(self):
        return self._name

    def get_faction_symbol_path(self):
        return self._symbol_path

    def get_match_config_path(self):
        pass

    def get_base_unit_button(self):
        return "r"  # Conscript Infantry Squad

    def get_base_unit_order_time(self):
        return self._base_unit_order_time
