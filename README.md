# htbuild — tiny HTML string builder for Python

htbuild lets you build HTML strings using a purely functional syntax in Python.
Why use templating languages when you can just use functions?

## Usage

Just import tags like `div` with `from htbuild import div`, then call them:

```py
dom = div('Hello world!')
```

Then you can get the string output by calling `str()` on it:

```py
str(dom)
# Returns '<div>Hello world!</div>'
```

...which means you can also just `print()` to see it in the terminal:

```py
print(dom)
# Prints '<div>Hello world!</div>'
```

To specify attributes, call the tag builder with keyword args:

```py
print(
  div(id='sidebar', foo='bar')
)
# Prints '<div id="sidebar" foo="bar"></div>'
```

To specify both attributes and children, first specify the attributes using
keyword args, then pass the children afterwards by passing them **inside a new
set of parentheses**:

```py
print(
  div(id='sidebar', foo='bar')(
    "Hello world!"
  )
)
# Prints '<div id="sidebar" foo="bar">Hello world!</div>'
```

This is required because Python doesn't allow you to pass keyword arguments
_before_ you pass normal arguments.

## Examples

If using Python 3.7+:

```py
# Import anything you want from htbuild, and it just works! None of these tags
# are hard-coded, so you can import literally anything.
# (This syntax requires Python 3.7+)
from htbuild import div, ul, li, img

image_paths = [
  'http://...',
  'http://...',
  'http://...',
]

dom = (
  div(id='container')(
    ul(_class='greetings')(
      li('hello'),
      li('hi'),
      li('whattup'),
    )
  )
)

print(dom)
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


# Programmatically add children

You can also pass a list to specify multiple children, which means you can
simply use `map()` and list comprehensions for great awesome:

```py
from htbuild import div, ul, li, img

image_paths = [
  'http://myimages.com/foo1.jpg',
  'http://myimages.com/foo2.jpg',
  'http://myimages.com/foo3.jpg',
]

html_element = (
  div(id='container')(
    ul(_class='image-list')(
      [
        li(img(src=image_path, _class='large-image'))
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
    _class=classes('btn', big=is_big)
    style=styles(
        color='black',
        font_family=fonts('Comic Sans', 'sans'),
        margin=px(0, 0, bottom_margin, 0),
        padding=(px(10), percent(5))
        box_shadow=[
            (0, 0, px(10), rgba(0, 0, 0, 0.1)),
            (0, 0, '2px', rgb(0, 0, 0)),
        ],
    )
  )
)
```
