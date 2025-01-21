import pygame
import random
import time

pygame.init()
pygame.mixer.init()

LARGHEZZA = 800
ALTEZZA = 600
DIMENSIONE_GRIGLIA = 20
FPS = 15
FONT = pygame.font.SysFont('arial', 30)
NEON_COLOR = (0, 255, 255)
BORDO_COLOR = (0, 0, 0)

SERPENTE_COLOR = (0, 255, 0)
MELA_COLOR = (255, 0, 0)

img_serpente = pygame.image.load("serpente.png")
img_serpente = pygame.transform.scale(img_serpente, (DIMENSIONE_GRIGLIA, DIMENSIONE_GRIGLIA))

img_mela = pygame.image.load("mela.png")
img_mela = pygame.transform.scale(img_mela, (DIMENSIONE_GRIGLIA, DIMENSIONE_GRIGLIA))

suono_mela = pygame.mixer.Sound("sound.mp3")
suono_death = pygame.mixer.Sound("death.mp3")
suono_start = pygame.mixer.Sound("start.mp3")

screen = pygame.display.set_mode((LARGHEZZA, ALTEZZA))
pygame.display.set_caption("Snake Game - Futuristic Edition")

def mostra_punteggio(punteggio):
    testo = FONT.render(f"Punteggio: {punteggio}", True, NEON_COLOR)
    screen.blit(testo, [LARGHEZZA // 4, 10])

def mostra_complimenti():
    testo_complimenti = FONT.render("COMPLIMENTI!", True, (0, 255, 0))
    screen.blit(testo_complimenti, [LARGHEZZA // 3, ALTEZZA // 2])
    pygame.display.update()
    time.sleep(0.5)
    screen.fill((0, 0, 0))

def reset_gioco():
    global serpente, dx, dy, mela, punteggio, fine_gioco
    serpente = [(400, 300), (380, 300), (360, 300)]
    dx, dy = DIMENSIONE_GRIGLIA, 0
    mela = (random.randint(1, (LARGHEZZA // DIMENSIONE_GRIGLIA) - 2) * DIMENSIONE_GRIGLIA,
            random.randint(1, (ALTEZZA // DIMENSIONE_GRIGLIA) - 2) * DIMENSIONE_GRIGLIA)
    punteggio = 0
    fine_gioco = False

def aggiorna_serpente():
    global serpente, dx, dy, mela, punteggio, fine_gioco
    if fine_gioco:
        return

    nuova_testa = (serpente[0][0] + dx, serpente[0][1] + dy)

    if nuova_testa in serpente or nuova_testa[0] < 0 or nuova_testa[1] < 0 or nuova_testa[0] >= LARGHEZZA or nuova_testa[1] >= ALTEZZA:
        fine_gioco = True
        suono_death.play()
        return

    serpente.insert(0, nuova_testa)

    if nuova_testa == mela:
        mela = (random.randint(1, (LARGHEZZA // DIMENSIONE_GRIGLIA) - 2) * DIMENSIONE_GRIGLIA,
                random.randint(1, (ALTEZZA // DIMENSIONE_GRIGLIA) - 2) * DIMENSIONE_GRIGLIA)
        punteggio += 1
        suono_mela.play()
        if punteggio == 10:
            mostra_complimenti()
    else:
        serpente.pop()

def draw_game():
    screen.fill((0, 0, 0))

    for segmento in serpente:
        screen.blit(img_serpente, (segmento[0], segmento[1]))

    screen.blit(img_mela, (mela[0], mela[1]))

    pygame.draw.rect(screen, BORDO_COLOR, (0, 0, LARGHEZZA, ALTEZZA), 5)

    mostra_punteggio(punteggio)

    if in_paused:
        testo_pausa = FONT.render("SEI IN PAUSA - Premi di nuovo Invio per continuare", True, (255, 255, 0))
        screen.blit(testo_pausa, [LARGHEZZA // 6, ALTEZZA // 2])

    if not fine_gioco:
        testo_pausa_legenda = FONT.render("PAUSA - Invio", True, (255, 255, 0))
        screen.blit(testo_pausa_legenda, [LARGHEZZA - 200, 10])

    pygame.display.update()

def key_press(event):
    global dx, dy
    if event.key == pygame.K_w and dy == 0:
        dx, dy = 0, -DIMENSIONE_GRIGLIA
    elif event.key == pygame.K_s and dy == 0:
        dx, dy = 0, DIMENSIONE_GRIGLIA
    elif event.key == pygame.K_a and dx == 0:
        dx, dy = -DIMENSIONE_GRIGLIA, 0
    elif event.key == pygame.K_d and dx == 0:
        dx, dy = DIMENSIONE_GRIGLIA, 0
    elif event.key == pygame.K_q:
        pygame.quit()
        quit()

def inizio_gioco():
    global fine_gioco
    suono_start.play()
    reset_gioco()
    fine_gioco = False

def main():
    global fine_gioco, in_paused, serpente, dx, dy, mela, punteggio
    fine_gioco = True
    in_paused = False

    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p and fine_gioco:
                    inizio_gioco()
                elif event.key == pygame.K_RETURN and not fine_gioco:
                    in_paused = not in_paused  # Toggle dello stato di pausa
                elif not fine_gioco and not in_paused:
                    key_press(event)

        if fine_gioco:
            screen.fill((0, 0, 0))
            testo_inizio = FONT.render("Premi 'P' per iniziare", True, NEON_COLOR)
            screen.blit(testo_inizio, [LARGHEZZA // 3, ALTEZZA // 4])
            pygame.display.update()
        else:
            if not in_paused:
                aggiorna_serpente()
            draw_game()

        clock.tick(FPS)

if __name__ == "__main__":
    main()