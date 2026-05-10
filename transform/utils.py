
from datetime import datetime
from zoneinfo import ZoneInfo

def resolve_field(record, aliases):
  """
  Returns the first matching fieled value from a list of aliases
  record: The record being transformed
  aliases: A list of possible field names
  """
  for alias in aliases:
    if alias in record:
      return record[alias]
  return None

def normalize_id(value):
  """
  Returns an integer representing value. If value is invalid return None
  value: the value that must be reresented as an integer
  """
  if value is None:
    return None

  return int(str(value).strip())


def normalize_text(text):
  """
  Returns a string representing text after removing whitespace and new lines
  text: the string that needs to be normalized
  """
  if not text:
      return None

  return " ".join(str(text).split())

def normalize_email(email):
  """
  Returns a string representing an email after removing whitespace and decapitalizing
  email: the string that needs to be normalized
  """
  if not email:
    return None

  return email.strip().lower()


def make_timestamp():
  dt = datetime.now(ZoneInfo("America/Vancouver"))
  return dt.strftime("%Y-%m-%d %H:%M:%S.") + f"{dt.microsecond // 1000:03d} " + dt.strftime("%z")