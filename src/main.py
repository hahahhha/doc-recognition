import cv2
import easyocr

from document_parser import DocumentParser
from parse_data import ParseDataObject

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


def main():
    img = cv2.imread('tests/images/upd1_page1.jpg', cv2.IMREAD_GRAYSCALE)
    dp = DocumentParser(img, parse_objects)
    dp.parse_scan_to_json('output.json')
    print('done')

if __name__ == '__main__':
    main()
