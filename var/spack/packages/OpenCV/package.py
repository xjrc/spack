from spack import *

class Opencv(Package):
    """OpenCV (Open Source Computer Vision Library) is an open source
    computer vision and machine learning software library. OpenCV was
    built to provide a common infrastructure for computer vision
    applications and to accelerate the use of machine perception in
    the commercial products."""

    homepage = "http://opencv.org"

    version('3.0.0',   git='https://github.com/Itseez/opencv.git',commit='c12243c')
    version('2.4.12.1',git='https://github.com/Itseez/opencv.git',commit='d0210f5')
    version('2.4.11',  git='https://github.com/Itseez/opencv.git',commit='2c9547e')
    version('2.4.10.4',git='https://github.com/Itseez/opencv.git',commit='00d9f69')
    version('2.4.9',   git='https://github.com/Itseez/opencv.git',commit='df8e282')

    #depends_on("gcc@4.4:")
    depends_on("cmake@2.6:")
    depends_on("pkg-config")
    depends_on("gtkplus@2.0:")
    depends_on("ffmpeg")
    depends_on("python@2.6:")
    depends_on("py-numpy")
    
    def install(self, spec, prefix):
        with working_dir('spack-build', create=True):
            cmake('..', *std_cmake_args)
            make()
            make("install")
