from envly import *
from typing import *
from typing import Protocol


class Pair(Protocol):
    @property
    def name(self) -> str:
        ...

    @property
    def Type_(self) -> str:
        # subject to change
        ...


class Member(Pair):
    pass


class Argument(Pair):
    pass


class Local(Pair):
    pass


class Statment(Protocol):
    pass


class LevirFunction(Protocol):
    @property
    def name(self) -> str:
        ...

    @property
    def rettype(self) -> str:
        ...

    @property
    def args(self) -> Dict[str, Argument]:
        ...


# blends middle and front
class LevirType(Protocol):
    @property
    def name(self) -> str:
        ...

    @property
    def mbrs(self) -> Dict[str, Member]:
        ...


class LevirModule(Protocol):

    # @property
    # def items(self) -> Dict[str, Union[LevirType, LevirFunction]]:
    #    ...

    def find(self, name: str) -> Option[Union[LevirType, LevirFunction]]:
        ...

    def has(self, name: str) -> bool:
        ...

    def iteritems(self) -> Iterable[Union[LevirType, LevirFunction]]:
        ...
