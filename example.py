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

from htbuild import div, ul, li, img, styles, classes, fonts
from htbuild.units import px
from htbuild.funcs import rgba

image_paths = [
  "http://myimages.com/foo1.jpg",
  "http://myimages.com/foo2.jpg",
  "http://myimages.com/foo3.jpg",
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

bottom_margin = 10

s = styles(
    color="black",
    font_family=fonts("Comic Sans", "sans"),
    margin=px(0, 0, bottom_margin, 0),
    box_shadow=[
        (0, 0, px(10), rgba(0, 0, 0, 0.1)),
        (0, 0, "2px", rgba(0, 0, 0, 0.5)),
    ],
)

print(s)
