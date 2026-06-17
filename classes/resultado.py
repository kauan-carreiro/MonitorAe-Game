import os
import pygame

from classes.constantes import (
    ALTURA_TELA,
    COR_BRANCO,
    COR_DESTAQUE,
    COR_FUNDO_PADRAO,
    COR_VERDE,
    COR_VERMELHO,
    LARGURA_TELA,
    PASTA_PERSONAGENS,
    PASTA_CENARIOS,
)
from classes.jogador import Jogador


class Resultado:
    """Tela de resultado com visual moderno, sprites dos jogadores e cenário personalizado."""

    # Tamanho dos sprites na tela de resultado
    SPRITE_LARGURA = 180
    SPRITE_ALTURA = 220

    def __init__(self, tela: pygame.Surface, dados: dict) -> None:
        self.tela = tela
        self.dados = dados
        self.vencedor: Jogador | None = dados.get("vencedor")
        self.jogador1: Jogador = dados["jogador1"]
        self.jogador2: Jogador = dados["jogador2"]
        self.tempo_total = dados.get("tempo_total_batalha", 0.0)

        # Fontes modernas (fallback para Arial)
        self.fonte_titulo = pygame.font.SysFont("segoe ui", 52, bold=True)
        self.fonte_subtitulo = pygame.font.SysFont("segoe ui", 28, bold=True)
        self.fonte_texto = pygame.font.SysFont("segoe ui", 22)
        self.fonte_instrucao = pygame.font.SysFont("segoe ui", 20, italic=True)

        # Carrega o cenário de vitória
        self.cenario = self._carregar_cenario()

        # Carrega os sprites dos jogadores (vitória ou derrota)
        self.sprite1 = self._carregar_sprite_jogador("player1", self._jogador_venceu(self.jogador1))
        self.sprite2 = self._carregar_sprite_jogador("player2", self._jogador_venceu(self.jogador2))

    def _jogador_venceu(self, jogador: Jogador) -> bool:
        """Verifica se o jogador foi o vencedor."""
        return self.vencedor is not None and self.vencedor is jogador

    def _carregar_cenario(self) -> pygame.Surface:
        """Carrega o cenário de resultado ou cria um gradiente personalizado."""
        caminho = os.path.join(PASTA_CENARIOS, "cenario_resultado.png")
        if os.path.isfile(caminho):
            try:
                imagem = pygame.image.load(caminho).convert()
                return pygame.transform.smoothscale(imagem, (LARGURA_TELA, ALTURA_TELA))
            except pygame.error:
                print("[AVISO] Falha ao carregar cenario_resultado.png, usando gradiente.")
        # Gradiente personalizado (tons de azul profundo)
        superficie = pygame.Surface((LARGURA_TELA, ALTURA_TELA))
        for y in range(ALTURA_TELA):
            fator = y / ALTURA_TELA
            cor = (
                int(20 + 30 * fator),
                int(30 + 50 * fator),
                int(60 + 40 * fator)
            )
            pygame.draw.line(superficie, cor, (0, y), (LARGURA_TELA, y))
        return superficie

    def _carregar_sprite_jogador(self, pasta: str, venceu: bool) -> pygame.Surface:
        """Carrega a imagem de vitória/derrota do jogador, com fallback para placeholder."""
        nome_arquivo = "idle_vitoria.png" if venceu else "idle_derrota.png"
        caminho = os.path.join(PASTA_PERSONAGENS, pasta, nome_arquivo)

        if os.path.isfile(caminho):
            try:
                imagem = pygame.image.load(caminho).convert_alpha()
                return pygame.transform.smoothscale(imagem, (self.SPRITE_LARGURA, self.SPRITE_ALTURA))
            except pygame.error:
                print(f"[AVISO] Falha ao carregar {caminho}, usando placeholder.")

        # Placeholder com cor (verde para vitória, vermelho para derrota)
        cor = COR_VERDE if venceu else COR_VERMELHO
        superficie = pygame.Surface((self.SPRITE_LARGURA, self.SPRITE_ALTURA), pygame.SRCALPHA)
        pygame.draw.rect(superficie, cor, superficie.get_rect(), border_radius=20)
        pygame.draw.rect(superficie, COR_BRANCO, superficie.get_rect(), width=3, border_radius=20)
        # Texto indicativo
        try:
            fonte = pygame.font.SysFont("segoe ui", 24, bold=True)
            texto = "VITÓRIA" if venceu else "DERROTA"
            texto_render = fonte.render(texto, True, COR_BRANCO)
            texto_rect = texto_render.get_rect(center=superficie.get_rect().center)
            superficie.blit(texto_render, texto_rect)
        except:
            pass
        return superficie

    def processar_evento(self, evento: pygame.event.Event) -> bool:
        """Retorna True quando o jogador deseja voltar ao menu (ESC ou ENTER)."""
        if evento.type == pygame.KEYDOWN:
            if evento.key in (pygame.K_ESCAPE, pygame.K_RETURN):
                return True
        return False

    def desenhar(self) -> None:
        # 1. Desenha o cenário
        self.tela.blit(self.cenario, (0, 0))

        # 2. Overlay escuro para destacar as informações (semitransparente)
        overlay = pygame.Surface((LARGURA_TELA, ALTURA_TELA), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 120))
        self.tela.blit(overlay, (0, 0))

        # 3. Sprites dos jogadores nos cantos inferiores
        # Player 1 (esquerda)
        x1 = 40
        y1 = ALTURA_TELA - self.SPRITE_ALTURA - 30
        self.tela.blit(self.sprite1, (x1, y1))

        # Player 2 (direita)
        x2 = LARGURA_TELA - self.SPRITE_LARGURA - 40
        y2 = ALTURA_TELA - self.SPRITE_ALTURA - 30
        self.tela.blit(self.sprite2, (x2, y2))

        # 4. Título centralizado
        if self.vencedor is None:
            titulo = "EMPATE!"
            cor_titulo = COR_DESTAQUE
        else:
            titulo = f"VENCEDOR: {self.vencedor.nome.upper()}"
            cor_titulo = COR_VERDE if self.vencedor is self.jogador1 else COR_VERMELHO

        texto_titulo = self.fonte_titulo.render(titulo, True, cor_titulo)
        sombra_titulo = self.fonte_titulo.render(titulo, True, (0, 0, 0))
        self.tela.blit(sombra_titulo, (LARGURA_TELA // 2 - texto_titulo.get_width() // 2 + 3, 43))
        self.tela.blit(texto_titulo, (LARGURA_TELA // 2 - texto_titulo.get_width() // 2, 40))

        # 5. Tempo total
        texto_tempo = self.fonte_subtitulo.render(
            f"Tempo de batalha: {self.tempo_total:.1f}s", True, COR_BRANCO
        )
        self.tela.blit(texto_tempo, (LARGURA_TELA // 2 - texto_tempo.get_width() // 2, 110))

        # 6. Estatísticas em caixas estilizadas
        self._desenhar_caixa_estatisticas(self.jogador1, 180, 180, alinhamento="esquerda")
        self._desenhar_caixa_estatisticas(self.jogador2, LARGURA_TELA - 180, 180, alinhamento="direita")

        # 7. Instrução para voltar
        instrucao = self.fonte_instrucao.render("Pressione ESC ou ENTER para voltar ao menu", True, COR_DESTAQUE)
        sombra_instrucao = self.fonte_instrucao.render("Pressione ESC ou ENTER para voltar ao menu", True, (0, 0, 0))
        self.tela.blit(sombra_instrucao, (LARGURA_TELA // 2 - instrucao.get_width() // 2 + 2, ALTURA_TELA - 48))
        self.tela.blit(instrucao, (LARGURA_TELA // 2 - instrucao.get_width() // 2, ALTURA_TELA - 50))

    def _desenhar_caixa_estatisticas(self, jogador: Jogador, centro_x: int, y: int, alinhamento: str) -> None:
        """Desenha uma caixa com as estatísticas do jogador, alinhada à esquerda ou direita."""
        largura_caixa = 300
        altura_caixa = 280
        if alinhamento == "esquerda":
            x = centro_x - largura_caixa // 2
        else:  # direita
            x = centro_x - largura_caixa // 2

        # Fundo da caixa (semitransparente com borda)
        caixa = pygame.Surface((largura_caixa, altura_caixa), pygame.SRCALPHA)
        caixa.fill((20, 20, 40, 200))
        pygame.draw.rect(caixa, COR_DESTAQUE, caixa.get_rect(), width=2, border_radius=15)
        self.tela.blit(caixa, (x, y))

        # Nome do jogador (centralizado)
        nome_render = self.fonte_subtitulo.render(jogador.nome, True, COR_DESTAQUE)
        nome_x = x + largura_caixa // 2 - nome_render.get_width() // 2
        self.tela.blit(nome_render, (nome_x, y + 15))

        # Estatísticas (alinhadas à esquerda dentro da caixa)
        estatisticas = [
            (f"Vida: {jogador.vida} / {jogador.vida_maxima}", COR_BRANCO),
            (f"Acertos: {jogador.total_acertos}", COR_VERDE),
            (f"Erros: {jogador.total_erros}", COR_VERMELHO),
            (f"Dano causado: {jogador.dano_total_causado}", COR_BRANCO),
            (f"Tempo médio: {jogador.calcular_tempo_medio():.2f}s" if jogador.calcular_tempo_medio() else "Tempo médio: --", COR_BRANCO),
            (f"Precisão: {jogador.calcular_precisao():.1f}%", COR_BRANCO),
        ]

        y_offset = 60
        for texto, cor in estatisticas:
            linha = self.fonte_texto.render(texto, True, cor)
            self.tela.blit(linha, (x + 20, y + y_offset))
            y_offset += 32