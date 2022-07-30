import dearpygui.dearpygui as dpg


def DPG_Setup():
    dpg.create_context()
    dpg.create_viewport(title="Conway's Game of Life", width=1920, height=1080)
    dpg.setup_dearpygui()


class Square:
    def __init__(self, x0: int , y0: int , x1: int , y1: int , alive: bool, name: str, Neighbor_count: int) -> None:
        """int, int, int, int, Bool"""
        self.x0 = x0
        self.y0 =y0 
        self.x1=x1 
        self.y1=y1 
        self.alive=alive 
        self.name=name 
        self.Neighbor_count = Neighbor_count

    def test(self):
        print(f"X0: {self.x0}, Y0: {self.y0}, X1: {self.x1}, Y1: {self.y1}, Alive: {self.alive}, Name: {self.name}, Neighbor_count: {self.Neighbor_count}")


def Make_squares(Square_size: int, Screen_x: int, Screen_y: int):
    Square_x_count = int(Screen_x / Square_size) 
    Square_y_count = int(Screen_y / Square_size) 
    #print(Square_x_count, Square_y_count)
    Square_2d_Array = []
    for Y in range(Square_y_count):
        Square_array = []
        for X in range(Square_x_count):
            Square_object = Square((Square_size * X), (Square_size * Y) , (0 + Square_size * (X+1)), (Square_size * (Y+1)), False, (f"Square_{X}.{Y}"), None)
            Square_array.append(Square_object)
        Square_2d_Array.append(Square_array)
    return Square_2d_Array, Square_x_count, Square_y_count

def Create_window(Square_2d_Array):
    with dpg.window(tag="Primary Window"):
        with dpg.drawlist(width=1920, height=1080, id = "Canvas"):
             for Row in Square_2d_Array:
                for Square_object in Row:
                    if (Square_object.alive):
                        fill = (255,255,255,255)
                    else:
                        fill = (0,0,0,0)
                    dpg.draw_rectangle([Square_object.x0, Square_object.y0], [Square_object.x1, Square_object.y1], tag = f"{Square_object.name}", color=(255,255,255,30), fill=fill, parent="Canvas")

    with dpg.window(label="Help Window", height=150, width=400, pos=[300, 300]):
        dpg.add_text("To Toggle Draw/Delete Squares, press 'Delete' ")
        dpg.add_spacer(width=100)
        dpg.add_text("To Toggle running the Simulation, press 'Enter' ")
        dpg.add_spacer(width=100)
        dpg.add_text("To Increase the speed of the Simulation, press 'W' ")
        dpg.add_spacer(width=100)
        dpg.add_text("To Decrease the speed of the Simulation, press 'S' ")

def Run_Draw_squares(sender, appdata):
    global Square_2d_Array
    Draw_Squares(Square_2d_Array)

def Draw_Squares(Square_2d_Array):
    #issue is its getting updated to quickly
    global alive_flag
    mouse_x, mouse_y = dpg.get_drawing_mouse_pos() 
    X_array = []
    for Square in Square_2d_Array[0]:
        X_array.append(Square.x0)
    X_array.append(mouse_x)
    X_array.sort()
    X_index = X_array.index(mouse_x)
    Y_array = []
    for Square in Square_2d_Array:
        Y_array.append(Square[0].y0)
    Y_array.append(mouse_y)
    Y_array.sort()
    Y_index = Y_array.index(mouse_y)
    X_index, Y_index = X_index - 1, Y_index - 1
    if (X_index >= 0 and Y_index >= 0):
        if (Square_2d_Array[Y_index][X_index].alive == False):
            Square_2d_Array[Y_index][X_index].alive = alive_flag
        if (Square_2d_Array[Y_index][X_index].alive == True):
            Square_2d_Array[Y_index][X_index].alive = alive_flag
        
def Conway_Flag(sender, appdata):
    global interval, Conway_Flagger, alive_flag
    if dpg.is_key_pressed(13):
        interval = 0.3
        Conway_Flagger = not Conway_Flagger
    if dpg.is_key_pressed(87):
        #Conway_Flagger = "Increased"
        if (interval < 0.1):
            interval = interval - 0.01
        else:
            interval = interval - 0.1
        if (interval < 0):
            interval = 0
    if dpg.is_key_pressed(83):
        if (interval < 0.1):
            interval = interval + 0.01
        else:
            interval = interval + 0.1
    if dpg.is_key_pressed(46):
        interval = 0
        alive_flag = not alive_flag
    return 0

def Conway_Logic(Square_2d_Array, Square_x_count, Square_y_count):
    global Conway_Flagger
    #Square_2d_Array[rand.randint(0,9)][rand.randint(0, 18)].alive = rand.choice([True, False])

    #Edit the Square_2d_Array and it will be updated. 

    #Conways Rules:
    # Death < 2 
    # Lives >= 2,3
    # Death >= 3
    # Lives == 3

    if (Conway_Flagger == False):
        return None

    for Y, Row in enumerate(Square_2d_Array):
        for X, Square_object in enumerate(Row):
            Neighbour_count = 0
            if ((Y - 1 >= 0 and X - 1 >= 0)):
                if (Square_2d_Array[Y - 1][X - 1].alive): #TopLeft
                    Neighbour_count += 1
                    #print(f"topleft {Neighbour_count}")
            if  ((Y - 1 >= 0 )):
                if (Square_2d_Array[Y - 1][X    ].alive): #TopMiddle
                    Neighbour_count += 1
                    #print(f"TopMiddle {Neighbour_count}")
            if ((Y - 1 >= 0) and  (X + 1 < Square_x_count)):
                if (Square_2d_Array[Y - 1][X + 1].alive): #TopRight
                    Neighbour_count += 1
                    #print(f"TopRight {Neighbour_count}")
            if ((X - 1 > 0)):
                if (Square_2d_Array[Y    ][X - 1].alive): #MiddleLeft
                    Neighbour_count += 1
                    #print(f"MiddleLeft {Neighbour_count}")
            if ((X + 1 < Square_x_count)):
                if (Square_2d_Array[Y    ][X + 1].alive): #MiddleRight
                    Neighbour_count += 1
                    #print(f"MiddleRight {Neighbour_count}")
            if ((Y + 1 < Square_y_count)):
                if (Square_2d_Array[Y + 1  ][X - 1].alive): #BottomLeft
                    Neighbour_count += 1
                    #print(f"BottomLeft {Neighbour_count}")
            if ((Y + 1 < Square_y_count)):
                if (Square_2d_Array[Y + 1][X    ].alive): #BottomMiddle
                    Neighbour_count += 1
                    #print(f"BottomMiddle {Neighbour_count}")
            if (Y + 1 < Square_y_count and X + 1 < Square_x_count):
                if (Square_2d_Array[Y + 1][X + 1].alive): #BottomRight
                    Neighbour_count += 1
                    #print(f"BottomRight {Neighbour_count}")
            Square_object.Neighbor_count = Neighbour_count
    

    for Y, Row in enumerate(Square_2d_Array):
        for X, Square_object in enumerate(Row):
            if (Square_object.Neighbor_count < 2):
                Square_object.alive = False

            if (Square_object.Neighbor_count == 3 or Square_object.Neighbor_count == 2):
                None


            if (Square_object.Neighbor_count > 3):
                Square_object.alive = False

            if (Square_object.Neighbor_count == 3):
                Square_object.alive = True

def Render_Loop(Square_2d_Array, Square_x_count, Square_y_count):
    global interval
    dpg.show_viewport()
    dpg.set_primary_window("Primary Window", True)
    with dpg.handler_registry():
        dpg.add_mouse_down_handler(callback=Run_Draw_squares)
        dpg.add_key_press_handler(callback=Conway_Flag)
    last_second = interval = 0
    while dpg.is_dearpygui_running():
        dpg.render_dearpygui_frame()
        if dpg.get_total_time() >= last_second + interval:
            for Row in Square_2d_Array:
                for Square_object in Row:
                    if (Square_object.alive):
                        fill = (255,255,255,255)
                    else:
                        fill = (0,0,0,0)
                    dpg.configure_item(f"{Square_object.name}", fill = fill) 
            Conway_Logic(Square_2d_Array, Square_x_count, Square_y_count)
            last_second = dpg.get_total_time()
            dpg.render_dearpygui_frame()
    dpg.destroy_context()

Conway_Flagger = False
alive_flag = True
DPG_Setup()
Square_2d_Array, Square_x_count, Square_y_count  = Make_squares(50, 1920, 1080)
Create_window(Square_2d_Array)
Render_Loop(Square_2d_Array, Square_x_count, Square_y_count)


