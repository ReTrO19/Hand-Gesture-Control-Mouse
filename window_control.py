import pyautogui
import win32api, win32con

class Mouse_Control:
    """ Mouse_Control Class has to parameter
    x_coord : x co-ordinate of the tip of the selected finger
    y_coord : y co-ordinate of the tip of the other finger selected
    """
    def __init__(self,x,y):
        self.x_coord = x * 2
        self.y_coord = y * 2
    """ Move the mouse to the provided x and y co-orinate of the screen """
    def mouse_move(self):
        # pyautogui.moveTo(self.x_coord, self.y_coord)
        win32api.SetCursorPos((self.x_coord, self.y_coord))
    """ Click the mouse to the provided x and y co-orinate on the screen """
    def mouse_click(self):
        # pyautogui.click(self.x_coord, self.y_coord)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, self.x_coord, self.y_coord, 0, 0)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, self.x_coord, self.y_coord, 0, 0)