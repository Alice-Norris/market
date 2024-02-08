from enum import StrEnum, IntEnum, Enum
from PySide6.QtCore import QEvent
APPLICATION_DATA = {
  "organization": "Aresu Nereru",
  "application": "MarketGaze"
}
FILE_DIRS = {
  "json" : "./data/json/",
  "icon" : "./data/icons/"
}

FILE_NAMES = {
  "json": [
    "class_job.json",
    "craft_type.json",
    "dc.json",
    "recipes.json"
  ],
  "icon": [
    "ALC.png", "ARM.png", "BSM.png", "BTN.png",
    "CRP.png", "CUL.png", "FSH.png", "GSM.png", 
    "LTW.png", "MIN.png", "WVR.png"
  ] 
}

class FiltOp(StrEnum):
  LTE = "lte"
  LT = "lt"
  GT = "gt"
  GTE = "gte"

class SortType(StrEnum):
  ASC = "asc"
  DESC = "desc"

class BoolQuery(StrEnum):
  MUST = "must"
  FILT = "filter"
  SHOULD = "should"
  MUSTNT = "must_not"
  
class TermQuery(StrEnum):
  #TERM = "term"
  TERMS = "terms"
  TERMS_SET = "terms_set"
  RANGE = "range"
  EXISTS = "exists"
  WILDCARD = "wildcard"
  IDS = "ids"

class FullTextQuery(StrEnum):
  MATCH = "match"
  PHRASE = "match_phrase"
  PHRASE_PRE = "match_phrase_prefix"
  MULTI = "multi_match"
  COMM = "common"
  Q_STRING = "query_string"
  S_Q_STRING = "simple_query_string"

# TODO: Remove this
class TermsLookup(StrEnum):
  IND = "index"
  TYPE = "type"
  ID = "id"
  PATH = "path"