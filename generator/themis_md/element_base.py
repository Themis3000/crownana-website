from abc import ABC, abstractmethod
from typing import TextIO


class TElement(ABC):
    keyword = ""

    def __init__(self, f: TextIO):
        self.content = self._read_content(f)[len(self.keyword):]

    @classmethod
    def is_element(cls, fragment: str) -> bool:
        """Should return true or false if a fragment is of this element type"""
        return fragment.startswith(cls.keyword)

    @abstractmethod
    def gen_html(self) -> str:
        """Should return html representation as a string"""
        pass

    def _read_content(self, f: TextIO) -> str:
        """Should read and the full content of the element from an IO stream"""
        return f.readline()


class TMergeableElement(TElement, ABC):
    def __init__(self, f: TextIO):
        super().__init__(f)
        self.content_list = [self.content]

    def merge(self, other):
        self.content_list.extend(other.content_list)
