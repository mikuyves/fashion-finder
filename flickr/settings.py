# -*- coding: utf-8 -*-

import sys
import os
from os.path import dirname
# Set the directory for using the modules in the same project such as eshop.
PROJECT_PATH = dirname(os.path.abspath(os.path.dirname(__file__)))
ESHOP_PATH = os.path.join(PROJECT_PATH, 'eshop/')
sys.path.append(PROJECT_PATH)
