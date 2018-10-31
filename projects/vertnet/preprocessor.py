# -*- coding: utf-8 -*-

"""preprocessor.AbstractPreProcessor implementation for preprocessing vertebrate data"""

# import logging
# import os
import multiprocessing

import uuid
import pandas as pd
# TODO: fix import error...
from preprocessor import AbstractPreProcessor

# haslength, haslifestage, hasmass, hassex
COLUMNS_MAP = {
        'decimallatitude' : 'latitude',
        'decimallongitude' : 'longitude',
        'eventdate' : 'event_date',
        'genus' : 'genus',
        'haslength' : 'has_length',
        'haslifestage' : 'has_life_stage',
        'hasmass' : 'has_mass',
        'hassex' : 'has_sex',
        'lengthinmm' : 'length_in_mm',
        'lengthtype' : 'length_type',
        'lengthunitsinferred' : 'length_units_inferred',
        'massing' : 'mass_in_g',
        'massunitsinferred' : 'mass_units_inferred',
        'occurrenceid' : 'occurrence_id',
        'specificepithet' : 'specific_epithet',
        'subgenus' : 'subgenus',
        'year' : 'year'
}

class PreProcessor(AbstractPreProcessor):
    def _process_data(self):
        num_processes = multiprocessing.cpu_count()
        chunk_size = 10 # TODO: increase
        data = pd.read_csv(self.input_dir, sep=',', header=0,
                usecols=['haslength', 'haslifestage', 'hasmass', 'hassex',
                'lengthinmm', 'lengthtype', 'lengthunitsinferred', 'massing',
                'massunitsinferred', 'decimallatitude', 'decimallongitude',
                'eventdate', 'genus', 'occurrenceid', 'specificepithet',
                'subgenus', 'year'], chunksize=chunk_size * num_processes)

        for chunk in data:
            chunks = [chunk.ix[chunk.index[i:i + chunk_size]] for i in range(0, chunk.shape[0], chunk_size)]
            with multiprocessing.Pool(processes=num_processes) as pool:
                pool.map(self._transform_chunk, chunks)

    def _transform_chunk(self, chunk):
        self._transform_data(chunk).to_csv(self.output_file, columns=self.headers, mode='a', header=False, index=False)

    def _transform_data(self, data):
        data['record_id'] = data.apply(lambda x: uuid.uuid4(), axis=1)
#        data.fillna("", inplace=True)  # replace all null values
        return data.rename(columns=COLUMNS_MAP)


# TODO: change input for input_dir and read_csv input file path 
preprocessor = PreProcessor('../../../../VNTraitsForFuTRES_subset.csv', "out_dir")
preprocessor.run()
