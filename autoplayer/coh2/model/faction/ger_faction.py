from autoplayer.coh2.model.faction.abstract_faction import AbstractFaction
from autoplayer.coh2.coordinates import match_faction_ger_coordinates
from autoplayer.coh2.paths import ger_symbol


class GERFaction(AbstractFaction):

    _symbol_path = ger_symbol
    _name = AbstractFaction.wehrmacht_name
    _base_unit_order_time = 28
    _match_select_coordinates = match_faction_ger_coordinates

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
        return "q" if self.grid_layout_used else "e"  # Pioneer # e - for classic

    def get_base_unit_order_time(self):
        return self._base_unit_order_time

    def get_match_select_coordinates(self):
        return self._match_select_coordinates
