import os
import pygame

from classes.constantes import (
    ALTURA_TELA,
    COR_BRANCO,
    COR_DESTAQUE,
    COR_FUNDO_PADRAO,
    LARGURA_TELA,
    PASTA_ASSETS,
)

# Tempo (em segundos) que o texto de instrução fica visível/invisível durante
# o efeito de piscar. Quanto menor o valor, mais rápido ele pisca.
INTERVALO_PISCAR_INSTRUCAO = 0.8


class TelaInicial:
    """Exibe a tela de abertura com logo, título estilizado e instruções."""

    def __init__(self, tela: pygame.Surface) -> None:
        self.tela = tela

        # Fontes modernas (fallback para Arial)
        self.fonte_titulo = pygame.font.SysFont("segoe ui", 60, bold=True)
        self.fonte_titulo_sec = pygame.font.SysFont("segoe ui", 52, bold=True)
        self.fonte_instrucao = pygame.font.SysFont("segoe ui", 28, italic=True)

        self.cronometro_pulsar = 0.0

        # Carrega a logo (se existir)
        self.logo = self._carregar_logo()

    def _carregar_logo(self) -> pygame.Surface | None:
        """Tenta carregar a logo de assets/imagens/logo.png."""
        caminho_logo = os.path.join(PASTA_ASSETS, "imagens", "logo.png")
        if os.path.isfile(caminho_logo):
            try:
                imagem = pygame.image.load(caminho_logo).convert_alpha()
                # Redimensiona para uma largura máxima de 400px (mantendo proporção)
                largura_max = 400
                proporcao = largura_max / imagem.get_width()
                nova_largura = int(imagem.get_width() * proporcao)
                nova_altura = int(imagem.get_height() * proporcao)
                return pygame.transform.smoothscale(imagem, (nova_largura, nova_altura))
            except pygame.error:
                print("[AVISO] Não foi possível carregar a logo. Usando fallback textual.")
        return None

    def processar_evento(self, evento: pygame.event.Event) -> bool:
        """Retorna True quando o jogador deseja avançar para a próxima tela."""
        return evento.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN)

    def atualizar(self, tempo_decorrido: float) -> None:
        self.cronometro_pulsar += tempo_decorrido

    def _desenhar_fundo(self) -> None:
        """Desenha um gradiente vertical suave."""
        for y in range(ALTURA_TELA):
            fator = y / ALTURA_TELA
            cor = (
                int(COR_FUNDO_PADRAO[0] * (1 - fator * 0.3)),
                int(COR_FUNDO_PADRAO[1] * (1 - fator * 0.3)),
                int(COR_FUNDO_PADRAO[2] * (1 - fator * 0.3)),
            )
            pygame.draw.line(self.tela, cor, (0, y), (LARGURA_TELA, y))

    def _desenhar_titulo(self) -> None:
        """Renderiza o título 'MonitorAê - Game' com partes amarelas e brancas."""
        parte1 = "Monitor"
        parte2 = "Aê"
        parte3 = " - Game"

        cor_amarela = COR_DESTAQUE
        cor_branca = COR_BRANCO

        texto1 = self.fonte_titulo.render(parte1, True, cor_branca)
        texto2 = self.fonte_titulo_sec.render(parte2, True, cor_amarela)
        texto3 = self.fonte_titulo.render(parte3, True, cor_amarela)

        largura_total = texto1.get_width() + texto2.get_width() + texto3.get_width()
        pos_x = (LARGURA_TELA - largura_total) // 2
        pos_y = 70

        # Sombra
        sombra_offset = 3
        for parte, cor in [(texto1, cor_branca), (texto2, cor_amarela), (texto3, cor_amarela)]:
            sombra = parte.copy()
            sombra.fill((0, 0, 0, 80), None, pygame.BLEND_RGBA_MULT)
            self.tela.blit(sombra, (pos_x + sombra_offset, pos_y + sombra_offset))
            self.tela.blit(parte, (pos_x, pos_y))
            pos_x += parte.get_width()

    def _desenhar_logo(self) -> None:
        """Desenha a logo (se existir) ou um texto alternativo."""
        if self.logo is not None:
            # Centraliza a logo acima do título
            logo_x = (LARGURA_TELA - self.logo.get_width()) // 2
            # Posiciona um pouco acima do título (deixando espaço)
            logo_y = 120
            self.tela.blit(self.logo, (logo_x, logo_y))
        else:
            # Fallback: texto estilizado
            texto_fallback = self.fonte_titulo.render("⚔️ Batalha do Conhecimento", True, COR_DESTAQUE)
            self.tela.blit(
                texto_fallback,
                (LARGURA_TELA // 2 - texto_fallback.get_width() // 2, 100),
            )

    def _desenhar_instrucao(self) -> None:
        """Desenha a instrução com efeito de piscar."""
        texto_visivel = (self.cronometro_pulsar % (INTERVALO_PISCAR_INSTRUCAO * 2)) < INTERVALO_PISCAR_INSTRUCAO
        if texto_visivel:
            texto_instrucao = self.fonte_instrucao.render(
                "Pressione qualquer tecla para começar",
                True,
                COR_BRANCO,
            )
            posicao_instrucao = texto_instrucao.get_rect(
                center=(LARGURA_TELA // 2, ALTURA_TELA // 2 + 200)
            )
            self.tela.blit(texto_instrucao, posicao_instrucao)

    def desenhar(self) -> None:
        """Desenha a tela inicial completa."""
        self._desenhar_fundo()
        self._desenhar_logo()
        self._desenhar_titulo()
        self._desenhar_instrucao()