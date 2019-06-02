from autoplayer.model.faction.abstract_faction import AbstractFaction


class OKWFaction(AbstractFaction):

    _symbol_path = "./resources/faction/okw_symbol_setup.png"
    _name = AbstractFaction.okw_name

    def __init__(self):
        AbstractFaction.__init__(self)

    def get_faction_name(self):
        return self._name

    def get_faction_symbol_path(self):
        return self._symbol_path

    def get_match_config_path(self):
        pass

    def get_base_unit_button(self):
        return "v"
