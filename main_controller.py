


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

        # финансовые показатели
        self.networth = 100
        self.cur_profit : int = 0 
        self.cur_loss : int = 0

        # количественные показатели
        self.auto_sold : int = 0 
        self.estate_sold : int = 0 
        self.med_sold : int = 0 

        # налог
        self.tax_percent = 5
        self.tax_value = 0

        self.ins_company : InsuranceComp = InsuranceComp()

        """ Переменные графического интерфейса в зоне ответственности MainController """

        self.root : tk.Tk = None


    # процедура запуска всей программы
    def run(self) -> None: 
        
        # создание корня интерфейса
        self.init_root() 

        # инициализация страховой компании (внутри неё есть перем., используемые интерфейсом)
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

    def init_gui(self) -> None:

        # Создаем главное окно
        

        params_label = ttk.Label(self.root,text="ПАРАМЕТРЫ",font=("Arial",20))
        params_label.grid(row=0, column=0, padx=10, pady=10)

        # Инициализируем переменные, хранящие значения слайдеров для параметров договора:

        self.ins_company.init_slider_vars()

        """ Создание слайдеров настройки программ страхования """

        auto_slider_label = ttk.Label(self.root, text="АВТО:",font=("Arial",16))
        auto_slider_label.grid(row=1, column=0, padx=10, pady=10)

        # сладер стоимости страховки
        auto_slider_price = tk.Scale(self.root, from_=3, to=10, orient="horizontal",label = "цена",resolution =1,
                                     variable = self.ins_company.auto_slider_price,command = self.set_auto_update_flag)
        auto_slider_price.grid(row=1, column=1, padx=10, pady=10)

        # слайдер времени действия
        auto_slider_time = tk.Scale(self.root, from_=3, to=12, orient="horizontal",label = "время",resolution =1,
                                    variable = self.ins_company.auto_slider_time,command = self.set_auto_update_flag)
        auto_slider_time.grid(row=1, column=2, padx=10, pady=10)

        # слайдер возмещения
        auto_slider_refund = tk.Scale(self.root, from_=0, to=100, orient="horizontal",label = "возврат",resolution =1,
                                      variable = self.ins_company.auto_slider_refund,command = self.set_auto_update_flag)
        auto_slider_refund.grid(row=1, column=3, padx=10, pady=10)

        # слайдер базового спроса автостраховки
        auto_slider_label = ttk.Label(self.root, text="Базовый спрос:",font=("Arial",12))
        auto_slider_label.grid(row=2, column=0, padx=10, pady=10)

        auto_slider_demand = tk.Scale(self.root, from_=2, to=20, orient="horizontal",resolution =1,
                                      variable = self.ins_company.auto_slider_base_demand)
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

    def set_auto_update_flag(self,event):
        self.ins_company.auto_config_updated = True 
        return 

    """ Методы выполнения итерации """

    def simulate_month(self) -> None:
        self.reset_sell()
        self.reset_loss()

        sell_stats = self.ins_company.gen_demand()
        self.update_sell(sell_stats)

        # пока не работает
        loss_stats = self.ins_company.gen_ins_cases()

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

    # обнуляет показатели связанные с продажей
    def reset_sell(self):
        self.auto_sold = 0 
        self.med_sold = 0
        self.estate_sold = 0 
        self.cur_profit = 0 

        return 

    # изменяет внутренее состояние после прибыли от продажи страховок
    def update_sell(self,sell_stats:Dict[str,Tuple[int,int]]):
        auto_sold_quantity,auto_profit = sell_stats["auto"]
        self.auto_sold = auto_sold_quantity
        self.cur_profit += auto_profit


        self.networth += self.cur_profit

    
    # изменяет внутренее состояние после убытков в виде налогов и страховых случаев
    def update_loss(self) -> None: 
        pass

    def reset_loss(self) -> None:
        self.loss = 0 
        self.tax_value = 0 

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
        self.print_sliders()
        self.ins_company.print_programs()
        print("-----------------------------------------")


    def print_finance(self) -> None:
        print(f"Текущий месяц: {self.curmonth}")

        print(f"Капитал: {self.networth}")
        print(f"Прибыль: {self.cur_profit}")
        print(f"Убыток: {self.cur_loss}")

        return 

    def print_sliders(self) -> None:
        self.ins_company.print_slider_values()
        return 
    
    # вывод количества проданных страховок различного типа
    def print_quantity(self) -> None:
        print(f"Количество проданных автостраховок {self.auto_sold}")

        return 
    


if __name__ == "__main__":
    pass 
