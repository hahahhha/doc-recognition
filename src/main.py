import cv2


def main():
    img = cv2.imread('tests/images/upd1_page1.jpg', cv2.IMREAD_GRAYSCALE)
    # dp = DocumentHeaderParser(img, parse_objects)
    # dp.parse_header_scan_to_json('output.json')
    # print('done')

if __name__ == '__main__':
    main()
