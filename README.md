# htbuild — tiny HTML string builder for Python

htbuild lets you build HTML strings using a purely functional syntax in Python.
Why use templating languages when you can just use functions?

## Usage

Just import tags like `div` with `from htbuild import div`, then call them:

```py
# Import any tag you want from htbuild, and it just works!
# (This syntax requires Python 3.7+. See below for an alternate syntax)
from htbuild import div

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


## Multiple children

Want to output multiple children? Just pass them all as arguments:

```py
from htbuild import div, ul, li, img

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

# Prints this (but without added spacing):
# <div id="container">
#   <ul class="greetings">
#     <li>hello</li>
#     <li>hi</li>
#     <li>whattup</li>
#   </ul>
# </div>
```

## Programmatically add children

You can also pass any iterable to specify multiple children, which means you can
simply use things like list comprehensions for great awesome:

```py
from htbuild import div, ul, li, img

image_paths = [
  'http://myimages.com/foo1.jpg',
  'http://myimages.com/foo2.jpg',
  'http://myimages.com/foo3.jpg',
]

dom = (
  div(id='container')(
    ul(_class='image-list')(
      li(img(src=image_path, _class='large-image'))
      for image_path in image_paths
    )
  )
)

print(dom)
# Prints:
# <div id="container">
#   <ul class="image-list">
#     <li><img src="http://myimages.com/foo1.jpg" class="large-image"/></li>
#     <li><img src="http://myimages.com/foo2.jpg" class="large-image"/></li>
#     <li><img src="http://myimages.com/foo3.jpg" class="large-image"/></li>
#   </ul>
# </div>
```

## Conditionally add elements

And because it's just Python, you can use an if/else expression to conditionally
insert elements:

```py
use_bold = True

dom = (
  div(
      b("bold text")
    if use_bold else
      "normal text"
  )
)

print(dom)
# Prints: <div><b>bold text</b></div>
```

## Styling

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
        font_family=fonts('Comic Sans', 'sans-serif'),
        margin=px(0, 0, bottom_margin, 0),
        padding=(px(10), percent(5))
        box_shadow=[
            (0, 0, px(10), rgba(0, 0, 0, 0.1)),
            (0, 0, '2px', rgb(0, 0, 0)),
        ],
    )
  )
)

# Prints:
# <div
#   class="btn big"
#   style="
#     color: black;
#     font-family: "Comic Sans", "sans-serif";
#     margin: 0 0 10px 0;
#     padding: 10px 5%;
#     box-shadow: 0 0 10px rgba(0, 0, 0, 0.1), 0 0 2px rgb(0, 0, 0);
#   "></div>
```


## Working with Python &lt; 3.7

If using Python &lt; 3.7, the import should look like this instead:

```py
from htbuild import H

div = H.div
ul = H.ul
li = H.li
img = H.img
# ...etc
```
