from conans import ConanFile
import os, shutil
from conans.tools import download, unzip, check_sha256
from conans import CMake

class ArbitraryName(ConanFile):
    name = "sfml"
    version = "2015.8.12"
    branch = "stable"
    settings = "os", "compiler", "arch", "build_type"
    options = {"shared": [True, False]}
    default_options = "shared=True"
    generators = "cmake"
    license = "zlib/png"
    url="http://github.com/TyRoXx/conan-sfml"
    exports = ["CMakeLists.txt"]
    ZIP_FOLDER_NAME = "SFML-6b9781475d70272538a5ce48ad96f583f3a373c3"
    so_version = '2.3'

    def source(self):
        zip_name = "6b9781475d70272538a5ce48ad96f583f3a373c3.zip"
        download("https://github.com/SFML/SFML/archive/%s" % zip_name, zip_name)
        check_sha256(zip_name, "78a646ed839e6ef36b21d73ac509403729a0a22f4d405f30bd3e3cdf0704d418")
        unzip(zip_name)
        os.unlink(zip_name)

    def build(self):
        cmake = CMake(self.settings)
        self.run("mkdir _build")
        self.run('cd _build && cmake ../%s -DBUILD_SHARED_LIBS=%s -DCMAKE_INSTALL_PREFIX=../install %s' %
            (self.ZIP_FOLDER_NAME, "ON" if self.options.shared else "OFF", cmake.command_line)
        )
        if self.settings.os == "Windows":
            self.run("cd _build && cmake --build . %s --target install --config %s" % (cmake.build_config, self.settings.build_type))
        else:
            self.run("cd _build && cmake --build . %s -- -j2 install" % cmake.build_config)

    def package(self):
        self.copy("*.*", "include", "install/include", keep_path=True)
        self.copy(pattern="*.a", dst="lib", src="install/lib", keep_path=False)
        self.copy(pattern="*.so." + self.so_version, dst="lib", src="install/lib", keep_path=False)
        self.copy(pattern="*.lib", dst="lib", src="install/lib", keep_path=False)
        self.copy(pattern="*.dll", dst="bin", src="install/lib", keep_path=False)

    def package_info(self):
        if (not self.settings.os == "Windows") and self.options.shared:
            self.cpp_info.libs = map(
                lambda name: ':lib' + name + ('-d' if self.settings.build_type == "Debug" else '') + '.so.' + self.so_version,
                ['sfml-audio', 'sfml-graphics', 'sfml-network', 'sfml-window', 'sfml-system']
            )
        else:
            self.cpp_info.libs = map(
                lambda name: name + ('-d' if self.settings.build_type == "Debug" else ''),
                map(
                    lambda name: name + ('' if self.options.shared else '-s'),
                    ['sfml-audio', 'sfml-graphics', 'sfml-network', 'sfml-window', 'sfml-system']
                )
            )
        if not self.settings.os == "Windows":
            self.cpp_info.libs.append("pthread")
            self.cpp_info.libs.append("dl")
