from autoplayer.coh2.model.map.abstract_map import AbstractMap
from autoplayer.coh2.paths import langresskaya_map, langresskaya_map_loadin_screen
from autoplayer.coh2.coordinates import langresskaya_enemy_base, \
    langresskaya_key_point_c, langresskaya_key_point_e, langresskaya_key_point_w, langresskaya_near_base_point


class LangresskayaMap(AbstractMap):

    _name = AbstractMap.langresskaya_name
    _name_loading_screen = langresskaya_map_loadin_screen
    _config_name_path = langresskaya_map
    _enemy_base = langresskaya_enemy_base
    _near_base_point = langresskaya_near_base_point
    _key_point_w = langresskaya_key_point_w
    _key_point_c = langresskaya_key_point_c
    _key_point_e = langresskaya_key_point_e

    def __init__(self):
        AbstractMap.__init__(self)

    def get_map_name(self):
        return self._name

    def get_map_name_loading_screen(self):
        return self._name_loading_screen

    def get_config_name_path(self):
        return self._config_name_path

    def get_enemy_base(self):
        return self._enemy_base

    def get_near_enemy_base_point(self):
        return self._near_base_point
