#!/usr/local/bin/python
# -*- coding: utf-8	 -*-

import posixpath

data_path =  posixpath.abspath('../../../data')


db_path = data_path + "/velos"
vacation_data_path = data_path  + '/jours_feries_timestamp.txt'
regression_path = data_path  + '/regression'
common_path = regression_path  + '/common'