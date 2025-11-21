import easyocr
import cv2
import numpy as np
import json

from document_object import DocumentObject
from parse_data import ParseDataObject
from img_bboxer import ImageBboxer


class DocumentParser:
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
        self.__document_objects = DocumentParser.convert_parse_objects_to_doc_objects(parse_data_objects, self.__img_bboxer)

        # читаем текст
        reader = easyocr.Reader(['ru', 'en'])
        self.__ocr_results = reader.readtext(self.__img)


    def __search_titles_bboxes(self) -> None:
        for doc_obj in self.__document_objects:
            for bbox, text, confidence in self.__ocr_results:
                if doc_obj.check_title_match(text):
                    doc_obj.insert_title_bbox_with_auto_value_bbox(bbox)


    def parse_scan_to_json(self, output_file_name: str) -> None:
        self.__search_titles_bboxes()
        json_data = dict(zip([do.json_title for do in self.__document_objects],
                             [[] for _ in range(len(self.__document_objects))]))
        for doc_obj in self.__document_objects:
            if not doc_obj.is_value_bbox_inserted:
                json_data[doc_obj.json_title] = ['not found']
                continue
            for bbox, text, confidence in self.__ocr_results:
                if ImageBboxer.is_totally_inside(doc_obj.value_bbox, bbox):
                    json_data[doc_obj.json_title].append(text)
        with open(output_file_name, 'w+', encoding='utf-8') as outfile:
            json.dump(json_data, outfile, ensure_ascii=False, indent=4)
        return