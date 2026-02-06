# -*- coding: utf-8 -*-
"""
Serviço SIMPLIFICADO para reservas públicas.
NÃO cria inquilino, NÃO verifica disponibilidade.
Usa ID fixo e mapeamento simples.
"""

class ReservaPublicaService:
    """
    Serviço para reservas públicas via site.
    Versão SIMPLES: usa IDs fixos pré-configurados.
    """
    
    
    ID_INQUILINO_PUBLICO = 999  # Deve existir na tabela inquilinos
    
    # Mapeamento: código do site -> ID real no banco
    MAPEAMENTO_CHALES = {
        "romantico": 13,   # Chalé Romântico
        "familiar": 14,    # Chalé Familiar
        "premium": 26      # Suíte Premium
    }
    
    def __init__(self, reserva_service):
        """
        :param reserva_service: Instância do ReservaService existente
        """
        self.reserva_service = reserva_service
    
    def criar_reserva_simples(self, dados_formulario):
        """
        Cria reserva pública de forma SIMPLIFICADA.
        
        Args:
            dados_formulario: dict com dados do formulário web
        
        Returns:
            int: ID da reserva criada
        
        Raises:
            Exception: Se dados inválidos
        """
        print("🔵 ReservaPublicaService.criar_reserva_simples()")
        
        # 1. VALIDAR DADOS BÁSICOS
        self._validar_dados_obrigatorios(dados_formulario)
        
        # 2. MAPEAR CHALÉ DESEJADO PARA ID REAL
        chale_id = self._mapear_chale(dados_formulario["chale_desejado"])
        
        # 3. PREPARAR DADOS PARA O SERVICE DE RESERVA EXISTENTE
        dados_reserva = {
            "idInquilino": self.ID_INQUILINO_PUBLICO,
            "idChale": chale_id,
            "inicio": dados_formulario["data_inicio"],
            "fim": dados_formulario["data_fim"],
            "observacoes": self._gerar_observacoes(dados_formulario)
        }
        
        print(f"📤 Dados preparados para reserva_service: {dados_reserva}")
        
        # 4. CHAMAR SERVIÇO EXISTENTE (já testado e funciona)
        reserva_id = self.reserva_service.createReserva(dados_reserva)
        
        print(f"✅ Reserva pública criada: ID {reserva_id}")
        return reserva_id
    
    def _validar_dados_obrigatorios(self, dados):
        """Valida campos obrigatórios"""
        obrigatorios = [
            "nome", "email", "telefone", "chale_desejado",
            "data_inicio", "data_fim", "numero_pessoas"
        ]
        
        faltantes = [campo for campo in obrigatorios if not dados.get(campo)]
        
        if faltantes:
            raise Exception(f"Campos obrigatórios faltando: {', '.join(faltantes)}")
        
        # Validar formato das datas (básico)
        if dados["data_fim"] <= dados["data_inicio"]:
            raise Exception("Data de check-out deve ser posterior ao check-in")
    
    def _mapear_chale(self, chale_desejado):
        """Converte 'romantico' para ID 1, etc."""
        chale_id = self.MAPEAMENTO_CHALES.get(chale_desejado.lower())
        
        if not chale_id:
            chal_disponiveis = list(self.MAPEAMENTO_CHALES.keys())
            raise Exception(
                f"Chalé '{chale_desejado}' não encontrado. "
                f"Opções: {', '.join(chal_disponiveis)}"
            )
        
        return chale_id
    
    def _gerar_observacoes(self, dados):
        """Gera observações com todos os dados do formulário"""
        return f"""
        🏡 RESERVA PÚBLICA VIA SITE CASA BRANCA
        
        📋 DADOS DO CLIENTE:
        • Nome: {dados['nome']}
        • Email: {dados['email']}
        • Telefone: {dados['telefone']}
        • Pessoas: {dados['numero_pessoas']}
        
        🗓️ PERÍODO:
        • Check-in: {dados['data_inicio']}
        • Check-out: {dados['data_fim']}
        
        🏠 CHALÉ:
        • Tipo: {dados['chale_desejado']}
        
        📝 OBSERVAÇÕES DO CLIENTE:
        {dados.get('observacoes', 'Nenhuma')}
        
        ---
        Reserva gerada automaticamente pelo site.
        """