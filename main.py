# Turma 2ESPG

# AUGUSTO DOUGLAS NOGUEIRA DE MENDONÇA - RM558371 
# GABRIEL VASQUEZ QUEIROZ DA SILVA – RM557056 
# GUILHERME ARAUJO DE CARVALHO – RM558926 
# GUSTAVO OLIVEIRA RIBEIRO – RM559163 

# Análise de algoritmos e notação O-grande das funções feita no arquivo PDF

from datetime import datetime
from dataclasses import dataclass, field
from typing import Dict

@dataclass
class Exame:
    resultados: dict
    analise: list[str] = field(default_factory=list)  # Análise do exame (avaliações)

@dataclass
class Usuario:
    nome: str
    idade: int
    genero: str
    exames: Dict[str, Dict[str, Exame]] = field(default_factory=dict)
    # exames: tipo -> data -> Exame

agenda = {}

def validar_cpf(cpf: str) -> bool:
    """Valida se o CPF tem 11 dígitos numéricos."""
    return cpf.isdigit() and len(cpf) == 11

def validar_data(data: str) -> bool:
    """Valida se a data está no formato dd/mm/aaaa."""
    try:
        datetime.strptime(data, "%d/%m/%Y")
        return True
    except ValueError:
        return False

def input_float(msg: str) -> float:
    """Força a entrada de um número decimal válido."""
    while True:
        try:
            return float(input(msg))
        except ValueError:
            print("⚠️  Valor inválido. Digite um número.")

def input_int(msg: str) -> int:
    """Força a entrada de um número inteiro válido."""
    while True:
        try:
            return int(input(msg))
        except ValueError:
            print("⚠️  Valor inválido. Digite um número inteiro.")

def cadastrar_usuario():
    """Cadastra um novo paciente com CPF, nome, idade e gênero."""
    print("\n👤 Cadastro de Novo Usuário")
    cpf = input("CPF (somente números): ").strip()
    if not validar_cpf(cpf):
        print("❌ CPF inválido. Deve conter 11 dígitos.")
        return
    if cpf in agenda:
        print("⚠️  Usuário já cadastrado.")
        return

    nome = input("Nome completo: ").strip()
    idade = input_int("Idade: ")
    genero = input("Gênero (M/F): ").strip().upper()
    if genero not in {"M", "F"}:
        print("⚠️  Gênero inválido.")
        return

    agenda[cpf] = Usuario(nome=nome, idade=idade, genero=genero)
    print("✅ Usuário cadastrado com sucesso!")

def cadastrar_exame():
    """Permite cadastrar um exame clínico para um paciente existente."""
    print("\n🧪 Cadastro de Novo Exame")
    cpf = input("CPF do paciente: ").strip()
    if cpf not in agenda:
        print("❌ Usuário não encontrado.")
        return

    print("\n📋  Tipo de Exame:")
    tipos_exame = {
        "1": "Hemograma Completo",
        "2": "Colesterol",
        "3": "Glicemia",
        "4": "Hormônios"
    }
    for key, value in tipos_exame.items():
        print(f"{key}️⃣  {value}")

    opcao = input("Escolha uma opção: ")
    data = input("🗓️ Data do exame (dd/mm/aaaa): ")
    if not validar_data(data):
        print("❌ Data inválida.")
        return

    genero = agenda[cpf].genero
    tipo = tipos_exame.get(opcao)
    if not tipo:
        print("❌ Opção inválida.")
        return

    resultados = coletar_resultados_exame(tipo, genero)
    if resultados is None:
        print("❌ Falha na coleta dos resultados do exame.")
        return

    # Gerar análise do exame
    analise = analisar_exame(tipo, resultados, genero)

    # Inicializa estrutura se precisar
    if tipo not in agenda[cpf].exames:
        agenda[cpf].exames[tipo] = {}

    if data in agenda[cpf].exames[tipo]:
        print(f"⚠️ Já existe um exame de {tipo} cadastrado na data {data}.")
        confirm = input("Deseja sobrescrever? (S/N): ").strip().upper()
        if confirm != "S":
            print("Operação cancelada, exame não cadastrado.")
            return

    agenda[cpf].exames[tipo][data] = Exame(resultados=resultados, analise=analise)
    print(f"✅ {tipo} cadastrado com sucesso na data {data}.")

def coletar_resultados_exame(tipo: str, genero: str) -> dict:
    """Coleta os resultados do exame com base no tipo e gênero."""
    if tipo == "Hemograma Completo":
        return {
            "Glóbulos vermelhos": input_float("Glóbulos vermelhos (milhões/µL): "),
            "Hemoglobina": input_float("Hemoglobina (g/dL): "),
            "Leucócitos": input_int("Leucócitos (células/µL): "),
            "Plaquetas": input_int("Plaquetas (células/µL): ")
        }
    elif tipo == "Colesterol":
        return {
            "Colesterol total": input_float("Colesterol total (mg/dL): "),
            "Colesterol HDL": input_float("Colesterol HDL (bom) (mg/dL): "),
            "Colesterol LDL": input_float("Colesterol LDL (ruim) (mg/dL): ")
        }
    elif tipo == "Glicemia":
        return {
            "Glicose": input_float("Glicose (mg/dL): ")
        }
    elif tipo == "Hormônios":
        return {
            "TSH": input_float("TSH (mU/L): "),
            "T4 livre": input_float("T4 livre (ng/dL): ")
        }
    return None

def analisar_exame(tipo: str, resultados: dict, genero: str) -> list[str]:
    """Chama a função de análise específica para o exame."""
    if tipo == "Hemograma Completo":
        return analisar_hemograma(resultados, genero)
    elif tipo == "Colesterol":
        return analisar_colesterol(resultados)
    elif tipo == "Glicemia":
        return analisar_glicemia(resultados)
    elif tipo == "Hormônios":
        return analisar_hormonios(resultados)
    else:
        return []

def analisar_hemograma(exame: dict, genero: str) -> list[str]:
    resultado = []
    if genero == "M":
        resultado.append(analisar_faixa("Glóbulos vermelhos", exame["Glóbulos vermelhos"], 4.7, 6.1, "milhões/µL"))
        resultado.append(analisar_faixa("Hemoglobina", exame["Hemoglobina"], 13.8, 17.2, "g/dL"))
    else:
        resultado.append(analisar_faixa("Glóbulos vermelhos", exame["Glóbulos vermelhos"], 4.2, 5.4, "milhões/µL"))
        resultado.append(analisar_faixa("Hemoglobina", exame["Hemoglobina"], 12.1, 15.1, "g/dL"))
    resultado.append(analisar_faixa("Leucócitos", exame["Leucócitos"], 4500, 11000, "células/µL"))
    resultado.append(analisar_faixa("Plaquetas", exame["Plaquetas"], 150000, 450000, "células/µL"))
    return resultado

def analisar_colesterol(exame: dict) -> list[str]:
    resultado = []
    resultado.append(analisar_faixa("Colesterol total", exame["Colesterol total"], 0, 190, "mg/dL", tipo="máx"))
    resultado.append(analisar_faixa("Colesterol HDL", exame["Colesterol HDL"], 40, float('inf'), "mg/dL", tipo="mín"))
    resultado.append(analisar_faixa("Colesterol LDL", exame["Colesterol LDL"], 0, 130, "mg/dL", tipo="máx"))
    return resultado

def analisar_glicemia(exame: dict) -> list[str]:
    valor = exame["Glicose"]
    if valor < 70:
        return ["Glicose baixa"]
    elif valor <= 99:
        return ["Glicose normal"]
    elif valor >= 126:
        return ["Glicose alta (possível diabetes)"]
    else:
        return ["Glicose elevada (pré-diabetes)"]

def analisar_hormonios(exame: dict) -> list[str]:
    resultado = []
    resultado.append(analisar_faixa("TSH", exame["TSH"], 0.4, 4.0, "mU/L"))
    resultado.append(analisar_faixa("T4 livre", exame["T4 livre"], 0.8, 2.0, "ng/dL"))
    return resultado

def analisar_faixa(nome: str, valor: float, minimo: float, maximo: float, unidade: str, tipo="normal") -> str:
    """Avalia se um valor está dentro da faixa esperada."""
    if tipo == "normal" and (valor < minimo or valor > maximo):
        if valor < minimo:
            return f"{nome} abaixo do ideal ({valor} {unidade})"
        else:
            return f"{nome} acima do ideal ({valor} {unidade})"
    elif tipo == "máx" and valor > maximo:
        return f"{nome} elevado ({valor} {unidade})"
    elif tipo == "mín" and valor < minimo:
        return f"{nome} baixo ({valor} {unidade})"
    return f"{nome} normal ({valor} {unidade})"

def visualizar_exames():
    """Mostra todos os exames de um paciente por CPF."""
    print("\n📂 Visualização de Todos os Exames")
    cpf = input("CPF do paciente: ").strip()
    if cpf not in agenda:
        print("❌ Usuário não encontrado.")
        return

    exames = agenda[cpf].exames
    if not exames:
        print("ℹ️ Nenhum exame cadastrado.")
        return

    print(f"\n🧾 Exames de {agenda[cpf].nome}:\n")
    for tipo, exames_por_data in exames.items():
        for data, exame in exames_por_data.items():
            print(f"📌 {tipo} - {data}:")
            for chave, valor in exame.resultados.items():
                print(f"   ➤  {chave}: {valor}")
            print("   ➤  Resultado da análise:")
            for anal in exame.analise:
                print(f"      • {anal}")
            print()

def visualizar_exame_especifico():
    """Permite selecionar um tipo de exame e data para visualizar o resultado específico."""
    print("\n🔍 Visualizar Exame Específico")
    cpf = input("CPF do paciente: ").strip()
    if cpf not in agenda:
        print("❌ Usuário não encontrado.")
        return

    exames = agenda[cpf].exames
    if not exames:
        print("ℹ️ Esse paciente não possui exames.")
        return

    print("\n📋 Exames disponíveis:")
    tipos = list(exames.keys())
    for i, tipo in enumerate(tipos, 1):
        datas = list(exames[tipo].keys())
        datas_str = ", ".join(datas)
        print(f"{i}. {tipo} (datas: {datas_str})")

    try:
        opcao = int(input("Escolha o exame: "))
        tipo_escolhido = tipos[opcao - 1]
    except (ValueError, IndexError):
        print("❌ Opção inválida.")
        return

    datas_disponiveis = list(exames[tipo_escolhido].keys())
    if len(datas_disponiveis) > 1:
        print(f"\nDatas disponíveis para {tipo_escolhido}:")
        for i, data in enumerate(datas_disponiveis, 1):
            print(f"{i}. {data}")
        try:
            opcao_data = int(input("Escolha a data do exame: "))
            data_escolhida = datas_disponiveis[opcao_data - 1]
        except (ValueError, IndexError):
            print("❌ Opção inválida.")
            return
    else:
        data_escolhida = datas_disponiveis[0]

    exame = exames[tipo_escolhido][data_escolhida]
    print(f"\n📑 Resultado do exame {tipo_escolhido} - {data_escolhida}:")
    for chave, valor in exame.resultados.items():
        print(f"   ➤  {chave}: {valor}")
    print("   ➤  Resultado da análise:")
    for anal in exame.analise:
        print(f"      • {anal}")

def apagar_usuario():
    """Remove um usuário e todos os seus exames com base no CPF."""
    print("\n🗑️ Apagar Usuário")
    cpf = input("CPF do usuário a ser removido: ").strip()
    if cpf in agenda:
        del agenda[cpf]
        print("✅ Usuário removido com sucesso.")
    else:
        print("❌ Usuário não encontrado.")

# Menu principal
def menu():
    """Exibe o menu principal e navega entre as funcionalidades."""
    while True:
        print("\n📊 === Sistema de Monitoramento de Exames Clínicos ===")
        print("1️⃣  Cadastrar novo usuário")
        print("2️⃣  Cadastrar novo exame")
        print("3️⃣  Visualizar exames")
        print("4️⃣  Visualizar exame em específico")
        print("5️⃣  Apagar usuário")
        print("6️⃣  Fechar programa")

        opcao = input("Escolha uma opção: ")
        match opcao:
            case "1":
                cadastrar_usuario()
            case "2":
                cadastrar_exame()
            case "3":
                visualizar_exames()
            case "4":
                visualizar_exame_especifico()
            case "5":
                apagar_usuario()
            case "6":
                print("👋 Encerrando o programa. Até mais!")
                break
            case _:
                print("❌ Opção inválida.")

if __name__ == "__main__":
    menu()