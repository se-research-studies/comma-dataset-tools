# OpenDaVINCI - Portable middleware for distributed components.
# Copyright (C) 2008 - 2015  Christian Berger
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

###########################################################################
# Enable the configuration of external projects.
INCLUDE (ExternalProject)

###########################################################################
# Include flags for compiling.
INCLUDE (CompileFlags)

###########################################################################
# Find and configure CxxTest.
INCLUDE (CheckCxxTestEnvironment)

###########################################################################
# Check for a working Java environment.
FIND_PACKAGE(Java)

IF(NOT("${Java_JAVA_EXECUTABLE}" STREQUAL ""))
    SET(HAVE_JAVA "1")
ENDIF()

###########################################################################
# Find OpenDaVINCI.
SET(OPENDAVINCI_DIR "${CMAKE_INSTALL_PREFIX}")
FIND_PACKAGE (OpenDaVINCI REQUIRED)

###########################################################################
# Check for a working threading and potential realtime library environment.
FIND_PACKAGE (Threads REQUIRED)
FIND_PACKAGE (LibRT)

