from spack import *

class PkgConfig(Package):
    """pkg-config is a helper tool used when compiling applications and libraries."""
    homepage = "http://www.freedesktop.org/wiki/Software/pkg-config/"
    url      = "http://pkgconfig.freedesktop.org/releases/pkg-config-0.28.tar.gz"

    version('0.28'  , 'aa3c86e67551adc3ac865160e34a2a0d')
    version('0.27.1', '5392b4e3372879c5bf856173b418d6a2')
    version('0.27'  , '3a4c9feab14b6719afd8904945d9b4e4')
    version('0.26'  , '47525c26a9ba7ba14bf85e01509a7234')
    version('0.25'  , 'a3270bab3f4b69b7dc6dbdacbcae9745')


    def install(self, spec, prefix):
        configure('--prefix=%s' % prefix)

        make()
        make("install")
