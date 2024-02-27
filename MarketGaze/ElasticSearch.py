from MarketGaze.Constants import BoolQuery, FiltOp, SortType, TermQuery
from json import dumps

#Represents a given Boolean-level element of the ElasticSearch query.
class BooleanLevel:
  def __init__(self, q_type: BoolQuery):
    self.term_qs: list[TermQuery] = []
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
  def __init__(self, field: str, values: str | list[str]):
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
  def __init__(self, field: str, values: list[str], req_matches=0):
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
  def __init__(self, ids: list[int]):
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

# Typing for type hints
AnyBool = Terms | TermsSet | Wildcard | Exists | IDs | Range  

class RequestBuilder:
  
  def __init__(cls):
    cls.last_req: str = None
    cls.curr_req: str = ""

    # Holds indexes, columns, sort, and boolean queries
    cls.indexes: list[str] = []
    cls.columns: list[str] = []
    cls.sort: dict[str, SortType] = {}
    cls.size: int = 0
    cls.start_index: int = 0

    #list of BooleanLevel classes to be used in the body of the query
    cls.bool_qs: {BoolQuery, AnyBool} = {
      BoolQuery.MUST: None,
      BoolQuery.FILT: None,
      BoolQuery.SHOULD: None,
      BoolQuery.MUSTNT: None
    }

  # Backs up last request and clears the current one, then starts setting up new request
  def new_req(cls, indexes: list[str]=[], columns: list[str]=[], size:int=0, start_index:int=0):
    cls.last_req = cls.curr_req
    cls.curr_req = ""
    cls.set_indexes_columns(indexes, columns)
    cls.set_size(size)
    cls.set_start(start_index)
  
  # Sets sorting type for a given column, which must have been set already.
  def add_sort(cls, type: SortType, column: str):
      if column in cls.columns:
        cls.sort[column] = {"order": type.value}

  # Adds a term query to a given BooleanLevel query
  def add_term_query(cls, bool_q: BoolQuery, term_q: TermQuery, params):
    # if 
    if not cls.bool_qs[bool_q]:
      bool_q_item = BooleanLevel(bool_q)
      cls.bool_qs[bool_q] = bool_q_item  
    cls.bool_qs[bool_q].add_term_q(term_q, params)

  # Sets indexes or columns. Since extending with an empty list does nothing, 
  # Only checks for presence if extend is false, so that existing indexes
  # and columns are not replaced with an empty list
  def set_indexes_columns(cls, indexes: list[str] = [], columns: list[str] = [], extend:bool=False):    
    match extend:
      case True:
        cls.indexes.extend(indexes)
        cls.columns.extend(columns)
      
      case False:
        if indexes:
          cls.indexes = indexes
        
        if columns: 
          cls.columns = columns

  # Sets number of results to get back
  def set_size(cls, size):
    cls.size = size

  # Sets the starting index of the search
  def set_start(cls, start_index):
    cls.start_index = start_index

  # Generates query, returning the constructed query as as JSON str
  def gen_query(cls):
    query = {
      "columns": ','.join(cls.columns),
      "indexes": ','.join(cls.indexes),
      "body": cls.gen_body(),
    }

    return dumps(query)
    
  # Call to generate the body of a query
  def gen_body(cls):
    body = {
      "size": str(cls.size),
      "from": str(cls.start_index),
    }
    if cls.sort:
      body["sort"] = cls.sort
      
    bool_body = {}

    for item in cls.bool_qs.items():
      bool_type_str = item[0].value
      if item[1] is not None:
        bool_res= item[1].gen_query()
        bool_body.update(bool_res)
    if bool_body:
      body["query"] = {"bool":bool_body}
    return body
  
  # Saves last request before constructing a new one
  def save_last_req(cls):
    cls.last_req = cls.curr_req

  # Gets current request
  def get_curr_req(cls):
    return cls.last_req