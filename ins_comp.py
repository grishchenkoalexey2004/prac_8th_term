
"""
    Модуль содержит в себе реализацию классов InsuranceAgreement и InsuranceComp

    InsuranceAgreement - класс описывающий страховой договор, т.е. условия договора и кол-во клиентов,
    которые его заключили в различные месяцы

    InsuranceComp - класс описывающий страховую компанию
    Страховая компания хранит в себе информацию о текущих параметрах моделирования, а также страховых договорах,
    которые актуальны или пока еще имеют клиентов.

"""


from typing import Dict,Tuple,List
from random import randint
from numpy.random import binomial,uniform,choice
from numpy import arange


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

        # параметры генерации страховых случаев
        self.days_prob : List[float] = [1/self.prog_time for i in range(self.prog_time)]
        
        # флаг наличия клиентов, подписавших договор
        self.has_clients: bool = False 
        # на 0-ой позиции - кол-во клиентов у которых 1 мес до истечения договора, на второй ...
        self.client_list: List[int] = [0 for i in range(prog_time)]
        # на 0-ой позиции - кол-во страховых случаев, которые наступят в ближайший месяц, на 1-ой ... 
        self.insurance_cases: List[int] = [0 for i in range(prog_time)]

    # добавляет новых клиентов, подписавших договор на текущей итерации + заранее вычисляет страховые случаи
    def add_clients(self,client_num : int,insurance_prob : float) -> None:
        if client_num!=0:
            self.has_clients = True

        self.client_list[self.prog_time-1] = client_num
        self.calc_insurance_cases(client_num,insurance_prob)
        return
    
    # предварительное вычисление страховых случаев для добавляемой группы клиентов
    def calc_insurance_cases(self,client_num:int,insurance_prob : float) -> None:
        # количество страховых случаев
        num_cases = binomial(n = client_num,p = insurance_prob,size = None)

        # распределение страховых случаев по дням
        positions = choice(self.prog_time,size = num_cases,p=self.days_prob)
        for day in positions:
            self.insurance_cases[day]+=1

        return 
    

    def gen_ins_cases(self) -> Tuple[int,int]:
        """
        1)Активирует заранее вычисленные страховые случаи

        2)Возвращает колво денежных компенсаций, а также сумму общую сумму денежной компенсации на текущей итерации 

        3)Обновляет массив с вычисленными страховыми случаями
        """ 

        ins_case_num = self.insurance_cases[0]
        refund_value = ins_case_num*self.prog_refund #! пока возвращает полную сумму, а должна возвращать процент
        
        self.update_ins_cases()

        return (ins_case_num,refund_value)


    def update_ins_cases(self) -> None:
        
        for i in range(len(self.insurance_cases)-1):
            self.insurance_cases[i] = self.insurance_cases[i+1]

        self.insurance_cases[-1] = 0

        return  
    
    
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
        return f"Prog_id: {self.prog_id}, prog_type: {self.prog_type}, clients: {self.client_list},ins_cases: {self.insurance_cases} "
    

class InsuranceComp:
    """
        Класс описывает страховую компанию
    """

    def __init__(self):
        
        # id созданной в последний раз программы страховки
        self.last_program_id = 0 

        # id текущих программ страхования различных типов
        self.cur_autoprog_id = None 
        self.cur_estateprog_id = None 
        self.cur_medprog_id = None 

        # "база" клиентов
        self.progs_active: List[int] = [] 
        self.ins_agreements: Dict[int,InsuranceAgreement] = dict()


        # делители коэф-тов для вычисления добавочного спроса (чем больше делитель тем менее эластичный спрос)
        self.auto_demand_delim = 10
        self.estate_demand_delim = 15 
        self.med_demand_delim = 5 


        """ Параметры моделирования и флаги"""

        self.auto_config_updated = False 
        self.med_config_updated = False 
        self.estate_config_updated = False 

        # вероятность возникновения страхвого случая
        self.insurance_prob: float = 0.05 # будет настраиваемым параметром

        # базовый спрос на все виды страховок
        self.base_demand : int = 10

        # условия автостраховки (c заданными начальными значениями)
        self.auto_slider_price : int =  5
        self.auto_slider_time : int = 5
        self.auto_slider_refund : int = 50 

        # условия медстраховки (c заданными начальными значениями)
        self.med_slider_price : int = 2
        self.med_slider_time : int = 5
        self.med_slider_refund : int = 10 



    """ Инициализация """
    
    def init_state(self) -> None:
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
    
    
    """ Обновление на каждой итерации"""
    
    # добавление проданных страховок в клиентскую базу, создание новых договоров при изменении условий
    def update_client_state(self,auto_demand,med_demand,estate_demand = None) -> None:
        # смотрим, не обновились ли у нас условия страхования
        
        # если обновились условия страхования - создаём новый договор и меняем id действующего страхового договора
        if self.auto_config_updated:
            self.last_program_id+=1
            self.cur_autoprog_id = self.last_program_id

            new_agr = self.create_ins_agr("auto",self.cur_autoprog_id)
            self.add_ins_agr(self.cur_autoprog_id,new_agr) 

            self.auto_config_updated = False

        if self.med_config_updated:
            self.last_program_id+=1
            self.cur_medprog_id = self.last_program_id

            new_agr = self.create_ins_agr("med",self.cur_medprog_id)
            self.add_ins_agr(self.cur_medprog_id,new_agr)

        # добавляем клиентов в действующий страховой договор
        self.ins_agreements[self.cur_autoprog_id].add_clients(auto_demand,insurance_prob=self.insurance_prob)
        self.ins_agreements[self.cur_medprog_id].add_clients(med_demand,insurance_prob=self.insurance_prob)

        
        # нужно добавить такую же логику про остальные типы страховок
        return None 

    def update_dates(self) -> None:
        #! нужно модифицировать, чтобы возвращала количество расторгнувших договор по каждому типу страховки
        for prog_id in self.progs_active:
            self.ins_agreements[prog_id].update_dates()
        
        return
    
    def update_case_percent(self,percent:int):
        for id in self.progs_active:
            self.ins_agreements[id].insurance_prob  = percent/100

        return 
    
    # создание объекта страхового договора определённого типа по заданным условиям
    def create_ins_agr(self,prog_type:str,prog_id: int)-> InsuranceAgreement:
        if prog_type == "auto":
            prog_price = self.auto_slider_price
            prog_refund = self.auto_slider_refund
            prog_time = self.auto_slider_time

        elif prog_type == "med":
            prog_price = self.med_slider_price
            prog_refund = self.med_slider_refund
            prog_time = self.med_slider_time 

        # пока что привязаны к слайдерам от автостраховки
        elif prog_type == "estate":
            prog_price = self.auto_slider_price
            prog_refund = self.auto_slider_refund
            prog_time = self.auto_slider_time

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
        # сброс параметров программ страхования
        self.reset_program_params()
        # сброс базы программ страхования
        self.reset_programs()
        # сброс вероятности страховых случаев
        self.reset_ins_prob()
        return 
    
    def reset_program_params(self) -> None:
        self.auto_config_updated = False 
        
        
        self.auto_slider_price = 5 
        self.auto_slider_time = 5 
        self.auto_slider_refund = 50

        self.med_slider_price = 2 
        self.med_slider_time = 5 
        self.med_slider_refund = 20  

        return 


    def reset_programs(self) -> None: 
        self.last_program_id = 0 
        self.client_num = 0
        self.progs_active.clear() 
        self.ins_agreements.clear()

        # создаем начальные значения после сброса
        self.init_programs_state()
        return 
    
    def reset_ins_prob(self):
        self.insurance_prob = 0.07

    # возвращает кол-во и сумму страховых возвратов по категориям страховок
    def gen_ins_cases(self) -> Tuple[int,int]: #! пока возвр. int, потом будет Dict[str,Tuple(int,int)]
        
        total_cases = 0 
        total_refund_sum = 0 

        for id in self.progs_active:
            ins_cases,refund_sum = self.ins_agreements[id].gen_ins_cases()
            total_cases += ins_cases
            total_refund_sum += refund_sum 

        return (total_cases,total_refund_sum)


    """ Генерация спроса, подсчёт прибыли """

    # выдает спрос на страховки различного типа с учётом текущих условий страхования

    def gen_demand(self) -> Dict[str,Tuple[int,int]]:
        # вычисление коэ-фта выгодности 
        
        auto_profit_coef = (self.auto_slider_refund*self.auto_slider_time)/self.auto_slider_price
        auto_add_demand = int(auto_profit_coef//self.auto_demand_delim)
        
        auto_demand = self.calc_demand(auto_add_demand)
        auto_profit = auto_demand*self.auto_slider_price

        med_profit_coef = (self.med_slider_refund*self.med_slider_time)/self.med_slider_price
        med_add_demand = int(med_profit_coef//self.med_demand_delim)

        med_demand = self.calc_demand(med_add_demand)
        med_profit = med_demand*self.med_slider_price

        self.update_client_state(auto_demand,med_demand)

        return_object = {"auto" : (auto_demand,auto_profit),"med" : (med_demand,med_profit)}
        

        return return_object

    # вычисляет случайную величину спроса по двум параметрам (базовый спрос + )
    def calc_demand(self,additional_demand:int) -> int:
        add_range = arange(0,additional_demand*2+1,step=1)
        return self.base_demand + int(choice(add_range,size = None,p = None))

    def print_slider_values(self):
        print(f"Auto price: {self.auto_slider_price}")
        print(f"Auto time: {self.auto_slider_time}")
        print(f"Auto refund: {self.auto_slider_refund}")

        print(f"Med price: {self.med_slider_price}")
        print(f"Med time: {self.med_slider_time}")
        print(f"Med refund: {self.med_slider_refund}")  

        print(f"Demand: {self.base_demand}")
        return 
    
    
    def print_programs(self):
        for id in self.progs_active:
            print(self.ins_agreements[id])

        return
    

# testing insurance case generation 
# generation is performed by calculation of insurance cases in the group and distribution of them 
if __name__ == "__main__":
    number = int(input())
    days = 12

    p = 0.05

    res = binomial(number,p = p,size = None)
    


    probs = [1/days for i in range(days)]
    

    positions = choice(days,size = res,p=probs)


    print(res)
    print(positions)
