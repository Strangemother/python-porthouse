from enum import Enum, EnumMeta
import enum


class DynamicStrEnum(EnumMeta):
    def __new__(metacls, cls, bases=None, classdict=None):
        init_members = classdict or {}

        enum_dict = enum._EnumDict()
        bases = bases or (Enum,)

        for key, value in init_members.items():
            enum_dict[key] = value

        props = type(enum_dict)()
        props['has'] = classmethod(has)

        for key in enum_dict._member_names:
            value = enum_dict[key]
            props[key] = key.lower() if len(value) == 0 else value

        names = set(enum_dict._member_names)
        for key, value in enum_dict.items():
            if key in names:
                continue
            props[key] = value

        return super(DynamicStrEnum, metacls).__new__(metacls,
                                                      cls, bases, props)


def generate_enum(name, members_dict, enum_bases=None):
    """Build and return a new Enum class

        Baked = DynamicStrEnum('Cooked', (CookedBase,), get_members())
    """
    return DynamicStrEnum(name, enum_bases or (Enum,), members_dict)


def has(cls, value):
    return value in cls._value2member_map_
