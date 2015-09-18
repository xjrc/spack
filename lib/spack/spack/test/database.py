##############################################################################
# Copyright (c) 2013, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Written by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://scalability-llnl.github.io/spack
# Please also see the LICENSE file for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License (as published by
# the Free Software Foundation) version 2.1 dated February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
"""
These tests check the database is functioning properly,
both in memory and in its file
"""
import unittest

from llnl.util.lock import *
from llnl.util.filesystem import join_path

import spack
from spack.database import Database


class DatabaseTest(unittest.TestCase):
    def setUp(self):
        self.original_db = spack.installed_db
        os.rename(self.original_db._index_path,self.original_db._index_path + ".backup")
        spack.installed_db = Database(self.original_db.root)
        if os.path.exists(spack.installed_db._index_path):
            os.remove(spack.installed_db._index_path)

    def tearDown(self):
        spack.installed_db = self.original_db
        os.rename(self.original_db._index_path + ".backup",self.original_db._index_path)

    def _test_read_from_install_tree(self):
        specs = spack.install_layout.all_specs()
        spack.installed_db.read()
        spack.installed_db.write()
        for entry in spack.installed_db._data.values():
            self.assertTrue(entry.spec in specs)
        self.assertEqual(len(specs),len(spack.installed_db._data))

    def _test_remove_and_add(self):
        specs = spack.install_layout.all_specs()
        removed_spec = specs[len(specs)-1]
        spack.installed_db.remove(removed_spec)
        for entry in spack.installed_db._data.values():
            self.assertTrue(entry.spec in specs[:len(specs)-1])
        self.assertEqual(len(specs)-1,len(spack.installed_db._data))
        self.assertTrue(removed_spec.dag_hash not in spack.installed_db._data)

        spack.installed_db.add(removed_spec,"")
        for entry in spack.installed_db._data.values():
            self.assertTrue(entry.spec in specs)
        self.assertEqual(len(specs),len(spack.installed_db._data))
        self.assertTrue(removed_spec.dag_hash in spack.installed_db._data)

    def _test_read_from_file(self):
        spack.installed_db.read()
        size = len(spack.installed_db._data)

        specs = spack.install_layout.all_specs()
        del spack.installed_db._data[specs[0].dag_hash]

        os.utime(spack.installed_db._file_path,None)
        spack.installed_db.read()

        self.assertEqual(size,len(spack.installed_db._data))
        self.assertEqual(size,len(specs))
        for entry in spack.installed_db._data.values():
            self.assertTrue(entry.spec in specs)
        self.assertTrue(specs[0].dag_hash in spack.installed_db._data)


    def _test_write_to_file(self):
        spack.installed_db.read()
        size = len(spack.installed_db._data)
        real_data = spack.installed_db._data

        specs = spack.install_layout.all_specs()
        del spack.installed_db._data[specs[0].dag_hash]

        spack.installed_db.write()
        spack.installed_db._data = real_data
        os.utime(spack.installed_db._file_path,None)
        spack.installed_db.read()
        self.assertEqual(size-1,len(spack.installed_db._data))


        self.assertEqual(size,len(specs))
        for entry in spack.installed_db._data:
            self.assertTrue(entry.spec in specs[1:])
        self.assertTrue(specs[0].dag_hash not in spack.installed_db._data)

    def test_ordered_test(self):
        self._test_read_from_install_tree()
        self._test_remove_and_add()
        self._test_read_from_file()
        self._test_write_to_file()
