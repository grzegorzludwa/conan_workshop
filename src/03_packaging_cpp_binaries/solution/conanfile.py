from conans import ConanFile, CMake

from pathlib import Path


class GreeterConan(ConanFile):
    name = "greeter"
    version = "0.1"
    license = "MIT"
    author = "Grzegorz Ludwa <gld@spyro-soft.com>"
    url = "https://github.com/grzegorzludwa/conan_workshop"
    description = "The greeter package"
    topics = ("binary", "workshop", "greeter")
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake"
    exports_sources = "src/*", "CMakeLists.txt"

    def build_requirements(self):
        self.build_requires(self.conan_data["build_requirements"]["cmake"])

    def requirements(self):
        self.requires(self.conan_data["requirements"]["hello_lib"])

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        self.copy("*", dst="bin", src="bin")

    def package_info(self):
        bin_path = Path(self.package_folder, "bin")
        self.output.info(f"Appending PATH environement variable: {bin_path}")
        self.env_info.PATH.append(str(bin_path))
