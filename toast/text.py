from toast.scene_graph import GameObject


class Text(GameObject):
    def __init__(self, font, message):
        """Class Constructor
        
        font:        A BitmapFont object.
        message:     A string.
        """
        super(Text, self).__init__()

        self.font = font
        self.__position = (0, 0)
        self.__time = 0
        self.visible = True
        self.__message = message

        self.char_list = []
        self.position_list = []
        
        self.__update_char_list()
        self._update_chars()

    def update(self, time=0.1667):
        super(Text, self).update(time)
        
        self.time += time

    def _update_chars(self, time=0.1667):
        left = 0
        index = 0
        for (_, rect) in self.char_list:
            rect.left = self.position[0] + self.position_list[index][0]
            rect.top = self.position[1] + self.position_list[index][1]
            left += rect.width
            index += 1

    def render(self, surface, offset=(0, 0)):
        if not self.visible:
            return
        
        for (image, rect) in self.char_list:
            surface.blit(image, rect)
       
    @property
    def message(self):
        return self.__message
    
    @message.setter     
    def message(self, message):
        self.__message = message
        self.__update_char_list()
        
    def __update_char_list(self):
        self.char_list = []
        self.position_list = []
        
        left = 0
        top = 0
        
        # Build the list of characters
        for char in self.__message:
            image = self.font.render(char)
            rect = image.get_rect()
            rect.left = left
            rect.top = top
            self.char_list.append((image, rect))
            self.position_list.append((left, top))
            left += rect.width

    def GetPosition(self):
        return self.__position

    def SetPosition(self, position):
        self.__position = position

    position = property(GetPosition, SetPosition)

    def GetTime(self):
        return self.__time

    def SetTime(self, time):
        self.__time = time

    time = property(GetTime, SetTime)
