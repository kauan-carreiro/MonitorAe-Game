from typing import List

import pygame

from classes.constantes import ALTURA_TELA, COR_BRANCO, COR_DESTAQUE, COR_FUNDO_PADRAO, LARGURA_TELA

# A IA expandiu a ideia original de lore fornecida na especificação do projeto.
PARAGRAFOS_HISTORIA: List[str] = [
    "Há muito tempo, em uma escola perdida entre números e palavras,",
    "dois estudantes lendários treinaram por anos para dominar",
    "a Matemática e a Língua Portuguesa.",
    "",
    "Hoje, eles se encontram no Coliseu do Saber para o confronto final.",
    "Aqui, não vence quem possui mais força física.",
    "Vence quem pensa mais rápido e responde com precisão.",
    "",
    "Cada resposta correta se transforma em energia intelectual,",
    "um golpe invisível que atinge o adversário.",
    "",
    "O vencedor será coroado o novo Guardião do Conhecimento.",
    "",
    "Que comece a Batalha do Conhecimento!",
]


class Historia:
    """Exibe o texto da história letra por letra, estilo Pokémon Fire Red."""

    VELOCIDADE_LETRA: float = 0.04   # segundos entre cada letra
    VELOCIDADE_RAPIDA: float = 0.01  # ao segurar ENTER/ESPAÇO

    def __init__(self, tela: pygame.Surface) -> None:
        self.tela = tela
        self.fonte_texto = pygame.font.SysFont("arial", 28)
        self.fonte_instrucao = pygame.font.SysFont("arial", 20)

        # Índice do parágrafo atual sendo digitado
        self.indice_paragrafo_atual: int = 0
        # Quantas letras do parágrafo atual já foram reveladas
        self.letras_reveladas: int = 0
        # Parágrafos completamente visíveis (anteriores ao atual)
        self.paragrafos_completos: int = 0

        self.cronometro: float = 0.0
        self.tudo_revelado: bool = False

        # Cursor piscante
        self.cronometro_cursor: float = 0.0
        self.cursor_visivel: bool = True

    def reiniciar(self) -> None:
        """Reinicia a revelação do texto."""
        self.indice_paragrafo_atual = 0
        self.letras_reveladas = 0
        self.paragrafos_completos = 0
        self.cronometro = 0.0
        self.tudo_revelado = False
        self.cronometro_cursor = 0.0
        self.cursor_visivel = True

    def _revelar_tudo(self) -> None:
        """Revela instantaneamente todo o texto restante."""
        self.indice_paragrafo_atual = len(PARAGRAFOS_HISTORIA) - 1
        self.letras_reveladas = len(PARAGRAFOS_HISTORIA[-1])
        self.paragrafos_completos = len(PARAGRAFOS_HISTORIA) - 1
        self.tudo_revelado = True

    def processar_evento(self, evento: pygame.event.Event) -> bool:
        """
        - Se o texto ainda está sendo digitado: ENTER/ESPAÇO/MOUSE revela tudo de uma vez.
        - Se já está tudo revelado: avança para a próxima tela.
        """
        if evento.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
            tecla_avanco = (
                evento.type == pygame.MOUSEBUTTONDOWN
                or (evento.type == pygame.KEYDOWN and evento.key in (pygame.K_SPACE, pygame.K_RETURN))
            )
            if tecla_avanco:
                if self.tudo_revelado:
                    return True  # avança para a batalha
                else:
                    self._revelar_tudo()
        return False

    def atualizar(self, tempo_decorrido: float) -> None:
        """Digita letra por letra. Vai mais rápido se ENTER/ESPAÇO estiver pressionado."""
        if self.tudo_revelado:
            # Pisca o cursor quando tudo está revelado
            self.cronometro_cursor += tempo_decorrido
            if self.cronometro_cursor >= 0.5:
                self.cronometro_cursor = 0.0
                self.cursor_visivel = not self.cursor_visivel
            return

        # Velocidade: normal ou rápida (segurando ENTER/ESPAÇO)
        teclas = pygame.key.get_pressed()
        velocidade = (
            self.VELOCIDADE_RAPIDA
            if (teclas[pygame.K_SPACE] or teclas[pygame.K_RETURN])
            else self.VELOCIDADE_LETRA
        )

        self.cronometro += tempo_decorrido
        while self.cronometro >= velocidade and not self.tudo_revelado:
            self.cronometro -= velocidade
            self._avancar_letra()

    def _avancar_letra(self) -> None:
        """Avança uma letra no parágrafo atual."""
        # Pula parágrafos vazios automaticamente
        while self.indice_paragrafo_atual < len(PARAGRAFOS_HISTORIA):
            paragrafo = PARAGRAFOS_HISTORIA[self.indice_paragrafo_atual]
            if paragrafo == "":
                # Parágrafo vazio: já está "completo", avança logo
                self.paragrafos_completos = self.indice_paragrafo_atual + 1
                self.indice_paragrafo_atual += 1
                self.letras_reveladas = 0
                continue

            if self.letras_reveladas < len(paragrafo):
                self.letras_reveladas += 1
                return
            else:
                # Parágrafo atual completo, passa para o próximo
                self.paragrafos_completos = self.indice_paragrafo_atual + 1
                self.indice_paragrafo_atual += 1
                self.letras_reveladas = 0

            break

        # Chegou no fim de tudo
        if self.indice_paragrafo_atual >= len(PARAGRAFOS_HISTORIA):
            self.tudo_revelado = True
            self.cursor_visivel = True

    def desenhar(self) -> None:
        self.tela.fill(COR_FUNDO_PADRAO)

        posicao_y = 100

        # Parágrafos completamente revelados
        for i in range(self.paragrafos_completos):
            paragrafo = PARAGRAFOS_HISTORIA[i]
            if paragrafo:
                texto_renderizado = self.fonte_texto.render(paragrafo, True, COR_BRANCO)
                posicao_x = LARGURA_TELA // 2 - texto_renderizado.get_width() // 2
                self.tela.blit(texto_renderizado, (posicao_x, posicao_y))
            posicao_y += 38

        # Parágrafo sendo digitado no momento
        if not self.tudo_revelado and self.indice_paragrafo_atual < len(PARAGRAFOS_HISTORIA):
            paragrafo_atual = PARAGRAFOS_HISTORIA[self.indice_paragrafo_atual]
            trecho_visivel = paragrafo_atual[: self.letras_reveladas]
            if trecho_visivel:
                texto_renderizado = self.fonte_texto.render(trecho_visivel, True, COR_BRANCO)
                posicao_x = LARGURA_TELA // 2 - texto_renderizado.get_width() // 2
                self.tela.blit(texto_renderizado, (posicao_x, posicao_y))

        # Instrução na parte inferior
        if self.tudo_revelado:
            msg = "Pressione ENTER para continuar"
            # Cursor piscante ao lado do texto (indica que pode avançar)
            if self.cursor_visivel:
                msg += " ▶"
        else:
            msg = "Pressione ENTER para pular"

        texto_instrucao = self.fonte_instrucao.render(msg, True, COR_DESTAQUE)
        self.tela.blit(
            texto_instrucao,
            (LARGURA_TELA // 2 - texto_instrucao.get_width() // 2, ALTURA_TELA - 60),
        )