# -*- coding: utf-8 -*-
"""
Controlador para reservas públicas (sem autenticação).
"""
from flask import request, jsonify

class ReservaPublicaControl:
    """
    Controlador SIMPLIFICADO para reservas públicas.
    """
    
    def __init__(self, reserva_service):
        """
        :param reserva_service: Instância do ReservaService
        """
        from api.service.reservaPublicaService import ReservaPublicaService
        
        self.reserva_service = reserva_service
        self.publica_service = ReservaPublicaService(reserva_service)
    
    def store_publica(self):
        """
        Endpoint público para criação de reservas.
        NÃO requer autenticação JWT.
        
        Formato esperado:
        {
            "reserva_publica": {
                "nome": "João Silva",
                "email": "joao@email.com",
                "telefone": "(11) 99999-9999",
                "chale_desejado": "romantico",
                "data_inicio": "2024-12-01",
                "data_fim": "2024-12-05",
                "numero_pessoas": 2,
                "observacoes": "Chegarei às 14h"
            }
        }
        """
        print("🔵 ReservaPublicaControl.store_publica() - INÍCIO")
        
        try:
            # 1. OBTER DADOS DA REQUISIÇÃO
            dados_request = request.json
            print(f"📩 Request JSON: {dados_request}")
            
            if not dados_request or "reserva_publica" not in dados_request:
                return jsonify({
                    "success": False,
                    "error": {
                        "message": "Formato inválido. Use: {'reserva_publica': {...}}",
                        "code": "INVALID_FORMAT"
                    }
                }), 400
            
            dados_form = dados_request["reserva_publica"]
            print(f"📝 Dados do formulário: {dados_form}")
            
            # 2. PROCESSAR RESERVA
            reserva_id = self.publica_service.criar_reserva_simples(dados_form)
            
            # 3. RETORNAR RESPOSTA DE SUCESSO
            resposta = {
                "success": True,
                "message": "✅ Reserva recebida com sucesso!",
                "data": {
                    "reserva": {
                        "id": reserva_id,
                        "status": "pendente",
                        "mensagem": "Nossa equipe entrará em contato para confirmação."
                    },
                    "contato": {
                        "nome": dados_form["nome"],
                        "email": dados_form["email"],
                        "telefone": dados_form["telefone"]
                    },
                    "instrucoes": [
                        "Aguarde nosso contato em até 24 horas úteis",
                        "Check-in a partir das 14h, check-out até 12h",
                        "Levar documento de identificação",
                        f"Dúvidas: (54) 99999-9999"
                    ]
                }
            }
            
            print(f"📤 Resposta de sucesso: {resposta}")
            return jsonify(resposta), 201
            
        except Exception as e:
            print(f"❌ Erro em store_publica: {str(e)}")
            return jsonify({
                "success": False,
                "error": {
                    "message": str(e),
                    "code": "RESERVA_ERROR"
                }
            }), 400