# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Geant4(CMakePackage):
    """Geant4 is a toolkit for the simulation of the passage of particles
    through matter. Its areas of application include high energy, nuclear
    and accelerator physics, as well as studies in medical and space
    science."""

    homepage = "http://geant4.cern.ch/"
    url = "https://gitlab.cern.ch/geant4/geant4/-/archive/v10.6.0/geant4-v10.6.0.tar.gz"

    maintainers = ['drbenmorgan']

    version('10.6.1', sha256='4fd64149ae26952672a81ce5579d3806fda4bd251d486897093ac57633a42b7e')
    version('10.6.0', sha256='eebe6a170546064ff81ab3b00f513ccd1d4122a026514982368d503ac55a4ee4')
    version('10.5.1', sha256='2397eb859dc4de095ff66059d8bda9f060fdc42e10469dd7890946293eeb0e39')
    version('10.4.3', sha256='67f3bb6405a2c77e573936c2b933f5a4a33915aa379626a2eb3012009b91e1da')
    version('10.4.0', sha256='e919b9b0a88476e00c0b18ab65d40e6a714b55ee4778f66bac32a5396c22aa74')
    version('10.3.3', sha256='bcd36a453da44de9368d1d61b0144031a58e4b43a6d2d875e19085f2700a89d8')

    _cxxstd_values = ('11', '14', '17')
    variant('cxxstd',
            default=_cxxstd_values[0],
            values=_cxxstd_values,
            multi=False,
            description='Use the specified C++ standard when building.')

    variant('threads', default=True, description='Build with multithreading')
    variant('vecgeom', default=False, description='Enable vecgeom support')
    variant('opengl', default=False, description='Optional OpenGL support')
    variant('x11', default=False, description='Optional X11 support')
    variant('motif', default=False, description='Optional motif support')
    variant('qt', default=False, description='Enable Qt support')

    depends_on('cmake@3.5:', type='build')
    depends_on('cmake@3.8:', type='build', when='@10.6.0:')

    depends_on('geant4-data@10.6.1', when='@10.6.1')
    depends_on('geant4-data@10.6.0', when='@10.6.0')
    depends_on('geant4-data@10.5.1', when='@10.5.1')
    depends_on('geant4-data@10.4.3', when='@10.4.3')
    depends_on('geant4-data@10.4.0', when='@10.4.0')
    depends_on('geant4-data@10.3.3', when='@10.3.3')

    depends_on("expat")
    depends_on("zlib")

    for std in _cxxstd_values:
        # CLHEP version requirements to be reviewed
        depends_on('clhep@2.3.3.0: cxxstd=' + std,
                   when='@10.3.3: cxxstd=' + std)

        # Spack only supports Xerces-c 3 and above, so no version req
        depends_on('xerces-c cxxstd=' + std, when='cxxstd=' + std)

        # Vecgeom specific versions for each Geant4 version
        depends_on('vecgeom@1.1.5 cxxstd=' + std,
                   when='@10.6.0:10.6.99 +vecgeom cxxstd=' + std)
        depends_on('vecgeom@1.1.0 cxxstd=' + std,
                   when='@10.5.0:10.5.99 +vecgeom cxxstd=' + std)
        depends_on('vecgeom@0.5.2 cxxstd=' + std,
                   when='@10.4.0:10.4.99 +vecgeom cxxstd=' + std)
        depends_on('vecgeom@0.3rc cxxstd=' + std,
                   when='@10.3.0:10.3.99 +vecgeom cxxstd=' + std)

    # Visualization driver ependencies
    depends_on("gl", when='+opengl')
    depends_on("glx", when='+opengl+x11')
    depends_on("libx11", when='+x11')
    depends_on("libxmu", when='+x11')
    depends_on("motif", when='+motif')
    depends_on("qt@5:", when="+qt")

    # As released, 10.03.03 has issues with respect to using external
    # CLHEP.
    patch('CLHEP-10.03.03.patch', level=1, when='@10.3.3')
    # These patches can be applied independent of the cxxstd value?
    patch('cxx17.patch', when='@:10.3.99 cxxstd=17')
    patch('cxx17_geant4_10_0.patch', level=1, when='@10.4.0 cxxstd=17')
    patch('geant4-10.4.3-cxx17-removed-features.patch',
          level=1, when='@10.4.3 cxxstd=17')

    def cmake_args(self):
        spec = self.spec

        # Core options
        options = [
            '-DGEANT4_BUILD_CXXSTD=c++{0}'.format(
                self.spec.variants['cxxstd'].value),
            '-DGEANT4_USE_SYSTEM_CLHEP=ON',
            '-DGEANT4_USE_SYSTEM_EXPAT=ON',
            '-DGEANT4_USE_SYSTEM_ZLIB=ON',
            '-DGEANT4_USE_G3TOG4=ON',
            '-DGEANT4_USE_GDML=ON',
            '-DXERCESC_ROOT_DIR={0}'.format(spec['xerces-c'].prefix)
        ]

        # Multithreading
        options.append(self.define_from_variant('GEANT4_BUILD_MULTITHREADED',
                                                'threads'))
        if '+threads' in spec:
            # This should be a variant
            options.append('-DGEANT4_BUILD_TLS_MODEL=global-dynamic')

        # install the data with geant4
        datadir = spec['geant4-data'].prefix.share
        dataver = '{0}-{1}'.format(spec['geant4-data'].name,
                                   spec['geant4-data'].version.dotted)
        datapath = join_path(datadir, dataver)
        options.append('-DGEANT4_INSTALL_DATADIR={0}'.format(datapath))

        # Vecgeom
        if '+vecgeom' in spec:
            options.append('-DGEANT4_USE_USOLIDS=ON')
            options.append('-DUSolids_DIR=%s' % spec[
                'vecgeom'].prefix.lib.CMake.USolids)

        # Visualization options
        if 'platform=darwin' not in spec:
            if "+x11" in spec and "+opengl" in spec:
                options.append('-DGEANT4_USE_OPENGL_X11=ON')
            if "+motif" in spec and "+opengl" in spec:
                options.append('-DGEANT4_USE_XM=ON')
            if "+x11" in spec:
                options.append('-DGEANT4_USE_RAYTRACER_X11=ON')

        if '+qt' in spec:
            options.append('-DGEANT4_USE_QT=ON')
            options.append(
                '-DQT_QMAKE_EXECUTABLE=%s' %
                spec['qt'].prefix.bin.qmake)

        return options
