## ----------------------------------------------------------------------------
## Gimel Studio © 2020 Correct Syntax, Noah Rahm. All rights reserved.
##
## FILE: meta.py
## AUTHOR(S): Noah Rahm
## PURPOSE: Define program meta info
## ----------------------------------------------------------------------------

# Program name
__NAME__ = "Gimel Studio"

# Program author
__AUTHOR__ = "Correct Syntax, Noah Rahm"

# Release version: [major].[minor]
__VERSION__ = "0.1"

# Release number 
__RELEASE__ = "1" 

# Build number
__BUILD__ = "2"

# Whether this program is in development mode
# USAGE: Switch to False before building as .exe or similar package to
# enable some end-user features that would otherwise hinder development
# and/or testing of the program.
__DEBUG__ = True

# Title string
__TITLE__ = '{0} v{1}.{2}'.format(__NAME__, __VERSION__, __RELEASE__)
