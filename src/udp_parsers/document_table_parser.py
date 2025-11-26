import cv2
import easyocr
import numpy as np
import matplotlib.pyplot as plt

from typing import List, Tuple
from dataclasses import dataclass


@dataclass
class TableCell:
    x1: int
    y1: int
    x2: int
    y2: int
    ocr_result: str


class DocumentTableParser:
    """обраотка табличных данных в читаемый вид будет происходить на десктопе"""
    def __create_table_mask(self) -> np.ndarray:
        gray = cv2.cvtColor(self.__img, cv2.COLOR_BGR2GRAY)
        _, th = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

        # kernel = np.ones((1, 1), np.uint8)
        horizonta_lsize = max(10, th.shape[1] // 30)
        horizontal_structure = cv2.getStructuringElement(cv2.MORPH_RECT, (horizonta_lsize, 1))
        horizontal = cv2.erode(th, horizontal_structure)
        horizontal = cv2.dilate(horizontal, horizontal_structure)

        vertical_size = max(10, th.shape[0] // 30)
        vertical_structure = cv2.getStructuringElement(cv2.MORPH_RECT, (1, vertical_size))
        vertical = cv2.erode(th, vertical_structure)
        vertical = cv2.dilate(vertical, vertical_structure)

        table_mask = cv2.add(horizontal, vertical)
        return table_mask

    def __find_cells_contours(self, table_mask) -> List:
        contours, hierarchy = cv2.findContours(table_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        cells = []
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            if w < 10 or h < 10 or y < self.__start_y:
                continue
            cells.append((x, y, w, h))
        return cells

    def __recognize_cells(self, cells) -> List[TableCell]:
        result = []
        for x1, y1, w, h in cells:
            x2, y2 = x1 + w, y1 + h
            if y1 < self.__start_y or y2 < self.__start_y:
                continue
            cell_text = self.__reader.readtext(self.__img[y1:y2+1, x1:x2+1])
            result.append(TableCell(int(x1), int(y1), int(x2), int(y2), cell_text))
        return result


    def __init__(self, image: np.ndarray, start_y: int):
        self.__img = image
        self.__reader = easyocr.Reader(['ru', 'en'])
        self.__start_y = start_y
        return

    def parse_table(self) -> List[TableCell]:
        table_mask = self.__create_table_mask()
        cells = self.__find_cells_contours(table_mask)
        return self.__recognize_cells(cells)


if __name__ == '__main__':
    img = cv2.imread('../tests/images/upd1_page1.jpg')
    dtp = DocumentTableParser(img, start_y=300)
    parsed = dtp.parse_table()
    print(*[p.ocr_result for p in parsed], sep='\n')
    # dtp = DocumentTableParser(img, start_y=300)
    # cnt = 0
    # contours = []
    # for x, y, w, h in dtp.parse_table():
    #     img = cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
    #     cnt += 1
    #     if cnt == 20:
    #         break
    #     contours.append((x, y, x+w, y+h))
    # print(*contours, sep='\n')
    plt.figure(figsize=(12, 8))
    plt.axis('off')
    # plt.imshow(horizontal, cmap='gray')
    # plt.imshow(vertical, cmap='gray')
    plt.imshow(img)
    plt.show()
