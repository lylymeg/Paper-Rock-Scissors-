import pygame
import random
import sys

pygame.init()

# Dimensions de la fenêtre
WIDTH, HEIGHT = 600, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pierre Papier Ciseaux Arcade")
clock = pygame.time.Clock()

# Couleurs
DARK_BG = (20, 24, 33)
CARD_BG = (30, 35, 45)
CARD_HOVER = (45, 55, 75)
PLAYER_COLOR = (0, 255, 157)   # Vert néon
AI_COLOR = (255, 75, 75)       # Rouge
WHITE = (255, 255, 255)
GRAY = (150, 150, 150)

# Polices
font_large = pygame.font.SysFont("Arial", 42, bold=True)
font_medium = pygame.font.SysFont("Arial", 28, bold=True)
font_small = pygame.font.SysFont("Arial", 18)

CHOICES = ["Pierre", "Papier", "Ciseaux"]
EMOJIS = {"Pierre": "🪨", "Papier": "📄", "Ciseaux": "✂️"}

def reset_game():
    return {
        "player_score": 0,
        "ai_score": 0,
        "player_choice": None,
        "ai_choice": None,
        "round_result": "Choisis ton arme !",
        "result_color": WHITE,
        "game_over": False
    }

game = reset_game()

# Boutons cliquables pour les choix
btn_width, btn_height = 130, 60
btn_y = 350
buttons = {
    "Pierre": pygame.Rect(75, btn_y, btn_width, btn_height),
    "Papier": pygame.Rect(235, btn_y, btn_width, btn_height),
    "Ciseaux": pygame.Rect(395, btn_y, btn_width, btn_height)
}

running = True
while running:
    mouse_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if game["game_over"]:
                game = reset_game()
            else:
                for choice, rect in buttons.items():
                    if rect.collidepoint(mouse_pos):
                        # Tour du joueur
                        game["player_choice"] = choice
                        # Tour de l'IA
                        game["ai_choice"] = random.choice(CHOICES)

                        p = game["player_choice"]
                        a = game["ai_choice"]

                        # Détermination du vainqueur du round
                        if p == a:
                            game["round_result"] = "Égalité !"
                            game["result_color"] = WHITE
                        elif (p == "Pierre" and a == "Ciseaux") or \
                             (p == "Papier" and a == "Pierre") or \
                             (p == "Ciseaux" and a == "Papier"):
                            game["round_result"] = "Tu gagnes ce round !"
                            game["result_color"] = PLAYER_COLOR
                            game["player_score"] += 1
                        else:
                            game["round_result"] = "L'ordinateur gagne ce round !"
                            game["result_color"] = AI_COLOR
                            game["ai_score"] += 1

                        # Vérification de la fin de partie (Premier à 3 points)
                        if game["player_score"] == 3 or game["ai_score"] == 3:
                            game["game_over"] = True

    screen.fill(DARK_BG)

    # 1. Affichage des Scores (HUD)
    p_score_txt = font_medium.render(f"Toi : {game['player_score']}", True, PLAYER_COLOR)
    ai_score_txt = font_medium.render(f"IA : {game['ai_score']}", True, AI_COLOR)
    screen.blit(p_score_txt, (60, 30))
    screen.blit(ai_score_txt, (WIDTH - ai_score_txt.get_width() - 60, 30))

    # Ligne de séparation
    pygame.draw.line(screen, (40, 50, 70), (60, 80), (WIDTH - 60, 80), 2)

    if not game["game_over"]:
        # 2. Affichage des choix de la manche en cours
        if game["player_choice"]:
            p_txt = font_medium.render(f"Toi : {EMOJIS[game['player_choice']]} {game['player_choice']}", True, WHITE)
            a_txt = font_medium.render(f"IA : {EMOJIS[game['ai_choice']]} {game['ai_choice']}", True, WHITE)
            screen.blit(p_txt, (80, 130))
            screen.blit(a_txt, (WIDTH - a_txt.get_width() - 80, 130))

        # Résultat du round
        res_txt = font_medium.render(game["round_result"], True, game["result_color"])
        screen.blit(res_txt, (WIDTH // 2 - res_txt.get_width() // 2, 230))

        # 3. Boutons interactifs (Pierre / Papier / Ciseaux)
        for choice, rect in buttons.items():
            is_hover = rect.collidepoint(mouse_pos)
            bg_col = CARD_HOVER if is_hover else CARD_BG
            pygame.draw.rect(screen, bg_col, rect, border_radius=10)
            pygame.draw.rect(screen, PLAYER_COLOR if is_hover else (60, 70, 90), rect, 2, border_radius=10)

            label = font_small.render(f"{EMOJIS[choice]} {choice}", True, WHITE)
            screen.blit(label, (rect.centerx - label.get_width() // 2, rect.centery - label.get_height() // 2))

    else:
        # 4. Écran de Fin de Match
        if game["player_score"] == 3:
            end_title = font_large.render("VICTOIRE DU MATCH !", True, PLAYER_COLOR)
        else:
            end_title = font_large.render("L'IA REMPORTE LE MATCH !", True, AI_COLOR)

        restart_txt = font_small.render("Clique ou appuie sur ESPACE pour rejouer", True, GRAY)
        screen.blit(end_title, (WIDTH // 2 - end_title.get_width() // 2, 180))
        screen.blit(restart_txt, (WIDTH // 2 - restart_txt.get_width() // 2, 270))

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            game = reset_game()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()