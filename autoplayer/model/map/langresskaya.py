from autoplayer.model.map.abstract_map import AbstractMap


class LangresskayaMap(AbstractMap):

    _name = AbstractMap.langresskaya_name
    _config_name_path = "./resources/map/langresskaya_name.png"
    _enemy_base = (113, 715)
    _near_base_point = (120, 679)
    _key_point_w = (99, 637)
    _key_point_c = (119, 651)
    _key_point_e = (151, 666)

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
