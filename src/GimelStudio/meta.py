# ----------------------------------------------------------------------------
# Gimel Studio Copyright 2019-2021 by Noah Rahm and contributors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# FILE: meta.py
# AUTHOR(S): Noah Rahm
# PURPOSE: Define program meta info
# ----------------------------------------------------------------------------


# GENERAL CONSTANTS

# Program name
APP_NAME = "Gimel Studio"

# Program author
APP_AUTHOR = "Noah Rahm and contributors"

# Release version: [major].[minor].[build]
APP_VERSION = (0, 5, 1)
APP_VERSION_TAG = "beta"
FULL_APP_VERSION_STRING = "{0}.{1}.{2} {3}".format(APP_VERSION[0],
                                                   APP_VERSION[1],
                                                   APP_VERSION[2],
                                                   APP_VERSION_TAG)

# Title string
APP_TITLE = "{0} {1}".format(APP_NAME, FULL_APP_VERSION_STRING)


# DEVELOPER OPTIONS

# Whether this program is in development mode
# USAGE: Switch to False before building as .exe or similar package to
# enable/disable some end-user features that would otherwise hinder
# development and/or testing of the program.
APP_DEBUG = True

# Whether to enable the experimental renderer threading
ENABLE_THREADING = False
