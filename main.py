import pygame
import requests




_circle_cache = {}
def _circlepoints(r):
    r = int(round(r))
    if r in _circle_cache:
        return _circle_cache[r]
    x, y, e = r, 0, 1 - r
    _circle_cache[r] = points = []
    while x >= y:
        points.append((x, y))
        y += 1
        if e < 0:
            e += 2 * y - 1
        else:
            x -= 1
            e += 2 * (y - x) - 1
    points += [(y, x) for x, y in points if x > y]
    points += [(-x, y) for x, y in points if x]
    points += [(x, -y) for x, y in points if y]
    points.sort()
    return points

def render(text, font, gfcolor=pygame.Color(0,0,0), ocolor=(255, 255, 255), opx=2):
    textsurface = font.render(text, True, gfcolor).convert_alpha()
    w = textsurface.get_width() + 2 * opx
    h = font.get_height()

    osurf = pygame.Surface((w, h + 2 * opx)).convert_alpha()
    osurf.fill((0, 0, 0, 0))

    surf = osurf.copy()

    osurf.blit(font.render(text, True, ocolor).convert_alpha(), (0, 0))

    for dx, dy in _circlepoints(opx):
        surf.blit(osurf, (dx + opx, dy + opx))

    surf.blit(textsurface, (opx, opx))
    return surf











white = (255, 255, 255)
red = (225, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 128)
black = (0, 0, 0)

#name
textx, texty = (249, 800)

#number
text1x, text1y = (83, 129)

#stats
text2x, text2y = (140, 270)

#muted
text3x, text3y = (420, 270)


# Function to fetch Pokémon data
def pokedex(num):

    url = f"https://pokeapi.co/api/v2/pokemon/{num}"
    response = requests.get(url).json()

    title = response['forms'][0]['name']
    image = response['sprites']['front_default']

    # Download the image
    r = requests.get(image, allow_redirects=True)
    file = "pokemon_image.png"
    with open(file, 'wb') as f:
        f.write(r.content)

    tall = response['height']
    mass = response['weight']

    # Convert height from decimeters to feet and inches
    def convert(dm: int):
        cm = dm * 10
        inches = cm / 2.54
        feet = inches // 12
        inches = inches % 12
        return f"{int(feet)}' {round(inches)}\""

    height_str = convert(tall)

    return title, height_str, mass, file


# Initialize Pygame and set up the window
pygame.display.set_caption('Pokedex')
pygame.mixer.init()  # Initialize the pygame mixer for audio
pygame.init()

pygame.mixer.music.load("pokemon.mp3")
pygame.mixer.music.set_volume(1)
pygame.mixer.music.play()

# Initialize number and fetch data
number = 1
name, height, weight, filename = pokedex(number)

# Set up the screen and fonts
screen = pygame.display.set_mode([498, 909])


font = pygame.font.Font('pokemon.ttf', 62)
text = font.render(name, True, black)
textRect = text.get_rect()
textRect.center = (textx, texty)

number_str = f"#{number}"
font1 = pygame.font.Font('pokemon.ttf', 50)
text1 = font1.render(number_str, True, black)
textRect1 = text1.get_rect()
textRect1.center = (text1x, text1y)

string = f"{height} | {str(int((weight / 10 * 2.205) + .5))} lbs"
font2 = pygame.font.Font('pokemon.ttf', 32)
text2 = render(string, font2, gfcolor=black, ocolor=(255, 255, 255), opx=2)
textRect2 = text2.get_rect()
textRect2.center = (text2x, text2y)

imp = pygame.image.load(filename).convert_alpha()
imp = pygame.transform.scale(imp, (500, 500))



font3 = pygame.font.Font('pokemon.ttf', 32)
text3 = font3.render("", True, black, white)
textRect3 = text3.get_rect()
textRect3.center = (text3x, text3y)

bg = pygame.image.load("images.png")
bg = pygame.transform.rotozoom(bg, 0, 3)

play = True
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_m:
                if play:
                    play = False
                    pygame.mixer.music.pause()

                    string = "muted"
                    text3 = font3.render(string, True, black,white)
                    textRect3 = text3.get_rect()
                    textRect3.center = (text3x, text3y)

                else:
                    play = True
                    pygame.mixer.music.unpause()
                    string = ""
                    text3 = font3.render(string, True, black,white)
                    textRect3 = text3.get_rect()
                    textRect3.center = (text3x, text3y)

            if event.key == pygame.K_RIGHT:
                number += 1
                if number == 152:
                    number = 1
                # increment the number correctly
                name, height, weight, filename = pokedex(number)

                # Update text and image
                text = font.render(name, True, black)
                textRect = text.get_rect()
                textRect.center = (textx,texty)

                number_str = f"#{number}"
                text1 = font1.render(number_str, True, black)
                textRect1 = text1.get_rect()
                textRect1.center = (text1x, text1y)

                string = f"{height} | {str(int((weight / 10 * 2.205) + .5))} lbs"
                text2 = render(string, font2, gfcolor=black, ocolor=(255, 255, 255), opx=2)
                textRect2 = text2.get_rect()
                textRect2.center = (text2x, text2y)

                imp = pygame.image.load(filename).convert_alpha()
                imp = pygame.transform.scale(imp, (500, 500))

            if event.key == pygame.K_LEFT:
                number -= 1  # increment the number correctly
                if number == 0:
                    number = 151
                name, height, weight, filename = pokedex(number)

                # Update text and image
                text = font.render(name, True, black)
                textRect = text.get_rect()
                textRect.center = (textx, texty)

                number_str = f"#{number}"
                text1 = font1.render(number_str, True, black)
                textRect1 = text1.get_rect()
                textRect1.center = (text1x, text1y)

                string = f"{height} | {str(int((weight / 10 * 2.205) + .5))} lbs"
                text2 = render(string, font2, gfcolor=black, ocolor=(255, 255, 255), opx=2)
                textRect2 = text2.get_rect()
                textRect2.center = (text2x, text2y)

                imp = pygame.image.load(filename).convert_alpha()
                imp = pygame.transform.scale(imp, (500, 500))



    screen.fill(white)
    screen.blit(bg, (0, 0))
    screen.blit(imp, (0, 270))
    screen.blit(text, textRect)
    screen.blit(text1, textRect1)
    screen.blit(text2, textRect2)
    screen.blit(text3, textRect3)


    pygame.display.flip()

pygame.quit()
