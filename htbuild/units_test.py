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
from htbuild.utils import styles
from htbuild.units import px, em, percent
from htbuild_test import normalize_whitespace
import unittest


class TestUnits(unittest.TestCase):
    def test_basic_usage(self):
        self.assertEqual(px(10), ('10px',))
        self.assertEqual(px(0), ('0',))
        self.assertEqual(em(5), ('5em',))
        self.assertEqual(percent(99), ('99%',))

    def test_varargs(self):
        self.assertEqual(px(10, 9, 8), ('10px', '9px', '8px'))
        self.assertEqual(px(0, 1), ('0', '1px'))
        self.assertEqual(em(5, 7), ('5em', '7em'))
        self.assertEqual(percent(99, 99.9), ('99%', '99.9%'))

    def test_builder(self):
        dom = div(style=styles(foo=px(10, 9, 8)))
        self.assertEqual(str(dom), normalize_whitespace('''
            <div style="foo:10px,9px,8px"></div>
        '''))

if __name__ == '__main__':
    unittest.main()
