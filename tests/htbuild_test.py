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

import unittest

from htbuilder import div, ul, li, img, h1, script, fragment
from htbuilder.funcs import rgba
from htbuilder.units import px, em, percent
from htbuilder.utils import styles

from .test_util import normalize_whitespace


class TestHtBuilder(unittest.TestCase):
    def test_empty(self):
        dom = div()
        self.assertEqual(
            str(dom),
            normalize_whitespace('<div></div>'),
        )

    def test_basic_usage(self):
        dom = div('hello')
        self.assertEqual(
            str(dom),
            normalize_whitespace('<div>hello</div>'),
        )

    def test_basic_usage_with_arg(self):
        dom = div(id='container')('hello')
        self.assertEqual(
            str(dom),
            normalize_whitespace('<div id="container">hello</div>'),
        )

    def test_self_closing(self):
        dom = img(src="foo")
        self.assertEqual(
            str(dom),
            normalize_whitespace('<img src="foo"/>'),
        )

    def test_tuple_children(self):
        children = tuple(range(5))
        dom = div(id='container')(children)
        self.assertEqual(str(dom), '<div id="container">01234</div>')

        dom = div(children)
        self.assertEqual(str(dom), '<div>01234</div>')

    def test_vararg_children(self):
        children = tuple(range(5))
        dom = div(id='container')(*children)
        self.assertEqual(str(dom), '<div id="container">01234</div>')

        dom = div(*children)
        self.assertEqual(str(dom), '<div>01234</div>')

    def test_list_children(self):
        children = list(range(5))
        dom = div(id='container')(children)
        self.assertEqual(str(dom), '<div id="container">01234</div>')

        dom = div(children)
        self.assertEqual(str(dom), '<div>01234</div>')

    def test_iterable_children(self):
        children = range(5)
        dom = div(id='container')(children)
        self.assertEqual(str(dom), '<div id="container">01234</div>')

        dom = div(children)
        self.assertEqual(str(dom), '<div>01234</div>')

    def test_nested_children(self):
        children = [range(2), tuple(range(3))]
        dom = div(id='container')(children)
        self.assertEqual(str(dom), '<div id="container">01012</div>')

        dom = div(children)
        self.assertEqual(str(dom), '<div>01012</div>')

    def test_complex_tree(self):
        dom = (
            div(id='container')(
                h1('Examples'),
                ul(
                    li("Example 1"),
                    li("Example 2"),
                    li("Example 3"),
                )
            )
        )
        self.assertEqual(
            str(dom),
            normalize_whitespace('''
                <div id="container">
                    <h1>Examples</h1>
                    <ul>
                        <li>Example 1</li>
                        <li>Example 2</li>
                        <li>Example 3</li>
                    </ul>
                </div>
            '''),
        )

    def test_multiple_html_args(self):
        dom = (
            div(
                id='container',
                _class='foo bar',
                style='color: red; border-radius: 10px;',
            )('hello')
        )
        self.assertEqual(
            str(dom),
            normalize_whitespace('''
              <div
                id="container"
                class="foo bar"
                style="color: red; border-radius: 10px;"
              >hello</div>
            '''),
        )

    def test_functional_component(self):
        component = ul(_class='myul')(
            li('Hello'),
        )

        dom = component(style='color: red')(
            li('Goodbye'),
        )

        self.assertEqual(
            str(dom),
            normalize_whitespace('''
              <ul
                class="myul"
                style="color: red"
                  ><li>Hello</li>
                  <li>Goodbye</li>
              </ul>
            '''),
        )

    def test_funcs_in_builder(self):
        dom = div(style=styles(color=rgba(10, 20, 30, 40)))
        self.assertEqual(str(dom), normalize_whitespace('''
            <div style="color:rgba(10,20,30,40)"></div>
        '''))

    def test_units_in_builder(self):
        dom = div(style=styles(foo=px(10, 9, 8)))
        self.assertEqual(str(dom), normalize_whitespace('''
            <div style="foo:10px 9px 8px"></div>
        '''))

    def test_funcs_and_units_in_builder(self):
        dom = div(style=styles(margin=px(0, 0, 10, 0)))
        self.assertEqual(str(dom), normalize_whitespace('''
            <div style="margin:0 0 10px 0"></div>
        '''))

    def test_funcs_and_units_in_builder(self):
        dom = div(style=styles(animate=['color', 'margin']))
        self.assertEqual(str(dom), normalize_whitespace('''
            <div style="animate:color,margin"></div>
        '''))

    def test_script_tag(self):
        dom = script(language="javascript")("console.log('omg!')")
        self.assertEqual(str(dom), normalize_whitespace('''
            <script language="javascript">console.log('omg!')</script>
        '''))

    def test_fragment_tag(self):
        dom = fragment(
            h1('hello'),
            div('world')
        )
        self.assertEqual(str(dom), normalize_whitespace('''
            <h1>hello</h1><div>world</div>
        '''))

    def test_get_set_del_attr(self):
        dom = div(foo="bar", boz="boink")

        self.assertEqual(dom.foo, "bar")
        self.assertEqual(dom.boz, "boink")

        dom.foo = "bar2"

        self.assertEqual(dom.foo, "bar2")
        self.assertEqual(dom.boz, "boink")

        dom.boz = "boink2"

        self.assertEqual(dom.foo, "bar2")
        self.assertEqual(dom.boz, "boink2")

        del dom.boz

        self.assertEqual(dom.foo, "bar2")
        with self.assertRaises(KeyError):
            getattr(dom, "boz")

        del dom.foo

        with self.assertRaises(KeyError):
            getattr(dom, "foo")
        with self.assertRaises(KeyError):
            getattr(dom, "boz")


if __name__ == '__main__':
    unittest.main()
