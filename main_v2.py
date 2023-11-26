import tkinter
import tkinter.messagebox
import customtkinter as ctk
import pandas as pd
import datetime as dt
import tkinter as tk
from PIL import Image, ImageTk, ImageDraw

ctk.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

def conversao_tempo_str(tempo_segundos):
    if tempo_segundos < 60:
        return f"{int(tempo_segundos)}''"
    else:
        return f"{int(tempo_segundos//60)}'"


class Driver:
    def __init__(self, name, phone, company, hour=None, status=None, dock=None):
        self.name = name
        self.phone = phone
        self.company = company
        self.status = 0  # 0 - standby, 1 - allocated, 2 - finished
        self.hour = hour  
        self.status = status
        self.dock = dock  

class Dock:
    def __init__(self, dock_number):
        self.dock_number = dock_number
        self.is_available = True

    def change_availability(self, IsAvailable):
        self.is_available = IsAvailable

class Drivers:
    def __init__(self):
        self.driver_list = []

    def add_driver(self, driver):
        self.driver_list.append(driver)

    def remove_driver(self, driver):
        self.driver_list.remove(driver)

    def display_drivers(self,status):
        lista_final = []
        for it in self.driver_list:
            if it.status == status:
                lista_final.append(it)
        return lista_final
    
    def change_driver_dock(self,name_driver,new_status,new_dock):
        for it in self.driver_list:
            if it.name == name_driver:
                it.status = new_status
                it.dock = new_dock
    
    def display_all(self):
        for it in self.driver_list:
            print(it.name)
            print(it.phone)
            print(it.company)
            print(it.hour)
            print(it.status)
            print(it.dock)

    
class Docks:
    def __init__(self):
        self.dock_list = []

    def add_dock(self, dock):
        self.dock_list.append(dock)

    def remove_dock(self, dock):
        self.dock_list.remove(dock)

    def display_docks(self,IsAvailable):
        lista_final = []
        for it in self.dock_list:
            if it.is_available == IsAvailable:
                lista_final.append(str(it.dock_number))
        return lista_final
    
    def change_availability(self,dock,IsAvailable):
        for it in self.dock_list:
            if it.dock_number == dock:
                it.change_availability(IsAvailable)

    def list_ocupied_docks(self):
        lista_final = []
        for it in self.dock_list:
            if it.is_available == False:
                lista_final.append(it.dock_number)
        return lista_final


class AppGUI(ctk.CTk):
   
    def __init__(self, app_instance):
        super().__init__()

        self.app = app_instance
        self.title("Gestão de cais JM")
        self.geometry(f"{1100}x{580}")

        self.grid_columnconfigure((1,2,3), weight=0)

        self.grid_columnconfigure(0, weight=0)  # Set weight to 0 for fixed width
        self.grid_columnconfigure(1, weight=0)  # Set weight to 1 for dynamic width

        self.grid_rowconfigure(0, weight=1)
        
        self.sidebar_frame = ctk.CTkFrame(self, width=100, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        titulo_c1 = "Ações"
        nome_botao1 = "Nova entrada"
        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text=titulo_c1,font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.sidebar_button_1 = ctk.CTkButton(self.sidebar_frame,text=nome_botao1,command=self.display_popup_insercao_driver)
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)
        self.sms_var = ctk.StringVar(value="on")
        self.checkbox = ctk.CTkCheckBox(self.sidebar_frame, text="Envio SMS",
                                     variable=self.sms_var, onvalue="on", offvalue="off")
        
        self.checkbox.grid(row=7,column=0,padx=20,pady=(20, 20),sticky='w')
        """
        self.appearance_mode_label = ctk.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.scaling_label = ctk.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = ctk.CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"],
                                                                command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 20))"""

        self.update_gui()
        self.update_waiting_times()

    def update_tables(self):
        self.display_standby_drivers()
        self.display_allocated_drivers()

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        ctk.set_widget_scaling(new_scaling_float)  
    
    def display_standby_drivers(self):
        self.coluna_2_estrutura = ctk.CTkFrame(self, width=250)
        self.coluna_2_estrutura.grid(row=0, column=1, padx=(30, 0), pady=(20, 0), sticky="nsew")

        self.title_label = ctk.CTkLabel(self.coluna_2_estrutura, text="Motoristas em espera", font=ctk.CTkFont(size=25, weight="bold"))
        self.title_label.grid(row=0, column=0, padx=(10, 10), pady=(0, 18), sticky="n")
        
        dados_motoristas = self.app.drivers.display_drivers(0)
        self.tempo_widgets = []  # List to store tempo widgets
        k = 1
        for i_LIST in dados_motoristas:
            # Create a subframe
            subframe = ctk.CTkFrame(self.coluna_2_estrutura)
            subframe.grid(row=k, column=0, padx=(10, 10), pady=(0, 10), sticky="nsew")

            subframe.grid_columnconfigure(0, weight=1)
            subframe.grid_columnconfigure(1, weight=1)

            # COLUNA 1
            self.nome_widget_motorista = ctk.CTkLabel(subframe, text=f"{i_LIST.name}")
            self.nome_widget_motorista.grid(row=0, column=0, padx=(10, 0), pady=(10, 5), sticky="w")

            self.telefone_widget_motorista = ctk.CTkLabel(subframe, text=f"{i_LIST.phone}")
            self.telefone_widget_motorista.grid(row=1, column=0, padx=(10, 0), pady=(0, 5), sticky="w")

            self.empresa_widget_motorista = ctk.CTkLabel(subframe, text=f"{i_LIST.company}")
            self.empresa_widget_motorista.grid(row=2, column=0, padx=(10, 0), pady=(0, 5), sticky="w")

            # COLUNA 2
            tempo_espera = (dt.datetime.now()-i_LIST.hour).total_seconds()
            tempo_widget_motorista = ctk.CTkLabel(subframe, text=f"{tempo_espera} Min", font=ctk.CTkFont(size=20, weight="bold"))
            tempo_widget_motorista.grid(row=0, column=1, padx=(10, 15), pady=(10, 0), sticky="E")
            self.tempo_widgets.append(tempo_widget_motorista)  # Add tempo widget to the list

            self.botao = ctk.CTkButton(master=subframe, text=f"Atribuir cais", width=100,
                                    command=lambda name=i_LIST.name: self.display_popup_alocacao_cais(name))
            self.botao.grid(row=2, column=1, padx=(10, 15), pady=(0, 15), sticky="E")
            k += 1
        self.update_waiting_times()
        
    def update_waiting_times(self):
        dados_motoristas = self.app.drivers.display_drivers(0)

        # Update waiting time for each driver
        for i, i_LIST in enumerate(dados_motoristas):
            tempo_espera = (dt.datetime.now() - i_LIST.hour).total_seconds()
            str_tempo_espera = conversao_tempo_str(tempo_espera)
            #self.tempo_widgets[i].configure(text="{} Min".format(int(tempo_espera)))
            self.tempo_widgets[i].configure(text=str_tempo_espera)

    # Schedule the function to be called again after a short interval (e.g., 1000 milliseconds)
        self.after(1000, self.update_waiting_times)

    def display_popup_insercao_driver(self): 

        self.popup_window = ctk.CTkToplevel() 
        self.popup_window.geometry("400x300")
        self.popup_window.title("Registo de camionista")
        ctk.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
        ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"
        self.popup_window.attributes('-topmost', 'true')

        self.popup_window.grid_columnconfigure(0, weight=1)  # Set weight to 1 for dynamic width

        self.popup_window.grid_rowconfigure(7, weight=1)
         # Create and pack widgets for name, phone number, and company
        self.name_label = ctk.CTkLabel(self.popup_window, text="Nome")
        self.name_entry = ctk.CTkEntry(self.popup_window,width=300)

        self.name_label.grid(row=0,column=0,pady=(10,3))
        self.name_entry.grid(row=1,column=0,pady=(0,6))
    
        self.phone_label = ctk.CTkLabel(self.popup_window, text="Contacto telefónico")
        self.phone_entry = ctk.CTkEntry(self.popup_window, width=300)

        self.phone_label.grid(row=2,column=0,pady=(10,3))
        self.phone_entry.grid(row=3,column=0,pady=(0,6))

        self.company_label = ctk.CTkLabel(self.popup_window, text="Empresa")
        self.company_entry = ctk.CTkEntry(self.popup_window, width=300)

        self.company_label.grid(row=4,column=0,pady=(10,3))
        self.company_entry.grid(row=5,column=0,pady=(0,6))

        self.submit_button = ctk.CTkButton(self.popup_window, width=300,text="Inserir",command=self.submit_info)
        self.submit_button.grid(row=6,column=0,pady=20)

        self.popup_window.grab_set()

        self.popup_window.wait_window()

    def display_popup_alocacao_cais(self,nome):
        self.popup_cais = ctk.CTkToplevel() 
        self.popup_cais.geometry("400x150")
        self.popup_cais.title("Atribuicao Cais")
        ctk.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
        ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"
        self.popup_cais.attributes('-topmost', 'true')
        
        self.popup_cais.grid_columnconfigure(0, weight=1)  # Set weight to 1 for dynamic width
        self.popup_cais.grid_rowconfigure(2, weight=1)

        self.legenda_cais = ctk.CTkLabel(self.popup_cais, text="Cais a atribuir")
        list_cais_disp = self.app.docks.display_docks(True)
        self.combo_cais = ctk.CTkComboBox(self.popup_cais, values=list_cais_disp, width=300)

        self.legenda_cais.grid(row=0,column=0,pady=(10,3))
        self.combo_cais.grid(row=1,column=0,pady=(0,6))

        self.submit_button = ctk.CTkButton(self.popup_cais, width=300,text="Alocar cais",command=lambda: self.submit_dock(nome))
        self.submit_button.grid(row=2,column=0,pady=20)

    def submit_dock(self,nome):
        num_cais = int(self.combo_cais.get())
        self.app.drivers.change_driver_dock(nome,1,num_cais)
        self.app.docks.change_availability(num_cais,False)
        print(self.app.drivers.display_all())
        print(self.app.docks.display_docks(False))
        self.update_gui()
        self.popup_cais.destroy()

    def submit_info(self):
        nome = self.name_entry.get()
        telefone = self.phone_entry.get()
        empresa = self.company_entry.get()
        hora = dt.datetime.now()

        new_driver = Driver(nome,telefone,empresa,hora,0)
        self.app.introduce_driver(new_driver)
        

        self.display_standby_drivers()
        self.popup_window.destroy()
        

    def display_allocated_drivers(self):

        self.coluna_3_estrutura = ctk.CTkFrame(self, width=250)
        self.coluna_3_estrutura.grid(row=0, column=2, padx=(30, 0), pady=(20, 0), sticky="nsew")

        self.title_label = ctk.CTkLabel(self.coluna_3_estrutura, text="Motoristas em carga", font=ctk.CTkFont(size=25, weight="bold"))
        self.title_label.grid(row=0, column=0, padx=(10, 10), pady=(0, 18), sticky="n")
        
        dados_motoristas = self.app.drivers.display_drivers(1)
        k = 1
        for i_LIST in dados_motoristas:
            # Create a subframe
            subframe = ctk.CTkFrame(self.coluna_3_estrutura)
            subframe.grid(row=k, column=0, padx=(10, 10), pady=(0, 10), sticky="nsew")
            subframe.columnconfigure([0,1],weight=1)

            #COLUNA1
            self.nome_widget_motorista = ctk.CTkLabel(subframe, text=f"{i_LIST.name}")
            self.nome_widget_motorista.grid(row=0, column=0, padx=(10, 0), pady=(10, 5), sticky="w")

            self.telefone_widget_motorista = ctk.CTkLabel(subframe, text=f"{i_LIST.phone}")
            self.telefone_widget_motorista.grid(row=1, column=0, padx=(10, 0), pady=(0, 5), sticky="w")

            self.empresa_widget_motorista = ctk.CTkLabel(subframe, text=f"{i_LIST.company}")
            self.empresa_widget_motorista.grid(row=2, column=0, padx=(10, 0), pady=(0, 5), sticky="w")
            tempo_espera = int((dt.datetime.now()-i_LIST.hour).total_seconds() // 60)

            #COLUNA2
            self.tempo_widget_motorista = ctk.CTkLabel(subframe, text=f"{tempo_espera} Min", font=ctk.CTkFont(size=20, weight="bold"))
            self.tempo_widget_motorista.grid(row=0, column=1, padx=(10, 10), pady=(10, 5), sticky="e")

            cais = i_LIST.dock
            self.cais_widget_motorista = ctk.CTkLabel(subframe, text=f"Cais {cais}", font=ctk.CTkFont(size=18, weight="bold"))
            self.cais_widget_motorista.grid(row=1, column=1, padx=(10, 10), pady=(0, 0), sticky="e")

            

            self.botao = ctk.CTkButton(master=subframe, text=f"Remover motorista", width=100)
                                      # command= lambda: self.display_popup_alocacao_cais(i_LIST.name))
            self.botao.grid(row=2, column=1, padx=(10, 10), pady=(0, 15), sticky="e")
            k += 1

    def display_docks(self):
        self.c4est_imagme = ctk.CTkFrame(self, width=250)
        self.c4est_imagme.grid(row=0, column=3, padx=(20, 0), pady=(20, 0), sticky="ne")
        self.c4est_imagme.grid_columnconfigure(3, weight=1)

        # Label for the title
        self.title_label = ctk.CTkLabel(self.c4est_imagme, text="Ocupação", font=ctk.CTkFont(size=25, weight="bold"))
        self.title_label.grid(row=0, column=0, padx=(10, 90), pady=(0, 10), sticky="n")

        # Load the image
        image_path = "docks_image.png"
        original_image = Image.open(image_path)
        resized_image = original_image.resize((250, 500), Image.ANTIALIAS)
        self.tk_image = ImageTk.PhotoImage(resized_image)
        #self.tk_image = ImageTk.PhotoImage(original_image)

        # Create a Canvas widget for drawing on top of the image
        self.canvas = tk.Canvas(self.c4est_imagme, bg="white", width=250, height=500)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_image)
        self.canvas.grid(row=2, column=0, sticky="nw")

        #Tirar lista de cais ocupados para desenhar locais a ocupar
        ocupados = self.app.docks.list_ocupied_docks()

        for j in ocupados:
            # Draw a red rectangle
            trapeze_coords = [147, 35, 
                            176, 52,  
                            70, 115, 
                            70, 81]
            

            modified_list = [num + 44.5*(j-1) if i % 2 != 0 else num for i, num in enumerate(trapeze_coords)]
        
            self.canvas.create_polygon(modified_list, outline="red", width=2, fill="red")
    
    def update_gui(self):
        self.display_standby_drivers()
        self.display_allocated_drivers()
        self.display_docks()


class App:
    def __init__(self):
        dock1 = Dock(1)
        dock2 = Dock(2)
        dock3 = Dock(3)
        dock4 = Dock(4)
        dock5 = Dock(5)
        dock6 = Dock(6)
        dock7 = Dock(7)
        dock8 = Dock(8)
        dock9 = Dock(9)

        docksf = Docks()
        docksf.add_dock(dock1)
        docksf.add_dock(dock2)
        docksf.add_dock(dock3)
        docksf.add_dock(dock4)
        docksf.add_dock(dock5)
        docksf.add_dock(dock6)
        docksf.add_dock(dock7)
        docksf.add_dock(dock8)
        docksf.add_dock(dock9)
        
        self.docks = docksf
               
        self.drivers = Drivers()
        self.app_gui = AppGUI(self)

    def introduce_driver(self,new_driver):
        self.drivers.add_driver(new_driver)



# Example Usage:

app = App()
app.app_gui.mainloop()


"""
# Create drivers
driver1 = Driver("John Doe", "123456789", "ABC Company")
driver2 = Driver("Jane Smith", "987654321", "XYZ Company")

# Create docks
dock1 = Dock(1)
dock2 = Dock(2)

# Add drivers to the app
app.drivers.add_driver(driver1)
app.drivers.add_driver(driver2)

# Add docks to the app
app.docks.add_dock(dock1)
app.docks.add_dock(dock2)

# Allocate a driver to a dock using events
app.events.handle_allocate_driver(driver1, dock1)

# Remove a driver from a dock using events
app.events.handle_remove_driver(driver1)
"""