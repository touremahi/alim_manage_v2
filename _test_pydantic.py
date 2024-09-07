from datetime import datetime
from pydantic import BaseModel, ValidationError

class User(BaseModel):
    id: int
    name: str = "Mahi"
    signup_ts: datetime | None
    tastes: dict[str, int]

external_data = {
    'id': 123,
    'signup_ts': '2019-06-01 12:22',  
    'tastes': {
        'wine': 9,
        b'cheese': 7,  
        'cabbage': '1.2',  
    },
}

try:
    user = User(**external_data)
    print(user.model_dump())
except ValidationError as e:
    print(e.errors())
user = User(**external_data)


