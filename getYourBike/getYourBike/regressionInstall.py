import regressionPersistance
import os.path

from paths import db_path
from paths import regression_path

if not os.path.exists('reression_path'):
		os.makedirs('reression_path')
regressionPersistance.createAllDirectories(db_path)