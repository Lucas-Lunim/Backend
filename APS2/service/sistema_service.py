class SistemaService:
    def __init__(self):
        self.eventos = []
        self.participantes = []
        self.inscricoes = []
        self.proximo_evento_id = 1
        self.proximo_participante_id = 1

    def listar_eventos(self):
        return self.eventos

    def buscar_evento(self, evento_id):
        for evento in self.eventos:
            if evento["id"] == evento_id:
                return evento
        return None

    def validar_evento(self, dados):
        if not dados.titulo.strip():
            raise ValueError("O título do evento não pode ser vazio.")
        if dados.capacidade <= 0:
            raise ValueError("A capacidade deve ser maior que zero.")

    def criar_evento(self, dados):
        self.validar_evento(dados)
        evento = {
            "id": self.proximo_evento_id,
            "titulo": dados.titulo,
            "descricao": dados.descricao,
            "data": dados.data,
            "horario": dados.horario,
            "local": dados.local,
            "capacidade": dados.capacidade,
            "categoria": dados.categoria,
        }
        self.eventos.append(evento)
        self.proximo_evento_id += 1
        return evento

    def atualizar_evento(self, evento_id, dados):
        evento = self.buscar_evento(evento_id)
        if evento is None:
            raise ValueError("Evento não encontrado.")
        self.validar_evento(dados)
        if dados.capacidade < len(self.listar_inscricoes(evento_id)):
            raise ValueError("A capacidade não pode ser menor que o número de inscritos.")
        evento["titulo"] = dados.titulo
        evento["descricao"] = dados.descricao
        evento["data"] = dados.data
        evento["horario"] = dados.horario
        evento["local"] = dados.local
        evento["capacidade"] = dados.capacidade
        evento["categoria"] = dados.categoria
        return evento

    def remover_evento(self, evento_id):
        evento = self.buscar_evento(evento_id)
        if evento is None:
            raise ValueError("Evento não encontrado.")
        # Remove também as inscrições para não deixar referências ao evento excluído.
        for inscricao in self.inscricoes[:]:
            if inscricao["evento_id"] == evento_id:
                self.inscricoes.remove(inscricao)
        self.eventos.remove(evento)

    def listar_participantes(self):
        return self.participantes

    def buscar_participante(self, participante_id):
        for participante in self.participantes:
            if participante["id"] == participante_id:
                return participante
        return None

    def validar_participante(self, dados):
        if not dados.nome.strip():
            raise ValueError("O nome do participante não pode ser vazio.")

    def criar_participante(self, dados):
        self.validar_participante(dados)
        participante = {
            "id": self.proximo_participante_id,
            "nome": dados.nome,
            "email": dados.email,
            "curso": dados.curso,
        }
        self.participantes.append(participante)
        self.proximo_participante_id += 1
        return participante

    def atualizar_participante(self, participante_id, dados):
        participante = self.buscar_participante(participante_id)
        if participante is None:
            raise ValueError("Participante não encontrado.")
        self.validar_participante(dados)
        participante["nome"] = dados.nome
        participante["email"] = dados.email
        participante["curso"] = dados.curso
        return participante

    def remover_participante(self, participante_id):
        participante = self.buscar_participante(participante_id)
        if participante is None:
            raise ValueError("Participante não encontrado.")
        # Ao excluir um participante, suas vagas ficam disponíveis novamente.
        for inscricao in self.inscricoes[:]:
            if inscricao["participante_id"] == participante_id:
                self.inscricoes.remove(inscricao)
        self.participantes.remove(participante)

    def inscrever(self, evento_id, participante_id):
        evento = self.buscar_evento(evento_id)
        if evento is None:
            raise ValueError("Evento não encontrado.")
        if self.buscar_participante(participante_id) is None:
            raise ValueError("Participante não encontrado.")
        for inscricao in self.inscricoes:
            if inscricao["evento_id"] == evento_id and inscricao["participante_id"] == participante_id:
                raise ValueError("Participante já está inscrito neste evento.")
        if len(self.listar_inscricoes(evento_id)) >= evento["capacidade"]:
            raise ValueError("Não existem vagas disponíveis para este evento.")
        inscricao = {"evento_id": evento_id, "participante_id": participante_id}
        self.inscricoes.append(inscricao)
        return inscricao

    def listar_inscricoes(self, evento_id):
        if self.buscar_evento(evento_id) is None:
            raise ValueError("Evento não encontrado.")
        inscritos = []
        for inscricao in self.inscricoes:
            if inscricao["evento_id"] == evento_id:
                participante = self.buscar_participante(inscricao["participante_id"])
                inscritos.append(participante)
        return inscritos


# Uma instância mantém os dados em memória entre as requisições.
sistema = SistemaService()
