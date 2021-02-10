from abc import ABC, abstractmethod


class AbstractMap(ABC):

    langresskaya_name = "langresskaya"

    def __init__(self):
        super().__init__()

    @abstractmethod
    def get_map_name(self):
        pass

    @abstractmethod
    def get_map_name_loading_screen(self):
        pass

    @abstractmethod
    def get_config_name_path(self):
        pass

    @abstractmethod
    def get_enemy_base(self):
        pass

    @abstractmethod
    def get_near_enemy_base_point(self):
        pass
