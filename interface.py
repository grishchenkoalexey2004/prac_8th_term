


import tkinter as tk

from typing import Dict,Tuple
from experiment import Experiment
from tkinter import ttk



class Interface:
    """
        Главный класс, отвечающий за взаимодействие между интерфейсом и всеми остальными классами
    """
    
    def __init__(self):

        self.experiment : Experiment = Experiment()
        
        # корень к которому все элементы цепляются
        self.root : tk.Tk = None

        """ Переменные графического интерфейса """

        # Текущие значения слайдеров автостраховки (нельзя определять до построения интерфейса, поэтому None)
        self.auto_slider_price : tk.Variable = None
        self.auto_slider_time : tk.Variable = None
        self.auto_slider_refund : tk.Variable = None
        self.auto_slider_base_demand : tk.Variable = None


    # процедура запуска всей программы
    def run(self) -> None: 
        
        # создание корня интерфейса
        self.init_root() 

        self.init_slider_vars()

        self.experiment.init_state()

        # запускаем конструктор интерфейса 
        self.init_gui()

        # Запускаем главный цикл обработки событий
        self.root.mainloop()

        return  
    
    def init_root(self) -> None:
        self.root = tk.Tk()
        self.root.title("Моделирование работы страховой компании")
        return

    def init_slider_vars(self) -> None:
        self.auto_slider_price = tk.Variable(value = 5)
        self.auto_slider_time : tk.Variable = tk.Variable(value = 5)
        self.auto_slider_refund : tk.Variable = tk.Variable(value = 50)
        self.auto_slider_base_demand : tk.Variable = tk.Variable(value = 10)

    def init_gui(self) -> None:

        # Создаем главное окно
        params_label = ttk.Label(self.root,text="ПАРАМЕТРЫ",font=("Arial",20))
        params_label.grid(row=0, column=0, padx=10, pady=10)

        """ Создание слайдеров настройки программ автострахования """

        auto_slider_label = ttk.Label(self.root, text="АВТО:",font=("Arial",16))
        auto_slider_label.grid(row=1, column=0, padx=10, pady=10)

        # сладер стоимости страховки
        auto_slider_price = tk.Scale(self.root, from_=3, to=10, orient="horizontal",label = "цена",resolution =1,
                                     variable = self.auto_slider_price,command = self.update_auto_config)
        auto_slider_price.grid(row=1, column=1, padx=10, pady=10)

        # слайдер времени действия
        auto_slider_time = tk.Scale(self.root, from_=3, to=12, orient="horizontal",label = "время",resolution =1,
                                    variable = self.auto_slider_time,command = self.update_auto_config)
        auto_slider_time.grid(row=1, column=2, padx=10, pady=10)

        # слайдер возмещения
        auto_slider_refund = tk.Scale(self.root, from_=0, to=100, orient="horizontal",label = "возврат",resolution =1,
                                      variable = self.auto_slider_refund,command = self.update_auto_config)
        auto_slider_refund.grid(row=1, column=3, padx=10, pady=10)

        # слайдер базового спроса автостраховки
        auto_slider_label = ttk.Label(self.root, text="Базовый спрос:",font=("Arial",12))
        auto_slider_label.grid(row=2, column=0, padx=10, pady=10)

        auto_slider_demand = tk.Scale(self.root, from_=2, to=20, orient="horizontal",resolution =1,
                                      variable = self.auto_slider_base_demand)
        auto_slider_demand.grid(row=2, column=1, padx=10, pady=10)

        """ Создание кнопок """
        
        # Кнопка старт/итерация
        button = ttk.Button(self.root, text="Старт/Итерация", command=self.iteration_button_click)
        button.grid(row=4, column=0, columnspan=1, pady=10)

        # # Кнопка стоп
        # button = ttk.Button(self.root, text="СТОП", command=self.stop_button_click)
        # button.grid(row=4, column=1, columnspan=1, pady=10)

        # Кнопка Reset

        button = ttk.Button(self.root, text="ЗАНОВО", command=self.reset_button_click)
        button.grid(row=4, column=2, columnspan=1, pady=10, padx = 10)
 
    """ Обработчики кнопок """

    def update_auto_config(self,event):
        price = int(self.auto_slider_price.get())
        time = int(self.auto_slider_time.get())
        refund = int(self.auto_slider_refund.get())
        demand = int(self.auto_slider_base_demand.get())

        self.experiment.update_auto_config(price,time,refund,demand)
    

    def reset_slider_vars(self) -> None:
        self.auto_slider_price.set(5)
        self.auto_slider_time.set(5)
        self.auto_slider_refund.set(50)
        self.auto_slider_base_demand.set(10)

        self.experiment.reset_modeling_params()
        return 
    
    def reset_button_click(self) -> None:
        print("Reset")

        self.experiment.reset()
        return 
    

    def iteration_button_click(self) -> None: 
        self.experiment.iteration_button_click()

        return 
        
    


if __name__ == "__main__":
    pass 
