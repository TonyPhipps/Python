# 'dataset' holds the input data for this script

# Uses regex to find and replace contents in columns in an imported table
# https://kanoki.org/2019/11/12/how-to-use-regex-in-pandas/
# https://stackoverflow.com/questions/56545962/string-extract-when-partial-string-matches-pandas
import re
import pandas as pd
import numpy as np
dataset['Columname']=dataset['Columname'].str.extract(r'^pattern$', flags=re.M)
