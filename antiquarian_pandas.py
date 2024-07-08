import sys
from dotenv import load_dotenv
from utils.cost import estimate_costs, get_costs_gpt4o, get_n_tokens
from utils.utils import ask_permission
from utils.ai import query_gpt
import pandas as pd


INPUT = "input/stj/processos_4777_T1.csv"
OUTPUT = "output/stj/processos_4777_T1_antiquarian.feather"
AI_MODEL = "gpt-4o"
DANGER_MODE = True

PROMPT = """Você foi encarregado de analisar um documento jurídico chamado "certidão de julgamento" e responder a perguntas específicas sobre ele. Suas respostas devem ser fornecidas em formato JSON.

Aqui está o texto da certidão de julgamento:

<certidao>
{variable}
</certidao>

Leia e analise cuidadosamente o texto acima para responder às seguintes perguntas:

1. Qual foi o resultado do julgamento? Responda com "ACEITO", "PARCIAL" ou "NEGADO".
2. A certidão menciona que o julgamento foi realizado em sessão virtual? Responda com "SIM" ou "NAO".
3. A decisão foi unânime (unanimidade)? Responda com "SIM" ou "NAO".
4. Houve efeitos modificativos? Responda com "SIM", "NAO". Se não houver menção de efeitos modificativos, responda null.
5. Como foi julgado o conhecimento (conhecer)? Responda com "SIM", "PARCIAL", "NAO". Se não houver menção de conhecimento, responda null.
6. Quais ministros votaram a favor?
7. Quais ministros foram vencidos?
8. Quais ministros fizeram um "voto-vista"?
9. Algum ministro vai lavrar o acórdão? Se não houver menção sobre lavrar, responda null.

Instruções para responder:

1. Leia cuidadosamente todo o texto para reunir todas as informações relevantes.
2. Para perguntas que exigem respostas "SIM" ou "NAO", procure menções explícitas no texto.
3. Para perguntas sobre ministros, use apenas os primeiros nomes em suas respostas.
4. Se não houver informações suficientes para responder a uma pergunta, use null como resposta.
5. Para a lista de ministros, os liste em ordem alfabética e separe os nomes com vírgulas se houver vários.
6. Lembre-se de incluir o primeiro nome do relator nas listas de votos aonde adequado.
7. Certifique-se de que suas respostas reflitam com precisão as informações fornecidas no texto.

Forneça sua resposta no seguinte formato JSON:

<answer>
{
    "resultado": ,
    "online": ,
    "unanimidade": ,
    "modificativos": ,
    "conhecer": ,
    "aFavor": ,
    "vencidos": ,
    "votoVista": ,
    "lavrara": 
}
</answer>

Preencha os valores para cada chave com base em sua análise do texto. Lembre-se de usar null se não houver informações suficientes para responder a uma determinada pergunta."""


def ai_cleanup(text: str) -> str:
    load_dotenv()

    prompt = PROMPT.replace("{variable}", text)
    model = AI_MODEL

    n_tokens = get_n_tokens(model, prompt)
    estimate_costs(model, n_tokens)

    if not DANGER_MODE:
        if not ask_permission():
            sys.exit(0)

    response = query_gpt(model, prompt)

    get_costs_gpt4o(response)

    return response.choices[0].message.content  # type: ignore


def main():
    df = pd.read_csv(INPUT)
    rows = df["decisao"].tolist()

    result = []

    try:
        for row in rows:
            result.append(ai_cleanup(row))

    finally:
        result_series = pd.Series(result)
        df["decisao_antiquarian"] = result_series
        df.to_csv(OUTPUT, index=False)

        print("expected size: ", df.shape[0])
        print("received size: ", result_series.size)
        print("Antiquarian: cleanup complete. Output written to", OUTPUT)


if __name__ == "__main__":
    main()