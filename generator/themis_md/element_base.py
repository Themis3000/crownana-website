from abc import ABC, abstractmethod
from typing import TextIO


class TElement(ABC):
    def __init__(self, f: TextIO):
        self.content = self._read_content(f)[len(self.keyword):]

    # noinspection PyPropertyDefinition
    @staticmethod
    @property
    @abstractmethod
    def keyword() -> str:
        pass

    @abstractmethod
    def gen_html(self) -> str:
        """Should return html representation as a string"""
        pass

    @abstractmethod
    def _read_content(self, f: TextIO) -> str:
        """Should read and the full content of the element from an IO stream"""
