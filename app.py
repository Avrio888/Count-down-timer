import pygame as pg
import time
pg.init()

clock = pg.time.Clock()
WIDTH = 400
HEIGHT = 400
screen = pg.display.set_mode((WIDTH, HEIGHT)) 

RectWidth = 250
RectHeight = 25

IsRunnig = True

Count = 101

def PrecentageBar(Count, RectWidth):
    return (Count/100) * RectWidth

def CenterX_Y(Screen_Width_Height, Object_Width_Height):
    return (Screen_Width_Height/2) - (Object_Width_Height/2)



#Start_Button + Font
ButtonW = 150
ButtonH = 50
ButtonStart = False
font = pg.font.Font('freesansbold.ttf', 24)
text = font.render('Start / Stop', True, (0, 0, 0))
textRect = text.get_rect(center=(CenterX_Y(WIDTH, 100)+50, CenterX_Y(HEIGHT, 50)+75))
ButtonPosition_x = 150
ButtonPosition_y = 225
Button_collor = (146, 220, 229)

def InBox(x, y, mouseX, mouseY, width, height):
    if mouseX >= x and mouseX<=x+width and mouseY>=y and mouseY<=y+height:
        return True
    return False

#def CountDown():
    
#MINUTES BUTTON SIZE
TIME_BUTTON_WIDTH = 100
TIME_BUTTON_HEIGHT = 50
font_button = pg.font.Font('freesansbold.ttf', 52)

#Minutes Button:
minutes_text = '0'
input_minutes_rect = pg.Rect(CenterX_Y(WIDTH, TIME_BUTTON_WIDTH)-75, CenterX_Y(HEIGHT, TIME_BUTTON_HEIGHT)-75, 100, 50)
MinutesAtctive = False

#Seconds Button:
seconds_text = '0'
input_seconds_rect = pg.Rect(CenterX_Y(WIDTH, TIME_BUTTON_WIDTH) + 75, CenterX_Y(HEIGHT, TIME_BUTTON_HEIGHT) - 75, 100, 50)
SecondsActive = False

def ValidInput(input_text):
    if input_text.isdigit() and int(input_text)>=0 and int(input_text)<=59:
        return True
    return False

def ConvertToSeconds(minutes, seconds):
    return int(minutes)*60 + int(seconds)
LastTimeDigit = 0
while IsRunnig:
    for event in pg.event.get():
        if event.type == pg.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            print(mouse_pos)
            if input_minutes_rect.collidepoint(mouse_pos) and not ButtonStart:
                minutes_text = ''
                MinutesAtctive = True
                SecondsActive = False
                Count =  101
            if input_seconds_rect.collidepoint(mouse_pos) and not ButtonStart:
                seconds_text = ''
                SecondsActive = True
                MinutesAtctive = False
                Count = 101
            if InBox(ButtonPosition_x, ButtonPosition_y, mouse_pos[0], mouse_pos[1], ButtonW, ButtonH) and ValidInput(minutes_text) and ValidInput(seconds_text):
                FirstTime = time.time()
                # Set the target duration in seconds (e.g., 120 seconds for 2 minutes)
                target_duration = ConvertToSeconds(minutes_text, seconds_text)
                initial_count = 100
                if target_duration != 0:
                    decrement_rate = initial_count / target_duration
                else: decrement_rate = 0
                last_time = pg.time.get_ticks()
                if ButtonStart == True:
                    ButtonStart = False
                else: ButtonStart = True
                MinutesAtctive = False
                SecondsActive = False
                Button_collor = (130, 255, 20)
                pg.draw.rect(screen, Button_collor, (CenterX_Y(WIDTH, 150), CenterX_Y(HEIGHT, 50) + 50, ButtonW, ButtonH))
                pg.display.update()
                time.sleep(0.1)
        if MinutesAtctive:
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_BACKSPACE:
                    minutes_text = minutes_text[:-1]
                else:
                    minutes_text += event.unicode
        elif SecondsActive:
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_BACKSPACE:
                    seconds_text = seconds_text[:-1]
                else:
                    seconds_text += event.unicode
        if event.type == pg.QUIT:
            IsRunnig = False
    
    if ButtonStart and ValidInput(minutes_text) and ValidInput(seconds_text):
        SecondTime = time.time()
        print(FirstTime, SecondTime, str(SecondTime - FirstTime), str(SecondTime - FirstTime)[0])   
        FirstDigit = str(SecondTime - FirstTime)[str(SecondTime - FirstTime).find('.')-1]
        
        if FirstDigit != LastTimeDigit:
            LastTimeDigit = FirstDigit
            if int(minutes_text) == 0 and int(seconds_text) == 0:
                ButtonStart = False
                minutes_text = '0'
                seconds_text = '0'
                Count = 101
                MinutesAtctive = False
                SecondsActive = False
            else:
                if int(seconds_text) == 0 and int(minutes_text) > 0:
                    minutes_text = str(int(minutes_text) - 1)
                    seconds_text = '59'
                else:
                    seconds_text = str(int(seconds_text) - 1)
                
            
        Button_collor = (146, 220, 229)
        current_time = pg.time.get_ticks()
        elapsed_time = current_time - last_time
        last_time = current_time

        Count -= decrement_rate * (elapsed_time / 1000)  # Decrease count based on elapsed time and decrement rate
        #print(elapsed_time, Count)
        if Count < 0:
            Count = 0

    PrecentageBarWidth = PrecentageBar(Count, RectWidth)
    #print(MinutesAtctive, SecondsActive, minutes_text, seconds_text)
    screen.fill((0, 0, 53))
    # Draw the progress bar
    pg.draw.rect(screen, (245, 237, 240), (CenterX_Y(WIDTH, RectWidth), CenterX_Y(HEIGHT, RectHeight) + 100, PrecentageBarWidth, RectHeight))
    # Draw the start_button
    pg.draw.rect(screen, Button_collor, (CenterX_Y(WIDTH, 100) - 25, CenterX_Y(HEIGHT, 50) + 50, ButtonW, ButtonH))
    # Draw the button's text
    screen.blit(text, textRect)
    # Draw the minutes button
    pg.draw.rect(screen, (255, 255, 255), input_minutes_rect)
    # Draw the seconds button
    pg.draw.rect(screen, (255, 255, 255), input_seconds_rect )
    # Draw the minutes text
    if minutes_text != '':
        if int(minutes_text) < 10:
            minutes_text_surface = font_button.render('0' + minutes_text, True, (0, 0, 0))
            screen.blit(minutes_text_surface, (input_minutes_rect.x + 20, input_minutes_rect.y + 2))
        else:
            minutes_text_surface = font_button.render(minutes_text, True, (0, 0, 0))
            screen.blit(minutes_text_surface, (input_minutes_rect.x + 20, input_minutes_rect.y + 2))
    # Draw the seconds text
    if seconds_text != '':
        if int(seconds_text) < 10:
            seconds_text_surface = font_button.render('0' + seconds_text, True, (0, 0, 0))
            screen.blit(seconds_text_surface, (input_seconds_rect.x + 20, input_seconds_rect.y + 2))
        else:
            seconds_text_surface = font_button.render(seconds_text, True, (0, 0, 0))
            screen.blit(seconds_text_surface, (input_seconds_rect.x + 20, input_seconds_rect.y + 2))
    pg.display.update()
    clock.tick(60)

pg.quit()