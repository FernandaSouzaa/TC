import json

class AFD:
    def __init__(self, estados, alfabeto, transicoes, estado_inicial, estados_finais):
        self.estados = set(estados)
        self.alfabeto = set(alfabeto)
        self.transicoes = transicoes  # dicionário: (estado, símbolo) → estado
        self.estado_inicial = estado_inicial
        self.estados_finais = set(estados_finais)

    def salvar_em_arquivo(self, caminho):
        dados = {
            "estados": list(self.estados),
            "alfabeto": list(self.alfabeto),
            "estado_inicial": self.estado_inicial,
            "estados_finais": list(self.estados_finais),
            "transicoes": {f"({k[0]},{k[1]})": v for k, v in self.transicoes.items()}
        }
        with open(caminho, "w") as f:
            json.dump(dados, f, indent=4)


    @staticmethod
    def carregar_de_arquivo(caminho):
        with open(caminho, "r") as f:
            dados = json.load(f)
        transicoes = {}
        for chave, destino in dados["transicoes"].items():
            chave = chave.strip("()").split(",")
            transicoes[(chave[0], chave[1])] = destino
        return AFD(
            dados["estados"],
            dados["alfabeto"],
            transicoes,
            dados["estado_inicial"],
            dados["estados_finais"]
        )

def minimizar_afd(afd):
    P = [afd.estados_finais.copy(), afd.estados - afd.estados_finais]

    while True:
        nova_P = []
        for grupo in P:
            particoes = {}
            for estado in grupo:
                assinatura = tuple(
                    next((i for i, g in enumerate(P) if afd.transicoes.get((estado, a)) in g), -1)
                    for a in afd.alfabeto
                )
                particoes.setdefault(assinatura, set()).add(estado)
            nova_P.extend(particoes.values())
        if nova_P == P:
            break
        P = nova_P

    estado_para_grupo = {}
    for i, grupo in enumerate(P):
        for estado in grupo:
            estado_para_grupo[estado] = f"S{i}"

    novo_estados = set(estado_para_grupo.values())
    novo_inicial = estado_para_grupo[afd.estado_inicial]
    novo_finais = {estado_para_grupo[e] for e in afd.estados_finais}

    novo_transicoes = {}
    for (estado, simbolo), destino in afd.transicoes.items():
        novo_transicoes[(estado_para_grupo[estado], simbolo)] = estado_para_grupo[destino]

    return AFD(novo_estados, afd.alfabeto, novo_transicoes, novo_inicial, novo_finais)

#Exemplo de uso:
afd = AFD.carregar_de_arquivo("Teoria da Computação/ExPrograma/afd1.json")

print("✅ AFD carregado com sucesso:")
print(f"Estados: {afd.estados}")
print(f"Alfabeto: {afd.alfabeto}")
print(f"Estado inicial: {afd.estado_inicial}")
print(f"Estados finais: {afd.estados_finais}")
print("Transições:")
for (estado, simbolo), destino in afd.transicoes.items():
    print(f"  δ({estado}, {simbolo}) -> {destino}")
print()

print("🔍 Iniciando a minimização do AFD...")

afd_min = minimizar_afd(afd)

print("✅ AFD minimizado com sucesso:")
print(f"Estados: {afd_min.estados}")
print(f"Estado inicial: {afd_min.estado_inicial}")
print(f"Estados finais: {afd_min.estados_finais}")
print("Transições:")
for (estado, simbolo), destino in afd_min.transicoes.items():
    print(f"  δ({estado}, {simbolo}) -> {destino}")
print()

afd_min.salvar_em_arquivo("afd_minimizado.json")
print("💾 AFD minimizado salvo em 'afd_minimizado.json'")

