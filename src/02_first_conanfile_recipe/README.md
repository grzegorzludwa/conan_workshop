# 02_first_conanfile_recipe

In this chapter we will create our first conan package.

All steps are done in `dev` container.
If you exited it, simply call `docker exec -it dev bash`

## Introduce `conan new` command

1. First check syntax and possible options for `conan new` command:
`conan new --help`.
2. Create few packages with different commands. Be careful, files are created
in current working directory. Check how they are different than the others.

## Create first conan package

### Prepare sources for lib package

1. Remove all not needed packages from previous step.
2. Create folder and move there `mkdir hello_lib; cd hello_lib`.
3. Create conan package with sources and tests `conan new hello_lib -s -t`.
4. With `conan inspect .` you can check what attributes are already set and/or
available for package.
5. With `conan info .` command it is possible to check some different info,
for example package ID and it's requirements.

Now it is time for presenter to say something more about basic conan attributes,
methods and CMake setup.

### Try to build lib package

1. Install all dependencies and generate `conanbuildinstall.cmake`:
`conan install . -if build`.
2. Open `build/conanbuildinstall.cmake` file in your editor. In this file you can
find all automatically defined CMake variables and macros.
3. Build package: `conan build . -bf build`. Probably it will fail, because of
missing `cmake`. We have two options:
    1. We can install `cmake` globally in our system/container. This has some
    advantages, but it is not flexible at all. It also become system requirement,
    while we should keep it as a package requirement. That's why we will go with
    the second option.
    2. Add `cmake` as a build requirement for our `hello_lib` package.

### Add cmake as a build requirement

If you strictly followed steps from this workshop you should still have
`conancenter` in your remotes. You can check it with `conan remote list`.

1. Search for `cmake` package in `conancenter`:

    ```script
    conan search cmake -r conancenter
    # or to check in every remote
    conan search cmake -r all
    ```

2. You should get list of available packages. We will use cmake/3.22.0 (latest
during this materials preparation).
3. Open `conanfile.py` and add following method before `build()` method:

    ```script
    def build_requirements(self):
        self.build_requires("cmake/3.22.0")
    ```

    > You can also specify build requirements with class attribute
    "build_requires". More info about build requirements can be found in
    documentation: [Build requirements](https://docs.conan.io/en/1.35/devtools/build_requires.html)
4. Now run `conan info .` to check what changed.
5. Try to build again the package.
6. Check what is inside `build` folder.

### Create package

1. Call `conan create .` and check the command user output. Compare output with
order of method execution from the documentation:
[Conan create method](https://docs.conan.io/en/latest/reference/commands/creator/create.html).

Package will be built, packaged and tested.

### Upload package to artifactory

1. Because we already configured container and have package built it is as simple
as calling:

```script
conan upload <PACKAGE_REFERENCE> -r <REMOTE_NAME> --all
e.g.
conan upload hello_lib/0.1 -r conan-workshop --all
```

If we will skip the `--all` option then only `conanfile.py` and exported files
will be uploaded to artifactory (without actually packaged files and binaries).
To see more info about `conan upload` check
[conan upload](https://docs.conan.io/en/latest/reference/commands/creator/upload.html).
