


import tkinter as tk

from typing import Dict,Tuple
from ins_comp import InsuranceComp
from tkinter import ttk



class MainController:
    """
        Главный класс, отвечающий за взаимодействие между интерфейсом и всеми остальными классами
    """
    
    def __init__(self):
        # флаги для управления итерациями
        self.modeling_started : bool = False
        self.modeling_finished : bool = False
        self.is_bankrupt : bool = False 

        # номер текущего месяца
        self.curmonth : int = 1

        """ Финансовые и количественные показатели (прибыль,убыток,колво страх. случаев)"""
        self.networth = 100
        self.cur_profit : int = 0 
        self.cur_loss : int = 0
        self.cur_net_profit : int = 0 

        # количественные показатели
        self.cur_auto_sold : int = 0 
        self.cur_estate_sol : int = 0 
        self.cur_med_sold : int = 0 

        self.cur_auto_ins_cases : int = 0
        self.cur_estate_ins_cases : int = 0 
        self.cur_med_ins_cases : int = 0 
    
        # налог
        self.tax_percent = 5
        self.tax_value = 0

        self.ins_company : InsuranceComp = InsuranceComp()

        """ Переменные графического интерфейса, параметры моделирования"""


        # корень к которому все элементы цепляются
        self.root : tk.Tk = None

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

        self.ins_company.init_state()

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
                                     variable = self.auto_slider_price,command = self.auto_update_config)
        auto_slider_price.grid(row=1, column=1, padx=10, pady=10)

        # слайдер времени действия
        auto_slider_time = tk.Scale(self.root, from_=3, to=12, orient="horizontal",label = "время",resolution =1,
                                    variable = self.auto_slider_time,command = self.auto_update_config)
        auto_slider_time.grid(row=1, column=2, padx=10, pady=10)

        # слайдер возмещения
        auto_slider_refund = tk.Scale(self.root, from_=0, to=100, orient="horizontal",label = "возврат",resolution =1,
                                      variable = self.auto_slider_refund,command = self.auto_update_config)
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

        # Кнопка стоп
        button = ttk.Button(self.root, text="СТОП", command=self.stop_button_click)
        button.grid(row=4, column=1, columnspan=1, pady=10)

        # Кнопка Reset

        button = ttk.Button(self.root, text="ЗАНОВО", command=self.reset_button_click)
        button.grid(row=4, column=2, columnspan=1, pady=10, padx = 10)
 

    """ Обработчики кнопок """
    def iteration_button_click(self) -> None: 

        if not self.modeling_started:
            print("Моделирование запущено!")
            self.modeling_started = True

        # проверяем остались ли еще итерации
        if self.modeling_finished or self.is_bankrupt:

            if self.modeling_finished:
                print("Моделирование завершено!, нажмите Reset")

            if self.is_bankrupt:
                print("Компания обанкротилась!")

        else:
            self.simulate_month()

        return 
    

    def stop_button_click(self) -> None:
        print("Пока нереализована")
        return 

    def reset_button_click(self) -> None:
        print("Reset")

        self.reset()
        return 
        

    """ Обработчики слайдеров """

    def auto_update_config(self,event):
        self.ins_company.auto_config_updated = True 
        self.ins_company.auto_slider_price = int(self.auto_slider_price.get() )
        self.ins_company.auto_slider_time = int(self.auto_slider_time.get() )
        self.ins_company.auto_slider_refund = int(self.auto_slider_refund.get())
        self.ins_company.auto_slider_base_demand = int(self.auto_slider_base_demand.get())
        return 

    """ Методы выполнения итерации """

    def simulate_month(self) -> None:
        self.reset_sell()
        self.reset_loss()

        sell_stats = self.ins_company.gen_demand()
        self.update_sell(sell_stats)

        # пока не работает
        loss_stats = self.ins_company.gen_ins_cases()
        self.update_loss(loss_stats)

        self.print_state()

        # обновление дат
        self.ins_company.update_dates()
        self.curmonth += 1

        # временно поставил 10 - конец симуляции по времени
        if self.curmonth>10:
            print("Симуляция завершена")
            self.modeling_finished = True 

        if self.networth<0:
            print("Компания обанкротилась")
            self.is_bankrupt = True


    # изменяет внутренее состояние после прибыли от продажи страховок
    def update_sell(self,sell_stats:Dict[str,Tuple[int,int]]):
        auto_sold_quantity,auto_profit = sell_stats["auto"]
        self.cur_auto_sold = auto_sold_quantity
        self.cur_profit += auto_profit

        self.cur_net_profit += self.cur_profit
        self.networth += self.cur_profit

    
    # изменяет внутренее состояние после убытков в виде налогов и страховых случаев
    def update_loss(self,loss:Tuple[int,int]) -> None: #! пока принимает int, потом будет принимать 
        self.cur_loss = loss[1]
        self.cur_net_profit -= loss[1]

        self.cur_auto_ins_cases = loss[0]

        return 
        
    # обнуляет показатели связанные с продажей
    def reset_sell(self):
        self.cur_auto_sold = 0 
        self.cur_med_sold = 0
        self.cur_estate_sol = 0 

        self.cur_profit = 0 
        self.cur_net_profit = 0
        return 

    def reset_loss(self) -> None:

        self.loss = 0 
        self.tax_value = 0 

        self.cur_auto_ins_cases = 0
        self.cur_estate_ins_cases = 0 
        self.cur_med_ins_cases = 0 

        return 
    

    def reset_slider_vars(self) -> None:
        self.auto_config_updated = False 
        
        self.auto_slider_price.set(5)
        self.auto_slider_time.set(5)
        self.auto_slider_refund.set(50)
        self.auto_slider_base_demand.set(10)
        self.ins_company.auto_slider_price = 5 
        self.ins_company.auto_slider_time = 5 
        self.ins_company.auto_slider_refund = 50
        self.auto_slider_base_demand = 10 

        return 


    def reset(self) -> None:

        self.networth = 100
        self.curmonth = 1 

        self.reset_sell() 
        self.reset_loss() 

        self.modeling_started = False
        self.modeling_finished = False   

        # reset страховой компании  
        self.ins_company.reset() 


    """ Методы вывода (вывод значений слайдеров, фин. и количественных показателей)"""

    def print_state(self) -> None:
        print("-----------------------------------------")
        self.print_finance() 
        self.print_quantity()
        self.ins_company.print_programs()
        print("-----------------------------------------")


    def print_finance(self) -> None:
        print(f"Текущий месяц: {self.curmonth}")

        print(f"Капитал: {self.networth}")
        print(f"Прибыль: {self.cur_profit}")
        print(f"Убыток: {self.cur_loss}")
        print(f"Чистая прибыль: {self.cur_net_profit}")

        return 

    def print_sliders(self) -> None:
        self.ins_company.print_slider_values()
        return 
    
    # вывод количества проданных страховок различного типа
    def print_quantity(self) -> None:
        print(f"Количество проданных автостраховок: {self.cur_auto_sold}")
        print(f"Количество страховых случаев (авто): {self.cur_auto_ins_cases}")
        return 
    


if __name__ == "__main__":
    pass 
