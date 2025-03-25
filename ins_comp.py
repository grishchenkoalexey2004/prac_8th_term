
"""
    Модуль содержит в себе реализацию классов InsuranceAgreement и InsuranceComp

    InsuranceAgreement - класс описывающий страховой договор, т.е. условия договора и кол-во клиентов,
    которые его заключили в различные месяцы

    InsuranceComp - класс описывающий страховую компанию
    Страховая компания хранит в себе информацию о текущих параметрах моделирования, а также страховых договорах,
    которые актуальны или еще имеют клиентов.



"""


from typing import Dict,Tuple
import tkinter as tk


class InsuranceAgreement:
    """
        Класс описывает объект страхового договора. 
        
        Страховой договор представляет из себя множество клиентов и страховую программу, 
        которую они подписали.
    """

    def __init__(self,prog_id: int, prog_type: str, prog_price: int, prog_time: int, prog_refund: int):
        # параметры страховой программы
        self.prog_id: int = prog_id
        self.prog_type: str = prog_type
        self.prog_price: int = prog_price
        self.prog_time: int = prog_time
        self.prog_refund: int = prog_refund
        
        # флаг наличия клиентов, подписавших договор
        self.has_clients: bool = False 
        # на 0-ой позиции - кол-во клиентов у которых 1 мес до истечения договора, на второй ...
        self.client_list: list[int] = [0 for i in range(prog_time)]

    # добавляет новых клиентов, подписавших договор на текущей итерации
    def add_clients(self,client_num:int) -> None:
        if client_num!=0:
            self.has_clients = True

        self.client_list[self.prog_time-1] = client_num

        return

    def gen_insurance_cases() -> int:
        """
        Активирует заранее вычисленные страховые случаи
        Возвращает сумму денежной компенсации на текущей итерации по данному страховому договору
        """
        pass
    
    
    def update_dates(self) -> int:
        """
        Обновляет сроки действия договоров с учётом пройденного месяца, удаляет клиентов 
        с истёкшим сроком договора, возвращая их количество 
        """
        deleted_count = self.client_list[0]

        for month in range(self.prog_time-1):
            self.client_list[month] = self.client_list[month+1]

        self.client_list[-1] = 0

        return deleted_count  
    
    def __repr__(self):
        return f"Prog_id: {self.prog_id}, prog_type: {self.prog_type}, clients: {self.client_list}"
    

class InsuranceComp:
    """
        Класс описывает страховую компанию
    """

    def __init__(self):

        self.client_num: int = 0 

        # флаги обновления конфигурации страховых программ
        self.auto_config_updated : bool = False
        self.estate_config_updated : bool = False 
        self.med_config_updated : bool = False

        """ Переменные интерфейса в зоне ответственности InsuranceComp"""

        # Текущие значения слайдеров автостраховки (нельзя определять до построения интерфейса)
        self.auto_slider_price : tk.Variable = None
        self.auto_slider_time : tk.Variable = None   
        self.auto_slider_refund : tk.Variable = None
        self.auto_slider_base_demand : tk.Variable = None

        # id созданной в последний раз программы страховки
        self.last_program_id = 0 

        # id текущих программ страхования различных типов
        self.cur_autoprog_id = None 
        self.cur_estateprog_id = None 
        self.cur_medprog_id = None 

        # "база" клиентов
        self.progs_active: List[int] = [] 
        self.ins_agreements: Dict[int,InsuranceAgreement] = dict()

    """ Инициализация """
    
    def init_state(self) -> None:
        self.init_slider_vars()
        self.init_programs_state()

        return

    # инициализация переменных отслеживания программ страхования
    def init_programs_state(self) -> None:
        self.cur_autoprog_id = 0 
        self.cur_estateprog_id = 1 
        self.cur_medprog_id = 2 

        self.last_program_id = 2 

        # инициализация начальных страховых программ

        self.add_ins_agr(self.cur_autoprog_id,self.create_ins_agr("auto",self.cur_autoprog_id))
        self.add_ins_agr(self.cur_estateprog_id,self.create_ins_agr("estate",self.cur_estateprog_id))
        self.add_ins_agr(self.cur_medprog_id,self.create_ins_agr("med",self.cur_medprog_id))

        return 
    
    # инициализация текущих переменных параметров страхования
    def init_slider_vars(self) -> None: 
        # временно поставил дефолтные значения
        self.auto_slider_price = tk.Variable(value = 5)
        self.auto_slider_time = tk.Variable(value = 5)
        self.auto_slider_refund = tk.Variable(value = 50)
        self.auto_slider_base_demand = tk.Variable(value = 10)

        return 
    
    """ Обновление на каждой итерации"""
    
    # добавление проданных страховок в клиентскую базу, создание новых договоров при изменении условий
    def update_client_state(self,auto_demand,estate_demand = None,med_demand = None) -> None:
        # смотрим, не обновились ли у нас условия страхования
        
        # если обновились условия страхования - создаём новый договор
        if self.auto_config_updated:
            self.last_program_id+=1
            self.cur_autoprog_id = self.last_program_id

            new_agr = self.create_ins_agr("auto",self.cur_autoprog_id)
            self.add_ins_agr(self.cur_autoprog_id,new_agr) 

            self.auto_config_updated = False

        self.ins_agreements[self.cur_autoprog_id].add_clients(auto_demand)
        

        # нужно добавить такую же логику про остальные типы страховок
        return None 

    def update_dates(self) -> None:
        #! нужно модифицировать, чтобы возвращала количество расторгнувших договор по каждому типу страховки
        for prog_id in self.progs_active:
            self.ins_agreements[prog_id].update_dates()
        
        return
    
    # создание страхового договора определённого типа по заданным условиям
    def create_ins_agr(self,prog_type:str,prog_id: int)-> InsuranceAgreement:
        if prog_type == "auto":
            prog_price = self.auto_slider_price.get()
            prog_refund = self.auto_slider_refund.get()
            prog_time = self.auto_slider_time.get() 

        # пока что привязаны к слайдерам от автостраховки
        elif prog_type == "estate":
            prog_price = self.auto_slider_price.get()
            prog_refund = self.auto_slider_refund.get()
            prog_time = self.auto_slider_time.get() 

        elif prog_type == "med":
            prog_price = self.auto_slider_price.get()
            prog_refund = self.auto_slider_refund.get()
            prog_time = self.auto_slider_time.get() 

        else:
            raise ValueError
        
        
        return InsuranceAgreement(prog_id,prog_type,prog_price,prog_time,prog_refund)
    
    # добавляет в "базу" новый страховой договор
    def add_ins_agr(self,prog_id:int,agr_obj:InsuranceAgreement) -> None: 
        self.progs_active.append(prog_id)
        self.ins_agreements[prog_id] = agr_obj

        return 
    
    """ Процедуры обновления состояния страховой компании """
    
    def reset(self) -> None:
        self.reset_programs()
        self.reset_slider_vars()

    def reset_slider_vars(self) -> None:
        self.auto_config_updated = False 
        
        self.auto_slider_price.set(5)
        self.auto_slider_time.set(5)
        self.auto_slider_refund.set(50)
        self.auto_slider_base_demand.set(10)

        return 
    
    def reset_programs(self) -> None: 
        self.last_program_id = 0 
        self.client_num = 0
        self.progs_active.clear() 
        self.ins_agreements.clear()

        # создаем начальные значения после сброса
        self.init_programs_state()
        return 

    def gen_ins_cases(self) -> Dict[str,int]:
        pass 
 

    def delete_ins_prog(ins_prog_id:int) -> None: 
        pass 


    """ Генерация спроса, подсчёт прибыли """

    # выдает спрос на страховки различного типа с учётом текущих условий страхования

    def gen_demand(self) -> Dict[str,Tuple[int,int]]:
        # вычисление коэ-фта выгодности 
        auto_profit_coef = (self.auto_slider_refund.get()*self.auto_slider_time.get())/self.auto_slider_price.get()
        auto_add_demand = int(auto_profit_coef//10)
        auto_demand = self.auto_slider_base_demand.get() + auto_add_demand + randint(-1*auto_add_demand,5)
        auto_profit = auto_demand*self.auto_slider_price.get()


        return_object = {"auto" : (auto_demand,auto_profit)}
        self.update_client_state(auto_demand)

        return return_object

    def print_slider_values(self):
        print(f"Auto price: {self.auto_slider_price.get()}")
        print(f"Auto time: {self.auto_slider_time.get()}")
        print(f"Auto refund: {self.auto_slider_refund.get()}")
        print(f"Auto demand: {self.auto_slider_base_demand.get()}")

        return 
    

    def print_programs(self):
        print(f"Кол-во клиентов: {self.client_num}")
        for id in self.progs_active:
            print(self.ins_agreements[id])

        return
    

if __name__ == "__main__":
    pass
