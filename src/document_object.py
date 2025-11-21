import re
from img_bboxer import ImageBboxer

class DocumentObject:
    __extend_value = 5
    def __init__(self, title, json_title, title_search_patter, image_bboxer: ImageBboxer):
        self.__title = title
        self.__json_title = json_title
        self.__title_search_patter = title_search_patter
        self.__is_value_bbox_inserted = False

        self.__title_bbox = None
        self.__value_bbox = None

        self.__image_bboxer = image_bboxer
        self.__value = None

    @property
    def title(self):
        return self.__title

    @property
    def json_title(self):
        return self.__json_title

    @property
    def is_value_bbox_inserted(self):
        return self.__is_value_bbox_inserted

    @property
    def title_bbox(self):
        return self.__title_bbox

    @property
    def value_bbox(self):
        return self.__value_bbox

    @property
    def value(self):
        return self.__value

    def check_title_match(self, to_check_line: str) -> bool:
        # тут можно будет позже сделать, чтобы сразу возвращалась еще и часть, "переполняющая" название
        match = re.search(self.__title_search_patter, to_check_line)
        return match is not None

    def insert_title_bbox_with_auto_value_bbox(self, title_bbox) -> None:
        self.__title_bbox = title_bbox
        right_extended_bbox = self.__image_bboxer.get_right_extended_bbox(title_bbox, extend_value=self.__extend_value)
        self.__value_bbox = right_extended_bbox
        self.__is_value_bbox_inserted = True

    def insert_value(self, value: str) -> None:
        if not self.__is_value_bbox_inserted:
            raise Exception("нельзя вставлять значения в document object с не найденным value bbox")
        self.__value = value