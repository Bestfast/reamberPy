from __future__ import annotations

from typing import Tuple, Dict, List

import pandas as pd

def item_props(prop_name='_props'):
    """ This decorator automatically creates the props needed to inherit.

    The format of the input MUST follow this strictly.

    SINGULAR<str> = TYPE<str>

    This is a custom decorator (unlike dataclass) because we intercept setter
    and getter to call our self.data pd.Series.

    This also generates the _from_series_allowed_names safety catch.
    """

    # noinspection PyShadowingNames
    def gen_props(cl: type, prop_name: str = prop_name):
        # Recursively finds all props and gathers them
        props_list = [getattr(cl, prop_name)]

        def get_prop(cl_: type):
            if cl_.__bases__ == type:
                return
            else:
                for b in cl_.__bases__:
                    if hasattr(b, prop_name):
                        props_list.append(getattr(b, prop_name))
                    get_prop(b)
        get_prop(cl)
        props = {k: v for i in props_list for k, v in i.items()}
        setattr(cl, prop_name, props)

        props: Dict[str, Tuple[str, str]]
        for k in props.keys():
            def setter(self, val, k_=k):
                self.data[k_] = val

            def getter(self, k_=k):
                return self.data[k_]

            setattr(cl, k, property(getter, setter))

        # noinspection PyDecorator
        @staticmethod
        def _from_series_allowed_names():
            names = []
            for b in cl.__bases__:
                if hasattr(b, '_from_series_allowed_names'):
                    # noinspection PyProtectedMember
                    names = [*names, *b._from_series_allowed_names()]
            return [*names, *props.keys()]

        cl._from_series_allowed_names = _from_series_allowed_names
        return cl
    return gen_props

def list_props(item_class: type, prop_name='_props'):
    """ This decorator automatically creates the props needed to inherit.

    This is a custom decorator (unlike dataclass) because we intercept setter
    and getter to call our self.data pd.DataFrame.

    This also generates the _from_series_allowed_names safety catch.
    """
    # noinspection PyShadowingNames
    def gen_props(cl: type, item_class_: type = item_class, prop_name:str = prop_name):
        props = getattr(item_class_, prop_name)
        _init_empty_dict = {}
        for k, v in props.items():
            _init_empty_dict[k] = pd.Series([], dtype=v)

            def setter(self, val, k_=k):
                self.df[k_] = val

            def getter(self, k_=k):
                return self.df[k_]

            setattr(cl, k, property(getter, setter))

        # noinspection PyDecorator, PyShadowingNames
        @staticmethod
        def _init_empty(props:dict = props) -> dict:
            return {k: pd.Series([], dtype=v) for k, v in props.items()}

        cl._init_empty = _init_empty

        # noinspection PyDecorator
        @staticmethod
        def _item_class(i=item_class_) -> type:
            return i

        cl._init_empty = _init_empty
        cl._item_class = _item_class

        return cl
    return gen_props

def stack_props(prop_name='_props'):
    """ This decorator automatically creates the props needed to inherit.

    This is a custom decorator (unlike dataclass) because we intercept setter
    and getter to call our self.data pd.DataFrame.

    The stack props must just be a string list

    This also generates the _from_series_allowed_names safety catch.
    """

    # noinspection PyShadowingNames
    def gen_props(cl: type, prop_name:str = prop_name):
        props = getattr(cl, prop_name)
        props: List[str]
        for k in props:
            def setter(self, val, k_=k):
                self[k_] = val

            def getter(self, k_=k):
                return self[k_]

            setattr(cl, k, property(getter, setter))
        return cl
    return gen_props

def map_props(prop_name='_props'):
    """ This decorator automatically creates the props needed to inherit.

    This is a custom decorator (unlike dataclass) because we intercept setter
    and getter to call our self.data pd.DataFrame.

    """
    # noinspection PyShadowingNames
    def gen_props(cl: type, prop_name:str = prop_name):
        props = getattr(cl, prop_name)
        for k, v in props.items():
            def setter(self, val, v_=v):
                self[v_][0].df = val.df

            def getter(self, v_=v):
                return self[v_][0]

            setattr(cl, k, property(getter, setter))
        return cl
    return gen_props
