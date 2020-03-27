# htbuild — tiny HTML string builder for Python

htbuild lets you build HTML strings using a purely functional syntax in Python.
Why use templating languages when you can just use functions?

## Examples

If using Python 3.7+:

```py
# Import anything you want from htbuild, and it just works! None of these tags
# are hard-coded, so you can import literally anything.
# (This syntax requires Python 3.7+)
from htbuild import div, ul, li, img

image_paths = [
  "http://...",
  "http://...",
  "http://...",
]

out = (
  div(id="container")(
    ul(_class="image-list")(
      [
        li(img(src=image_path, _class="large-image"))
        for image_path in image_paths
      ]
    )
  )
)

print(out)
```

If using Python &lt; 3.7, the import should look like this instead:

```py
from htbuild import H

div = H.div
ul = H.ul
li = H.li
img = H.img
```

...then the rest is the same as in the previous example.


# Programmatically addign children

You can also pass a list to specify multiple children, which means you can
simply use `map()` and list comprehensions for great awesome:

```py
from htbuild import div, ul, li, img

image_paths = [
  "http://myimages.com/foo1.jpg",
  "http://myimages.com/foo2.jpg",
  "http://myimages.com/foo3.jpg",
]

html_element = (
  div(id="container")(
    ul(_class="image-list")(
      [
        li(img(src=image_path, _class="large-image"))
        for image_path in image_paths
      ]
    )
  )
)
```

# Styling

We provide helpers to write styles without having to pass huge style strings as
arguments. Instead, just use handy builders like `styles()`, `classes()`,
`fonts()`, along with helpers you can import from the `units` and `funcs`
modules.

```py
# styles, classes, and fonts are special imports to help build attribute strings.
from htbuild import div, styles, classes, fonts

# You can import anything from .units and .funcs to make it easier to specify
# units like "%" and "px", as well as functions like "rgba()" and "rgba()".
from htbuild.units import percent, px
from htbuild.funcs import rgba, rgb

bottom_margin = 10
is_big = True

dom = (
  div(
    _class=classes("btn", big=is_big)
    style=styles(
        color="black",
        font_family=fonts("Comic Sans", "sans"),
        margin=px(0, 0, bottom_margin, 0),
        padding=(px(10), percent(5))
        box_shadow=[
            (0, 0, px(10), rgba(0, 0, 0, 0.1)),
            (0, 0, "2px", rgb(0, 0, 0)),
        ],
    )
  )
)
```
