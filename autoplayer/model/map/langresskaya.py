from autoplayer.model.map.abstract_map import AbstractMap
from autoplayer.constants.paths import langresskaya_map
from autoplayer.constants.coordinates import langresskaya_enemy_base, \
    langresskaya_key_point_c, langresskaya_key_point_e, langresskaya_key_point_w, langresskaya_near_base_point


class LangresskayaMap(AbstractMap):

    _name = AbstractMap.langresskaya_name
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

    def get_config_name_path(self):
        return self._config_name_path

    def get_enemy_base(self):
        return self._enemy_base

    def get_near_enemy_base_point(self):
        return self._near_base_point
