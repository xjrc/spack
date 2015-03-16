from spack import *
import os

# OCR only works for Linux right now.
ocr_type = 'x86-pthread-x86'


class Ocr(Package):
    """The Open Community Runtime project is creating an application
       building framework that explores new methods of high-core-count
       programming. The initial focus is on HPC applications. Its goal
       is to create a tool that helps app developers improve the power
       efficiency, programmability, and reliability of their work
       while maintaining app performance."""

    homepage = "https://01.org/open-community-runtime"

    version('2015-02-16', 'aa0a54633b3b8b8faa3bebdad70c0cdc',
            url='https://github.com/01org/ocr/archive/xstack-intel__2015-02-16.tar.gz')

    def setup_dependent_environment(self):
        """Convention for dependents to find OCR is to use this environment variable."""
        os.environ['OCR_INSTALL'] = self.prefix


    def patch(self):
        # substitute Spack compiler for the default gcc compiler, so
        # we can swap it.
        filter_file(r'^CC\s*:= .*$', 'CC := cc', join_path('build', ocr_type, 'Makefile'))


    def install(self, spec, prefix):
        # Build is fairly simple, but requires some env vars.
        os.environ['OCR_TYPE'] = ocr_type
        os.environ['OCR_INSTALL_ROOT'] = prefix
        with working_dir('build'):
            make()
            make('install')

        # Build always wants to install into the OCR_TYPE subdirectory
        # of the install root.  Pull it out of there since Spack has
        # its own prefix.
        with working_dir(prefix):
            for subdir in ('bin', 'config', 'include', 'lib'):
                move(join_path(ocr_type, subdir), subdir)
            rmtree(ocr_type)

