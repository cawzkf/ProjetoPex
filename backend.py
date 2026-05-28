import random
from typing import Dict, Optional


def verificar_par_ou_impar(numero: int) -> str:
    """Verifica se um numero inteiro e par ou impar.

    :param numero: numero inteiro a ser avaliado.
    :return: "par" se o numero for par, "impar" caso contrario.
    """
    return "par" if numero % 2 == 0 else "impar"


def gerar_numero_computador(minimo: int = 1, maximo: int = 5) -> int:
    """Sorteia o numero jogado pelo computador.

    :param minimo: menor valor possivel do sorteio.
    :param maximo: maior valor possivel do sorteio.
    :return: numero inteiro sorteado entre minimo e maximo.
    """
    return random.randint(minimo, maximo)


def normalizar_escolha(escolha: str) -> str:
    """Padroniza a escolha do jogador para "par" ou "impar".

    Aceita variacoes como "par", "p", "impar" ou "i".

    :param escolha: texto informado pelo jogador.
    :return: "par" ou "impar".
    :raises ValueError: se a escolha for vazia ou invalida.
    """
    if escolha is None:
        raise ValueError("A escolha não pode estar vazia.")

    escolha_normalizada = escolha.strip().lower().replace("í", "i")

    if escolha_normalizada in ["p", "par"]:
        return "par"

    if escolha_normalizada in ["i", "impar"]:
        return "impar"

    raise ValueError("Escolha inválida. Use 'par' ou 'impar'.")


def validar_numero_jogador(numero: int) -> int:
    """Valida o numero escolhido pelo jogador.

    O valor vem da contagem de dedos, entao o intervalo aceito e de 0 a 5.

    :param numero: numero escolhido pelo jogador.
    :return: o proprio numero, quando valido.
    :raises TypeError: se o numero nao for inteiro.
    :raises ValueError: se o numero estiver fora do intervalo de 0 a 5.
    """
    if not isinstance(numero, int):
        raise TypeError("O número do jogador precisa ser inteiro.")

    if numero < 0 or numero > 5:
        raise ValueError("O número do jogador precisa estar entre 0 e 5.")

    return numero


def jogar_par_ou_impar(
    escolha: str,
    jogador: int,
    computador: Optional[int] = None
) -> Dict[str, object]:
    """Executa uma rodada completa do jogo Par ou Impar.

    :param escolha: escolha do jogador ("par" ou "impar").
    :param jogador: numero do jogador, normalmente capturado pela mao.
    :param computador: numero do computador; se None, e sorteado.
    :return: dicionario com escolha, jogador, computador, soma, resultado e vencedor.
    """
    escolha_normalizada = normalizar_escolha(escolha)
    numero_jogador = validar_numero_jogador(jogador)

    if computador is None:
        numero_computador = gerar_numero_computador()
    else:
        numero_computador = computador

    soma = numero_jogador + numero_computador
    resultado = verificar_par_ou_impar(soma)

    if escolha_normalizada == resultado:
        vencedor = "Você ganhou!"
    else:
        vencedor = "O computador ganhou!"

    return {
        "escolha": escolha_normalizada,
        "jogador": numero_jogador,
        "computador": numero_computador,
        "soma": soma,
        "resultado": "par" if resultado == "par" else "impar",
        "vencedor": vencedor
    }
