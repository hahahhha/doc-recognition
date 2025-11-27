from dataclasses import dataclass


@dataclass
class OcrResultObject:
    x1: int
    y1: int
    x2: int
    y2: int
    text: str