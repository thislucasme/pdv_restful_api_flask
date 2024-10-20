from dataclasses import dataclass
from typing import Optional
from marshmallow import Schema, fields, post_load

@dataclass
class QueryProductPagination:
    page: Optional[int] = None
    limit: Optional[int] = None
    queryText: Optional[str] = None
    codigoBarras: Optional[str] = None

class QueryProductPaginationSchema(Schema):
    page = fields.Int(required=True)
    limit = fields.Int(required=True)
    queryText = fields.Str(required=True)
    codigoBarras = fields.Str(required=True)
    
    @post_load
    def make_product(self, data, **kwargs):
        return QueryProductPagination(**data)
