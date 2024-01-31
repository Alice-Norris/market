from constants import TermQuery, BoolQuery, SortType
from es_queries import BooleanLevel, Terms, TermsSet, Wildcard, Exists, IDs, Range
from json import dumps

# Typing for type hints
AnyBool = Terms | TermsSet | Wildcard | Exists | IDs | Range  

class RequestBuilder:
  
  def __init__(cls):
    cls.last_req: str = None
    cls.curr_req: str = ""

    # Holds indexes, columns, sort, and boolean queries
    cls.indexes: [str] = []
    cls.columns: [str] = []
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
  def new_req(cls, indexes:[str]=[], columns:[str]=[], size:int=0, start_index:int=0):
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
  def set_indexes_columns(cls, indexes: [str] = [], columns: [str] = [], extend:bool=False):    
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