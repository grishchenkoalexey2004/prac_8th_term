from typing import Dict,Optional
import tkinter as tk
from tkinter import ttk

class InsuranceProgram:
    """
        Класс описывающий конфигурацию страховой программы
    """

    def __init__(self,prog_id:int,prog_type:str,time:int,price:int,max_comp:int):

        self.prog_id : int = prog_id

        self.prog_type : str = prog_type
        self.time : int = time 
        self.price : int = price
        self.max_comp : int = max_comp

        self.profit_coef : float = (time*max_comp)/price


class InsuranceAgreement:
    """
        Класс описывает объект страхового договора. 
        
        Страховой договор представляет из себя множество клиентов и страховую программу, 
        которую они подписали.
    """

    def __init__(self,prog_id: int, prog_config:InsuranceProgram):
        self.prog_id: int = prog_id
        self.prog_type: str = prog_config.prog_type 

        self.has_clients: bool = False 
        self.client_list: list[int] = [] 
        self.case_dates: list[int] = [] 

        self.prog_config : InsuranceProgram


    def add_clients(client_arr:list[int]) -> None:
        """ добавляет новых клиентов, подписавших договор на текущей итерации """
        pass

    def gen_insurance_cases() -> int:
        """
        Активирует заранее вычисленные страховые случаи
        Возвращает сумму денежной компенсации на текущей итерации по данному страховому договору
        """

        pass    

class InsuranceComp:
    """
        Класс описывает страховую компанию
    """

    def __init__(self):

        self.client_num: int = 0 

        self.auto_base_demand : int = 10    
        self.estate_base_demand : int = 5        
        self.med_base_demand : int = 20 

        self.auto_config : Optional[InsuranceProgram] = None 
        self.estate_config : Optional[InsuranceProgram] = None 
        self.med_config : Optional[InsuranceProgram] = None 

        self.progs_active: list[int] = [] 
        self.ins_agreements: Dict[int,InsuranceAgreement] = dict()


    def gen_ins_cases(self) -> Dict[str,int]:
        pass 

    def add_ins_agr(ins_agr:InsuranceAgreement) -> None:
        pass 

    def delete_ins_prog(ins_prog_id:int) -> None: 
        pass 

    def gen_demand() -> None: 
        pass 



class MainController:
    """
        Главный класс, отвечающий за взаимодействие между интерфейсом и всеми остальными классами
    """
    
    def __init__(self):
        self.modeling_started : bool = False
        self.curmonth : int = 1

        self.cur_profit : int = 0 
        self.cur_loss : int = 0

        self.networth = 100
        self.tax_percent = 5

        self.ins_company : InsuranceComp = InsuranceComp()



        """ Переменные графического интерфейса """

        self.root : tk.Tk = None

        self.auto_config_updated : bool = False

        self.auto_slider_price : tk.Variable = None
        self.auto_slider_time : tk.Variable = None   
        self.auto_slider_refund : tk.Variable = None



    def run(self) -> None: 
        """ Самая первая процедура для запуска """

        # запускаем конструктор интерфейса 
        self.construct_gui()

        # Запускаем главный цикл обработки событий
        self.root.mainloop()

        return  
    

    def construct_gui(self) -> None:

        # Создаем главное окно
        self.root = tk.Tk()
        self.root.title("Моделирование работы страховой компании")

        params_label = ttk.Label(self.root,text="ПАРАМЕТРЫ",font=("Arial",20))
        params_label.grid(row=0, column=0, padx=10, pady=10)


        # Инициализируем переменные:

        self.auto_slider_price = tk.Variable(value = 5)
        self.auto_slider_time = tk.Variable(value = 5)
        self.auto_slider_refund = tk.Variable(value = 50)

        """ Создание слайдеров настройки программ страхования """

        auto_slider_label = ttk.Label(self.root, text="АВТО:",font=("Arial",16))
        auto_slider_label.grid(row=1, column=0, padx=10, pady=10)

        # сладер стоимости страховки
        auto_slider_price = tk.Scale(self.root, from_=3, to=10, orient="horizontal",resolution =1,
                                     variable = self.auto_slider_price,command = self.update_auto_config)
        auto_slider_price.grid(row=1, column=1, padx=10, pady=10)

        # слайдер времени действия
        auto_slider_time = tk.Scale(self.root, from_=3, to=12, orient="horizontal",resolution =1,
                                    variable = self.auto_slider_time,command = self.update_auto_config)
        auto_slider_time.grid(row=1, column=2, padx=10, pady=10)

        # слайдер возмещения
        auto_slider_refund = tk.Scale(self.root, from_=0, to=100, orient="horizontal",resolution =1,
                                      variable = self.auto_slider_refund,command = self.update_auto_config)
        auto_slider_refund.grid(row=1, column=3, padx=10, pady=10)

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

        self.simulate_month()

        return 
    

    def stop_button_click(self) -> None:
        print("Пока нереализована")

    def reset_button_click(self) -> None:
        self.networth = 100
        self.curmonth = 1 


        self.modeling_started = False 
        self.auto_config_updated = False

        print("Reset")


    """ Обработчики слайдеров """

    def update_auto_config(self,event):
        self.auto_config_updated = True 


    """ Методы выполнения итерации """

    def simulate_month(self) -> None:

        self.print_finance()
        self.curmonth += 1

        # временно поставил 10 - конец симуляции по времени
        if self.curmonth>10:
            print("Симуляция завершена")


    def print_finance(self) -> None:
        print(f"Текущий месяц: {self.curmonth}\nКапитал: {self.networth}\nПрибыль: {self.cur_profit}\nУбыток: {self.cur_loss}")



main_controller = MainController()

main_controller.run() 

