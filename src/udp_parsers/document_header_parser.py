import easyocr
import cv2
import numpy as np

from document_object import DocumentObject
from parse_data_object import ParseDataObject
from img_bboxer import ImageBboxer

from get_temp_ocr_results import get_ocr_results
from ocr_result_object import OcrResultObject

class DocumentHeaderParser:
    @staticmethod
    def convert_parse_objects_to_doc_objects(parse_objects: list[ParseDataObject], img_bboxer: ImageBboxer) -> list[DocumentObject]:
        document_objects = []
        for pdo in parse_objects:
            do = DocumentObject(pdo.field_title, pdo.json_field_title, pdo.title_search_pattern, img_bboxer)
            document_objects.append(do)
        return document_objects

    def __init__(self, scan_img: np.ndarray, parse_data_objects: list[ParseDataObject]):
        self.__img = scan_img.copy()
        self.__img_bboxer = ImageBboxer(scan_img)
        self.__document_objects = DocumentHeaderParser.convert_parse_objects_to_doc_objects(parse_data_objects, self.__img_bboxer)

        # читаем текст
        reader = easyocr.Reader(['ru', 'en'])
        # self.__ocr_results = reader.readtext(self.__img)
        # на время теста для более быстрой отладки!!!
        self.__ocr_results = get_ocr_results()


    def __search_titles_bboxes(self) -> None:
        for doc_obj in self.__document_objects:
            for bbox, text, confidence in self.__ocr_results:
                if doc_obj.check_title_match(text):
                    doc_obj.insert_title_bbox_with_auto_value_bbox(bbox)


    def parse_header_scan_to_dict(self) -> dict[str, list[OcrResultObject]]:
        self.__search_titles_bboxes()
        scanned_data = dict(zip([do.json_title for do in self.__document_objects],
                                [[] for _ in range(len(self.__document_objects))]))
        for doc_obj in self.__document_objects:
            if not doc_obj.is_value_bbox_found:
                scanned_data[doc_obj.json_title] = ['not found']
                continue
            for bbox, text, confidence in self.__ocr_results:
                if ImageBboxer.is_totally_inside(doc_obj.value_bbox, bbox):
                    p1, p2, p3, p4 = [[int(p[0]), int(p[1])] for p in bbox]
                    scanned_data[doc_obj.json_title].append(
                        OcrResultObject(p1[0], p1[1], p3[0], p3[1], text)
                    )
        return scanned_data