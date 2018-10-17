# -*- coding: utf-8 -*-

"""preprocessor.AbstractPreProcessor implementation for preprocessing test vertebrate data"""

" This is an example preprocessor with basic functionality "

# import os
import uuid
import pandas as pd
from preprocessor import AbstractPreProcessor

# traits being mapped to expected format 
COLUMNS_MAP = {
        'haslength' : 'has_length',
        'haslifestage' : 'has_life_stage',
        'hasmass' : 'has_mass',
        'hassex' : 'has_sex',
        'lengthinmm' : 'length_in_mm',
        'lengthtype' : 'length_type',
        'lengthunitsinferred' : 'length_units_inferred',
        'massing' : 'mass_in_g',
        'massunitsinferred' : 'mass_units_inferred'
}

class PreProcessor(AbstractPreProcessor):
    # reads in selected traits
    def _process_data(self):
        data = pd.read_csv(self.input_dir, sep=',', header=0, usecols=['haslength',
            'haslifestage', 'hasmass', 'hassex', 'lengthinmm', 'lengthtype',
            'lengthunitsinferred', 'massing', 'massunitsinferred'])
        self._transform_data(data).to_csv(self.output_file, columns=self.headers, mode='a', header=False, index=False)

    def _transform_data(self, data):
        data['record_id'] = data.apply(lambda x: uuid.uuid4(), axis=1)
        return data.rename(columns=COLUMNS_MAP)

# TODO: change input for input_dir and read_csv input file path 
preprocessor = PreProcessor('../../VNTraitsForFuTRES_subset.csv', "out_dir")
preprocessor.run()
