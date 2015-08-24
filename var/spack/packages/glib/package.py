from spack import *

class Glib(Package):
    """The GLib package contains a low-level libraries useful for
       providing data structure handling for C, portability wrappers
       and interfaces for such runtime functionality as an event loop,
       threads, dynamic loading and an object system."""
    homepage = "https://developer.gnome.org/glib/"


    version('2.44.1', '83efba4722a9674b97437d1d99af79db',url='http://ftp.gnome.org/pub/gnome/sources/glib/2.44/glib-2.44.1.tar.xz')
    version('2.43.1', '758eacdfb5d8e48c07456fcfe91b4486',url='http://ftp.gnome.org/pub/gnome/sources/glib/2.43/glib-2.43.1.tar.xz')
    version('2.42.1', '89c4119e50e767d3532158605ee9121a',url="http://ftp.gnome.org/pub/gnome/sources/glib/2.42/glib-2.42.1.tar.xz")

    depends_on("libffi")

    # This appears to be required for some compilers but not others.
    # Since it is unclear how to test for this directly at this time
    # it appears safer to just require the library.
    depends_on("gettext")
    

    def install(self, spec, prefix):
        configure("--prefix=%s" % prefix)
        make()
        make("install")
