from flask import Flask, request, jsonify
import requests
from flasgger import Swagger

app = Flask(__name__)
swagger = Swagger(app)  # Inicializa o Swagger

@app.route('/cep', methods=['GET'])
def buscar_cep():
    """
    Busca informações de um CEP
    ---
    parameters:
      - name: cep
        in: query
        type: string
        required: true
        description: CEP a ser consultado
    responses:
      200:
        description: Informações do CEP
        schema:
          id: CepInfo
          properties:
            cep:
              type: string
              description: O CEP consultado
            logradouro:
              type: string
              description: Logradouro do endereço
            bairro:
              type: string
              description: Bairro do endereço
            localidade:
              type: string
              description: Cidade do endereço
            uf:
              type: string
              description: Estado do endereço
      400:
        description: Erro na requisição
    """
    cep = request.args.get('cep')
    if not cep:
        return jsonify({'error': 'CEP não informado'}), 400

    try:
        response = requests.get(f"https://viacep.com.br/ws/{cep}/json/")
        data = response.json()

        if "erro" in data:
            return jsonify({"error": "CEP inválido"}), 400

        return jsonify(data), 200
    except Exception as e:
        return jsonify({'message': 'Erro ao buscar o CEP', 'error': str(e)}), 400

# Inicializa a aplicação
if __name__ == '__main__':
    app.run(debug=True)
