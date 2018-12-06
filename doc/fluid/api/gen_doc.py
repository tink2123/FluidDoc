#   Copyright (c) 2018 PaddlePaddle Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import print_function
import argparse
import sys
import types

import paddle.fluid as fluid


def parse_arg():
    parser = argparse.ArgumentParser()
    parser.add_argument('--submodules', nargs="*")
    parser.add_argument(
        'module', type=str, help='Generate the documentation of which module')
    return parser.parse_args()


class DocGenerator(object):
    def __init__(self, module_name=None, stream=sys.stdout):
        if module_name == "":
            module_name = None
        self.stream = stream
        if module_name is None:
            self.module_name = "fluid"
        else:
            self.module_name = "fluid." + module_name
        if module_name is None:
            self.module = fluid
        else:
            if not hasattr(fluid, module_name):
                raise ValueError("Cannot find fluid.{0}".format(module_name))
            else:
                self.module = getattr(fluid, module_name)
        self.stream.write('''..  THIS FILE IS GENERATED BY `gen_doc.{py|sh}`
    !DO NOT EDIT THIS FILE MANUALLY!

''')

        self._print_header_(self.module_name, dot='=', is_title=True)

    def print_submodule(self, submodule_name):
        submodule = getattr(self.module, submodule_name)
        if submodule is None:
            raise ValueError("Cannot find submodule {0}".format(submodule_name))
        self.print_section(submodule_name)

        for item in sorted(submodule.__all__,key=str.lower):
            self.print_item(item)

    def print_current_module(self):
        for item in sorted(self.module.__all__,key=str.lower):
            self.print_item(item)

    def print_section(self, name):
        self._print_header_(name, dot='=', is_title=False)

    def print_item(self, name):
        item = getattr(self.module, name, None)
        if item is None:
            return
        if isinstance(item, types.TypeType):
            self.print_class(name)
        elif isinstance(item, types.FunctionType):
            self.print_method(name)
        else:
            pass

    def print_class(self, name):
        self._print_ref_(name)
        self._print_header_(name, dot='-', is_title=False)
        self.stream.write('''..  autoclass:: paddle.{0}.{1}
    :members:
    :noindex:

'''.format(self.module_name, name))
        self._print_cn_ref(name)

    def print_method(self, name):
        self._print_ref_(name)
        self._print_header_(name, dot='-', is_title=False)
        self.stream.write('''..  autofunction:: paddle.{0}.{1}
    :noindex:

'''.format(self.module_name, name))
        self._print_cn_ref(name)

    def _print_header_(self, name, dot, is_title):
        dot_line = dot * len(name)
        if is_title:
            self.stream.write(dot_line)
            self.stream.write('\n')
        self.stream.write(name)
        self.stream.write('\n')
        self.stream.write(dot_line)
        self.stream.write('\n')
        self.stream.write('\n')

    def _print_ref_(self, name):
        self.stream.write(".. _api_{0}_{1}:\n\n".format("_".join(
            self.module_name.split(".")), name))
    def _print_cn_ref(self,name):
    	self.stream.write("Read Chinese Version: :ref:`cn_api_{0}_{1}`\n\n".format("_".join(
    		self.module_name.split(".")),name))


def main():
    args = parse_arg()
    gen = DocGenerator(args.module)
    if args.submodules is None:
        gen.print_current_module()
    else:
        for submodule_name in args.submodules:
            gen.print_submodule(submodule_name)


if __name__ == '__main__':
    main()
