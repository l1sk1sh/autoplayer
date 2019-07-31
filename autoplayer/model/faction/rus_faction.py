from autoplayer.model.faction.abstract_faction import AbstractFaction
from autoplayer.constants.coordinates import match_faction_rus_coordinates
from autoplayer.constants.paths import rus_symbol


class RUSFaction(AbstractFaction):

    _symbol_path = rus_symbol
    _name = AbstractFaction.ussr_name
    _base_unit_order_time = 28
    _match_select_coordinates = match_faction_rus_coordinates

    def __init__(self, grid_layout_used):
        AbstractFaction.__init__(self)
        self.grid_layout_used = grid_layout_used

    def get_faction_name(self):
        return self._name

    def get_faction_symbol_path(self):
        return self._symbol_path

    def get_match_config_path(self):
        pass

    def get_base_unit_button(self):
        return "w" if self.grid_layout_used else "c"  # Conscript Infantry Squad # c - for classic

    def get_base_unit_order_time(self):
        return self._base_unit_order_time

    def get_match_select_coordinates(self):
        return self._match_select_coordinates
