from flask import Flask, render_template, request
from backend import verificar_par_ou_impar, jogar_par_ou_impar

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def home():
    """Renderiza a pagina inicial e processa as duas versoes do jogo.

    Em requisicoes POST, identifica a acao ("simples" ou "jogo"), executa a
    funcao correspondente do backend e devolve o resultado para a pagina.

    :return: HTML renderizado a partir de index.html.
    """
    resultado_simples = None
    resultado_jogo = None
    erro = None

    if request.method == "POST":
        acao = request.form.get("acao")

        try:
            if acao == "simples":
                numero = int(request.form.get("numero"))
                resultado = verificar_par_ou_impar(numero)
                resultado_simples = f"O número {numero} é {resultado}."

            elif acao == "jogo":
                escolha = request.form.get("escolha")
                jogador = int(request.form.get("jogador"))
                resultado_jogo = jogar_par_ou_impar(escolha, jogador)

        except ValueError as mensagem_erro:
            erro = str(mensagem_erro)

    return render_template(
        "index.html",
        resultado_simples=resultado_simples,
        resultado_jogo=resultado_jogo,
        erro=erro
    )


if __name__ == "__main__":
    app.run(debug=True)
