from constants import FiltOp
from constants import TermQuery, BoolQuery
 
#Represents a given Boolean-level element of the ElasticSearch query.
class BooleanLevel:
  def __init__(self, q_type: BoolQuery):
    self.term_qs: [TermQuery] = []
    self.query_type = q_type
    self.bool_q = []

    # This dictionary is used to create Term-level queries
    self.terms = { 
      TermQuery.EXISTS: Exists,
      TermQuery.TERMS: Terms,
      TermQuery.TERMS_SET: TermsSet,
      TermQuery.RANGE: Range,
      TermQuery.WILDCARD: Wildcard,
      TermQuery.IDS: IDs
    }

  # Adds a Term-level query
  def add_term_q(self, term: TermQuery, params: dict[str, str | bool | int | dict]):
    term_func = self.terms[term]
    self.term_qs.append(term_func(**params))

  # 
  def gen_query(self):
    self.gen_term_list()
    return {self.query_type.value: self.bool_q}
    
  def gen_term_list(self):
    if self.term_qs:
      term_q = self.term_qs.pop().gen_query()
      self.bool_q.append(term_q)
      self.gen_query()


# --- Term-Level Queries --- #
# TODO: Add validation for parameters #
# Equivalent to the "term" and "terms" queries for ElasticSearch
class Terms:
  def __init__(self, field: str, values: str or [str]):
    self.field = field
    self.values = values

  def gen_query(self):
    query = {}
    if self.values is not list:
      return {"term": {self.field: self.values}}
    else:
      return {"terms": {self.field: [self.values]}}

# Equivalent to the "terms_set" queries for ElasticSearch
class TermsSet:
  def __init__(self, field: str, values: [str], req_matches=0):
    if len(values) <= 1:
      return
    
    self.field = field
    self.values = values
    self.req_matches = req_matches

  def gen_query(self):
    return {
      "terms_set": {
        self.field: self.values, "minimum_should_match_field": self.req_matches
        }
      }

# Equivalent to "wildcard" queries for ElasticSearch
class Wildcard:
  def __init__(self, field, value: str, case_insens: bool=False):
    self.field = field
    self.value = value
    self.case_insens = case_insens
  
  def gen_query(self):
    return {
      "wildcard": {
        self.field: {
          "value": self.value,
          "case_insensitive": self.case_insens
        }
      }
    }

# Equivalent to "exists" query for ElasticSearch
class Exists:
  def __init__(self, field_name: str):
    self.field_name = field_name
  
  def gen_query(self):
    return {
      "exists": {
        "field": self.field_name
      }
    }

# Equivlanet to "ids" ElasticSearch query
class IDs:
  def __init__(self, ids: [int]):
    self.ids = ids
    for index, id in enumerate(self.ids):
      self.ids[index] = str(id)
  
  def gen_query(self):
    return {
      "ids": {
        "values": self.ids
      }
    }

# Equivalent to "range" ElasticSearch query
class Range:
  def __init__(self, field_name: str, ranges: dict[FiltOp: int]):
    self.field_name = field_name
    self.ranges = ranges
  
  def gen_query(self):
    range_dict = {self.field_name: {}}

    for range in self.ranges.items():
      range_dict[self.field_name][range[0].value] = range[1]

    query = {
      "range": range_dict
    }
    return query