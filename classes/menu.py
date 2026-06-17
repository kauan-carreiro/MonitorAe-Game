"""
Menu principal do jogo, com navegação por teclado e seleção dos modos de batalha.
"""

from typing import List, Optional

import pygame

from classes.constantes import ALTURA_TELA, COR_BRANCO, COR_CINZA_CLARO, COR_DESTAQUE, COR_FUNDO_PADRAO, LARGURA_TELA

OPCOES_MENU: List[str] = [
    "Batalha Matemática",
    "Batalha Português",
    "Batalha Mista",
    "Sair",
]


class Menu:
    """Controla a navegação e a seleção de opções do menu principal."""

    def __init__(self, tela: pygame.Surface) -> None:
        self.tela = tela
        self.fonte_titulo = pygame.font.SysFont("arial", 46, bold=True)
        self.fonte_opcao = pygame.font.SysFont("arial", 32)
        self.fonte_ajuda = pygame.font.SysFont("arial", 18)
        self.indice_opcao_selecionada = 0

    def processar_evento(self, evento: pygame.event.Event) -> Optional[str]:
        """
        Processa a entrada do teclado. Retorna a opção escolhida (texto) quando
        o jogador confirma uma seleção com ENTER, ou None caso contrário.
        """
        if evento.type != pygame.KEYDOWN:
            return None

        if evento.key == pygame.K_DOWN:
            self.indice_opcao_selecionada = (self.indice_opcao_selecionada + 1) % len(OPCOES_MENU)
        elif evento.key == pygame.K_UP:
            self.indice_opcao_selecionada = (self.indice_opcao_selecionada - 1) % len(OPCOES_MENU)
        elif evento.key == pygame.K_RETURN:
            return OPCOES_MENU[self.indice_opcao_selecionada]

        return None

    def desenhar(self) -> None:
        self.tela.fill(COR_FUNDO_PADRAO)

        texto_titulo = self.fonte_titulo.render("BATALHA DO CONHECIMENTO", True, COR_DESTAQUE)
        self.tela.blit(texto_titulo, (LARGURA_TELA // 2 - texto_titulo.get_width() // 2, 90))

        posicao_y_inicial = 260
        espacamento_entre_opcoes = 60
        for indice, opcao in enumerate(OPCOES_MENU):
            esta_selecionada = indice == self.indice_opcao_selecionada
            cor_da_opcao = COR_DESTAQUE if esta_selecionada else COR_BRANCO
            prefixo = "»  " if esta_selecionada else "    "
            texto_renderizado = self.fonte_opcao.render(prefixo + opcao, True, cor_da_opcao)
            posicao_x = LARGURA_TELA // 2 - texto_renderizado.get_width() // 2
            self.tela.blit(texto_renderizado, (posicao_x, posicao_y_inicial + indice * espacamento_entre_opcoes))

        texto_ajuda = self.fonte_ajuda.render("Use as setas para navegar e ENTER para confirmar", True, COR_CINZA_CLARO)
        self.tela.blit(texto_ajuda, (LARGURA_TELA // 2 - texto_ajuda.get_width() // 2, ALTURA_TELA - 50))