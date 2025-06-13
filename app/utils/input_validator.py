import re
from fastapi import HTTPException, status

def has_middle_space(input_str):
  return bool(re.search(r'(?<!^)\s(?!$)', input_str))

def check_input_parameter(input_parameter: str)->str:
  if not isinstance(input_parameter,str):
    raise ValueError("Parameter must be a string")
  input_parameter.strip()
  
  if not input_parameter:
    raise HTTPException(
      status_code=status.HTTP_400_BAD_REQUEST,
      detail=f"Empty {input_parameter}")
  
  if has_middle_space(input_parameter):
    raise HTTPException(
      status_code=status.HTTP_400_BAD_REQUEST,
      detail=f"Invalid parameter: {input_parameter}, please enter without empty spaces")
  
  input_parameter = input_parameter.replace(" ", "")
  if not input_parameter:
    raise HTTPException(
      status_code=status.HTTP_400_BAD_REQUEST,
      detail="Empty parameter: {input_parameter}")
  
  return input_parameter

def is_valid_namesurname(input_str):
    regex = r"^[a-zA-Z\s\-&_']+$"
    return bool(re.match(regex, input_str))

