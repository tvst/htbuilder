# htbuild — Tiny HTML string builder for Python

Build HTML strings using a purely functional syntax:

## Examples

If using Python 3.7+:

```
from htbuild import div, ul, li, img  # This syntax requires Python 3.7+

image_paths = [
  "http://...",
  "http://...",
  "http://...",
]

out = div(id="container")(
  ul(_class="image-list")(
    [
      li(img(src=image_path, _class="large-image"))
      for image_path in image_paths
    ]
  )
)

print(out)
```

If using Python &lt; 3.7, the import should look like this instead:

```
from htbuild import H

div = H.div
ul = H.ul
li = H.li
img = H.img

# ...then the rest is the same as in the previous example.
```
