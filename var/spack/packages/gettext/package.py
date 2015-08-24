from spack import *

class Gettext(Package):
    """GNU `gettext' is an important step for the GNU Translation
    Project, as it is an asset on which we may build many other
    steps. This package offers to programmers, translators, and even
    users, a well integrated set of tools and documentation."""

    homepage = "http://www.gnu.org/software/gettext/"
    url      = "ftp://ftp.gnu.org/pub/gnu/gettext/gettext-0.19.5.tar.gz"

    version('0.19.5.1', '2b2ab90f6405a414bbe30cf6655f3e28')
    version('0.19.5'  , '0f3c108d64e8dcd9e6fbdff4ca722feb')
    version('0.19.4'  , 'd3511af1e604a3478900d2c2b4a4a48e')
    version('0.19.3'  , 'c365029ffc866fc4e485d9e5ca60b260')
    version('0.19.2'  , '6898a2fc5d711b17278a59cfbfc10bc5')

    def install(self, spec, prefix):
        configure('--prefix=%s' % prefix)

        make()
        make("install")
