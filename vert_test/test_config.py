import pytest
import os
from process.config import Config

def test_config(tmpdir):
    base_dir = os.path.dirname(__file__)
    config = Config( {
        'output_dir': str(tmpdir),
        'base_dir': os.path.join(base_dir, "."),
        'data_file': os.path.join(base_dir, "data/invalid_input.csv"),
        'config_dir': os.path.join(base_dir, "config")
    }, kw=False)

    # verify that passed in args & kwargs are accessible as attributes
    assert config.kw == False
    assert config.output_dir == tmpdir

    # should setup some attributes
    # These two failing turning off for now
    assert config.invalid_data_file == tmpdir.join('invalid_data.csv')

    # verify that none existent attribute returns None
    assert config.doesnt_exist is None

    print(len(config.rules))
    # verify rules were parsed 5 rules + 1 default
    assert len(config.rules) == -1 # TODO: confirm rule length
    # should split | delimited rule columns
    assert isinstance(config.rules[0]['columns'], list)
    # should assign default error level
    for rule in config.rules:
        assert rule['level'] in ["error", "warning"]

    # should parse entities and perform label substitution
    assert {
            'alias': 'vertebrateOrganism',
            'concept_uri': 'http://purl.obolibrary.org/obo/NCBITaxon_7742',
            'unique_key': 'occurence_id',
            'identifier_root': 'urn:vertOrganism',
            'columns': [('genus', 'http://rs.tdwg.org/dwc/terms/genus')]
        } in config.entities

    assert {
            'alias': 'organismalTraitObsProc',
            'concept_uri': 'http://purl.obolibrary.org/obo/OVT_0000002',
            'unique_key': 'occurence_id',
            'identifier_root': 'urn:traitObsProc',
            'columns': [('record_id', 'http://rs.tdwg.org/dwc/terms/EventID'), ('latitude', 'http://rs.tdwg.org/dwc/terms/decimalLatitude'),
                        ('longitude', 'http://rs.tdwg.org/dwc/terms/decimalLongitude'), ('year', 'http://rs.tdwg.org/dwc/terms/year'),
                        ('event_date', 'http://rs.tdwg.org/dwc/terms/even')]
        } in config.entities

    assert len(config.entities) == 2

    # should parse relations and perform label substitution
    assert {
            'subject_entity_alias': 'vertebrateOrganism',
            'predicate': 'http://purl.obolibrary.org/obo/OBI_0000295',
            'object_entity_alias': 'organismalTraitObsgProc'
        } in config.relations
