# ⚔️ Batalha do Conhecimento

> Disputa local de conhecimento entre dois jogadores, ideal para escolas públicas com poucos recursos tecnológicos.

---

## Docs de comentários sobre o projeto
Daniel Hardman: https://docs.google.com/document/d/1UiNBWj87X-gdmjlYIDYjL0_pY6zpNgiLQH3rtrhYAFk/edit?usp=sharing

## Sobre o projeto

**Batalha do Conhecimento** é um jogo educacional desenvolvido em Python com a biblioteca **Pygame**. Ele oferece uma experiência de **competição local** entre dois jogadores, que respondem perguntas de **Matemática** e **Português** em tempo real. Cada jogador utiliza seu próprio conjunto de teclas, tornando o jogo acessível mesmo em ambientes com um único computador — perfeito para salas de aula com **falta de equipamentos eletrônicos individuais**.

O jogo foi projetado para ser **leve**, **divertido** e **educativo**, estimulando o aprendizado colaborativo e a competição saudável. Com uma interface visual atrativa, animações de personagens, efeitos sonoros e sistema de pontuação baseado em velocidade e precisão, ele transforma o estudo em uma batalha épica.

---

## 🎯 Funcionalidades

### Tela Inicial
- **Logo e título** estilizados
- **Pressione qualquer tecla** para avançar para a história

### História
- Narrativa envolvente com dois personagens: **Jeromel** e **Felisberto**
- Texto digitado progressivamente com efeito de máquina de escrever
- Possibilidade de pular toda a história com **ENTER**

### Menu Principal
- **Batalha Matemática** — apenas perguntas de matemática
- **Batalha Português** — apenas perguntas de português
- **Batalha Mista** — perguntas aleatórias de ambas as matérias
- **Sair** — encerra o jogo

### Batalha (Gameplay)
- **Disputa local** para **dois jogadores** em um único teclado
- **Contagem regressiva** (3, 2, 1, GO!) antes de cada pergunta
- Cada jogador tem **4 teclas** para escolher alternativas (A, B, C, D):
  - **Jogador 1**: `Q`, `W`, `E`, `R`
  - **Jogador 2**: `U`, `I`, `O`, `P`
- **Tempo limite** para responder (8 segundos)
- **Cálculo de dano** baseado em:
  - Correção da resposta
  - Tempo de resposta (rápida, média, lenta)
  - Dificuldade da pergunta (fácil, normal, difícil)
  - Bônus para quem acertar **primeiro** na rodada
- **Animações** dos personagens:
  - Ataque (quando acerta)
  - Dano (quando sofre dano)
  - Erro (quando erra)
- **Mensagens flutuantes** de dano (`-10`, `-18`, etc.)
- **Barra de vida** com cores dinâmicas (verde, amarelo, vermelho)
- **Cronômetro** visual para cada rodada
- **Música de fundo** e **efeitos sonoros** (ataque, dano, vitória)
- **Cenários** aleatórios a cada batalha
- **Tela de controles** (F1) que pode ser aberta a qualquer momento para lembrar as teclas
- **Finalização automática** quando um jogador perde toda a vida ou após 20 perguntas
- **Tela de resultado** com estatísticas detalhadas de cada jogador

### Tela de Resultado
- Exibe o **vencedor** ou **empate**
- **Estatísticas individuais**:
  - Vida restante
  - Acertos e erros
  - Dano total causado
  - Tempo médio de resposta
  - Precisão (percentual de acertos)
- **Sprites** dos personagens em vitória/derrota (se disponíveis)
- **Cenário especial** para a tela de resultado
- Pressione **ESC** ou **ENTER** para voltar ao menu

### Controles e Acessibilidade
- **Tela de controles** (F1) exibe o mapeamento de teclas para ambos os jogadores
- Pode ser aberta/fechada a qualquer momento durante a batalha, **congelando** o jogo
- Ideal para salas de aula com **projetor** ou **TV** — todos veem as teclas na tela

---

## 📁 Estrutura de Pastas

```
batalha_do_conhecimento/
│
├── main.py                     ← Ponto de entrada do jogo
│
├── classes/                    ← Todas as classes do jogo
│   ├── __init__.py
│   ├── batalha.py              ← Lógica principal da batalha
│   ├── calculadora_dano.py     ← Fórmula de cálculo de dano
│   ├── constantes.py           ← Configurações (teclas, cores, tempos, etc.)
│   ├── gerenciador_animacoes.py← Carrega sprites dos personagens
│   ├── gerenciador_cenarios.py ← Carrega e sorteia cenários
│   ├── gerenciador_perguntas.py← Gerencia o banco de perguntas
│   ├── gerenciador_sons.py     ← Gerencia música e efeitos sonoros
│   ├── historia.py             ← Tela da história inicial
│   ├── jogador.py              ← Dados e estatísticas do jogador
│   ├── menu.py                 ← Menu principal
│   ├── pergunta.py             ← Estrutura de uma pergunta
│   ├── personagem.py           ← Sprite animado do personagem
│   ├── resultado.py            ← Tela de resultado final
│   ├── tela_controles.py       ← Overlay de teclas
│   └── tela_inicial.py         ← Tela de abertura
│
├── assets/                     ← Recursos multimídia
│   ├── personagens/            ← Sprites dos personagens (player1, player2)
│   │   ├── player1/
│   │   │   ├── idle_1.png      ← Quadros de idle
│   │   │   ├── idle_2.png
│   │   │   ├── idle_3.png
│   │   │   ├── ataque.png
│   │   │   ├── dano.png
│   │   │   └── errou.png
│   │   └── player2/            (mesma estrutura)
│   ├── cenarios/               ← Imagens de fundo (cenario_1.png, etc.)
│   │   ├── cenario_1.png
│   │   ├── cenario_2.png
│   │   ├── cenario_3.png
│   │   └── cenario_resultado.png (opcional)
│   └── sons/                   ← Áudios (MP3 e WAV)
│       ├── musica_batalha.mp3
│       ├── som_ataque.wav
│       ├── som_dano.wav
│       └── som_vitoria.wav
│
├── dados/                      ← Banco de dados do jogo
│   └── perguntas.json          ← Todas as perguntas (600 questões)
│
└── README.md                   ← Este arquivo
```

---

## ⚙️ Como Executar

### Pré-requisitos
- **Python 3.8** ou superior
- **Pygame** instalado

### Passos

```bash
# 1. Clone o repositório (ou baixe os arquivos)
git clone https://github.com/seu-usuario/batalha-do-conhecimento.git

# 2. Entre na pasta do projeto
cd batalha-do-conhecimento

# 3. Instale o Pygame (se ainda não tiver)
pip install pygame

# 4. Execute o jogo
python main.py
```

> No Windows, use `python main.py`; no Linux/Mac, pode ser `python3 main.py`.

---

## 🎮 Regras do Jogo

### Objetivo
Ser o **último jogador com vida** ou ter a **maior vida** após 20 perguntas.

### Como Jogar
1. **Escolha o modo** (Matemática, Português ou Misto)
2. Uma **contagem regressiva** (3, 2, 1, GO!) aparece antes de cada pergunta
3. A pergunta é exibida no centro da tela com **4 alternativas** (A, B, C, D)
4. Cada jogador pressiona sua tecla correspondente à alternativa escolhida:
   - **Jogador 1**: `Q` (A), `W` (B), `E` (C), `R` (D)
   - **Jogador 2**: `U` (A), `I` (B), `O` (C), `P` (D)
5. O tempo de resposta é cronometrado; respostas rápidas causam **mais dano**
6. Quem acertar **primeiro** ganha um **bônus** de dano
7. O dano é aplicado ao **oponente**
8. O jogo termina quando um jogador chega a **0 de vida** ou após **20 perguntas**

### Cálculo de Dano

| Dificuldade | Rápida (< 2s) | Média (2s–5s) | Lenta (> 5s) |
|-------------|---------------|---------------|--------------|
| Fácil       | 10            | 8             | 5            |
| Normal      | 14            | 11            | 8            |
| Difícil     | 18            | 15            | 10           |

- **Bônus** de **+3** para quem acertar primeiro na rodada.

### Tela de Controles (F1)
- Pressione **F1** a qualquer momento para abrir/fechar a tela de controles
- Útil para lembrar as teclas, especialmente em ambiente de sala de aula

---

## 🧩 Personalizações Rápidas

| O que mudar | Onde mexer |
|-------------|------------|
| **Teclas dos jogadores** | `classes/constantes.py` → `TECLAS_JOGADOR_1` e `TECLAS_JOGADOR_2` |
| **Vida inicial** | `classes/constantes.py` → `VIDA_INICIAL` |
| **Tempo limite de resposta** | `classes/constantes.py` → `TEMPO_LIMITE_RESPOSTA` |
| **Tabela de dano** | `classes/constantes.py` → `TABELA_DANO` |
| **Número máximo de perguntas** | `classes/constantes.py` → `QUANTIDADE_MAXIMA_PERGUNTAS_POR_BATALHA` |
| **Adicionar/remover perguntas** | `dados/perguntas.json` (siga a estrutura existente) |
| **Cenários** | Substitua imagens em `assets/cenarios/` (resolução 1024×768) |
| **Sprites dos personagens** | Substitua imagens em `assets/personagens/player1/` e `player2/` |
| **Música e sons** | Substitua arquivos em `assets/sons/` (MP3 para música, WAV para efeitos) |
| **Cor dos personagens (placeholder)** | Em `classes/batalha.py`, ao criar `Personagem`, passe a cor desejada |
| **Texto da história** | `classes/historia.py` → lista `PARAGRAFOS_HISTORIA` |

---

## 🖥️ Tecnologias Utilizadas

- **Python 3** — linguagem principal
- **Pygame** — biblioteca para gráficos, áudio e eventos
- **JSON** — armazenamento das perguntas
- **Programação Orientada a Objetos** — organização do código em classes

---

## 📊 Banco de Perguntas

O arquivo `dados/perguntas.json` contém **600 perguntas** distribuídas igualmente entre **Matemática** e **Português**, com:

- **5 descritores** por matéria (ex: D01 – Números Naturais, D02 – Frações, etc.)
- **3 níveis de dificuldade**: fácil, médio, difícil
- **20 perguntas** por combinação (descritor × nível)

A estrutura é:

```json
{
  "matematica": {
    "D01": {
      "nome": "Descritor 1 - Números Naturais",
      "facil": [
        {
          "id": 1,
          "enunciado": "Qual é o resultado de 15 + 27?",
          "alternativas": ["A) 40", "B) 42", "C) 38", "D) 45"],
          "resposta": "B"
        },
        ...
      ],
      "medio": [ ... ],
      "dificil": [ ... ]
    },
    ...
  },
  "portugues": { ... }
}
```

Você pode **adicionar, editar ou remover** perguntas livremente, desde que mantenha a estrutura.

---

## 🎨 Recursos Visuais

### Personagens
- Cada jogador possui uma pasta com sprites:
  - 3 quadros de **idle** (animação contínua)
  - 1 quadro de **ataque**
  - 1 quadro de **dano**
  - 1 quadro de **erro**
- Se uma imagem não for encontrada, o jogo gera um **placeholder colorido** com o nome do estado
- Tamanho padrão dos sprites: **220×260** (pode ser ajustado em `gerenciador_animacoes.py`)

### Cenários
- Imagens de fundo em resolução **1024×768**
- O jogo sorteia aleatoriamente um cenário a cada batalha
- Se não encontrar a imagem, cria um **gradiente** com cores de fallback

### Interface
- Design moderno com **bordas arredondadas**, **sombras** e **transparências**
- **Barras de vida** com cores dinâmicas
- **Cronômetro** grande e visível
- **Mensagens flutuantes** de dano com efeito de desaparecimento

---

## 🔧 Requisitos Técnicos

- **Resolução base**: 1024×768 (escalável para qualquer tamanho de janela, com letterbox)
- **Taxa de quadros**: 60 FPS
- **Teclado**: necessário para ambos os jogadores (jogo local)
- **Áudio**: opcional (o jogo funciona sem som)

---

## 📝 Notas para Educadores

Este jogo foi criado pensando em **escolas públicas** com **acesso limitado a dispositivos eletrônicos**. Com apenas **um computador** e **um projetor** (ou TV), dois alunos podem competir simultaneamente, tornando a aula mais interativa e engajadora.

- **Modos de jogo** permitem focar em Matemática ou Português separadamente
- **Dificuldade balanceada** para diferentes níveis de aprendizado
- **Controles claros** e **tela de ajuda** (F1) facilitam o uso
- **Feedback visual e sonoro** imediato mantém os alunos motivados

---

## 🤝 Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para:

- Reportar **issues**
- Sugerir **novas funcionalidades**
- Enviar **pull requests** com melhorias

---

**Divirta-se e que vença o melhor conhecedor! 🏆**
