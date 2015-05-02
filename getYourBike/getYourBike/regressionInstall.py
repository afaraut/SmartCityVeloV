import regressionPersistance
import os.path

db_path = '../../data/velos'


if not os.path.exists('../../data/regression'):
		os.makedirs('../../data/regression')
regressionPersistance.createAllDirectories(db_path)