# Copyright 2020 Thiago Teixeira
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
htbuilder -- Tiny HTML string builder for Python
===========================================

Build HTML strings using a purely functional syntax:

Example
-------

>>> from htbuilder import div, ul, li, img
>>>
>>> image_paths = [
...   "http://...",
...   "http://...",
...   "http://...",
... ]
>>>
>>> out = div(id="container")(
...   ul(_class="image-list")(
...     [
...       li(img(src=image_path, _class="large-image"))
...       for image_path in image_paths
...     ]
...   )
... )
>>>
>>> print(out)
>>>
>>> # Or convert to string with:
>>> x = str(out)

"""

from __future__ import annotations

from typing import Any, Iterable

from .funcs import func
from .units import unit
from .utils import classes, fonts, rule, styles

EMPTY_ELEMENTS = set(
    [
        # https://developer.mozilla.org/en-US/docs/Glossary/Empty_element
        "area",
        "base",
        "br",
        "col",
        "embed",
        "hr",
        "img",
        "input",
        "keygen",
        "link",
        "meta",
        "param",
        "source",
        "track",
        "wbr",
        # SVG
        "circle",
        "line",
        "path",
        "polygon",
        "polyline",
        "rect",
    ]
)


class HtmlElement:
    _MEMBERS = {
        "_cannot_have_attributes",
        "_cannot_have_children",
        "_tag",
        "_attrs",
        "_children",
    }

    def __init__(self, tag: str | None, *children: Any, **attrs: Any):
        """An HTML element."""
        self._tag = tag.lower() if tag else None
        self._attrs = attrs or {}
        self._children = _to_flat_list(children) or []

        self._cannot_have_attributes = tag is None
        self._cannot_have_children = tag in EMPTY_ELEMENTS

    def __call__(self, *children: Any, **attrs: Any) -> HtmlElement:
        if children:
            if self._cannot_have_children:
                raise TypeError(f"{self._tag} cannot have children")
            flattened = _to_flat_list(children)
            self._children += flattened

        if attrs:
            if self._cannot_have_attributes:
                raise TypeError("Fragments cannot have attributes")
            self._attrs = {**self._attrs, **attrs}

        return self

    def __getattr__(self, name: str) -> Any:
        if self._cannot_have_attributes:
            raise TypeError("Fragments cannot have attributes")

        if name in self._attrs:
            return self._attrs[name]

        raise AttributeError(f"No such attribute {name}")

    def __setattr__(self, name: str, value: Any) -> None:
        if name.startswith("_"):
            if name not in HtmlElement._MEMBERS and self._cannot_have_attributes:
                raise TypeError("Fragments cannot have attributes")

            object.__setattr__(self, name, value)
            return

        self._attrs[name] = value

    def __delattr__(self, name: str) -> None:
        if self._cannot_have_attributes:
            raise TypeError("Fragments cannot have attributes")

        del self._attrs[name]

    def __getitem__(self, *children: Any):
        return self(children)

    def __str__(self) -> str:
        children = "".join([str(c) for c in self._children])

        if self._tag is None:
            return children

        tag = _clean_name(self._tag)
        attrs = " ".join([f'{_clean_name(k)}="{v}"' for k, v in self._attrs.items()])

        if self._cannot_have_children:
            if self._attrs:
                return f"<{tag} {attrs}/>"
            else:
                return f"<{tag}/>"
        else:
            if self._attrs:
                return f"<{tag} {attrs}>{children}</{tag}>"
            else:
                return f"<{tag}>{children}</{tag}>"

    def _repr_html_(self) -> str:
        return str(self)


class HtmlTag:
    def __init__(self, tag: str | None):
        """HTML element builder."""
        self._tag = tag

    def __call__(self, *args: Any, **kwargs: Any) -> HtmlElement:
        return HtmlElement(self._tag, *args, **kwargs)

    def __getitem__(self, *children) -> HtmlElement:
        return self(*children)

    def __str__(self) -> str:
        return str(self())


def _clean_name(name: str) -> str:
    """
    This allows you to use reserved words by prepending/appending underscores.
    For example, "_class" instead of "class".
    """
    return name.strip("_").replace("_", "-")


fragment = HtmlTag(None)


def _to_flat_list(obj: Any) -> Any:
    queue = [list(obj)]
    out: list[Any] = []

    while queue:
        item = queue.pop(0)

        # Strings are iterables so they need to be excluded separately.
        if isinstance(item, str):
            out.append(item)

        elif not isinstance(item, Iterable):
            out.append(item)

        else:
            queue = list(item) + queue

    return out


def __getattr__(tag: str) -> HtmlTag:
    return HtmlTag(tag)
