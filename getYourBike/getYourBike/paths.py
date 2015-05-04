#!/usr/local/bin/python
# -*- coding: utf-8	 -*-

from pathlib import Path
import os

data_path = Path(os.path.dirname(os.path.abspath(__file__))).parent.parent / 'data'

#data_path =  Path('../../data').resolve()

db_path = data_path / 'velos'
db_path_string = str(db_path).decode('latin-1')

vacation_data_path = data_path  / 'jours_feries_timestamp.txt'
regression_path = data_path  / 'regression'
common_path = regression_path  / 'common'

