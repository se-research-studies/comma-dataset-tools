# ODVDCommaAi - Messages to use Comma AI's dataset with OpenDaVINCI.
# Copyright (C) 2016  Christian Berger
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

CMAKE_MINIMUM_REQUIRED (VERSION 2.8)

PROJECT (ODVDCommaAI)

###########################################################################
# Set the search path for .cmake files.
SET (CMAKE_MODULE_PATH "${CMAKE_CURRENT_SOURCE_DIR}/cmake/Modules" ${CMAKE_MODULE_PATH})

###########################################################################
# Check properties of the platform we are going to be compiled on.
INCLUDE (CheckPlatform)

###########################################################################
# Setting where to install the binaries.
SET(INSTALL_DIR ${CMAKE_INSTALL_PREFIX})

###########################################################################
# Display configuration.
MESSAGE("")
SET(ODDATASTRUCTUREGENERATOR_EXECUTABLE ${INSTALL_DIR}/bin/odDataStructureGenerator-latest.jar)
MESSAGE(STATUS "Using ${ODDATASTRUCTUREGENERATOR_EXECUTABLE} to generate code from data structure models.")
MESSAGE(STATUS "Installing artifacts to:    ${INSTALL_DIR}")
MESSAGE("")

# This "external project" simply deletes the existing libodvdcommaai.
ExternalProject_Add (libodvdcommaai-cleanup
    DOWNLOAD_COMMAND ""
    UPDATE_COMMAND ${CMAKE_COMMAND} -E remove_directory ${CMAKE_CURRENT_BINARY_DIR}/libodvdcommaai
    PATCH_COMMAND ""
    SOURCE_DIR ""
    CONFIGURE_COMMAND ""
    BUILD_COMMAND ""
    TEST_COMMAND ""
    INSTALL_COMMAND "")

ExternalProject_Add (libodvdcommaai
    DEPENDS libodvdcommaai-cleanup
    DOWNLOAD_COMMAND ""
    UPDATE_COMMAND cd ${CMAKE_CURRENT_BINARY_DIR} && ${Java_JAVA_EXECUTABLE} -jar ${ODDATASTRUCTUREGENERATOR_EXECUTABLE} --withCMake ${CMAKE_CURRENT_SOURCE_DIR}/ODVDCommaAI.odvd
    PATCH_COMMAND ""
    SOURCE_DIR "${CMAKE_CURRENT_BINARY_DIR}/libodvdcommaai"
    CMAKE_ARGS "-DCMAKE_INSTALL_PREFIX=${INSTALL_DIR}"
    CMAKE_ARGS "-DCMAKE_TOOLCHAIN_FILE=${TOOLCHAIN_FILE}"
    CMAKE_ARGS "-DCXXTEST_INCLUDE_DIR=${CXXTEST_INCLUDE_DIR}"
    TEST_BEFORE_INSTALL 1
    TEST_COMMAND ${CMAKE_CTEST_COMMAND} ${CTEST_PARAMETERS}
    INSTALL_COMMAND ${CMAKE_COMMAND} --build ${CMAKE_CURRENT_BINARY_DIR}/libodvdcommaai-prefix/src/libodvdcommaai-build --target install COMMAND ${CMAKE_COMMAND} --build ${CMAKE_CURRENT_BINARY_DIR}/libodvdcommaai-prefix/src/libodvdcommaai-build --target ${MAKE_PACKAGE})

