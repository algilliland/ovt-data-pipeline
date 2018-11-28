# -*- coding: utf-8 -*-

"""preprocessor.AbstractPreProcessor implementation for preprocessing vertebrate data"""

# import logging
# import os
import multiprocessing

import uuid
import pandas as pd
from preprocessor import AbstractPreProcessor

# haslength, haslifestage
COLUMNS_MAP = {
        'occurrenceid' : 'occurrence_id',
        'genus' : 'genus',
        'specificepithet' : 'specific_epithet',
        'eventdate' : 'event_date',
        'year' : 'year',
        'decimallatitude' : 'latitude',
        'decimallongitude' : 'longitude',
        'haslength' : 'has_length',
        'lengthtype' : 'length_type',
        'lengthinmm' : 'length_in_mm',
        'lengthunitsinferred' : 'length_units_inferred',
        'hasmass' : 'has_mass',
        'massing' : 'mass_in_g',
        'massunitsinferred' : 'mass_units_inferred'
}

class PreProcessor(AbstractPreProcessor):
    def _process_data(self):
        num_processes = multiprocessing.cpu_count()
        chunk_size = 10000
        data = pd.read_csv(self.input_dir, sep=',', header=0,
                usecols=['haslength', 'hasmass', 'lengthinmm', 'lengthtype',
                    'lengthunitsinferred', 'massing', 'massunitsinferred',
                    'decimallatitude', 'decimallongitude','eventdate', 'genus',
                    'occurrenceid', 'specificepithet', 'year'],
                chunksize=chunk_size * num_processes)

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


