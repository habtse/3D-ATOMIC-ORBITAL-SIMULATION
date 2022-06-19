from app import App
import pygame 

firstSelection = -1

class SelectionBox():

    def __init__(self, left, top, width, height, default_color, highlight_color, font, option_list, selected = 0):
        self.rect = pygame.Rect(left, top , width, height)
        self.default_color = default_color
        self.highlight_color = highlight_color
        self.font = font
        self.option_list = option_list
        self.selected = selected
        self.draw_menu = False
        self.menu_active = False
        self.active_option = -1
    def info(self,surface):
        
        pygame.draw.rect(surface,self.default_color, self.rect)
        msg = self.font.render('well come to 3D atomic orbital simulation ', 1, (0, 0, 255))
        surface.blit(msg, msg.get_rect(center = self.rect.center))
    def info2(self,surface):
        
        pygame.draw.rect(surface,self.default_color, self.rect)
        msg = self.font.render(' Please sellect the orbital you want to simulate', 1, (0, 0, 255))
        surface.blit(msg, msg.get_rect(center = self.rect.center))
        
    def draw(self, surface):
        # thi draw function draws the menu box
        pygame.draw.rect(surface, self.highlight_color if self.menu_active else self.default_color, self.rect)
        pygame.draw.rect(surface, (0, 0, 0), self.rect,2)
        msg = self.font.render(self.option_list[self.selected], 1, (0.0,0.0,1.0))
        surface.blit(msg, msg.get_rect(center = self.rect.center))

        if self.draw_menu:
            for i, text in enumerate(self.option_list):
                rect = self.rect.copy()
                rect.top += (i+1) * self.rect.height
                pygame.draw.rect(surface,self.highlight_color if i == self.active_option else self.default_color, rect)
                msg = self.font.render(text, 1, (0, 0, 0))
                surface.blit(msg, msg.get_rect(center = rect.center))
            outer_boarder = (self.rect.left, self.rect.top + self.rect.height, self.rect.width, self.rect.height * len(self.option_list))
            pygame.draw.rect(surface, (0, 0, 0), outer_boarder, 2)
    def update(self, event_list):
        mouse_position = pygame.mouse.get_pos()
        self.menu_active = self.rect.collidepoint(mouse_position)
        
        self.active_option = -1
        for i in range(len(self.option_list)):
            rect = self.rect.copy()
            rect.y += (i+1) * self.rect.height
            if rect.collidepoint(mouse_position):
                self.active_option = i
                break

        if not self.menu_active and self.active_option == -1:
            self.draw_menu = False

        for event in event_list:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.menu_active:
                    self.draw_menu = not self.draw_menu
                elif self.draw_menu and self.active_option >= 0:
                    self.selected = self.active_option
                    self.draw_menu = False
                    print(self.active_option)
                    return self.active_option
        return -1
    def submit(self, surface):
        # create submit button
        mouse_position = pygame.mouse.get_pos()
        buttonHover =  self.rect.collidepoint(mouse_position)
        
        pygame.draw.rect(surface, self.highlight_color if buttonHover else self.default_color, self.rect)
        pygame.draw.rect(surface, (0, 0, 0), self.rect,2)
        msg = self.font.render('Simulate', 1, (0, 0, 0))
        surface.blit(msg, msg.get_rect(center = self.rect.center))
        for event in event_list:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if buttonHover:
                    app = App(firstSelection)
                    app.mainLoop()
   

pygame.init()
clock = pygame.time.Clock()
window = pygame.display.set_mode((1000, 950))
# create selection list one 
list1 = SelectionBox(
    300, 200, 160, 40, (0, 255, 255), (100, 200, 255), pygame.font.SysFont(None, 30), 
    ["S_orbital", "Px_Orbital", "Py_Orbital", "Pz_Orbital", "Dzx_Orbital", "Dz2_Orbital", "Dyz_Orbital","Dxy_Orbital", "Dx2-y2_Orbital", "F1_Orbital", "F2_Orbital", "F3_Orbital","F4_Orbital", "F5_Orbital","F6_Orbital", "F7_Orbital"])

# create submit button 
submitButton=SelectionBox(
    500,200, 160, 40, (0,255,0), (100, 200, 255), pygame.font.SysFont(None, 30), 
    ["Submit"])
#create info
comand=SelectionBox(
    40, 60, 900, 80, (255,255,255), (255, 255, 255), pygame.font.SysFont(pygame.font.get_default_font(), 40), 
    ["Submit"])
comand2=SelectionBox(
    40, 120, 900, 80, (255,255,255), (255, 255, 255), pygame.font.SysFont(pygame.font.get_default_font(), 40), 
    ["Submit"])
run = True
while run:
    clock.tick(60)
    event_list = pygame.event.get()
    for event in event_list:
        if event.type == pygame.QUIT:
            run = False
    
    selected_option1 = list1.update(event_list)
    # selected_option2 = list2.update(event_list)
    selected_option3 = submitButton.update(event_list)
    
    if selected_option1 >= 0:
        firstSelection=selected_option1
    # if selected_option2 >= 0:
    #     secondSellection= selected_option2

    window.fill((255, 255, 255))
    comand.info(window)
    comand2.info2(window)
    list1.draw(window)
    # list2.draw(window)
    submitButton.submit(window)
    pygame.display.update()
    

