set(EspressoScriptInterface_SRC
    "${CMAKE_CURRENT_SOURCE_DIR}/accumulators/initialize.cpp"
    "${CMAKE_CURRENT_SOURCE_DIR}/initialize.cpp"
    "${CMAKE_CURRENT_SOURCE_DIR}/collision_detection/initialize.cpp"
    "${CMAKE_CURRENT_SOURCE_DIR}/constraints/initialize.cpp"
    "${CMAKE_CURRENT_SOURCE_DIR}/cluster_analysis/initialize.cpp"
    "${CMAKE_CURRENT_SOURCE_DIR}/lbboundaries/initialize.cpp"
    "${CMAKE_CURRENT_SOURCE_DIR}/virtual_sites/initialize.cpp"
    "${CMAKE_CURRENT_SOURCE_DIR}/observables/initialize.cpp"
    "${CMAKE_CURRENT_SOURCE_DIR}/pair_criteria/initialize.cpp"
    "${CMAKE_CURRENT_SOURCE_DIR}/mpiio/initialize.cpp"
    "${CMAKE_CURRENT_SOURCE_DIR}/ScriptInterfaceBase.cpp"
    "${CMAKE_CURRENT_SOURCE_DIR}/shapes/initialize.cpp"
    "${CMAKE_CURRENT_SOURCE_DIR}/Variant.cpp"
    "${CMAKE_CURRENT_SOURCE_DIR}/ParallelScriptInterface.cpp"
    "${CMAKE_CURRENT_SOURCE_DIR}/ParallelScriptInterfaceSlave.cpp"
    "${CMAKE_CURRENT_SOURCE_DIR}/ScriptInterfaceBase.cpp"
)

if(H5MD)
    list(APPEND EspressoScriptInterface_SRC
        "${CMAKE_CURRENT_SOURCE_DIR}/h5md/initialize.cpp"
        "${CMAKE_CURRENT_SOURCE_DIR}/h5md/h5md.cpp"
        )
    endif(H5MD)

if( WITH_COVERAGE )
  set(CMAKE_CXX_FLAGS_RELEASE "${CMAKE_CXX_FLAGS_RELEASE} -g -Og")
  if( CMAKE_CXX_COMPILER_ID STREQUAL "Clang")
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -fprofile-instr-generate -fcoverage-mapping")
  else()
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} --coverage -fprofile-arcs -ftest-coverage")
    link_libraries(gcov)
  endif()
endif()

add_library(EspressoScriptInterface SHARED ${EspressoScriptInterface_SRC})
install(TARGETS EspressoScriptInterface LIBRARY DESTINATION ${LIBDIR})
set_target_properties(EspressoScriptInterface PROPERTIES SOVERSION ${SOVERSION})
add_dependencies(EspressoScriptInterface EspressoConfig EspressoConfig)
target_link_libraries(EspressoScriptInterface EspressoCore)

include_directories(${CMAKE_CURRENT_SOURCE_DIR})

include_directories(${CMAKE_SOURCE_DIR}/src)
include_directories(${CMAKE_SOURCE_DIR}/src/core)
include_directories(${CMAKE_BINARY_DIR}/src/core)
if (HDF5_FOUND)
    include_directories(${CMAKE_SOURCE_DIR}/libs/h5xx SYSTEM)
    include_directories(${CMAKE_SOURCE_DIR}/src/core/io/writer/h5md)
    include_directories(${CMAKE_BINARY_DIR}/src/core/io/writer/h5md)
endif(HDF5_FOUND)
