# 03_packaging_cpp_binaries

In this chapter we will create new package `greeter` which will use the
`hello_lib` from previous chapter.

We will create a simple executable which depends on `hello_lib` and uses
`hello_lib()` function to print greetings.

## Check template package

To speed up the learning process a template package in `greeter` folder is
already prepared. Places which needs your attention are tagged with **TODO:**.

1. Check `greeter/src/greeter.cpp` file.
2. Check `greeter/CMakeLists.txt` file.
3. Check `greeter/conanfile.py` file.

## Configure requirements

Conan automatically parses `conandata.yml` file, when it is present next to
`conanfile.py`. It can be used to store configuration data. We will put there
our requirements.

1. Create `conandata.yml` file next to `conanfile.py` and put inside:

    ``` yaml
    build_requirements:
        cmake: "cmake/3.22.0"

    requirements:
        hello_lib: "hello_lib/0.1"
    ```

2. We need to build the package using `cmake`. Also `hello_lib` is required.
Add requirements to `conanfile.py`.

    ``` python
    def build_requirements(self):
        self.build_requires(self.conan_data["build_requirements"]["cmake"])

    def requirements(self):
        self.requires(self.conan_data["requirements"]["hello_lib"])
    ```

3. Additionally we have to configure the `generators` attribute, because we are
using cmake. This generator will produce the `conanbuildinfo.cmake` inside build
folder, where all automatically generated CMake variables and macros are defined.
More info about generators: [Generators](https://docs.conan.io/en/latest/reference/generators.html).

    ``` python
    generators = "cmake"
    ```

## Fix package

1. Try to build package:

    ``` script
    conan install . -if build
    conan build . -bf build
    ```

    It will probably fail at this stage. Try to fix it.
2. After successful fix you should be able to run generated binary.

    ``` script
    # ./build/bin/greeter
    hello_lib/0.1: Hello World Release!
    ```

> If you will not be able to fix it check how `exports_sources` attribute looks
in the `solution/conanfile.py`.

## Package files

Now we need to package our binary file.

1. Try to create package. We skip test stage for now, because it is not ready
yet.

    ``` script
    conan create . me/testing --test-folder=None`
    ```

    You should see **warning** in logs:

    ``` script
    ...
    greeter/0.1@me/testing: Generating the package
    greeter/0.1@me/testing: Package folder /root/.conan/data/greeter/0.1/me/testing/package/f4f0f1ee404e1525e1fdf2497a7d748676217898
    greeter/0.1@me/testing: Calling package()
    greeter/0.1@me/testing package(): WARN: No files in this package!  <<<---
    greeter/0.1@me/testing: Package 'f4f0f1ee404e1525e1fdf2497a7d748676217898' created
    ...
    ```

2. Add `self.copy` command to the `package()` method, which will copy generated
binary to the package bin folder.

    ``` script
    self.copy("*", dst="bin", src="bin")
    ```

3. Create package again `conan create . --test-folder=None`.

    You should see that the `greeter` binary was packaged.
    ``` script
    greeter/0.1@me/testing package(): Packaged 1 file: greeter
    ```

4. Check how the package in package folder looks like.

## Append PATH variable

I want to extend the PATH environment variable, so later it can be used with
`virtualenv` generator.

1. Use `self.env_info` attribute in `package_info()` method to achieve goal.
More info: [env_info](https://docs.conan.io/en/latest/reference/conanfile/methods.html#env-info)

    ``` python
    bin_path = Path(self.package_folder, "bin")
    self.env_info.PATH.append(str(bin_path))
    ```

2. Add console info:

    ``` python
    self.env_info....
    self.output.info(f"Appending PATH environement variable: {bin_path}")
    ```

## Fix test_package

The test stage while creating package should check if the package is created
correctly - check if we can include and use the library/binary. So it
**is not** a place to run unit or integration tests. That's why we
usually create a small test package which only include and run basic functions,
or even only run binary, depending on type of package.

Below you can find a snippet how binary can be run and the output checked.

    ```
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
    ```
