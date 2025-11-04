# -*- coding: utf-8 -*-
from api.dao.reservaDAO import ReservaDAO
from api.dao.inquilinoDAO import InquilinoDAO
from api.dao.chaleDAO import ChaleDAO
from api.modelo.reserva import Reserva
from api.utils.errorResponse import ErrorResponse
from datetime import datetime, date

class ReservaService:
	def __init__(self, reserva_dao: ReservaDAO, inquilino_dao: InquilinoDAO, chale_dao: ChaleDAO):
		print("⬆️  ReservaService.__init__()")
		self.__ReservaDAO = reserva_dao
		self.__InquilinoDAO = inquilino_dao
		self.__ChaleDAO = chale_dao

	def createReserva(self, reservaBodyRequest: dict) -> int:
		print("🟣 ReservaService.createReserva()")

		# Validação de campos obrigatórios
		idInquilino = reservaBodyRequest.get("idInquilino")
		idChale = reservaBodyRequest.get("idChale")
		inicio = reservaBodyRequest.get("inicio")
		fim = reservaBodyRequest.get("fim")

		# Validação de chaves estrangeiras
		if not idInquilino or not self.__InquilinoDAO.findById(idInquilino):
			raise ErrorResponse(400, "Inquilino não encontrado", {"message": f"idInquilino {idInquilino} não existe"})
		if not idChale or not self.__ChaleDAO.findById(idChale):
			raise ErrorResponse(400, "Chalé não encontrado", {"message": f"idChale {idChale} não existe"})

		# Validação de datas
		valid, errors = self._validar_datas(inicio, fim)
		if not valid:
			raise ErrorResponse(400, "Erro de validação de datas", {"errors": errors})

		# Impedir sobreposição de reservas para o mesmo chalé
		if self._existe_sobreposicao(idChale, inicio, fim):
			raise ErrorResponse(400, "Conflito de reserva", {"message": "Já existe uma reserva para este chalé neste período."})

		reserva = Reserva()
		reserva.idInquilino = idInquilino
		reserva.idChale = idChale
		reserva.inicio = inicio
		reserva.fim = fim

		return self.__ReservaDAO.create(reserva)

	def _validar_datas(self, inicio, fim):
		errors = []
		try:
			di = datetime.strptime(str(inicio), "%Y-%m-%d").date()
		except Exception:
			errors.append("Data de início inválida ou formato incorreto (esperado YYYY-MM-DD).")
			di = None
		try:
			df = datetime.strptime(str(fim), "%Y-%m-%d").date()
		except Exception:
			errors.append("Data de fim inválida ou formato incorreto (esperado YYYY-MM-DD).")
			df = None
		if di and df:
			if df <= di:
				errors.append("Data de fim deve ser posterior à data de início.")
			if di < date.today():
				errors.append("Data de início não pode ser anterior a hoje.")
		return (len(errors) == 0), errors

	def _normalizar_data(self, data_input):
		"""
		Converte qualquer formato de data (str, date, datetime) para date.
		Retorna None se a conversão falhar.
		"""
		try:
			if data_input is None:
				return None
			elif isinstance(data_input, str):
				return datetime.strptime(data_input, "%Y-%m-%d").date()
			elif isinstance(data_input, datetime):
				return data_input.date()
			elif isinstance(data_input, date):
				return data_input
			else:
				print(f"⚠️  Tipo de data não reconhecido: {type(data_input)}")
				return None
		except Exception as e:
			print(f"⚠️  Erro ao normalizar data: {e}")
			return None

	def _existe_sobreposicao(self, idChale, inicio, fim, idReserva_ignorar=None):
		"""
		Verifica se existe sobreposição de datas para o chalé.
		
		:param idChale: ID do chalé
		:param inicio: Data de início da reserva
		:param fim: Data de fim da reserva
		:param idReserva_ignorar: ID da reserva atual (para ignorar no update)
		:return: True se houver sobreposição, False caso contrário
		"""
		print(f"🔍 Verificando sobreposição para chalé {idChale}")
		
		# Normalizar datas de entrada
		di = self._normalizar_data(inicio)
		df = self._normalizar_data(fim)
		
		if not di or not df:
			print("⚠️  Erro ao normalizar datas de entrada")
			return False

		print(f"   Período a verificar: {di} até {df}")

		# Buscar todas as reservas do chalé
		try:
			reservas = self.__ReservaDAO.findByField("idChale", idChale)
			print(f"   Encontradas {len(reservas)} reservas para este chalé")
		except Exception as e:
			print(f"⚠️  Erro ao buscar reservas: {e}")
			return False
		
		for r in reservas:
			# Ignorar a própria reserva no caso de update
			if idReserva_ignorar and r.get("idReserva") == idReserva_ignorar:
				print(f"   ⏭️  Ignorando reserva {r.get('idReserva')} (própria reserva)")
				continue
			
			# Normalizar datas do banco
			ri = self._normalizar_data(r.get("inicio"))
			rf = self._normalizar_data(r.get("fim"))
			
			if not ri or not rf:
				print(f"⚠️  Erro ao normalizar datas da reserva {r.get('idReserva')}")
				continue
			
			print(f"   Comparando com reserva {r.get('idReserva')}: {ri} até {rf}")
			
			# Verificar sobreposição: (inicio < fim_existente) AND (fim > inicio_existente)
			if (di < rf) and (df > ri):
				print(f"   ⚠️  SOBREPOSIÇÃO DETECTADA com reserva {r.get('idReserva')}")
				return True
		
		print("   ✅ Nenhuma sobreposição encontrada")
		return False

	def findAll(self) -> list[dict]:
		print("🟣 ReservaService.findAll()")
		return self.__ReservaDAO.findAll()

	def findById(self, idReserva: int) -> dict | None:
		print("🟣 ReservaService.findById()")
		return self.__ReservaDAO.findById(idReserva)

	def updateReserva(self, idReserva: int, jsonReserva: dict) -> bool:
		print("🟣 ReservaService.updateReserva()")
		print(f"   idReserva: {idReserva}")
		print(f"   jsonReserva: {jsonReserva}")
		
		try:
			reserva = Reserva()
			reserva.idReserva = idReserva
			reserva.idInquilino = jsonReserva.get("idInquilino")
			reserva.idChale = jsonReserva.get("idChale")
			reserva.inicio = jsonReserva.get("inicio")
			reserva.fim = jsonReserva.get("fim")
			
			print(f"   Objeto Reserva criado com sucesso")

			# Validações de chaves estrangeiras
			print(f"   Validando idInquilino: {reserva.idInquilino}")
			if not self.__InquilinoDAO.findById(reserva.idInquilino):
				raise ErrorResponse(400, "Inquilino não encontrado", {"message": f"idInquilino {reserva.idInquilino} não existe"})
			
			print(f"   Validando idChale: {reserva.idChale}")
			if not self.__ChaleDAO.findById(reserva.idChale):
				raise ErrorResponse(400, "Chalé não encontrado", {"message": f"idChale {reserva.idChale} não existe"})
			
			# Validação de datas
			print(f"   Validando datas: {reserva.inicio} até {reserva.fim}")
			valid, errors = self._validar_datas(reserva.inicio, reserva.fim)
			if not valid:
				raise ErrorResponse(400, "Erro de validação de datas", {"errors": errors})
			
			# Verificar sobreposição (ignorando a própria reserva)
			print(f"   Verificando sobreposição...")
			if self._existe_sobreposicao(reserva.idChale, reserva.inicio, reserva.fim, idReserva):
				raise ErrorResponse(400, "Conflito de reserva", {"message": "Já existe uma reserva para este chalé neste período."})

			print(f"   Atualizando no banco de dados...")
			resultado = self.__ReservaDAO.update(reserva)
			print(f"   ✅ Atualização concluída: {resultado}")
			return resultado
			
		except ErrorResponse as er:
			print(f"❌ ErrorResponse capturado: {er}")
			raise
		except Exception as e:
			print(f"❌ Erro não tratado em updateReserva: {type(e).__name__}: {str(e)}")
			import traceback
			traceback.print_exc()
			raise

	def deleteReserva(self, idReserva: int) -> bool:
		print("🟣 ReservaService.deleteReserva()")
		reserva = Reserva()
		reserva.idReserva = idReserva
		return self.__ReservaDAO.delete(reserva)