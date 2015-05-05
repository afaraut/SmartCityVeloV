import os
import regressionPersistance
from pathlib import Path

from paths import regression_path

if not Path.exists(regression_path):
	Path.mkdir(regression_path)
regressionPersistance.createAllDirectories()