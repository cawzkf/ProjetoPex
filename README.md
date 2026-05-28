# Jogo Par ou Ímpar com Visão Computacional

Projeto de Computação Gráfica que implementa o clássico jogo **Par ou Ímpar** em duas versões:

- **Interface web (Flask):** jogue pelo navegador.
- **Visão computacional (OpenCV + MediaPipe):** jogue mostrando a mão para a webcam — o número de dedos levantados é o seu palpite.

## Estrutura

```
ProjetoPex/
├── app.py            # interface web (Flask)
├── backend.py        # lógica do jogo
├── visao.py          # versão com câmera + MediaPipe
├── requirements.txt  # dependências
├── static/
│   └── style.css     # estilo da página
└── templates/
    └── index.html    # página web
```

## Como rodar (Windows / PowerShell)

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt

python app.py      # interface web → http://127.0.0.1:5000
python visao.py    # versão com câmera
```

> **Atenção à versão:** a API `mp.solutions` do MediaPipe usada em `visao.py` exige
> **Python 3.12** e `mediapipe==0.10.21`. Versões 0.10.30+ removeram esse módulo.

## Controles da versão com câmera

| Tecla | Ação |
|-------|------|
| `P`   | escolher PAR |
| `I`   | escolher ÍMPAR |
| `J`   | jogar com a quantidade de dedos detectada |
| `Q`   | sair |
