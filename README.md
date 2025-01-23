# htbuilder — tiny HTML string builder for Python

[![htbuilder Downloads Last Month](https://assets.piptrends.com/get-last-month-downloads-badge/htbuilder.svg 'htbuilder Downloads Last Month by pip Trends')](https://piptrends.com/package/htbuilder)

htbuilder lets you build HTML strings using a purely functional syntax in Python.
Why use templating languages when you can just use functions?

(PS: If you like this, check out [jsbuilder](https://github.com/tvst/jsbuilder) which
lets you build JavaScript strings by simply annotating Python functions!)

## Installation

Just PIP it!

```py
pip install htbuilder
```

## Usage

Just import tags like `div` with `from htbuilder import div`, then call them:

```py
# Import any tag you want from htbuilder, and it just works!
from htbuilder import div

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

To specify both attributes and children, you can just use regular Python argument
notation:

```py
print(
  div("Hello world!", id='sidebar', foo='bar')
)
# Prints '<div id="sidebar" foo="bar">Hello world!</div>'
```

...but some might find this order a bit weird! It doesn't the ordering you might be used to in HTML.

So we also support two other notations:

1. You can then pass the children afterwards **inside a new set of parentheses**:

   ```py
   print(
     div(id='sidebar', foo='bar')(
       "Hello world!"
     )
   )
   # Prints '<div id="sidebar" foo="bar">Hello world!</div>'
   ```

1. Or you can pass the children inside `[]` for added clarity:

   ```py
   print(
     div(id='sidebar', foo='bar')[
       "Hello world!"
     ]
   )
   # Prints '<div id="sidebar" foo="bar">Hello world!</div>'
   ```

All these notations are totally valid and fine! Just pick the one you like best.

## Multiple children

Want to output multiple children? Just pass them all as arguments:

```py
from htbuilder import div, ul, li, img

dom = (
  div(id='container')[
    ul(_class='greetings')[
      li('hello'),
      li('hi'),
      li('whattup'),
    ]
  ]
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
simply use things like generator expressions for great awesome:

```py
from htbuilder import div, ul, li, img

image_paths = [
  'http://myimages.com/foo1.jpg',
  'http://myimages.com/foo2.jpg',
  'http://myimages.com/foo3.jpg',
]

dom = (
  div(id='container')[
    ul(_class='image-list')[
      li(img(src=image_path, _class='large-image'))
      for image_path in image_paths
    ]
  ]
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
    b("bold text") if use_bold else "normal text"
  )
)

print(dom)
# Prints: <div><b>bold text</b></div>
```

## Modify elements imperatively

Elements accumulate the arguments you send to them, so you can intersperse DOM and code very
naturally:

```py
parent = div()

for url in img_urls:
  child = img(src="https://foo.com/myimage.png")
  child.width = 200
  child.height = 100

  if alt_text:
    child.alt = alt_text
  else:
    child.alt = "The developer forgot to enter a description. Go scold them!"

  parent(child)
```

## Styling

We provide helpers to write styles without having to pass huge style strings as
arguments. Instead, just use handy builders like `styles()`, `classes()`,
`fonts()`, along with helpers you can import from the `units` and `funcs`
modules.

```py
# styles, classes, and fonts are special imports to help build attribute strings.
from htbuilder import div, styles, classes, fonts

# You can import anything from .units and .funcs to make it easier to specify
# units like "%" and "px", as well as functions like "rgba()" and "rgba()".
from htbuilder.units import percent, px
from htbuilder.funcs import rgba, rgb

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

## Underscores are magic

### Use underscores instead of dashes

Like most popular languages, Python doesn't support dashes in identifiers. So if you want to build
an element that includes dashes in the tag name or attributes, like `<my-element foo-bar="baz">`, you can
do so by using underscores instead:

```py
from htbuilder import my_element

dom = my_element(foo_bar="baz")

print(dom)
# Prints:
# <my-element foo-bar="baz"></my-element>
```

### Prefix with underscore to avoid reserved words

The word `class` is reserved in Python, so if you want to set an element's `class` attribute you
should prepend it with an underscore like this:

```py
dom = div(_class="myclass")

print(dom)
# Prints:
# <div class="myclass"></div>
```

This works because underscores preceding or following any identifier are automatically stripped away
for you.
