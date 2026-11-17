cmake_minimum_required(VERSION 3.20)
project(wb_filter LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)
if(NOT CMAKE_BUILD_TYPE AND NOT CMAKE_CONFIGURATION_TYPES)
  set(CMAKE_BUILD_TYPE Release)
endif()

add_executable(wb_filter src/main.cpp)
string(TOUPPER "${CMAKE_BUILD_TYPE}" _bt)
target_compile_definitions(wb_filter PRIVATE
  WB_CXX_ID="${CMAKE_CXX_COMPILER_ID}"
  WB_CXX_VERSION="${CMAKE_CXX_COMPILER_VERSION}"
  WB_BUILD_TYPE="${CMAKE_BUILD_TYPE}"
  WB_CXX_FLAGS="${CMAKE_CXX_FLAGS} ${CMAKE_CXX_FLAGS_${_bt}}")

enable_testing()
add_executable(test_filters tests/test_filters.cpp)
target_include_directories(test_filters PRIVATE src)
foreach(case constant_unchanged median_sort_even ema_first_sample startup_partial_window
             threshold_equal_third missing_resets isolated_spike_no_trigger sustained_rise_triggers)
  add_test(NAME ${case} COMMAND test_filters ${case})
endforeach()
