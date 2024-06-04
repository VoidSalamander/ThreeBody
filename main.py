from game import *
from common import *

pygame.init()
pygame.mixer.init()

part1 = stream.Part()
instru1 = instrument.Piano()
part1.insert(0, instru1)

part2 = stream.Part()
instru2 = instrument.Piano()
part2.insert(0, instru2)

part3 = stream.Part()
instru3 = instrument.Piano()
part3.insert(0, instru3)
part_list = [part1, part2, part3]

note_gen_num = [0, 0, 0]
rhythm1 = []
rhythm2 = []
rhythm3 = []

rhythms = [rhythm1, rhythm2, rhythm3]

rhythm_list = [0.25, 0.25, 0.25, 0.5, 1, 1.5, 2, 3]

for r in rhythms:
    for _ in range(random.randint(4, 6)):
        myrhythm = random.choice(rhythm_list)
        r.append(myrhythm)

note_table = [
    [60, 62, 64, 65, 67, 69, 71],
    [69, 71, 72, 74, 76, 79, 81],
    [79, 81, 83, 84, 86, 89, 91]
]

clock = pygame.time.Clock()
font = pygame.font.Font('freesansbold.ttf', 32)

def create_note(part, sound, rhythm):
    n = note.Note(sound)
    n.quarterLength = rhythm
    n.volume.velocity = 127
    part.append(n)
    pass

def play_music():
    score = stream.Score()
    score.append(part1)
    score.append(part2)
    score.append(part3)
    score.write("midi", "mymusic.mid")
    pygame.mixer.music.load('mymusic.mid')
    pygame.mixer.music.play()

mygame = game()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                mygame.GameManager = "setting"
            elif event.key == pygame.K_a:
                play_music()

    mygame.game_loop()

    if mygame.GameManager == "setting":
        if mygame.selected_body:
            index = bodies.index(mygame.selected_body)
            text = font.render(f"{note_table[index]}", True, (0, 0, 0))
            win.blit(text, (600, 550))
            text = font.render(f"{rhythms[index]}", True, (0, 0, 0))
            win.blit(text, (600, 600))


    for row in range(lock_row):
        for col in range(lock_col):
            if lock_list[row][col] == 1:
                lock_list[row][col] = 0
                rhythm_index = note_gen_num[row] % len(rhythms[row])
                create_note(part_list[row], note_table[row][col], rhythms[row][rhythm_index])
                note_gen_num[row] += 1
    
    pygame.display.update()
    clock.tick(60)

pygame.quit()



#score.show('midi')

