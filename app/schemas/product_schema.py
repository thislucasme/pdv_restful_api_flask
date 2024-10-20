from dataclasses import dataclass
from typing import Optional
from marshmallow import Schema, fields, post_load

@dataclass
class Product:
    categorias_id: Optional[str] = None
    promocao_id: Optional[str] = None
    estoque: Optional[int] = None
    codigo_barras: Optional[str] = None
    observacao: Optional[str] = None
    controlar_estoque: Optional[bool] = None
    venda_fracionada: Optional[bool] = None
    valor_aberto: Optional[float] = None
    fornecedores_id: Optional[str] = None
    users_id: Optional[str] = None
    descricao: Optional[str] = None
    url_image: Optional[str] = None
    preco_custo: Optional[float] = None
    preco_venda: Optional[float] = None
    quantidade: Optional[int] = None
    _id: str = None

class ProdutoSchema(Schema):
    categorias_id = fields.Str(allow_none=True)
    promocao_id = fields.Str(allow_none=True)
    estoque = fields.Int(allow_none=True)
    codigo_barras = fields.Str(allow_none=True)
    observacao = fields.Str(allow_none=True)
    controlar_estoque = fields.Bool(allow_none=True)
    venda_fracionada = fields.Bool(allow_none=True)
    valor_aberto = fields.Float(allow_none=True)
    fornecedores_id = fields.Str(allow_none=True)
    users_id = fields.Str(allow_none=True)
    descricao = fields.String(required=True)
    url_image = fields.Str(allow_none=True)
    preco_custo = fields.Float(allow_none=True)
    preco_venda = fields.Float(allow_none=True)
    quantidade = fields.Int(allow_none=True)

    @post_load
    def make_product(self, data, **kwargs):
        return Product(**data)
