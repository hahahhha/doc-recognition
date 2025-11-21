import numpy as np


class ImageBboxer:
    def __init__(self, img: np.ndarray):
        self.__img_width = img.shape[1]
        self.__img_height = img.shape[0]

    def get_right_extended_bbox(self, left_bbox: list, extend_value = 0):
        lt, rt, rb, lb = left_bbox
        new_lt = [int(lt[0]), int(lt[1]) - extend_value]
        new_rt = [self.__img_width, int(rt[1])]
        new_rb = [self.__img_width, int(rb[1])]
        new_lb = [int(rb[0]), int(rb[1]) + extend_value]
        return [new_lt, new_rt, new_rb, new_lb]

    @staticmethod
    def is_totally_inside(outside_bbox: list, inside_bbox: list):
        def bbox_to_limits(bbox):
            xs = [point[0] for point in bbox]
            ys = [point[1] for point in bbox]
            return [min(xs), min(ys), max(xs), max(ys)]

        outside_limits = bbox_to_limits(outside_bbox)
        inside_limits = bbox_to_limits(inside_bbox)

        # Проверяем, что внутренний bbox полностью внутри внешнего
        return (inside_limits[0] >= outside_limits[0] and  # min_x внутри
                inside_limits[1] >= outside_limits[1] and  # min_y внутри
                inside_limits[2] <= outside_limits[2] and  # max_x внутри
                inside_limits[3] <= outside_limits[3])  # max_y внутри