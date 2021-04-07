from typing import *

__all__ = (
    "DataVariable",
)  # '_Field', '_DefaultField', '_FactoryField', '_DerivedField')


# fields implement the methods `.field_default(self) -> object`
# the one that shoudl be used are defined int env_bootsrtap


class DataVariable:
    def __init__(self, *args, **kwargs) -> Union[None]:
        if hasattr(self, "__annotations__"):
            anotes = type(self).__annotations__
        else:
            # OPTIMIZE: add a optimization here to not need to check
            anotes = {}

        # print(f"{args=}, {kwargs=}")

        if len(args) > len(anotes):
            raise TypeError(
                f"{type(self).__name__}.__init__(...) called with "
                f"{len(args)-len(anotes)} too many positional arguments"
            )

        # assign kwargs to args
        for arg, name in zip(args, anotes.keys()):
            # self._set_field_(name, arg)
            kwargs[name] = arg

        # set all non dfaults args
        for name, attr in kwargs.items():
            self._set_field_(name, attr)

        # load in defaults
        if len(kwargs) != len(anotes):  # see if it needs ot be laoded in
            cls = type(self)
            missing_poses = []
            for deflt in set(anotes) - set(kwargs):
                if not hasattr(cls, deflt):
                    missing_poses.append(deflt)
                else:
                    attr = getattr(cls, deflt)
                    self._set_field_(deflt, attr)
                    kwargs[deflt] = attr
                    # if attr is field do stuff
                    # if hasattr(attr, 'field_default'):
                    #    attr = attr.field_default(self)
                    # kwargs[deflt] = attr
            # else: # for
            if len(missing_poses):
                plural = ("s", "")[len(missing_poses) == 1]
                names = ", ".join(repr(pos_name) for pos_name in missing_poses)
                raise TypeError(
                    f"{type(self).__name__}.__init__(...) missing "
                    f"{len(missing_poses)} required positional "
                    f"argument{plural}: {names}"
                )

        extra_kwargs = set(kwargs) - set(anotes)
        way = len(extra_kwargs)
        if way:  # too many kwargs
            plural = ("", "1")[way > 2]
            raise TypeError(
                f"{type(self).__name__}.__init__(...) has {way} too many "
                f"keyword argument{plural}: {set(kwargs) - set(anotes)}"
            )

        if set(kwargs) > set(anotes):
            kwargs_set, anotes_set = set(kwargs), set(anotes)
            way = len(kwargs_set) - len(anotes_set)
            extras = ", ".join(repr(kw) for kw in kwargs_set - anotes_set)
            raise TypeError(
                f"{type(self).__name__}.__init__(...) called with "
                f"{way} too many keyword arguments: {extras}"
            )

        # for attr_name, attr in kwargs.items():
        #    global _Field
        #    #if isinstance(attr, _Field):
        #    #    attr = attr.field_default(self)
        #    setattr(self, attr_name, attr)

    def _set_field_(self, name: str, attr: object) -> None:
        global _Field
        # print(name, attr)
        if isinstance(attr, _Field):
            attr = attr.field_default(self)
        setattr(self, name, attr)

    def __repr__(self) -> str:
        params = tuple(f"{name}={repr(attr)}" for name, attr in self._attr_items_())
        return f"{type(self).__name__}({', '.join(params)})"

    def __eq__(self, other) -> bool:
        if not isinstance(other, type(self)):
            return False

        return all(a == b for a, b in zip(self._attrs_(), other._attrs_()))

    def __hash__(self) -> int:
        return hash(self._attrs_())

    def _attr_items_(self) -> Dict[str, object]:
        return tuple(
            (name, getattr(self, name)) for name in self.__annotations__
        )  # if not name.startswith('_'))

    def _attrs_(self) -> Tuple[object, ...]:
        return tuple(getattr(self, name) for name in self.__annotations__)


# for data Variable
class _Field(DataVariable):
    def field_default(self, inst) -> object:
        raise NotImplementedError(f"_Field must be subclassed to be used")


class _DefaultField(_Field):
    value: object

    def field_default(self, inst) -> object:
        return self.value


class _FactoryField(_Field):
    factory: Callable[[], object]

    def field_default(self, inst) -> object:
        return self.factory()


class _DerivedField(_Field):
    derivation: Callable[[object], object]

    def field_default(self, inst) -> object:
        return self.derivation(inst)


def test(print):
    tg_env = __import__("tg_env")

    Option = tg_env.Option
    Nothing = Option
    Some = Option

    class Point(DataVariable):
        x: int
        y: int
        z: Option[int] = _DefaultField(Nothing)

    hash(Point(1, 2))

    print(Point(1, 2))
    print(Point(1, 2, 3))

    class qux(DataVariable):
        x: int
        squared: int = _DerivedField(lambda self: self.x ** 2)
        _secret: Option[int] = Nothing  # needs more enhancement

    # todo: add a test for 0 pos and extra kwargs
    q = qux()
