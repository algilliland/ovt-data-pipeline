#!/bin/sh
python ./process.py test_npn test_data/data/test_npn/output --input_dir test_data/data/test_npn/input --config_dir test_data/config --ontology https://raw.githubusercontent.com/futres/ovt/master/ontology/ovt-reasoned.owl  --base_dir test_data/projects/test_npn --project_base test_data.projects.test_npn --verbose
