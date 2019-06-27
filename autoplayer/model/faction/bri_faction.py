from autoplayer.model.faction.abstract_faction import AbstractFaction


class BRIFaction(AbstractFaction):

    _symbol_path = "./resources/faction/bri_symbol_setup.png"
    _name = AbstractFaction.british_name
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
        return "q"  # Infantry Section # t - for classic

    def get_base_unit_order_time(self):
        return self._base_unit_order_time
