import random
import pygame
from PIL import Image

# Pygame başlatma
pygame.init()

# Pencere boyutları ve başlık
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Rock-Paper-Scissors Game")

# Renkler
WHITE = (255, 255, 255)

# Eylemler ve görsel/ses dosyaları
actions = ["rock", "paper", "scissors"]
images = {
    "rock": "rock_image.png",
    "paper": "paper_image.png",
    "scissors": "scissors_image.png",
    "player1": "ken.jpg",  # Player 1 için görsel
    "player2": "ryu.jpg"   # Player 2 için görsel
}

# Görselleri yükleyip hazırla
loaded_images = {}
for action in images:
    image = Image.open(images[action])
    image = image.resize((200, 200))  # Görseli yeniden boyutlandır
    loaded_images[action] = pygame.image.fromstring(image.tobytes(), image.size, image.mode).convert_alpha()

# Raunt ses dosyaları
round_sounds = {
    1: "round-1.mp3",
    2: "round-2.mp3",
    3: "round-3.mp3",
    4: "round-4.mp3",
    5: "round-5.mp3"
}

sound_effects = {
    "player1_wins": "player-1-wins.mp3",
    "player2_wins": "player-2-wins.mp3",
    "tie": "try-again.ogg",
    "game_over": "game-over.wav"
}

# Font ve oyuncu adları
font = pygame.font.Font(None, 36)
player1_name = "KEN (Player One)"
player2_name = "RYU (Player Two)"

# Skorlar ve raunt sayısı
player1_score = 0
player2_score = 0
current_round = 1

def display_image(image, pos):
    """ Görseli ekranda gösterir """
    screen.blit(image, pos)

def display_text(text, pos):
    """ Metni ekranda gösterir """
    text_surface = font.render(text, True, (0, 0, 0))
    screen.blit(text_surface, pos)

def play_sound(file_path):
    """ Sesi çalar """
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()

# Oyun döngüsü
running = True
while running:
    # Raunt sesi çal ve raunt numarasını göster
    if current_round in round_sounds:
        play_sound(round_sounds[current_round])
        screen.fill(WHITE)
        display_image(loaded_images["player1"], (100, 200))
        display_text(player1_name, (100, 180))  # Player 1 ismini görselin üstüne yaz
        display_image(loaded_images["player2"], (500, 200))
        display_text(player2_name, (500, 180))  # Player 2 ismini görselin üstüne yaz
        round_text = f"Round {current_round}"
        display_text(round_text, (width // 2 - 50, height // 2 - 100))
        pygame.display.flip()
        pygame.time.wait(2000)  # Raunt sesi bitene kadar bekle

    # Oyuncu resimlerini ve isimlerini göster
    screen.fill(WHITE)
    display_image(loaded_images["player1"], (100, 200))
    display_text(player1_name, (100, 180))  # Player 1 ismini görselin üstüne yaz
    display_image(loaded_images["player2"], (500, 200))
    display_text(player2_name, (500, 180))  # Player 2 ismini görselin üstüne yaz

    pygame.display.flip()
    pygame.time.wait(2000)  # 2 saniye bekle

    # Oyun mantığı
    player_choices = [random.choice(actions) for _ in range(2)]
    player1_choice, player2_choice = player_choices

    # Karşılaştırma ve skor güncelleme
    if player1_choice == player2_choice:
        result = "tie"
    elif (player1_choice == "rock" and player2_choice == "scissors") or \
            (player1_choice == "scissors" and player2_choice == "paper") or \
            (player1_choice == "paper" and player2_choice == "rock"):
        result = "player1_wins"
        player1_score += 1
    else:
        result = "player2_wins"
        player2_score += 1

    # Görselleri ve sesleri göster
    screen.fill(WHITE)
    display_image(loaded_images[player1_choice], (100, 200))
    display_image(loaded_images[player2_choice], (500, 200))
    play_sound(sound_effects[result])

    # Skorları ve raunt numarasını göster
    display_text(f"{player1_name}: {player1_score}", (100, 50))
    display_text(f"{player2_name}: {player2_score}", (500, 50))
    display_text(f"Round {current_round}", (width // 2 - 50, 10))

    pygame.display.flip()
    pygame.time.wait(3000)  # 3 saniye bekle

    # Raunt artırma ve kontrol
    if result != "tie":
        current_round += 1
        if current_round > 5:
            current_round = 5  # Maksimum 5 raunt

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Oyun sona erdi mi kontrol et
    if player1_score == 3 or player2_score == 3:
        play_sound(sound_effects["game_over"])
        pygame.time.wait(2000)  # "Game Over" sesi bitene kadar bekle
        winner = player1_name if player1_score > player2_score else player2_name
        screen.fill(WHITE)
        display_text(f"{winner} wins!", (width // 2 - 100, height // 2))
        pygame.display.flip()
        pygame.time.wait(3000)  # Kazananı göster ve çık
        running = False

pygame.quit()
