# 04_conan_config_and_profiles

In this chapter we will take a look at the conan config and profiles.

## Conan home folder

By default when you run conan for the first time it creates a configuration
folder in user home directory: `~/.conan`. It's worth to mention, that after
fresh installation you will not have many files inside the config folder. They
are generated automatically or install the whole conan config from repository
or zip file.

``` console
root@cc23eb3a317f:/# pip install conan
# ...
root@cc23eb3a317f:/# ls ~/.conan
ls: cannot access '/root/.conan': No such file or directory
root@cc23eb3a317f:/# conan
# ...
root@cc23eb3a317f:/# ls ~/.conan
conan.conf  version.txt
root@cc23eb3a317f:/# conan remote list
WARN: Remotes registry file missing, creating default one in /root/.conan/remotes.json
conancenter: https://center.conan.io [Verify SSL: True]
root@cc23eb3a317f:/# ls ~/.conan
artifacts.properties  cacert.pem  conan.conf  remotes.json  version.txt
root@cc23eb3a317f:/# conan install cmake/3.22.0@
Auto detecting your dev setup to initialize the default profile (/root/.conan/profiles/default)
Found gcc 10
gcc>=5, using the major as version

************************* WARNING: GCC OLD ABI COMPATIBILITY ***********************
 
Conan detected a GCC version > 5 but has adjusted the 'compiler.libcxx' setting to
'libstdc++' for backwards compatibility.
Your compiler is likely using the new CXX11 ABI by default (libstdc++11).

If you want Conan to use the new ABI for the default profile, run:

    $ conan profile update settings.compiler.libcxx=libstdc++11 default

Or edit '/root/.conan/profiles/default' and set compiler.libcxx=libstdc++11

************************************************************************************



Default settings
    os=Linux
    os_build=Linux
    arch=x86_64
    arch_build=x86_64
    compiler=gcc
    compiler.version=10
    compiler.libcxx=libstdc++
    build_type=Release
*** You can change them in /root/.conan/profiles/default ***
*** Or override with -s compiler='other' -s ...s***


Configuration:
[settings]
arch=x86_64
arch_build=x86_64
build_type=Release
compiler=gcc
compiler.libcxx=libstdc++
compiler.version=10
os=Linux
os_build=Linux
[options]
[build_requires]
[env]

cmake/3.22.0: Not found in local cache, looking in remotes...
cmake/3.22.0: Trying with 'conancenter'...
Downloading conanmanifest.txt completed [0.10k]
# ...
root@cc23eb3a317f:/# ls ~/.conan
artifacts.properties  cacert.pem  conan.conf  data  hooks  profiles  remotes.json  settings.yml  version.txt
```

You can check more details about configuration files in documentation:
[Configuration files](https://docs.conan.io/en/latest/reference/config_files.html).

1. Summary of folders and files explained by presenter.

## Create your own profile

1. Change directory to `~/.conan/profiles`.
2. Copy `default` file under name: `default_debug`.
3. Edit `default_debug` file:

    ``` script
    build_type=Debug
    ```

## Build greeter package with new profile

1. Change directory to `greeter` package from previous chapter.
2. Install packages with the newly created profile.

    ``` console
    conan install . -if build -pr default_debug
    ```

    You should get an error:
    ``` console
    Installing (downloading, building) binaries...
    ERROR: Missing binary: hello_lib/0.1:ef0c3edca1cf558ed18a8d520327dc2ba60a60a2

    hello_lib/0.1: WARN: Can't find a 'hello_lib/0.1' package for the specified settings, options and dependencies:
    - Settings: arch=x86_64, build_type=Debug, compiler=gcc, compiler.libcxx=libstdc++, compiler.version=10, os=Linux
    - Options: fPIC=True, shared=False
    - Dependencies: 
    - Requirements: 
    - Package ID: ef0c3edca1cf558ed18a8d520327dc2ba60a60a2

    ERROR: Missing prebuilt package for 'hello_lib/0.1'
    Use 'conan search hello_lib/0.1 --table=table.html -r=remote' and open the table.html file to see available packages
    Or try to build locally from sources with '--build=hello_lib'

    More Info at 'https://docs.conan.io/en/latest/faq/troubleshooting.html#error-missing-prebuilt-package'
    ```

    But wait?! We already have the hello_lib built, right? Not exactly...

3. Run `conan info hello_lib/0.1@`. The example output should looks like this:

    ``` console
    hello_lib/0.1
        ID: 82ef5eac51c38971dea2fd342dd55ddf2ddfbbc3
        ...
    ```

    Now compare this `ID` with package ID that conan was trying to install.
    **They are different.**

    This happened, because we changed the the settings.build_type in our profile.
    Previously built package used "Release" type, right now we have "Debug".

    **Setting, options and requirements by default** change the package ID.
    So conan recognise them as two different binaries - which is true.
    I wrote "by default" because we can influence on the package ID and what
    changes it in `package_id()` method. We will not do it right now, just
    remember about it and if needed check documentation:
    [Defining Package ABI Compatibility](https://docs.conan.io/en/latest/creating_packages/define_abi_compatibility.html).

4. We will use solution suggested by conan - build missing binaries during
install step.

    ``` console
    conan install . -if build -pr default_debug --build=missing
    ```

5. Upload new hello_lib package to artifactory.

    ``` console
    conan upload hello_lib/0.1@:ef0c3edca1cf558ed18a8d520327dc2ba60a60a2 -r conan-workshop
    ```

6. Check packages available in artifactory.

    ``` console
    conan search hello_lib/0.1@ -r conan-workshop --table table.html
    ```

    Open `table.html` in browser.

7. Build `greeter` package `conan build . -bf build`.
8. Run binary `./build/bin/greeter`. See that the message changed - now there
is "Debug" in message.
9. Additionally you can create package with the new profile and push it to
artifactory.

    ``` console
    conan create . -pr default_debug
    conan upload greeter/0.1 -r conan-workshop --all
    ```

## Default conan profile

If you want to specify your own default conan profile you have 3 possibilities:

1. Modify `~/.conan/profiles/default`. Not recommended.
2. Modify the `default_profile` key in `~/.conan/conan.conf` and put path to
your default profile.
3. Set `CONAN_DEFAULT_PROFILE_PATH` environment variable.
