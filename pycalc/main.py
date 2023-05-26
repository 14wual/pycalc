# ██╗    ██╗██╗   ██╗ █████╗ ██╗     
# ██║    ██║██║   ██║██╔══██╗██║     
# ██║ █╗ ██║██║   ██║███████║██║     (code by wual)
# ██║███╗██║██║   ██║██╔══██║██║     
# ╚███╔███╔╝╚██████╔╝██║  ██║███████╗
#  ╚══╝╚══╝  ╚═════╝ ╚═╝  ╚═╝╚══════╝

# See proyect >> https://github.com/14wual/pycalc
# Follow me >> https://twitter.com/14wual

import customtkinter, webbrowser, csv, configparser, pyperclip
from PIL import Image
from tkinter import messagebox
from plyer import notification

expression=""
up=False

class events:

    def label_clicked(self):
        notification.notify(
            title='PyCalc | Calculator',
            message='Expression copied to clipboard.',
            timeout=1
        )
        global expression
        pyperclip.copy(expression)

    def setting_from_hist(self):
        self.historic_frame.grid_forget()
        events.settings(self)

    def setting_from_btns(self):
        self.buttons_frame.grid_forget()
        events.settings(self)

    def switch_event(self):

        value = self.hist_switch_var.get()

        config = configparser.ConfigParser()
        config.read('C:/Program Files/pycalc/src/config.ini')

        if value == "off":
            config.set('settings', 'history', str(False))
            messagebox.showinfo("Your history will not be saved.", "Your history will not be saved!\nRestart the program to correctly apply the new settings.")
        elif value == "on":
            config.set('settings', 'history', str(True))
            messagebox.showinfo("Your history will be saved.", "Your history will be saved!\nRestart the program to correctly apply the new settings.")


        with open('C:/Program Files/pycalc/src/config.ini', 'w') as config_file:
            config.write(config_file)

    def settings(self):

        self.textbox_visualizer.configure(text="Settings")
        global expression;expression=""

        self.settings_frame.columnconfigure(0, weight=1)
        
        config = configparser.ConfigParser()
        config.read('C:/Program Files/pycalc/src/config.ini')

        self.close_button=customtkinter.CTkButton(master=self.settings_frame, text='Close', width=15, height=15, command=lambda:events.restore(self), fg_color=self.COLOR_BG_NUMBERS, hover_color=self.COLOR_BG_OPERATORS,text_color=self.COLOR_TEXT)
        self.close_button.grid(row=0, column=0, padx=5, pady=(0,0), sticky="nsew", columnspan=4)

        if config.get('settings', 'history') == "True":self.hist_switch_var = customtkinter.StringVar(value="on")
        elif config.get('settings', 'history') == "False":self.hist_switch_var = customtkinter.StringVar(value="off")

        self.hist_switch = customtkinter.CTkSwitch(master=self.settings_frame, text="Save History", command=lambda:events.switch_event(self),
                                 variable=self.hist_switch_var, onvalue="on", offvalue="off")
        self.hist_switch.grid(row=1, column=0, padx=5, pady=5, sticky="nsew", columnspan=4)
        
        self.settings_frame.grid(row=2, column=0, padx=5, pady=5, sticky="nsew", columnspan=4)

    def restore(self):
        self.textbox_visualizer.configure(text="0")
        self.historic_frame.grid_forget()
        self.settings_frame.grid_forget()
        self.buttons_frame.grid(row=2, column=0, padx=5, pady=5, sticky="nsew", columnspan=4)

    def go_calc(self, old):
        global expression;expression=str(old)
        self.textbox_visualizer.configure(text=expression)
        self.historic_frame.grid_forget()
        self.buttons_frame.grid(row=2, column=0, padx=5, pady=5, sticky="nsew", columnspan=4)

    def hist(self):
        self.buttons_frame.grid_forget()

        self.textbox_visualizer.configure(text="Historic")
        global expression;expression=""

        self.close_button=customtkinter.CTkButton(master=self.historic_frame, text='Close', width=15, height=15, command=lambda:events.restore(self), fg_color=self.COLOR_BG_NUMBERS, hover_color=self.COLOR_BG_OPERATORS,text_color=self.COLOR_TEXT)
        self.close_button.grid(row=0, column=0, padx=5, pady=(0,0), sticky="nsew", columnspan=4)

        self.historic_frame.columnconfigure(0, weight=1)

        config = configparser.ConfigParser()
        config.read('C:/Program Files/pycalc/src/config.ini')

        if config.get('settings', 'history') == "True":

            number_rows = 9
            with open('C:/Program Files/pycalc/src/log/history.csv', "r") as file:
                lector_csv = csv.reader(file)
                rows = list(lector_csv)

            rows_without_header = rows[1:]
            last_rows = rows_without_header[-number_rows:]

            for count, row in enumerate(last_rows):
                
                self.history_expression=customtkinter.CTkLabel(master=self.historic_frame, text=row[0], text_color=self.COLOR_BG_NUMBERS, fg_color=self.COLOR_BG_TRANSPARENT)
                self.history_expression.grid(row=count+1, column=0, padx=5, pady=5, sticky="nsew", columnspan=3)

                self.go_button=customtkinter.CTkButton(master=self.historic_frame, text='calc', width=15, height=15, fg_color=self.COLOR_BG_OPERATORS, hover_color=self.COLOR_BG_NUMBERS, text_color=self.COLOR_TEXT, command=lambda act_row=row:events.go_calc(self, act_row[0]))
                self.go_button.grid(row=count+1, column=3, padx=5, pady=(5,0), sticky="nsew")

        elif config.get('settings', 'history') == "False":

            self.label_Error=customtkinter.CTkLabel(master=self.historic_frame, text="History\nNot\nActive", text_color=self.COLOR_BG_NUMBERS, fg_color=self.COLOR_BG_TRANSPARENT, font=customtkinter.CTkFont(size=40))
            self.label_Error.grid(row=1, column=0, padx=5, pady=5, sticky="nsew", columnspan=4)

            self.actuvate_history_button=customtkinter.CTkButton(master=self.historic_frame, text='Activate', width=15, height=15, command=lambda:events.setting_from_hist(self), fg_color=self.COLOR_BG_OPERATORS, hover_color=self.COLOR_BG_NUMBERS,text_color=self.COLOR_TEXT)
            self.actuvate_history_button.grid(row=2, column=0, padx=5, pady=(0,0), sticky="nsew", columnspan=4)
        
        self.historic_frame.grid(row=2, column=0, padx=5, pady=5, sticky="nsew", columnspan=4)

    def lock_window(self):pass
    def update_expression(self, value):
        global expression;
        if value in ["+", "-", "*", "/"] and expression[-1:] in ["+", "-", "*", "/"]:expression=expression[:-1]
        if not expression and value in ["+", "-", "*", "/"]:return
        expression += value
        self.textbox_visualizer.configure(text=expression)
    
    def ce(self):
        global expression;expression=""
        self.textbox_visualizer.configure(text="")
    
    def delete(self):
        global expression;expression=expression[:-1]
        self.textbox_visualizer.configure(text=expression)

    def calc(self):
        global expression
        try:
            result=str(round(eval(expression), 2))
            self.textbox_visualizer.configure(text=result)
        except:
            self.textbox_visualizer.configure(text="Sintax Err.");result="0"
        finally:
            try:
                with open('C:/Program Files/pycalc/src/log/history.csv', "a", newline="") as file:
                    escritor_csv = csv.writer(file)
                    escritor_csv.writerow([expression, result])
            except Exception as e:print("E: ", e)
            finally:expression=result

class PyCalc(customtkinter.CTk):

    def key_pressed(self, event):
        global expression
        if event.keysym in ['plus', 'minus', 'asterisk', 'slash']:
            if event.keysym == 'plus':events.update_expression(self, "+")
            elif event.keysym == 'minus':events.update_expression(self, "-")
            elif event.keysym == 'asterisk':events.update_expression(self, "*")
            elif event.keysym == 'slash':events.update_expression(self, "/")
        elif event.keysym.isdigit():events.update_expression(self, event.keysym)
        elif event.keysym == 'BackSpace':events.delete(self)
        elif event.keysym == 'Return':events.calc(self)
        else:pass
            
    def __init__(self):
        super().__init__()

        self.resizable(width=False, height=False)
        self.title("PyCalc")
        self.geometry("228x415")

        self.bind("<KeyPress>", self.key_pressed)

        # -------------------- COLORS --------------------
        self.COLOR_BG_TRANSPARENT='transparent'
        self.COLOR_BG_NUMBERS='#3D3B39'
        self.COLOR_BG_OPERATORS='#333231'
        FRAMES_1_BG='#22201E' 
        self.COLOR_TEXT='#696969'

        # -------------------- FRAMES --------------------
        self.main_frame=customtkinter.CTkFrame(master=self, fg_color=FRAMES_1_BG)
        self.visualizer_frame=customtkinter.CTkScrollableFrame(master=self.main_frame, fg_color=FRAMES_1_BG, orientation='horizontal', height=50)
        self.buttons_frame=customtkinter.CTkFrame(master=self.main_frame, fg_color=FRAMES_1_BG)
        self.historic_frame=customtkinter.CTkScrollableFrame(master=self.main_frame, fg_color=FRAMES_1_BG, height=255)
        self.settings_frame=customtkinter.CTkFrame(master=self.main_frame, fg_color=FRAMES_1_BG, height=255)

        # -------------------- IMAGES --------------------
        time_image=customtkinter.CTkImage(
            light_image=Image.open("C:/Program Files/pycalc/src/images/time-past.png"),
            dark_image=Image.open("C:/Program Files/pycalc/src/images/time-past.png"),
            size=(15, 15)
        )

        menu_image=customtkinter.CTkImage(
            light_image=Image.open("C:/Program Files/pycalc/src/images/menu-burger.png"),
            dark_image=Image.open("C:/Program Files/pycalc/src/images/menu-burger.png"),
            size=(15, 15)
        )

        heart_image=customtkinter.CTkImage(
            light_image=Image.open("C:/Program Files/pycalc/src/images/heart.png"),
            dark_image=Image.open("C:/Program Files/pycalc/src/images/heart.png"),
            size=(15, 15)
        )

        settings_image=customtkinter.CTkImage(
            light_image=Image.open("C:/Program Files/pycalc/src/images/settings-sliders.png"),
            dark_image=Image.open("C:/Program Files/pycalc/src/images/settings-sliders.png"),
            size=(15, 15)
        )

        delete_image=customtkinter.CTkImage(
            light_image=Image.open("C:/Program Files/pycalc/src/images/delete.png"),
            dark_image=Image.open("C:/Program Files/pycalc/src/images/delete.png"),
            size=(20, 20)
        )

        divide_image=customtkinter.CTkImage(
            light_image=Image.open("C:/Program Files/pycalc/src/images/divide.png"),
            dark_image=Image.open("C:/Program Files/pycalc/src/images/divide.png"),
            size=(15, 15)
        )

        cross_image=customtkinter.CTkImage(
            light_image=Image.open("C:/Program Files/pycalc/src/images/cross-small.png"),
            dark_image=Image.open("C:/Program Files/pycalc/src/images/cross-small.png"),
            size=(20, 20)
        )

        plus_image=customtkinter.CTkImage(
            light_image=Image.open("C:/Program Files/pycalc/src/images/plus-small.png"),
            dark_image=Image.open("C:/Program Files/pycalc/src/images/plus-small.png"),
            size=(20, 20)
        )

        minus_image=customtkinter.CTkImage(
            light_image=Image.open("C:/Program Files/pycalc/src/images/minus-small.png"),
            dark_image=Image.open("C:/Program Files/pycalc/src/images/minus-small.png"),
            size=(20, 20)
        )

        self.unlock_image=customtkinter.CTkImage(
            light_image=Image.open("C:/Program Files/pycalc/src/images/arrow-down-right-from-square.png"),
            dark_image=Image.open("C:/Program Files/pycalc/src/images/arrow-down-right-from-square.png"),
            size=(15, 15)
        )

        self.lock_image=customtkinter.CTkImage(
            light_image=Image.open("C:/Program Files/pycalc/src/images/arrow-up-right-from-square.png"),
            dark_image=Image.open("C:/Program Files/pycalc/src/images/arrow-up-right-from-square.png"),
            size=(15, 15)
        )

        # -------------------- OTHER BTNS --------------------
        menu_button=customtkinter.CTkButton(master=self.main_frame, text='PyCalc', image=menu_image, width=15, height=15, fg_color=self.COLOR_BG_TRANSPARENT,text_color=self.COLOR_BG_NUMBERS, hover_color=self.COLOR_BG_OPERATORS)
        menu_button.grid(row=0, column=0, padx=5, pady=(5,0), sticky="nsew", columnspan=4)

       # -------------------- VISUALIZER --------------------
        self.textbox_visualizer=customtkinter.CTkLabel(master=self.visualizer_frame, text='0', text_color=self.COLOR_BG_NUMBERS, fg_color=self.COLOR_BG_TRANSPARENT, font=customtkinter.CTkFont(size=40))
        self.textbox_visualizer.grid(row=0, column=0, padx=5, pady=5, sticky="e", columnspan=3)
        self.textbox_visualizer.bind("<Button-1>", events.label_clicked)

        # -------------------- BTN ROW 0 --------------------
        self.button_CE=customtkinter.CTkButton(master=self.buttons_frame, text='CE', width=45, height=45, fg_color=self.COLOR_BG_OPERATORS, hover_color=self.COLOR_BG_NUMBERS, command=lambda:events.ce(self), text_color=self.COLOR_TEXT)
        self.button_delete=customtkinter.CTkButton(master=self.buttons_frame, text='', image=delete_image,width=45, height=45, fg_color=self.COLOR_BG_OPERATORS, hover_color=self.COLOR_BG_NUMBERS, command=lambda:events.delete(self), text_color=self.COLOR_TEXT)
        self.button_split=customtkinter.CTkButton(master=self.buttons_frame, text='', image=divide_image, width=45, height=45, fg_color=self.COLOR_BG_OPERATORS, hover_color=self.COLOR_BG_NUMBERS,command=lambda:events.update_expression(self=self, value='/'))
        
        self.button_CE.grid(row=0, column=0, padx=5, pady=(0,5), sticky="nsew")
        self.button_delete.grid(row=0, column=1, padx=5, pady=(0,5), sticky="nsew", columnspan=2)
        self.button_split.grid(row=0, column=3, padx=5, pady=(0,5), sticky="nsew")

        # -------------------- BTN ROW 1 --------------------
        self.button_7=customtkinter.CTkButton(master=self.buttons_frame, text='7', width=45, height=45, fg_color=self.COLOR_BG_NUMBERS, hover_color=self.COLOR_BG_OPERATORS, command=lambda:events.update_expression(self=self, value='7'), text_color=self.COLOR_TEXT)
        self.button_8=customtkinter.CTkButton(master=self.buttons_frame, text='8', width=45, height=45, fg_color=self.COLOR_BG_NUMBERS, hover_color=self.COLOR_BG_OPERATORS, command=lambda:events.update_expression(self=self, value='8'), text_color=self.COLOR_TEXT)
        self.button_9=customtkinter.CTkButton(master=self.buttons_frame, text='9', width=45, height=45, fg_color=self.COLOR_BG_NUMBERS, hover_color=self.COLOR_BG_OPERATORS, command=lambda:events.update_expression(self=self, value='9'), text_color=self.COLOR_TEXT)
        self.button_plus=customtkinter.CTkButton(master=self.buttons_frame, text='', image=cross_image, width=45, height=45, fg_color=self.COLOR_BG_OPERATORS, hover_color=self.COLOR_BG_NUMBERS, command=lambda:events.update_expression(self=self, value='*'))
        
        self.button_7.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
        self.button_8.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")
        self.button_9.grid(row=1, column=2, padx=5, pady=5, sticky="nsew")
        self.button_plus.grid(row=1, column=3, padx=5, pady=5, sticky="nsew")

        # -------------------- BTN ROW 2 --------------------
        self.button_4=customtkinter.CTkButton(master=self.buttons_frame, text='4', width=45, height=45, fg_color=self.COLOR_BG_NUMBERS, hover_color=self.COLOR_BG_OPERATORS, command=lambda:events.update_expression(self=self, value='4'), text_color=self.COLOR_TEXT)
        self.button_5=customtkinter.CTkButton(master=self.buttons_frame, text='5', width=45, height=45, fg_color=self.COLOR_BG_NUMBERS, hover_color=self.COLOR_BG_OPERATORS, command=lambda:events.update_expression(self=self, value='5'), text_color=self.COLOR_TEXT)
        self.button_6=customtkinter.CTkButton(master=self.buttons_frame, text='6', width=45, height=45, fg_color=self.COLOR_BG_NUMBERS, hover_color=self.COLOR_BG_OPERATORS, command=lambda:events.update_expression(self=self, value='6'), text_color=self.COLOR_TEXT)
        self.button_minus=customtkinter.CTkButton(master=self.buttons_frame, text='', image=minus_image, width=45, height=45, fg_color=self.COLOR_BG_OPERATORS, hover_color=self.COLOR_BG_NUMBERS, command=lambda:events.update_expression(self=self, value='-'))
        
        self.button_4.grid(row=2, column=0, padx=5, pady=5, sticky="nsew")
        self.button_5.grid(row=2, column=1, padx=5, pady=5, sticky="nsew")
        self.button_6.grid(row=2, column=2, padx=5, pady=5, sticky="nsew")
        self.button_minus.grid(row=2, column=3, padx=5, pady=5, sticky="nsew")

        # -------------------- BTN ROW 3 --------------------
        self.button_1=customtkinter.CTkButton(master=self.buttons_frame, text='1', width=45, height=45, fg_color=self.COLOR_BG_NUMBERS, hover_color=self.COLOR_BG_OPERATORS, command=lambda:events.update_expression(self=self, value='1'), text_color=self.COLOR_TEXT)
        self.button_2=customtkinter.CTkButton(master=self.buttons_frame, text='2', width=45, height=45, fg_color=self.COLOR_BG_NUMBERS, hover_color=self.COLOR_BG_OPERATORS, command=lambda:events.update_expression(self=self, value='2'), text_color=self.COLOR_TEXT)
        self.button_3=customtkinter.CTkButton(master=self.buttons_frame, text='3', width=45, height=45, fg_color=self.COLOR_BG_NUMBERS, hover_color=self.COLOR_BG_OPERATORS, command=lambda:events.update_expression(self=self, value='3'), text_color=self.COLOR_TEXT)
        self.button_plus=customtkinter.CTkButton(master=self.buttons_frame, text='', image=plus_image, width=45, height=45, fg_color=self.COLOR_BG_OPERATORS, hover_color=self.COLOR_BG_NUMBERS,command=lambda:events.update_expression(self=self, value='+'))
        
        self.button_1.grid(row=3, column=0, padx=5, pady=5, sticky="nsew")
        self.button_2.grid(row=3, column=1, padx=5, pady=5, sticky="nsew")
        self.button_3.grid(row=3, column=2, padx=5, pady=5, sticky="nsew")
        self.button_plus.grid(row=3, column=3, padx=5, pady=5, sticky="nsew")

        # -------------------- BTN ROW 4 --------------------
        self.button_dot=customtkinter.CTkButton(master=self.buttons_frame, text='.', width=45, height=45, fg_color=self.COLOR_BG_OPERATORS, hover_color=self.COLOR_BG_NUMBERS, command=lambda:events.update_expression(self=self, value='.'), text_color=self.COLOR_TEXT)
        self.button_0=customtkinter.CTkButton(master=self.buttons_frame, text='0', width=45, height=45, fg_color=self.COLOR_BG_NUMBERS, hover_color=self.COLOR_BG_OPERATORS, command=lambda:events.update_expression(self=self, value='0'), text_color=self.COLOR_TEXT)
        self.button_equal=customtkinter.CTkButton(master=self.buttons_frame, text='=', width=45, height=45, command=lambda:events.calc(self=self),)
        
        self.button_dot.grid(row=4, column=0, padx=5, pady=5, sticky="nsew")
        self.button_0.grid(row=4, column=1, padx=5, pady=5, sticky="nsew")
        self.button_equal.grid(row=4, column=2, padx=5, pady=5, sticky="nsew", columnspan=2)
        
        # -------------------- FRAMES POSITIONS --------------------
        self.main_frame.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")
        self.visualizer_frame.grid(row=1, column=0, padx=5, pady=5, sticky="nsew", columnspan=4)
        self.buttons_frame.grid(row=2, column=0, padx=5, pady=5, sticky="nsew", columnspan=4)

        # -------------------- BTN ROW 5 --------------------
        self.hist_button=customtkinter.CTkButton(master=self.main_frame, text='History', image=time_image, width=15, height=15, fg_color=self.COLOR_BG_TRANSPARENT, hover_color=self.COLOR_BG_OPERATORS,text_color=self.COLOR_BG_NUMBERS, command=lambda:events.hist(self))
        self.hist_button.grid(row=3, column=0, padx=5, pady=(0,5), sticky="nsew")

        self.lock_button=customtkinter.CTkButton(master=self.main_frame, text='', image=self.lock_image, width=15, height=15, fg_color=self.COLOR_BG_TRANSPARENT,text_color=self.COLOR_BG_NUMBERS, hover_color=self.COLOR_BG_OPERATORS, command=events.lock_window(self))
        self.lock_button.grid(row=3, column=1, padx=5, pady=(0,5), sticky="nsew")

        self.settings_button=customtkinter.CTkButton(master=self.main_frame, text='', image=settings_image, width=15, height=15, fg_color=self.COLOR_BG_TRANSPARENT,text_color=self.COLOR_BG_NUMBERS, hover_color=self.COLOR_BG_OPERATORS, command=lambda:events.setting_from_btns(self))
        self.settings_button.grid(row=3, column=2, padx=5, pady=(0,5), sticky="nsew")

        support_button=customtkinter.CTkButton(master=self.main_frame, text='', image=heart_image, width=15, height=15, fg_color=self.COLOR_BG_TRANSPARENT,text_color=self.COLOR_BG_NUMBERS, hover_color=self.COLOR_BG_OPERATORS, command=lambda:webbrowser.open('https://github.com/14wual/pycalc/stargazers'))
        support_button.grid(row=3, column=3, padx=5, pady=(0,5), sticky="nsew")

    # add methods to app
    def button_click(self):
        print("button click")

class startUp:

    def __init__(self) -> None:

            app = PyCalc()
            app.mainloop()