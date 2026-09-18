import csv
import random
from datetime import datetime, timedelta
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DADOS_DIR = BASE_DIR / "dados"
DADOS_DIR.mkdir(exist_ok=True)


def gerar_chamados():
    random.seed(42)

    arquivo = DADOS_DIR / "chamados_suporte.csv"

    categorias = {
        "Acesso": [
            "Reset de senha",
            "Usuário bloqueado",
            "Permissão em pasta",
            "Acesso ao sistema",
        ],
        "Sistema": [
            "Erro ao abrir sistema",
            "Lentidão",
            "Funcionalidade indisponível",
            "Erro após atualização",
        ],
        "Rede": [
            "Sem acesso à internet",
            "Falha de DNS",
            "VPN indisponível",
            "Conexão instável",
        ],
        "Impressão": [
            "Impressora offline",
            "Fila de impressão travada",
            "Erro de driver",
            "Impressão lenta",
        ],
        "Banco de Dados": [
            "Erro em consulta",
            "Dados inconsistentes",
            "Falha de conexão",
            "Relatório sem dados",
        ],
    }

    canais = ["Portal", "E-mail", "Telefone", "Chat"]
    tecnicos = ["Ana Souza", "Bruno Lima", "Carla Mendes", "Diego Rocha", "Elisa Martins"]

    sla_por_prioridade = {
        "Crítica": 1,
        "Alta": 4,
        "Média": 8,
        "Baixa": 24,
    }

    prioridades = ["Crítica", "Alta", "Média", "Baixa"]
    pesos_prioridade = [0.08, 0.22, 0.48, 0.22]

    status_opcoes = ["Fechado", "Resolvido", "Em andamento", "Aguardando usuário"]
    pesos_status = [0.62, 0.20, 0.10, 0.08]

    inicio = datetime(2026, 6, 1, 8, 0)
    fim = datetime(2026, 8, 31, 18, 0)
    intervalo_segundos = int((fim - inicio).total_seconds())

    linhas = []

    for i in range(1, 201):
        categoria = random.choice(list(categorias.keys()))
        assunto = random.choice(categorias[categoria])
        prioridade = random.choices(prioridades, weights=pesos_prioridade, k=1)[0]
        sla_horas = sla_por_prioridade[prioridade]
        canal = random.choices(canais, weights=[0.35, 0.25, 0.20, 0.20], k=1)[0]
        tecnico = random.choice(tecnicos)
        nivel = random.choices(["N1", "N2"], weights=[0.78, 0.22], k=1)[0]
        status = random.choices(status_opcoes, weights=pesos_status, k=1)[0]

        data_abertura = inicio + timedelta(seconds=random.randint(0, intervalo_segundos))

        base_reincidencia = 0.12
        if categoria in ["Sistema", "Rede", "Banco de Dados"]:
            base_reincidencia += 0.10
        reincidente = "Sim" if random.random() < base_reincidencia else "Não"

        if status in ["Fechado", "Resolvido"]:
            fator_categoria = {
                "Acesso": 0.55,
                "Sistema": 1.15,
                "Rede": 1.05,
                "Impressão": 0.75,
                "Banco de Dados": 1.25,
            }[categoria]

            if random.random() < 0.22:
                tempo_resolucao = sla_horas * random.uniform(1.05, 2.20) * fator_categoria
            else:
                tempo_resolucao = sla_horas * random.uniform(0.20, 0.95) * fator_categoria

            tempo_resolucao = round(max(0.2, tempo_resolucao), 2)
            data_fechamento = data_abertura + timedelta(hours=tempo_resolucao)
            sla_cumprido = "Sim" if tempo_resolucao <= sla_horas else "Não"

            if sla_cumprido == "Sim" and reincidente == "Não":
                csat = random.choices([3, 4, 5], weights=[0.10, 0.35, 0.55], k=1)[0]
            elif sla_cumprido == "Não" and reincidente == "Sim":
                csat = random.choices([1, 2, 3, 4], weights=[0.30, 0.35, 0.25, 0.10], k=1)[0]
            else:
                csat = random.choices([2, 3, 4, 5], weights=[0.15, 0.30, 0.35, 0.20], k=1)[0]

            data_fechamento_str = data_fechamento.strftime("%Y-%m-%d %H:%M:%S")
        else:
            tempo_resolucao = ""
            data_fechamento_str = ""
            sla_cumprido = "Pendente"
            csat = ""

        linhas.append([
            f"CH-{i:04d}",
            data_abertura.strftime("%Y-%m-%d %H:%M:%S"),
            data_fechamento_str,
            categoria,
            assunto,
            prioridade,
            canal,
            nivel,
            status,
            tecnico,
            sla_horas,
            tempo_resolucao,
            sla_cumprido,
            reincidente,
            csat,
        ])

    cabecalho = [
        "id_chamado",
        "data_abertura",
        "data_fechamento",
        "categoria",
        "assunto",
        "prioridade",
        "canal",
        "nivel_atendimento",
        "status",
        "tecnico",
        "sla_horas",
        "tempo_resolucao_horas",
        "sla_cumprido",
        "reincidente",
        "csat",
    ]

    with arquivo.open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(cabecalho)
        writer.writerows(linhas)

    return arquivo


def gerar_logs():
    random.seed(84)

    arquivo = DADOS_DIR / "logs_sistema.csv"

    sistemas = [
        "Portal Web",
        "API Clientes",
        "Banco Oracle",
        "VPN Corporativa",
        "Servidor de Impressao",
    ]
    severidades = ["INFO", "WARNING", "ERROR", "CRITICAL"]

    tipos = {
        "Portal Web": ["login_failed", "timeout", "http_500", "slow_response"],
        "API Clientes": ["auth_error", "timeout", "rate_limit", "http_500"],
        "Banco Oracle": ["connection_error", "deadlock", "query_timeout", "high_cpu"],
        "VPN Corporativa": ["connection_drop", "auth_failed", "latency", "dns_error"],
        "Servidor de Impressao": ["spooler_error", "printer_offline", "queue_stuck", "driver_error"],
    }

    mensagens = {
        "login_failed": "Falha de autenticação detectada",
        "timeout": "Tempo limite excedido na operação",
        "http_500": "Erro interno do servidor",
        "slow_response": "Tempo de resposta acima do esperado",
        "auth_error": "Erro de autenticação na API",
        "rate_limit": "Limite de requisições excedido",
        "connection_error": "Falha de conexão com o banco de dados",
        "deadlock": "Deadlock detectado entre transações",
        "query_timeout": "Consulta excedeu o tempo limite",
        "high_cpu": "Uso elevado de CPU no servidor de banco",
        "connection_drop": "Conexão VPN interrompida",
        "auth_failed": "Falha de autenticação na VPN",
        "latency": "Latência de rede acima do normal",
        "dns_error": "Falha na resolução de DNS",
        "spooler_error": "Falha no serviço de spooler",
        "printer_offline": "Impressora detectada como offline",
        "queue_stuck": "Fila de impressão bloqueada",
        "driver_error": "Erro no driver de impressão",
    }

    inicio = datetime(2026, 6, 1, 0, 0)
    fim = datetime(2026, 8, 31, 23, 59)
    intervalo = int((fim - inicio).total_seconds())

    linhas = []

    for i in range(1, 301):
        sistema = random.choice(sistemas)
        tipo_evento = random.choice(tipos[sistema])

        if tipo_evento in [
            "http_500",
            "connection_error",
            "deadlock",
            "query_timeout",
            "connection_drop",
            "spooler_error",
        ]:
            severidade = random.choices(severidades, weights=[0.05, 0.15, 0.55, 0.25], k=1)[0]
        else:
            severidade = random.choices(severidades, weights=[0.25, 0.45, 0.25, 0.05], k=1)[0]

        data_evento = inicio + timedelta(seconds=random.randint(0, intervalo))

        id_chamado = ""
        if severidade in ["ERROR", "CRITICAL"] and random.random() < 0.60:
            id_chamado = f"CH-{random.randint(1, 200):04d}"

        origem = random.choice(["Aplicacao", "Servidor", "Rede", "Banco de Dados"])
        status_evento = random.choices(
            ["Resolvido", "Monitorando", "Aberto"],
            weights=[0.62, 0.23, 0.15],
            k=1,
        )[0]

        linhas.append([
            f"LOG-{i:04d}",
            data_evento.strftime("%Y-%m-%d %H:%M:%S"),
            sistema,
            severidade,
            tipo_evento,
            mensagens[tipo_evento],
            origem,
            status_evento,
            id_chamado,
        ])

    cabecalho = [
        "id_evento",
        "data_evento",
        "sistema",
        "severidade",
        "tipo_evento",
        "mensagem",
        "origem",
        "status_evento",
        "id_chamado",
    ]

    with arquivo.open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(cabecalho)
        writer.writerows(linhas)

    return arquivo


if __name__ == "__main__":
    chamados = gerar_chamados()
    logs = gerar_logs()
    print(f"Arquivos gerados: {chamados} e {logs}")
