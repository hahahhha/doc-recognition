import cv2
import numpy as np
import json

from document_header_parser import DocumentHeaderParser
from document_table_parser import DocumentTableParser
from parse_data_object import ParseDataObject
from src.udp_parsers.ocr_result_object import OcrResultObject

parse_objects = [
    ParseDataObject("продавец", "продавец", "seller"),
    ParseDataObject("адрес", "адрес", "address"),
    ParseDataObject("инн/кпп продавца", r"инн.*кпп\s*продавца", 'seller inn/kpp'),
    ParseDataObject("грузоотправитель и его адрес", r"грузоотправитель\s*и\s*его\s*адрес", 'gruz address'),
    ParseDataObject("грузополучатель и его адрес", r"грузополучатель\s*и\s*его\s*адрес", 'poluchat address'),
    ParseDataObject("к платежно-расчетному документу", r"к\s*платежно.*расчетному\s*документу", 'platezh raschet'),
    ParseDataObject("покупатель", "покупатель", 'buyer'),
    ParseDataObject("адрес", "адрес", 'address'),
    ParseDataObject("инн/кпп покупателя", r"инн.*кпп\s*покупателя", 'buyer inn/kpp'),
    ParseDataObject("валюта: наименование, код", r"валюта.*\s*наименование.*\s*код", 'currency'),
]

class UpdScanParser:
    # """сканирует ОДИН файл, для каждого файла нужно создавать новый""" или нет
    def __init__(self, img_to_parse: np.ndarray, header_parse_objects: list):
        self.__img = img_to_parse
        self.__header_parse_objects = header_parse_objects

    def parse_to_file(self, output_filename):
        header_parser = DocumentHeaderParser(self.__img, self.__header_parse_objects)
        parsed_header = header_parser.parse_header_scan_to_dict()
        highest_y = 0
        for res_list in parsed_header.values():
            to_check = [ocr_res.y2 for ocr_res in res_list]
            if not to_check:
                continue
            highest_y = max(highest_y, max(to_check))
        table_parser = DocumentTableParser(self.__img, highest_y + 1)
        parsed_table = table_parser.parse_table()
        result_dict = dict()
        for json_name, ocr_res_list in parsed_header.items():
            text = ' '.join(ocr_res.text for ocr_res in ocr_res_list)
            result_dict[json_name] = text
        result_dict['table'] = []
        for ocr_res in parsed_table:
            d = {
                "text": ocr_res.text,
                "coordinates": [[ocr_res.x1, ocr_res.y1], [ocr_res.x2, ocr_res.y2]],
            }
            result_dict['table'].append(d)
        with open(output_filename, 'w', encoding='utf-8') as f:
            json.dump(result_dict, f, ensure_ascii=False, indent=4)
        return result_dict


if __name__ == '__main__':
    img = cv2.imread("../tests/images/upd1_page1.jpg")
    usp = UpdScanParser(img, parse_objects)
    table = usp.parse_to_file('output.json')['table']
    canvas = np.zeros(img.shape, dtype=np.uint8)
    import random as rnd
    cnt = 0
    for d in table:
        text = d['text']
        p1, p2 = d['coordinates']
        canvas = cv2.rectangle(canvas, p1, p2, (rnd.randint(100, 255), rnd.randint(100, 255), rnd.randint(100, 255)), 2)
        canvas = cv2.putText(canvas, 'data', p2, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255))
        cnt += 1
    cv2.imwrite('res.jpg', canvas)
    print(cnt)
    print(len(table))