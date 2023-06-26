import pygame
import PySimpleGUI as sg
from tkinter import messagebox

pygame.init()
win = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Space Marker")
background_image = pygame.image.load("bg.jpg")
background_image = pygame.transform.scale(background_image, (800, 600))
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
icon = pygame.image.load("icone.png")
pygame.display.set_icon(icon)
pygame.mixer.music.load("music.mp3")
pygame.mixer.music.play(-1)
points = []
selected_point = None
text_font = pygame.font.Font(None, 20)
line_distance_text = "" 

def show_dialog():
    layout = [
        [sg.Text('Nome da Estrela')],
        [sg.Input(key='-NAME-')],
        [sg.Button('OK'), sg.Button('Cancelar')]
    ]
    window = sg.Window('Nome da Estrela', layout)

    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED or event == 'Cancelar':
            window.close()
            return None
        elif event == 'OK':
            window.close()
            return values['-NAME-']
def draw_points():
    for point, name in points:
        pygame.draw.circle(win, RED, point, 5)
        text_surface = text_font.render(name, True, BLACK)
        win.blit(text_surface, (point[0] + 10, point[1] - 10))
def draw_lines():
    for i in range(len(points) - 1):
        start_point, start_name = points[i]
        end_point, end_name = points[i + 1]
        pygame.draw.line(win, RED, start_point, end_point, 2)
        distance_x = abs(end_point[0] - start_point[0])
        distance_y = abs(end_point[1] - start_point[1])
        line_text = f"Distância: X={distance_x}, Y={distance_y}"
        text_surface = text_font.render(line_text, True, BLACK)
        mid_point = ((start_point[0] + end_point[0]) // 2, (start_point[1] + end_point[1]) // 2)
        win.blit(text_surface, (mid_point[0] + 10, mid_point[1] + 10))
def save_points():
    with open("points.txt", "w") as file:
        for point, name in points:
            file.write(f"{point[0]},{point[1]},{name}\n")
    messagebox.showinfo("Salvar Pontos", "Pontos salvos com sucesso!")
def load_points():
    global points
    try:
        with open("points.txt", "r") as file:
            points = []
            for line in file:
                x, y, name = line.strip().split(",")
                points.append(((int(x), int(y)), name))
    except FileNotFoundError:
        messagebox.showinfo("Carregar Pontos", "Nenhum ponto salvo encontrado!")
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao carregar os pontos:\n{str(e)}")
def delete_points():
    global points
    points = []

run = True
clock = pygame.time.Clock()

while run:
    clock.tick(60)  
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            run = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            star_name = show_dialog()
            if star_name:
                points.append((mouse_pos, star_name))
    win.blit(background_image, (0, 0))
    draw_points()
    draw_lines()
    pygame.display.flip()
pygame.quit()
