from conans import ConanFile, CMake

required_conan_version = ">=1.33.0"


class GreeterConan(ConanFile):
    name = "greeter"
    version = "0.1"
    license = "MIT"
    author = "Grzegorz Ludwa <gld@spyro-soft.com>"
    url = "https://github.com/grzegorzludwa/conan_workshop"
    description = "The greeter package"
    topics = ("binary", "workshop", "greeter")
    settings = "os", "compiler", "build_type", "arch"

    generators = # TODO: add generator
    exports_sources = "src/*" # TODO: fix source files, that will be exported

    # TODO: Add requirements

    def build(self):
        cmake = CMake(self)
        # we do not specify the source_folder argument,
        # because CMakeLists.txt is next to conanfile
        cmake.configure()
        cmake.build()

    def package(self):
        # TODO: copy binary to package folder
        # self.copy("", dst="", src="")
        pass

    def package_info(self):
        # TODO: append this package bin folder to the environement variable PATH
        # Log info about this fact to the console
        pass
