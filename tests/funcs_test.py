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

from htbuilder.funcs import rgba, hsl


class TestFuncs(unittest.TestCase):
    def test_basic_usage(self):
        out = rgba(0, 0, 0, 0.1)
        self.assertEqual(out, "rgba(0,0,0,0.1)")

        out = hsl(270, "60%", "70%")
        self.assertEqual(out, "hsl(270,60%,70%)")


if __name__ == '__main__':
    unittest.main()
