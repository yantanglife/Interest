import telnetlib
import tkinter as tk
from time import sleep
from threading import Thread
import tkinter.messagebox as message_box


class LoginFrame(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.pack(fill="both", expand="yes")
        self.__create_widgets()

    def __create_widgets(self):
        """"""
        '''frame1: address. Left: label, Right: text.'''
        self.frame1 = tk.Frame(self)
        self.frame1_left = tk.Frame(self.frame1)
        self.frame1_right = tk.Frame(self.frame1)
        self.addr_label = tk.Label(self.frame1_left, text="Login", font=("微软雅黑", 15), width='6')
        self.addr_text = tk.Entry(self.frame1_right, font=("", 13), width='20')
        self.addr_label.pack()
        self.addr_text.pack()
        self.frame1_left.pack(side="left")
        self.frame1_right.pack(side="right")
        self.frame1.pack(side="top")
        '''frame2: name'''
        self.frame2 = tk.Frame(self)
        self.frame2_left = tk.Frame(self.frame2)
        self.frame2_right = tk.Frame(self.frame2)
        self.name_label = tk.Label(self.frame2_left, text="Name", font=("微软雅黑", 15), width='6')
        self.name_text = tk.Entry(self.frame2_right, font=("", 13), width='20')
        self.name_text.bind('<Return>', self.__enter)
        self.name_label.pack()
        self.name_text.pack()
        self.frame2_left.pack(side="left")
        self.frame2_right.pack(side="right")
        self.frame2.pack(side="top")
        '''frame3: button'''
        self.frame3 = tk.Frame(self)
        self.button = tk.Button(self.frame3, text='login', font=("", 15), width='7',
                                cursor="hand2", command=self.__login)
        self.button.pack()
        self.frame3.pack(side="top")
        ''''''
        self.addr_text.insert(0, "192.168.108.100:5005")
        self.addr_text.focus()

    def __enter(self, event):
        self.__login()

    def __login(self):
        addr = self.addr_text.get()
        name = self.name_text.get()
        print(addr, name)
        try:
            server_ip, server_port = self.addr_text.get().split(':')
            con.open(server_ip, port=int(server_port), timeout=10)
            ''' If con success, server will send bytes(b'Connect Success') '''
            response = con.read_some()
            if response != b'Connect Success':
                message_box.showerror(title="Error", message="Connect Fail!")
                return
            ''' Then we should login '''
            con.write(("login " + str(self.name_text.get()) + '\n').encode("utf-8"))
            response = con.read_some()
            ''' server's response '''
            if response == b'UserName Empty':
                message_box.showerror(title="Error", message="UserName Empty!")
            elif response == b'UserName Exist':
                message_box.showerror(title="Error", message="UserName Exist!")
            else:
                print(response)
                '''Login Success, show ChatFrame.'''
                self.destroy()
                ChatFrame()
        except Exception:
            print('error.')
            message_box.showerror(title="Error", message="Connect Fail!")


class ChatFrame(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.pack(fill="both", expand="yes")
        self.__create_widgets()
        th_receive = Thread(target=self.receive)
        th_receive.start()
        app.master.minsize(width=650, height=500)

    def __create_widgets(self):
        """"""
        '''frame1: chat_area'''
        # self.frame1 = tk.Frame(self)
        self.frame4 = tk.Frame(self)
        self.y_scrollbar = tk.Scrollbar(self.frame4)
        self.x_scrollbar = tk.Scrollbar(self.frame4, orient="horizontal")
        self.chat_area = tk.Text(self.frame4)
        # Combine scrollbar with text.
        self.y_scrollbar.config(command=self.chat_area.yview)
        self.x_scrollbar.config(command=self.chat_area.xview)
        # If wrap = 'none' in config. text would show in one line.
        self.chat_area.config(xscrollcommand=self.x_scrollbar.set, yscrollcommand=self.y_scrollbar.set,
                              font=("Times", 12), width='30', wrap="none")
        # Pack order is important.
        self.x_scrollbar.pack(side="bottom", fill="both")
        self.y_scrollbar.pack(side="right", fill="both")
        self.chat_area.pack(fill="both", expand="yes")
        self.chat_area.config(state="disabled")
        self.frame4.pack(expand="yes", fill="both", anchor="center")
        # self.frame1.pack(side="top")
        '''frame2: message area. send_BUTTON, users_BUTTON, close_BUTTON'''
        self.frame2 = tk.Frame(self)
        self.frame2_left = tk.Frame(self.frame2)
        self.frame2_right = tk.Frame(self.frame2)
        self.message = tk.Entry(self.frame2_left, font=("Times", 13), width='50')
        self.send_button = tk.Button(self.frame2_right, text='send', font=("", 10), width='7',
                                     cursor="hand2", command=self.__send)
        self.users_button = tk.Button(self.frame2_right, text='users', font=("", 10), width='7',
                                      cursor="hand2", command=self.__look_users)
        self.close_button = tk.Button(self.frame2_right, text='close', font=("", 10), width='7',
                                      cursor="hand2", command=self.__close)
        self.message.bind('<Return>', self.__enter)
        self.message.pack()
        self.frame2_left.pack(side="left")
        self.send_button.pack(side="left")
        self.users_button.pack(side="left")
        self.close_button.pack(side="left")
        self.frame2_right.pack(side="right")
        self.frame2.pack(side="top", pady=5)
        ''''''
        self.message.focus()

    def __enter(self, event):
        self.__send()

    def __send(self):
        """ Send message to server."""
        message = str(self.message.get()).strip()
        if message != '':
            con.write(('say ' + message + '\n').encode("utf-8"))
            # clear message area.
            self.message.delete(0, "end")

    def __look_users(self):
        """ look all users in the ChatRoom. """
        con.write(b'look\n')

    def __close(self):
        """ Close ChatFrame, and telnetlib.Telnet() should be closed too. """
        con.write(b'logout\n')
        con.close()
        app.master.destroy()

    def receive(self):
        """ self.receive() will be execute in a thread, it's function is receiving data from SERVER
        and then show these data in chat_area. """
        while True:
            sleep(0.6)
            try:
                # When con is closed, throw EOFError.
                result = con.read_very_eager()
                if result != b'':
                    # trans bytes to str
                    result = bytes.decode(result)
                    self.chat_area.config(state="normal")
                    self.chat_area.insert("end", "{}\n".format(result))
                    self.chat_area.config(state="disabled")
            except EOFError:
                break


if __name__ == "__main__":
    con = telnetlib.Telnet()
    app = LoginFrame()
    app.master.title("yantang")
    app.master.minsize(width=300, height=200)
    app.mainloop()
    ''' If using right-up CLOSE_BUTTON to close ChatFrame, con will still be execute. '''
    con.close()


