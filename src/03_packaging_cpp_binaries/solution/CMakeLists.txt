cmake_minimum_required(VERSION 3.1)
project(greeter CXX)

# Include conanbuildinfo.cmake to load all variables and macros
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
# Run conan_basic_setup() macro to set all variables and macros. More info:
# https://docs.conan.io/en/1.43/reference/generators/cmake.html#conan-basic-setup
# TARGETS will define CMake targets of required packages
conan_basic_setup(TARGETS)

# Add executable named "greeter" - This is also the target name
add_executable(greeter src/greeter.cpp)

# Link "CONAN_PKG::hello_lib" library target to "greeter" target
target_link_libraries(greeter PUBLIC CONAN_PKG::hello_lib)
# Or using conan macro
# conan_target_link_libraries(greeter)


# ## 2nd approach
# # We can also simply skip creating targets and use CMake variables
# include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
# # Run conan_basic_setup() macro without TARGETS:
# conan_basic_setup()

# # Add executable named "greeter" - This is also the target name
# add_executable(greeter src/greeter.cpp)

# # Link "CONAN_PKG::hello_lib" library target to "greeter" target
# target_link_libraries(greeter ${CONAN_LIBS})
# # Or using exact CMake variable
# # target_link_libraries(greeter ${CONAN_LIBS_HELLO_LIB})
