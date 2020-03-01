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
htbuild -- Tiny HTML string builder for Python
===========================================

Build HTML strings using a purely functional syntax:

Example
-------

If using Python 3.7+:

>>> from htbuild import div, ul, li, img  # This syntax requires Python 3.7+
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


If using Python < 3.7, the import should look like this instead:

>>> from htbuild import H
>>>
>>> div = H.div
>>> ul = H.ul
>>> li = H.li
>>> img = H.img
>>>
>>> # ...then the rest is the same as in the previous example.

"""

from iteration_utilities import deepflatten


# https://developer.mozilla.org/en-US/docs/Glossary/Empty_element
EMPTY_ELEMENTS = set([
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
])


class _ElementCreator(object):
    def __getattr__(self, tag):
        return HtmlTag(tag)


class HtmlTag(object):
    def __init__(self, tag):
        """HTML element builder."""
        self._tag = tag

    def __call__(self, *args, **kwargs):
        el = HtmlElement(self._tag)
        el(*args, **kwargs)
        return el


class HtmlElement(object):
    def __init__(self, tag, attrs={}, children=[]):
        """An HTML element."""
        self._tag = tag.lower()
        self._attrs = attrs
        self._children = children
        self._is_empty = tag in EMPTY_ELEMENTS

    def __call__(self, *children, **attrs):
        if children and attrs:
            raise TypeError("Cannot have both children and attrs")

        if children:
            if self._is_empty:
                raise TypeError("<%s> cannot have children" % self._tag)
            self._children = deepflatten([*self._children, *children])

        if attrs:
            self._attrs = {**self._attrs, **attrs}

        return self

    def __str__(self):
        args = {
            "tag": self._tag,
            "attrs": " ".join([
                "%s=\"%s\"" % (_clean_attr_name(k), v)
                for k, v in self._attrs.items()
            ]),
            "children": "".join([str(c) for c in self._children])
        }

        if self._is_empty:
            if self._attrs:
                return "<%(tag)s %(attrs)s>" % args
            else:
                return "<%(tag)s>" % args
        else:
            if self._attrs:
                return "<%(tag)s %(attrs)s>%(children)s</%(tag)s>" % args
            else:
                return "<%(tag)s>%(children)s</%(tag)s>" % args


def _clean_attr_name(k):
    # This allows you to use reserved words by prepending/appending underscores.
    # For example, "_class" instead of "class".
    return k.strip("_")


def classes(*names, convert_underscores=True, **names_and_bools):
    """Join multiple class names with spaces between them.

    Example
    -------

    >>> classes("foo", "bar", baz=False, boz=True, long_name=True)
    "foo bar boz long-name"

    Or, if you want to keep the underscores:

    >>> classes("foo", "bar", long_name=True, convert_underscores=False)
    "foo bar long_name"

    """
    if convert_underscores:
        def clean(name):
            return name.replace("_", "-")
    else:
        def clean(name):
            return name

    classes = [clean(name) for name in names]

    for name, include in names_and_bools.items():
        if include:
            classes.append(clean(name))

    return " ".join(classes)


def styles(**rules):
    """Create a style string from Python objects.

    For rules that have multiple components use tuples or lists. Tuples are
    joined with spaces " ", lists are joined with commas ",". And although you
    can use lists for font-family rules, we also provide a helper called
    `fonts()` that wraps font names in quotes as well. See example below.

    Example
    -------

    >>> styles(
    ...     background="black",
    ...     font_family=fonts("Comic Sans", "sans"),
    ...     margin=(0, 0, "10px", 0),
    ...     box_shadow=[
    ...         (0, 0, "10px", func.rgba(0, 0, 0, 0.1)),
    ...         (0, 0, "2px", func.rgba(0, 0, 0, 0.5)),
    ...     ],
    ... )
    ...
    "background:black;font-family:\"Comic Sans\",\"sans\";margin:0 0 10px 0;
    box-shadow:0 0 10px rgba(0,0,0,0.1),0 0 2px rgba(0,0,0,0.5)"

    """
    if not isinstance(rules, dict):
        raise TypeError("Style must be a dict")

    return ";".join(
        "%s:%s" % (k.replace("_", "-"), _parse_style_value(v))
        for (k, v) in rules.items()
    )

    return _parse_style_value(v)


def _parse_style_value(style):
    if isinstance(style, tuple):
        return ",".join(_parse_style_value(x) for x  in style)

    if isinstance(style, list):
        return ";".join(_parse_style_value(x) for x  in style)

    return str(style)


class _FuncBuilder(object):
    """"""
    def __getattr__(self, name):
        def _the_func(*args):
            return "%s(%s)" % (name, ",".join(str(x) for x in args))
        return _the_func


func = _FuncBuilder()


def fonts(*names):
    """Join fonts with quotes and commas.

    >>> fonts("Comic Sans, "sans")
    "\"Comic Sans\", \"Sans\""
    """
    return ",".join('"%s"' % name for name in names)


# Python >= 3.7
# https://docs.python.org/3/reference/datamodel.html#customizing-module-attribute-access
def __getattr__(tag):
    return HtmlTag(tag)


# For Python < 3.7
H = _ElementCreator()
