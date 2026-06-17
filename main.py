import sys
import pygame
from classes.constantes import (
    LARGURA_TELA, ALTURA_TELA, QUADROS_POR_SEGUNDO, TITULO_JANELA,
    ESTADO_TELA_INICIAL, ESTADO_HISTORIA, ESTADO_MENU, ESTADO_BATALHA,
    ESTADO_RESULTADO, ESTADO_CREDITOS,
    PASTA_CENARIOS, PASTA_SONS, CAMINHO_PERGUNTAS
)
from classes.tela_inicial import TelaInicial
from classes.historia import Historia
from classes.menu import Menu
from classes.batalha import Batalha
from classes.gerenciador_perguntas import GerenciadorPerguntas
from classes.gerenciador_cenarios import GerenciadorCenarios
from classes.gerenciador_sons import GerenciadorSons

class Jogo:
    def __init__(self):
        pygame.init()
        self.tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
        pygame.display.set_caption(TITULO_JANELA)
        self.clock = pygame.time.Clock()
        self.estado = ESTADO_TELA_INICIAL

        # Instancia gerenciadores (compartilhados)
        self.gerenciador_perguntas = GerenciadorPerguntas(CAMINHO_PERGUNTAS)
        self.gerenciador_cenarios = GerenciadorCenarios(PASTA_CENARIOS)
        self.gerenciador_sons = GerenciadorSons()

        # Telas iniciais
        self.tela_inicial = TelaInicial(self.tela)
        self.historia = Historia(self.tela)
        self.menu = Menu(self.tela)

        self.batalha = None
        self.modo_jogo = None

    def executar(self):
        rodando = True
        while rodando:
            tempo_decorrido = self.clock.tick(QUADROS_POR_SEGUNDO) / 1000.0

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    rodando = False
                    break

                if self.estado == ESTADO_TELA_INICIAL:
                    if self.tela_inicial.processar_evento(evento):
                        self.estado = ESTADO_HISTORIA
                        self.historia.reiniciar()

                elif self.estado == ESTADO_HISTORIA:
                    if self.historia.processar_evento(evento):
                        self.estado = ESTADO_MENU

                elif self.estado == ESTADO_MENU:
                    escolha = self.menu.processar_evento(evento)
                    if escolha:
                        if escolha == "Sair":
                            rodando = False
                        elif escolha == "Créditos":
                            # Redirecionar para tela de créditos (não implementada)
                            print("Tela de créditos (em breve)")
                        else:
                            # Mapeia opção do menu para modo de jogo
                            modo_map = {
                                "Batalha Matemática": "matematica",
                                "Batalha Português": "portugues",
                                "Batalha Mista": "mista"
                            }
                            self.modo_jogo = modo_map.get(escolha)
                            if self.modo_jogo:
                                self.batalha = Batalha(
                                    self.tela,
                                    self.modo_jogo,
                                    self.gerenciador_perguntas,
                                    self.gerenciador_cenarios,
                                    self.gerenciador_sons
                                )
                                self.estado = ESTADO_BATALHA

                elif self.estado == ESTADO_BATALHA:
                    self.batalha.processar_evento(evento)
                    if self.batalha.batalha_finalizada:
                        # Aqui você deve transicionar para a tela de resultado
                        # Por enquanto, volta ao menu
                        self.estado = ESTADO_MENU

                elif self.estado == ESTADO_RESULTADO:
                    # TODO: implementar tela de resultado
                    pass

                elif self.estado == ESTADO_CREDITOS:
                    # TODO: implementar créditos
                    pass

            # Atualização
            if self.estado == ESTADO_TELA_INICIAL:
                self.tela_inicial.atualizar(tempo_decorrido)
            elif self.estado == ESTADO_HISTORIA:
                self.historia.atualizar(tempo_decorrido)
            elif self.estado == ESTADO_BATALHA:
                self.batalha.atualizar(tempo_decorrido)

            # Desenho
            if self.estado == ESTADO_TELA_INICIAL:
                self.tela_inicial.desenhar()
            elif self.estado == ESTADO_HISTORIA:
                self.historia.desenhar()
            elif self.estado == ESTADO_MENU:
                self.menu.desenhar()
            elif self.estado == ESTADO_BATALHA:
                self.batalha.desenhar()
            elif self.estado == ESTADO_RESULTADO:
                pass  # desenhar resultado
            elif self.estado == ESTADO_CREDITOS:
                pass  # desenhar créditos

            pygame.display.flip()

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    jogo = Jogo()
    jogo.executar()