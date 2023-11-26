import tkinter
import tkinter.messagebox
import customtkinter as ctk
import pandas as pd
import datetime as dt
import tkinter as tk
from PIL import Image, ImageTk, ImageDraw

ctk.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

class Motoristas:
    def __init__(self):
        self.colunas = ['nome', 'telefone', 'empresa', 'hora', 'status', 'cais']
        self.dataframe = pd.DataFrame(columns=self.colunas)

    def adicionar_motoristas(self, nome, telefone, empresa):
        hora = dt.datetime.now()
        nova_linha = pd.DataFrame([{'nome': nome, 'telefone': telefone, 'empresa': empresa, 'hora': hora, 'status': 0}])
        self.dataframe = pd.concat([self.dataframe,nova_linha],ignore_index=True)
    
    def dados_filtrados(self,status):
        return self.dataframe[self.dataframe['status']==status]
    
    def alocar_cais(self,indice_motorista,cais):
        self.dataframe.iloc[[indice_motorista]]['cais'] = cais

class JanelaInsercaoMotorista(ctk.CTkToplevel):
    def __init__(self, data_manager): #, *args, **kwargs
        super().__init__() #*args, **kwargs
        self.geometry("400x300")
        self.title("Registo de camionista")
        self.data_manager = data_manager

         # Create and pack widgets for name, phone number, and company
        self.name_label = ctk.CTkLabel(self, text="Nome")
        self.name_entry = ctk.CTkEntry(self,width=300)

        self.name_label.pack(pady=(10,3))
        self.name_entry.pack(pady=(0,6))
    
        self.phone_label = ctk.CTkLabel(self, text="Contacto telefónico")
        self.phone_entry = ctk.CTkEntry(self, width=300)

        self.phone_label.pack(pady=(10,3))
        self.phone_entry.pack(pady=(0,6))

        self.company_label = ctk.CTkLabel(self, text="Empresa")
        self.company_entry = ctk.CTkEntry(self, width=300)

        self.company_label.pack(pady=(10,3))
        self.company_entry.pack(pady=(0,6))

        self.submit_button = ctk.CTkButton(self, width=300,text="Inserir",command=self.submit_info)
        self.submit_button.pack(pady=20)

    def submit_info(self):
        nome = self.name_entry.get()
        telefone = self.phone_entry.get()
        empresa = self.company_entry.get()
        hora = dt.datetime.now()

        self.data_manager.adicionar_motoristas(nome, telefone, empresa)
        self.destroy()

class JanelaAtribuicaoCais(ctk.CTkToplevel):
    def __init__(self, data_manager, nome):  #, *args, **kwargs
        super().__init__() #*args, **kwargs
        self.geometry("400x150")
        self.title("Atribuicao Cais")
        self.data_manager = data_manager

        self.legenda_cais = ctk.CTkLabel(self, text="Cais a atribuir")
        self.combo_cais = ctk.CTkComboBox(self, values=["CAIS " + str(num) for num in ["1", "2", "3", "4", "5", "6", "7", "8", "9"]], width=300)

        self.legenda_cais.pack(pady=(10,3))
        self.combo_cais.pack(pady=(0,6))

        self.submit_button = ctk.CTkButton(self, width=300,text="Atribuir cais",command=self.submeter_cais(nome))
        self.submit_button.pack(pady=20)

    def submeter_cais(self,nome):
        num_cais = self.combo_cais.get()
        self.data_manager[self.data_manager["nome"]==nome]["status"] = 1
        

        #self.data_manager.add_entry(nome, telefone, empresa)
        #self.destroy()

class App(ctk.CTk):
    def __init__(self, data_manager):
        super().__init__()

        self.title("Gestão de cais JM")
        self.geometry(f"{1100}x{580}")

        self.data_manager = data_manager
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
        self.sidebar_button_1 = ctk.CTkButton(self.sidebar_frame,text=nome_botao1, command=self.open_popup)
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)
        self.appearance_mode_label = ctk.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = ctk.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))
        self.scaling_label = ctk.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = ctk.CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"],
                                                               command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 20))
        self.update_data()
        self.update_data2()

        """
        self.c4est_imagme = ctk.CTkFrame(self, width=250)
        self.c4est_imagme.grid(row=0, column=3, padx=(20, 0), pady=(20, 0), sticky="ne")
        self.c4est_imagme.grid_columnconfigure(3, weight=1)

        self.title_label = ctk.CTkLabel(self.c4est_imagme, text="Ocupação", font=ctk.CTkFont(size=25, weight="bold"))
        self.title_label.grid(row=0, column=0, padx=(10, 90), pady=(0, 10), sticky="n")

        image = Image.open("docks_image.png")   
    

        self.image = ctk.CTkImage(light_image=image, dark_image=image, size=(215, 500))
        self.image_label = ctk.CTkLabel(self.c4est_imagme, image=self.image,width=50, text="")  # display image with a CTkLabel

        self.image_label.grid(row=2, column=0, sticky="nw")
            """ 
        
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

        # Draw a red rectangle
        trapeze_coords = [147, 35, 
                          180, 50,  
                          70, 117, 
                          70, 80]
        
       
        self.canvas.create_polygon(trapeze_coords, outline="red", width=2, fill="red")



    def update_data(self):
        # TABELA MOTORISTAS ESPERA
        self.coluna_2_estrutura = ctk.CTkFrame(self, width=250)
        self.coluna_2_estrutura.grid(row=0, column=1, padx=(30, 0), pady=(20, 0), sticky="nsew")

        self.title_label = ctk.CTkLabel(self.coluna_2_estrutura, text="Motoristas em espera", font=ctk.CTkFont(size=25, weight="bold"))
        self.title_label.grid(row=0, column=0, padx=(10, 10), pady=(0, 18), sticky="n")

        df_motoristas_espera = self.data_manager.dados_filtrados(0)

        for i in range(len(df_motoristas_espera)):
            # Create a subframe
            subframe = ctk.CTkFrame(self.coluna_2_estrutura)
            subframe.grid(row=i+1, column=0, padx=(10, 10), pady=(0, 10), sticky="nsew")

            self.nome_widget_motorista = ctk.CTkLabel(subframe, text=f"Nome {self.data_manager.dataframe.iloc[i,0]}")
            self.nome_widget_motorista.grid(row=0, column=0, padx=(10, 60), pady=(10, 5), sticky="w")

            self.telefone_widget_motorista = ctk.CTkLabel(subframe, text=f"Telefone {self.data_manager.dataframe.iloc[i,1]}")
            self.telefone_widget_motorista.grid(row=1, column=0, padx=(10, 60), pady=(0, 5), sticky="w")

            self.tempo_widget_motorista = ctk.CTkLabel(subframe, text=f"Tempo {i} Min", font=ctk.CTkFont(size=20, weight="bold"))
            self.tempo_widget_motorista.grid(row=0, column=1, padx=(10, 10), pady=(10, 0), sticky="w")

            self.empresa_widget_motorista = ctk.CTkLabel(subframe, text=f"Empresa {self.data_manager.dataframe.iloc[i,2]}")
            self.empresa_widget_motorista.grid(row=2, column=0, padx=(10, 0), pady=(0, 5), sticky="w")

            self.botao = ctk.CTkButton(master=subframe, text=f"Atribuir cais", width=100, 
                                       command=lambda i=i: self.abrir_popup_cais(self.data_manager,self.data_manager.dataframe.iloc[i,0]))
            self.botao.grid(row=2, column=1, rowspan=1, padx=(10, 10), pady=(0, 10), sticky="w")

            #self.wait_window(self.toplevel_window)

    def update_data2(self):
        
        self.coluna_3_estrutura = ctk.CTkFrame(self, width=450)
        self.coluna_3_estrutura.grid(row=0, column=2, padx=(30, 0), pady=(20, 0), sticky="nsew")

        self.title_label = ctk.CTkLabel(self.coluna_3_estrutura, text="Motoristas em carga", font=ctk.CTkFont(size=25, weight="bold"))
        self.title_label.grid(row=0, column=0, padx=(10, 10), pady=(0, 18), sticky="n")

        df_motoristas_alocados = self.data_manager.dados_filtrados(1)

        for i in range(len(df_motoristas_alocados)):
            # Create a subframe
            subframe = ctk.CTkFrame(self.coluna_3_estrutura)
            subframe.grid(row=i+1, column=0, padx=(10, 10), pady=(0, 10), sticky="nsew")

            self.nome_widget_motorista = ctk.CTkLabel(subframe, text=f"Nome {i}")
            self.nome_widget_motorista.grid(row=0, column=0, padx=(10, 60), pady=(10, 5), sticky="w")

            self.telefone_widget_motorista = ctk.CTkLabel(subframe, text=f"Telefone {i}")
            self.telefone_widget_motorista.grid(row=1, column=0, padx=(10, 60), pady=(0, 5), sticky="w")

            self.tempo_widget_motorista = ctk.CTkLabel(subframe, text=f"Tempo {i} Min", font=ctk.CTkFont(size=20, weight="bold"))
            self.tempo_widget_motorista.grid(row=0, column=1, padx=(10, 10), pady=(10, 0), sticky="w")

            self.empresa_widget_motorista = ctk.CTkLabel(subframe, text=f"Empresa {i}")
            self.empresa_widget_motorista.grid(row=2, column=0, padx=(10, 0), pady=(0, 5), sticky="w")

            self.botao = ctk.CTkButton(master=subframe, text=f"Botao {i+1}", width=100)
            self.botao.grid(row=2, column=1, rowspan=1, padx=(10, 10), pady=(0, 10), sticky="w")




    def open_popup(self):
         self.toplevel_window = JanelaInsercaoMotorista(self.data_manager)
         self.toplevel_window.attributes('-topmost', 'true')

         self.wait_window(self.toplevel_window)
         
         self.update_data()
    
    def abrir_popup_cais(self,dataframe,motorista):
         self.janela_cais_aberta = JanelaAtribuicaoCais(dataframe,motorista)
         self.janela_cais_aberta.attributes('-topmost', 'true')

         self.wait_window(self.janela_cais_aberta)
         
         self.update_data()

    def sidebar_button_event(self):
        print("sidebar_button click")

    def change_appearance_mode_event(self, new_appearance_mode: str):
        ctk.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        ctk.set_widget_scaling(new_scaling_float)    


if __name__ == "__main__":
    motoristas = Motoristas()
    app = App(motoristas)
    app.mainloop()