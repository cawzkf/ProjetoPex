"""Versao do jogo Par ou Impar com visao computacional.

Comandos na tela:
    P: escolher PAR
    I: escolher IMPAR
    J: jogar usando a quantidade de dedos detectada
    Q: sair
"""

import cv2
import mediapipe as mp
from backend import jogar_par_ou_impar

mp_maos = mp.solutions.hands
mp_desenho = mp.solutions.drawing_utils

maos = mp_maos.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

# No Windows o backend padrao (MSMF) abre a camera mas falha ao ler os frames;
# o DirectShow (cv2.CAP_DSHOW) e mais estavel.
camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)


def contar_dedos(pontos_mao, lado_mao):
    """Conta quantos dedos estao levantados a partir dos pontos da mao.

    Para indicador, medio, anelar e minimo, o dedo e considerado levantado
    quando a ponta esta acima da base (menor coordenada Y). O polegar usa a
    coordenada X, e a regra se inverte conforme a mao seja direita ou esquerda.

    :param pontos_mao: landmarks da mao retornados pelo MediaPipe.
    :param lado_mao: "Right" ou "Left", indicando a mao detectada.
    :return: quantidade de dedos levantados (0 a 5).
    """
    dedos = 0

    pontas = [8, 12, 16, 20]
    bases = [6, 10, 14, 18]

    for ponta, base in zip(pontas, bases):
        if pontos_mao.landmark[ponta].y < pontos_mao.landmark[base].y:
            dedos += 1

    if lado_mao == "Right":
        if pontos_mao.landmark[4].x < pontos_mao.landmark[3].x:
            dedos += 1
    else:
        if pontos_mao.landmark[4].x > pontos_mao.landmark[3].x:
            dedos += 1

    return dedos


def escrever_texto(frame, texto, posicao, escala=0.75, espessura=2):
    """Escreve um texto sobre o frame da camera.

    Usa texto sem acento para evitar falhas de renderizacao no OpenCV.

    :param frame: imagem (frame) onde o texto sera desenhado.
    :param texto: texto a ser exibido.
    :param posicao: tupla (x, y) com a posicao do texto.
    :param escala: fator de escala da fonte.
    :param espessura: espessura do traco da fonte.
    :return: None.
    """
    cv2.putText(
        frame,
        texto,
        posicao,
        cv2.FONT_HERSHEY_SIMPLEX,
        escala,
        (0, 255, 0),
        espessura
    )


def main():
    """Executa o loop principal: captura a camera, detecta a mao e joga.

    Le os frames da webcam, conta os dedos levantados e responde as teclas
    P, I, J e Q para escolher par/impar, jogar e sair.

    :return: None.
    """
    escolha_usuario = "par"
    quantidade_dedos = None
    ultimo_resultado = None

    if not camera.isOpened():
        print("Erro: nao foi possivel acessar a camera.")
        return

    while True:
        sucesso, frame = camera.read()

        if not sucesso:
            print("Erro ao acessar a camera.")
            break

        frame = cv2.flip(frame, 1)
        imagem_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        resultado = maos.process(imagem_rgb)

        if resultado.multi_hand_landmarks:
            pontos_mao = resultado.multi_hand_landmarks[0]
            lado_mao = resultado.multi_handedness[0].classification[0].label
            quantidade_dedos = contar_dedos(pontos_mao, lado_mao)

            mp_desenho.draw_landmarks(
                frame,
                pontos_mao,
                mp_maos.HAND_CONNECTIONS
            )

            texto_dedos = f"Dedos levantados: {quantidade_dedos}"
        else:
            texto_dedos = "Nenhuma mao detectada"
            quantidade_dedos = None

        escrever_texto(frame, texto_dedos, (30, 50), 0.9, 2)
        escrever_texto(frame, f"Sua escolha: {escolha_usuario.upper()}", (30, 90), 0.75, 2)
        escrever_texto(frame, "P=Par | I=Impar | J=Jogar | Q=Sair", (30, 130), 0.65, 2)

        if ultimo_resultado:
            escrever_texto(frame, f"Voce jogou: {ultimo_resultado['jogador']}", (30, 180), 0.7, 2)
            escrever_texto(frame, f"PC jogou: {ultimo_resultado['computador']}", (30, 215), 0.7, 2)
            escrever_texto(frame, f"Soma: {ultimo_resultado['soma']}", (30, 250), 0.7, 2)
            escrever_texto(frame, f"Resultado: {ultimo_resultado['resultado']}", (30, 285), 0.7, 2)
            escrever_texto(frame, ultimo_resultado["vencedor"], (30, 330), 0.85, 2)

        cv2.imshow("Jogo Par ou Impar com Visao Computacional", frame)

        tecla = cv2.waitKey(1) & 0xFF

        if tecla == ord("q"):
            break

        if tecla == ord("p"):
            escolha_usuario = "par"
            ultimo_resultado = None

        if tecla == ord("i"):
            escolha_usuario = "impar"
            ultimo_resultado = None

        if tecla == ord("j"):
            if quantidade_dedos is not None:
                ultimo_resultado = jogar_par_ou_impar(
                    escolha=escolha_usuario,
                    jogador=quantidade_dedos
                )
                print(ultimo_resultado)
            else:
                print("Mostre a mao para a camera antes de jogar.")

    camera.release()
    maos.close()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
