##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
from spack import *


class PkgConfig(Package):
    """pkg-config is a helper tool used when compiling applications
    and libraries"""

    homepage = "http://www.freedesktop.org/wiki/Software/pkg-config/"
    url      = "http://pkgconfig.freedesktop.org/releases/pkg-config-0.28.tar.gz"

    version('0.29.1', 'f739a28cae4e0ca291f82d1d41ef107d')
    version('0.28',   'aa3c86e67551adc3ac865160e34a2a0d')

    parallel = False

    # The following patch is needed for gcc-6.1
    patch('g_date_strftime.patch', when='%gcc@6.1')

    def install(self, spec, prefix):
        configure("--prefix={0}".format(prefix),
                  "--enable-shared",
                  # There's a bootstrapping problem here;
                  # glib uses pkg-config as well, so break
                  # the cycle by using the internal glib.
                  "--with-internal-glib")

        make()
        make("install")
