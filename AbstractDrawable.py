from __future__ import annotations
from abc import abstractmethod


class AbstractDrawable:
    """
    Base class for drawable items
    """
    @abstractmethod
    def align_components(self) -> AbstractDrawable:
        """
        Align drawable items in layouts/scenes
        :return self:
        """
        ...

    @abstractmethod
    def customize_components(self) -> AbstractDrawable:
        """
        Set custom properties to drawable items
        :return self:
        """
        ...

    @abstractmethod
    def connect_components(self) -> AbstractDrawable:
        """
        Connect QSignals to QSlots
        :return self:
        """
        ...

    def init(self) -> AbstractDrawable:
        """
        Initialize drawable item
        :return self:
        """
        return self.align_components().customize_components().connect_components()
