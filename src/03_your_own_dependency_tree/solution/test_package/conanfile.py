from io import StringIO

from conans import ConanFile, tools
from conans.errors import ConanException


class GreeterTestConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"

    def build(self):
        pass

    def imports(self):
        self.copy("*", dst="bin", src="bin")

    def test(self):
        if not tools.cross_building(self):
            output = StringIO()
            self.run(
                "bin/greeter",
                output=output,
                run_environment=True,
            )

            if "Hello World" in output.getvalue():
                self.output.info("Test OK")
            else:
                raise ConanException(
                    "Couldn't find Hello World in output. "
                    "Test package FAILED."
                )
