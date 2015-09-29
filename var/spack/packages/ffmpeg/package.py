from spack import *

class Ffmpeg(Package):
    """OpenCV (Open Source Computer Vision Library) is an open source
    computer vision and machine learning software library. OpenCV was
    built to provide a common infrastructure for computer vision
    applications and to accelerate the use of machine perception in
    the commercial products."""

    homepage = "http://opencv.org"

    version('2.7.2',  git='https://github.com/FFmpeg/FFmpeg.git',commit='15466db69e60f486c44e4c3e680d27c951f125d7')
    version('2.6.4',  git='https://github.com/FFmpeg/FFmpeg.git',commit='b17cec526214dff9d6ac1d97b70167d15a4e14d7')
    version('2.5.8',  git='https://github.com/FFmpeg/FFmpeg.git',commit='1eb646ec9f87ed488f52561867e107eaee89e20c')
    version('2.4.11', git='https://github.com/FFmpeg/FFmpeg.git',commit='98f167202262bd6cce85a1845915023a4b2e2b49')
    version('2.3.6',  git='https://github.com/FFmpeg/FFmpeg.git',commit='db27f50e0658e91758e8a17fdcf390e6bc93c1d2')
    

    #depends_on("gcc@4.4:")
    depends_on("cmake@2.6:")
    depends_on("pkg-config")
    depends_on("gtkplus@2.0:")
    
    def install(self, spec, prefix):
        configure("--prefix=%s" % prefix)

        make()
        make("install")
            
