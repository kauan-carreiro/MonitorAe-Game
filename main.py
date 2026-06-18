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
from classes.resultado import Resultado
from classes.gerenciador_perguntas import GerenciadorPerguntas
from classes.gerenciador_cenarios import GerenciadorCenarios
from classes.gerenciador_sons import GerenciadorSons


class Jogo:
    def __init__(self):
        pygame.init()
        self.tela_cheia = False

        # Surface virtual: todo o jogo sempre desenha aqui (1024x768)
        self.surface_jogo = pygame.Surface((LARGURA_TELA, ALTURA_TELA))

        # Janela real exibida pelo SO
        self.janela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA), pygame.RESIZABLE)
        pygame.display.set_caption(TITULO_JANELA)
        self.clock = pygame.time.Clock()
        self.estado = ESTADO_TELA_INICIAL

        # Gerenciadores
        self.gerenciador_perguntas = GerenciadorPerguntas(CAMINHO_PERGUNTAS)
        self.gerenciador_cenarios = GerenciadorCenarios(PASTA_CENARIOS)
        self.gerenciador_sons = GerenciadorSons()

        # Telas — todas recebem a surface virtual, nunca a janela real
        self.tela_inicial = TelaInicial(self.surface_jogo)
        self.historia = Historia(self.surface_jogo, self.gerenciador_sons)
        self.menu = Menu(self.surface_jogo, self.gerenciador_sons)

        # Estado da batalha
        self.batalha = None
        self.modo_jogo = None
        self.resultado = None

        # Música calma de fundo, tocando desde a tela inicial (pressione uma
        # tecla), passando pela tela de história e pelo menu de seleção de
        # modo. Só para quando a batalha começa, que tem sua própria música
        # (tocar_musica_de_batalha troca a faixa automaticamente).
        self.gerenciador_sons.tocar_musica_lofi()

    def _alternar_tela_cheia(self):
        self.tela_cheia = not self.tela_cheia
        if self.tela_cheia:
            self.janela = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        else:
            self.janela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA), pygame.RESIZABLE)

    def _escalar_e_exibir(self):
        """Escala a surface virtual mantendo a proporção 4:3 (1024x768),
        centralizando na janela e preenchendo as sobras com barras pretas
        (letterboxing/pillarboxing) em vez de distorcer a imagem."""
        larg_janela, alt_janela = self.janela.get_size()

        # Maior escala que ainda cabe inteira na janela, sem cortar nada
        escala = min(larg_janela / LARGURA_TELA, alt_janela / ALTURA_TELA)
        nova_larg = round(LARGURA_TELA * escala)
        nova_alt = round(ALTURA_TELA * escala)

        # Posição para centralizar a imagem escalada na janela
        pos_x = (larg_janela - nova_larg) // 2
        pos_y = (alt_janela - nova_alt) // 2

        scaled = pygame.transform.scale(self.surface_jogo, (nova_larg, nova_alt))

        self.janela.fill((0, 0, 0))  # barras pretas nas sobras
        self.janela.blit(scaled, (pos_x, pos_y))
        pygame.display.flip()

    def executar(self):
        rodando = True
        while rodando:
            tempo_decorrido = self.clock.tick(QUADROS_POR_SEGUNDO) / 1000.0

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    rodando = False
                    break

                # ------------------- REDIMENSIONAR JANELA -------------------
                if evento.type == pygame.VIDEORESIZE and not self.tela_cheia:
                    self.janela = pygame.display.set_mode((evento.w, evento.h), pygame.RESIZABLE)

                # ------------------- TELA CHEIA (F11) -------------------
                if evento.type == pygame.KEYDOWN and evento.key == pygame.K_F11:
                    self._alternar_tela_cheia()

                # ------------------- TELA INICIAL -------------------
                if self.estado == ESTADO_TELA_INICIAL:
                    if self.tela_inicial.processar_evento(evento):
                        self.estado = ESTADO_HISTORIA
                        self.historia.reiniciar()

                # ------------------- HISTÓRIA -------------------
                elif self.estado == ESTADO_HISTORIA:
                    if self.historia.processar_evento(evento):
                        self.estado = ESTADO_MENU

                # ------------------- MENU -------------------
                elif self.estado == ESTADO_MENU:
                    escolha = self.menu.processar_evento(evento)
                    if escolha:
                        if escolha == "Sair":
                            rodando = False
                        elif escolha == "Créditos":
                            print("Tela de créditos (em breve)")
                        else:
                            modo_map = {
                                "Batalha Matemática": "matematica",
                                "Batalha Português": "portugues",
                                "Batalha Mista": "mista"
                            }
                            self.modo_jogo = modo_map.get(escolha)
                            if self.modo_jogo:
                                self.batalha = Batalha(
                                    self.surface_jogo,
                                    self.modo_jogo,
                                    self.gerenciador_perguntas,
                                    self.gerenciador_cenarios,
                                    self.gerenciador_sons
                                )
                                self.estado = ESTADO_BATALHA

                # ------------------- BATALHA -------------------
                elif self.estado == ESTADO_BATALHA:
                    if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                        self.batalha.finalizar_batalha_antecipadamente()
                    else:
                        self.batalha.processar_evento(evento)

                    if self.batalha.batalha_finalizada:
                        dados = self.batalha.obter_dados_resultado()
                        self.resultado = Resultado(self.surface_jogo, dados)
                        self.estado = ESTADO_RESULTADO

                # ------------------- RESULTADO -------------------
                elif self.estado == ESTADO_RESULTADO:
                    if self.resultado.processar_evento(evento):
                        self.estado = ESTADO_MENU
                        self.resultado = None
                        self.gerenciador_sons.tocar_musica_lofi()

                # ------------------- CRÉDITOS -------------------
                elif self.estado == ESTADO_CREDITOS:
                    pass

            # ------------------- ATUALIZAÇÃO -------------------
            if self.estado == ESTADO_TELA_INICIAL:
                self.tela_inicial.atualizar(tempo_decorrido)
            elif self.estado == ESTADO_HISTORIA:
                self.historia.atualizar(tempo_decorrido)
            elif self.estado == ESTADO_MENU:
                self.menu.atualizar(tempo_decorrido)  # mantém a seta de seleção piscando
            elif self.estado == ESTADO_BATALHA:
                self.batalha.atualizar(tempo_decorrido)

            # ------------------- DESENHO -------------------
            if self.estado == ESTADO_TELA_INICIAL:
                self.tela_inicial.desenhar()
            elif self.estado == ESTADO_HISTORIA:
                self.historia.desenhar()
            elif self.estado == ESTADO_MENU:
                self.menu.desenhar()
            elif self.estado == ESTADO_BATALHA:
                self.batalha.desenhar()
            elif self.estado == ESTADO_RESULTADO:
                self.resultado.desenhar()
            elif self.estado == ESTADO_CREDITOS:
                pass

            self._escalar_e_exibir()

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    jogo = Jogo()
    jogo.executar()