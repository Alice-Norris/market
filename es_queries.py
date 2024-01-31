from constants import FiltOp
from constants import TermQuery, BoolQuery
 
#Represents a given Boolean-level element of the ElasticSearch query.
class BooleanLevel:
  def __init__(cls, q_type: BoolQuery):
    cls.term_qs: [TermQuery] = []
    cls.query_type = q_type
    cls.bool_q = []

    # This dictionary is used to create Term-level queries
    cls.terms = { 
      TermQuery.EXISTS: Exists,
      TermQuery.TERMS: Terms,
      TermQuery.TERMS_SET: TermsSet,
      TermQuery.RANGE: Range,
      TermQuery.WILDCARD: Wildcard,
      TermQuery.IDS: IDs
    }

  # Adds a Term-level query
  def add_term_q(cls, term: TermQuery, params: dict[str, str | bool | int | dict]):
    term_func = cls.terms[term]
    cls.term_qs.append(term_func(**params))

  # 
  def gen_query(cls):
    cls.gen_term_list()
    return {cls.query_type.value: cls.bool_q}
    
  def gen_term_list(cls):
    if cls.term_qs:
      term_q = cls.term_qs.pop().gen_query()
      cls.bool_q.append(term_q)
      cls.gen_query()


# --- Term-Level Queries --- #
# TODO: Add validation for parameters #
# Equivalent to the "term" and "terms" queries for ElasticSearch
class Terms:
  def __init__(cls, field: str, values: str or [str]):
    cls.field = field
    cls.values = values

  def gen_query(cls):
    query = {}
    if cls.values is not list:
      return {"term": {cls.field: cls.values}}
    else:
      return {"terms": {cls.field: [cls.values]}}

# Equivalent to the "terms_set" queries for ElasticSearch
class TermsSet:
  def __init__(cls, field: str, values: [str], req_matches=0):
    if len(values) <= 1:
      return
    
    cls.field = field
    cls.values = values
    cls.req_matches = req_matches

  def gen_query(cls):
    return {
      "terms_set": {
        cls.field: cls.values, "minimum_should_match_field": cls.req_matches
        }
      }

# Equivalent to "wildcard" queries for ElasticSearch
class Wildcard:
  def __init__(cls, field, value: str, case_insens: bool=False):
    cls.field = field
    cls.value = value
    cls.case_insens = case_insens
  
  def gen_query(cls):
    return {
      "wildcard": {
        cls.field: {
          "value": cls.value,
          "case_insensitive": cls.case_insens
        }
      }
    }

# Equivalent to "exists" query for ElasticSearch
class Exists:
  def __init__(cls, field_name: str):
    cls.field_name = field_name
  
  def gen_query(cls):
    return {
      "exists": {
        "field": cls.field_name
      }
    }

# Equivlanet to "ids" ElasticSearch query
class IDs:
  def __init__(cls, ids: [int]):
    cls.ids = ids
    for index, id in enumerate(cls.ids):
      cls.ids[index] = str(id)
  
  def gen_query(cls):
    return {
      "ids": {
        "values": cls.ids
      }
    }

# Equivalent to "range" ElasticSearch query
class Range:
  def __init__(cls, field_name: str, ranges: dict[FiltOp: int]):
    cls.field_name = field_name
    cls.ranges = ranges
  
  def gen_query(cls):
    range_dict = {cls.field_name: {}}

    for range in cls.ranges.items():
      range_dict[cls.field_name][range[0].value] = range[1]

    query = {
      "range": range_dict
    }
    return query