from conans import ConanFile, tools


class GreeterTestConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"

    def build(self):
        pass

    def imports(self):
        self.copy("*", dst="bin", src="bin")

    def test(self):
        if not tools.cross_building(self):
            # TODO: run greeter binary and check output
            raise
