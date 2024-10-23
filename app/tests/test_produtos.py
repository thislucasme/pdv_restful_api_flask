import unittest
from app import create_app, mongo
from app.models.produto_model import ProdutoModel
from app.schemas.product_schema import ProdutoSchema

class ProdutoTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
        self.produto_schema = ProdutoSchema()

    def tearDown(self):
        #limpar as collections
        mongo.cx.close()

    def test_create_product(self):
        new_product = {
            "categorias_id": "123",
            "promocao_id": None,
            "estoque": 50,
            "codigo_barras": "1234567890123",
            "observacao": "Produto em bom estado",
            "controlar_estoque": True,
            "venda_fracionada": False,
            "valor_aberto": 10.99,
            "fornecedores_id": "456",
            "users_id": None,
            "descricao": "Refrigerante coca cola 2L",
            "url_image": "http://exemplo.com/imagem.jpg",
            "preco_custo": 7.50,
            "preco_venda": 12.00,
            "quantidade": 100
        }


        response = self.client.post('/produtos/', json=new_product)
        self.assertEqual(response.status_code, 200)

        data = response.get_json()
        self.assertIn('_id', data) 
        self.assertEqual(data['descricao'], new_product['descricao']) 

    def test_create_product_invalid(self):
            invalid_products = [
                 {
                    "promocao_id": None,
                    "observacao": "Produto em bom estado",
                    "valor_aberto": 10.99,
                    "fornecedores_id": "456",
                    "url_image": "http://exemplo.com/imagem.jpg"
                },
                {    
                }
            ]

            for invalid_product in invalid_products:
                response = self.client.post('/produtos/', json=invalid_product)
                self.assertEqual(response.status_code, 400)

        

if __name__ == '__main__':
    unittest.main()
