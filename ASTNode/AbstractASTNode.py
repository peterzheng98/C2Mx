from abc import abstractmethod
from enum import Enum


class AbstractASTNode:
    nodeType = None
    originalPosition = None

    @abstractmethod
    def generateMx(self) -> str:
        raise NotImplementedError()
