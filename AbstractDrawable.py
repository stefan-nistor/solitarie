from __future__ import annotations
from abc import abstractmethod


class AbstractDrawable:
    @abstractmethod
    def align_components(self) -> AbstractDrawable:
        ...

    @abstractmethod
    def customize_components(self) -> AbstractDrawable:
        ...

    @abstractmethod
    def connect_components(self) -> AbstractDrawable:
        ...

    def init(self) -> AbstractDrawable:
        return self.align_components().customize_components().connect_components()
