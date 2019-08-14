from autoplayer.model.faction.abstract_faction import AbstractFaction
from autoplayer.config.coordinates import match_faction_usa_coordinates
from autoplayer.config.paths import usa_symbol


class USAFaction(AbstractFaction):

    _symbol_path = usa_symbol
    _name = AbstractFaction.usa_name
    _base_unit_order_time = 28
    _match_select_coordinates = match_faction_usa_coordinates

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
        return "q" if self.grid_layout_used else "r"  # Rifleman # r - for classic

    def get_base_unit_order_time(self):
        return self._base_unit_order_time

    def get_match_select_coordinates(self):
        return self._match_select_coordinates
