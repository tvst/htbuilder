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

from htbuild import div, ul, li, img, h1
import re
import unittest


class TestHtBuild(unittest.TestCase):
    def test_basic_usage(self):
        dom = div(id='container')('hello')
        self.assertEqual(
            str(dom),
            normalize_whitespace('<div id="container">hello</div>'),
        )

    def test_iterable_children(self):
        children = ('one', 'two', 'three')
        dom = div(id='container')(children)
        self.assertEqual(
            str(dom),
            normalize_whitespace('<div id="container">onetwothree</div>'),
        )

    def test_vararg_children(self):
        children = ('one', 'two', 'three')
        dom = div(id='container')(*children)
        self.assertEqual(
            str(dom),
            normalize_whitespace('<div id="container">onetwothree</div>'),
        )

    def test_complex_tree(self):
        dom = div(id='container')(
            h1('Examples'),
            ul(
                li("Example 1"),
                li("Example 2"),
                li("Example 3"),
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
        dom = div(id='container', _class='foo bar', style='color: red; border-radius: 10px;')('hello')
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


def normalize_whitespace(s):
    s = s.replace('\n', '')
    s = re.sub(r'([<>"])\s+([<>"])', r'\1\2', s)
    s = re.sub(r'^ \s+', r'', s)
    s = re.sub(r' \s+$', r'', s)
    s = re.sub(r' \s+', r' ', s)
    return s


if __name__ == '__main__':
    unittest.main()
