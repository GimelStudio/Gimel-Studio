## ----------------------------------------------------------------------------
## Gimel Studio Copyright 2020 Noah Rahm, Correct Syntax. All rights reserved.
##
## Licensed under the Apache License, Version 2.0 (the "License");
## you may not use this file except in compliance with the License.
## You may obtain a copy of the License at
##
##    http://www.apache.org/licenses/LICENSE-2.0
##
## Unless required by applicable law or agreed to in writing, software
## distributed under the License is distributed on an "AS IS" BASIS,
## WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
## See the License for the specific language governing permissions and
## limitations under the License.
##
## FILE: file_support.py
## AUTHOR(S): Noah Rahm
## PURPOSE: Define the supported filetypes 
## ----------------------------------------------------------------------------

# File import/open support
SUPPORTED_FILETYPES_OPEN = [
    ".jpeg", 
    ".jpg", 
    ".png", 
    ".bmp",
    ".webp", 
    ".tga",
    ".tiff"
    ]

# File export/save support
SUPPORTED_FILETYPES_SAVE = [
    ".jpeg", 
    ".jpg", 
    ".png", 
    ".bmp",
    ".gif",
    ".webp",
    ".xbm",
    ".pcx", 
    ".eps",
    ".tiff",
    ".tga"
    ]


def SupportFTOpen(file_ext="", list_all=False):
    """ Returns whether the given file extension is supported for import/open in Gimel Studio. 
    
    :param str file_ext: the file extension in question
    :param boolean list_all: if is `True`, returns a list of all the supported filetypes instead.
    """
    if list_all == True:
        return SUPPORTED_FILETYPES_OPEN
    else:
        if file_ext in SUPPORTED_FILETYPES_OPEN:
            return True
        else:
            return False

  
def SupportFTSave(file_ext="", list_all=False):
    """ Returns whether the given file extension is supported for export/save in Gimel Studio. 
    
    :param str file_ext: the file extension in question
    :param boolean list_all: if is `True`, returns a list of all the supported filetypes instead.
    """
    if list_all == True:
        return SUPPORTED_FILETYPES_SAVE
    else:
        if file_ext in SUPPORTED_FILETYPES_SAVE:
            return True
        else:
            return False
