cmake_minimum_required(VERSION 3.14)  # CMake version check
project(eac)                          # Create project "eac"

# GoogleTest requires at least C++17
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Coverage build type
option(ENABLE_COVERAGE "Enable code coverage" OFF)

if(ENABLE_COVERAGE)
  message(STATUS "Building with code coverage enabled")
  set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} --coverage -fprofile-arcs -ftest-coverage")
  set(CMAKE_EXE_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS} --coverage")
endif()

include(FetchContent)
FetchContent_Declare(
  googletest
  URL https://github.com/google/googletest/archive/03597a01ee50ed33e9dfd640b249b4be3799d395.zip
  DOWNLOAD_EXTRACT_TIMESTAMP TRUE
)
FetchContent_MakeAvailable(googletest)

# Add main.cpp file of the project root directory as a source file
set(SOURCE_FILES main.cpp)

# Add executable target with source files listed in SOURCE_FILES variable
add_executable(x-as-code-cpp ${SOURCE_FILES})

# Library with the code to be tested
add_library(
  samples
  sample1.cpp
  sample2.cpp
)

# Test executable
add_executable(
  eac_test
  eac_test.cpp
  sample1_unittest.cpp
  sample2_unittest.cpp
)

target_link_libraries(
  eac_test
  samples
  GTest::gtest_main
)

# Custom target to run tests directly (without CTest)
add_custom_target(run_tests
  COMMAND ${CMAKE_CURRENT_BINARY_DIR}/eac_test --gtest_output=xml:${CMAKE_CURRENT_BINARY_DIR}/test-results.xml
  DEPENDS eac_test
  WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}
  COMMENT "Running tests with GoogleTest..."
)

# Custom target for coverage report
if(ENABLE_COVERAGE)
  find_program(GCOV_PATH gcov)
  find_program(LCOV_PATH lcov)
  find_program(GENHTML_PATH genhtml)

  if(LCOV_PATH AND GENHTML_PATH)
    add_custom_target(coverage
      # Clear previous coverage data
      COMMAND ${LCOV_PATH} --directory . --zerocounters

      # Run tests
      COMMAND ${CMAKE_CURRENT_BINARY_DIR}/eac_test

      # Capture coverage data, ignoring errors from GoogleTest
      COMMAND ${LCOV_PATH} --directory . --capture --output-file coverage.info --ignore-errors mismatch,inconsistent,negative,format --rc derive_function_end_line=0

      # Remove system headers, external dependencies, and test files from coverage
      COMMAND ${LCOV_PATH} --remove coverage.info '/usr/*' '*/_deps/*' '*/test/*' '*_unittest.cpp' '*_test.cpp' 'eac_test.cpp' --output-file coverage_filtered.info --ignore-errors unused

      # Generate HTML report
      COMMAND ${GENHTML_PATH} coverage_filtered.info --output-directory coverage_html --ignore-errors source

      DEPENDS eac_test
      WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}
      COMMENT "Generating code coverage report..."
    )

    message(STATUS "Code coverage targets available: 'make coverage'")
  else()
    message(WARNING "lcov or genhtml not found. Coverage report generation will not be available.")
  endif()
endif()