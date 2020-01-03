import wx
from CONSTANTS import *
from sockets_wrappers import *
import json
import main_client
import main_server

username = ""
isIntro = True
isConnected = False

class Frame(wx.Frame):

    def __init__(self,data_sock : client_socket = client_socket(SERVER_IP, DATA_PORT), input_sock : client_socket = client_socket(SERVER_IP, INPUT_PORT),  info_sock : client_socket = client_socket(SERVER_IP, 1234), isCtrl = None):

        self.data_sock = data_sock
        self.input_sock = input_sock
        self.info_sock = info_sock
        self.newFrame = None
        self.isCtrl = isCtrl
        self.app = wx.App()
        wx.Frame.__init__(self, None, title= 'TeamViewer_client', size= GUI_SIZE)
        if isIntro:
            self.panel = IntroPanel(self)
        else:
            self.panel = MainPanel(self)
        self.Show()
        self.app.MainLoop()


    def _on_button_click(self, e):
        global username, isIntro
        if isIntro:
            username = self.panel.text_ptr.GetValue()
            if not username or not self.panel.isControl.GetValue() and not self.panel.isShare.GetValue():
                self.panel.error_msg()
                return
            else:
                self.isCtrl = self.panel.isControl.GetValue()
                print (self.isCtrl)
                print (username)
                msg = username  + ':' + str(self.isCtrl)
                print (msg)
                self.info_sock.send(msg)
                self.Close()
                print("closing")
                isIntro = False
                return

    def _on_room_button_click(self, e, room_number):
        self.info_sock.send(to_str(room_number))
        self.info_sock.close()
        main_client.main(self.data_sock, self.input_sock)
        self.Close()


class IntroPanel(wx.Panel):
    def __init__(self, parent: Frame):

        wx.Frame.__init__(self, parent)

        text = wx.StaticText(self, -1, "Enter Username", pos=(GUI_X / 3, GUI_Y / 5))
        font = wx.Font(13, wx.DECORATIVE, wx.ITALIC, wx.BOLD)
        text.SetFont(font)

        self.isControl = wx.CheckBox(self, label = "Control other pc", pos=(GUI_X/3, GUI_Y / 5 + 30))
        self.isShare = wx.CheckBox(self, label="Share with other pc", pos=(GUI_X / 3, GUI_Y / 5 + 60))
        self.text_ptr = wx.TextCtrl(self, pos=(GUI_X / 3, GUI_Y / 2.5), size=(GUI_X / 3, 20))

        self.Bind(wx.EVT_CHECKBOX, self._onChecked)

        button = wx.Button(self, label="Confirm", size=(GUI_X / 4, 40), pos=(GUI_X / 2.75, GUI_Y / 1.75))
        button.Bind(wx.EVT_BUTTON, parent._on_button_click)

    def _onChecked(self, e):
        cb = e.GetEventObject()
        if cb.GetLabel() == "Control other pc":
            self.isShare.SetValue(False)
        else:
            self.isControl.SetValue(False)

    def error_msg(self):
        error_text = wx.StaticText(self, -1, "Error, must fill all fields", pos= (GUI_X/3, 10))

class MainPanel(wx.Panel):

    def __init__(self, parent: Frame):

        wx.Frame.__init__(self, parent)

        print("initiating main panel")

        if parent.isCtrl is True:
            print("trying to recieve json bytes")
            json_dict = to_str(parent.info_sock.receive())
            print("trying to turn msg to dict")
            dict = json.loads(json_dict)
            self.l_buttons = []
            print(dict)

            if not dict:
                text = wx.StaticText(self, -1, "No users connected for you to control", pos=(GUI_X / 10, GUI_Y / 5))
                text2 = wx.StaticText(self, -1, "Please close and try again later", pos=(GUI_X / 10, GUI_Y / 4))
                font = wx.Font(13, wx.DECORATIVE, wx.ITALIC, wx.BOLD)
                text.SetFont(font)
                text2.SetFont(font)
                parent.info_sock.send("-1")
            else:
                print("trying to create button", dict)
                button_x = GUI_X / 6
                button_y = 20
                for key in dict:
                    button = wx.Button(self, label= "Room number: " + key + " user: " + dict[key], size=(GUI_X / 4 + 100, 40), pos=(button_x, button_y))
                    self.Bind(wx.EVT_BUTTON, lambda event: parent._on_room_button_click(event, key), button)
                    self.l_buttons.append(button)
                    if(button_y >= GUI_Y):
                        button_x = GUI_X / 6 + GUI_X / 4 + 10
                        button_y = 20
                    else:
                        button_y += 60
        else:
            print("trying to screen")
            text = wx.StaticText(self, -1, "Sharing Screen... waiting for control", pos=(GUI_X / 10, GUI_Y / 5))
            font = wx.Font(13, wx.DECORATIVE, wx.ITALIC, wx.BOLD)
            text.SetFont(font)
            parent.info_sock.close()
            main_server.main(parent.data_sock, parent.input_sock)


    def error_msg(self):
        pass


def main():
    #dataSock.send("das:False")
    frame = Frame() #TODO add dataSock and inputSock into frame
    while isIntro:
        continue
    new_frame = Frame(frame.data_sock, frame.input_sock, frame.info_sock, frame.isCtrl)

if __name__ == '__main__':
    main()
