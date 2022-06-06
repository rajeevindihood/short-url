
from __future__ import annotations

from pydantic import BaseModel

class HashModel(BaseModel):
    url: str

# CREATE TABLE hash_keys (
# 	id SERIAL  PRIMARY KEY,
# 	original_key VARCHAR (255) NOT NULL,
# 	hash_key  VARCHAR (8) NOT NULL,
# 	creation_date  TIMESTAMP,
#     last_visiting_time TIMESTAMP,
#     UNIQUE(hash_key, original_key)
# );

# ALTER TABLE hash_keys 
# ADD COLUMN is_enabled boolean default true, 
# ADD COLUMN expiry_date timestamp;