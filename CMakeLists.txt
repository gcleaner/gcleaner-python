# Name of the project
project (gcleaner)

# The oldest stable cmake version we support
cmake_minimum_required (VERSION 2.6)

# Cmake version to use
cmake_policy (VERSION 2.8)

# Tell to Cmake where its modules can be found in our project directory
list (APPEND CMAKE_MODULE_PATH ${CMAKE_SOURCE_DIR}/cmake)
enable_testing()

# Where we install data directory (if we have any)
set(DATADIR "${CMAKE_INSTALL_PREFIX}/share")

# What to call that directory where we install data too
set(PKGDATADIR "${DATADIR}/gcleaner")
set(GETTEXT_PACKAGE ${CMAKE_PROJECT_NAME})
set(EXEC_NAME "gcleaner")
set(RELEASE_NAME "GCleaner")
set(VERSION "0.02.139")
set(VERSION_INFO "Release")
set(APP_LAUNCHER "gcleaner.desktop")

# We're about to use pkgconfig to make sure dependencies are installed so let's find pkgconfig first
find_package(PkgConfig)

# Hide redundant and logic warnings of C language
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wall -Wno-unused-but-set-variable -Wno-unused-variable -ffast-math -march=native")
set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -Wall -Wno-unused-but-set-variable -Wno-unused-variable -ffast-math -march=native")

# Now let's actually check for the required dependencies
pkg_check_modules(DEPS REQUIRED gtk+-3.0>=3.10.0 gio-2.0 glib-2.0)

add_definitions(${DEPS_CFLAGS})
link_libraries(${DEPS_LIBRARIES} -lm)
link_directories(${DEPS_LIBRARY_DIRS})

# Make sure we have python
set(Python_ADDITIONAL_VERSIONS 3.6)
find_package(PythonLibs 3 REQUIRED)

# Add another subdirectory for compile source (for example: gschemas)
add_subdirectory(data)


# Install the binaries we just made
#install(TARGETS ${EXEC_NAME} RUNTIME DESTINATION bin)

# Install our .desktop file so the Applications menu will see it
install (FILES ${CMAKE_CURRENT_SOURCE_DIR}/data/gtk-widgets-gcleaner.css DESTINATION ${DATADIR}/gcleaner/)
install (FILES ${CMAKE_CURRENT_SOURCE_DIR}/data/gcleaner.desktop DESTINATION ${DATADIR}/applications/)
install (FILES ${CMAKE_CURRENT_SOURCE_DIR}/data/icons/24/gcleaner.svg DESTINATION ${DATADIR}/icons/hicolor/24x24/apps)
install (FILES ${CMAKE_CURRENT_SOURCE_DIR}/data/icons/32/gcleaner.svg DESTINATION ${DATADIR}/icons/hicolor/32x32/apps)
install (FILES ${CMAKE_CURRENT_SOURCE_DIR}/data/icons/48/gcleaner.svg DESTINATION ${DATADIR}/icons/hicolor/48x48/apps)
install (FILES ${CMAKE_CURRENT_SOURCE_DIR}/data/icons/64/gcleaner.svg DESTINATION ${DATADIR}/icons/hicolor/64x64/apps)
install (FILES ${CMAKE_CURRENT_SOURCE_DIR}/data/icons/128/gcleaner.svg DESTINATION ${DATADIR}/icons/hicolor/128x128/apps)
install (FILES ${CMAKE_CURRENT_SOURCE_DIR}/data/media/settings32.svg DESTINATION ${DATADIR}/gcleaner/media/)
install (FILES ${CMAKE_CURRENT_SOURCE_DIR}/data/media/flash16.png DESTINATION ${DATADIR}/gcleaner/media/)
# Put the python files later ....

# Uninstall target
configure_file(
    "${CMAKE_CURRENT_SOURCE_DIR}/cmake_uninstall.cmake.in"
    "${CMAKE_CURRENT_BINARY_DIR}/cmake_uninstall.cmake"
    IMMEDIATE @ONLY)

add_custom_target(uninstall
    COMMAND ${CMAKE_COMMAND} -P ${CMAKE_CURRENT_BINARY_DIR}/cmake_uninstall.cmake)
