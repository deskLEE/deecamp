class Schedule:
    """Class Schedule.
    """
#课程类，课程ID，班级ID，教师ID是固定的
#需要初始化和调整的是教室ID，星期ID，时间ID
    def __init__(self, courseId, classId, teacherId):
        """Init
        Arguments:
            courseId: int, unique course id.
            classId: int, unique class id.
            teacherId: int, unique teacher id.
        """
        self.courseId = courseId
        self.classId = classId
        self.teacherId = teacherId

        self.roomId = 0
        self.weekDay = 0
        self.slot = 0

    def random_init(self, roomRange):
        """random init.
        Arguments:
            roomSize: int, number of classrooms.
        """
        self.roomId = np.random.randint(1, roomRange + 1, 1)[0]
        self.weekDay = np.random.randint(1, 6, 1)[0]
        self.slot = np.random.randint(1, 6, 1)[0]
#其中，教室ID，星期ID，时间都是在（1，6）之间取一个整数

#schedule_cost用于冲突检测，检测冲突的函数
    def schedule_cost(population, elite):
        """calculate conflict of class schedules.
        Arguments:
            population: List, population of class schedules.
            elite: int, number of best result.
        #输入schedules这个类的population（种群）
        #输入最佳结果的数目 elite
        Returns:
            index of best result.
            best conflict score.
        #返回最佳结果的index
        #返回最佳结果的冲突分数
        """
        conflicts = []
        n = len(population[0])
            #conflicts是list  //  population的列数为n
        for p in population:
            #对于population的每一个entity，p是entity.
            conflict = 0
            #conflict的是0
            for i in range(0, n - 1):
            #对entity的每一个实例进行循环
                for j in range(i + 1, n):
            #冒泡判断，对i中的后面j
                    # check course in same time and same room
                    if p[i].roomId == p[j].roomId and p[i].weekDay == p[j].weekDay and p[i].slot == p[j].slot:
                        conflict += 1
            #如果课程在相同的时间和相同的教室进行
                    # check course for one class in same time
                    if p[i].classId == p[j].classId and p[i].weekDay == p[j].weekDay and p[i].slot == p[j].slot:
                        conflict += 1
            #如果一个班级的教室在同一时间
                    # check course for one teacher in same time
                    if p[i].teacherId == p[j].teacherId and p[i].weekDay == p[j].weekDay and p[i].slot == p[j].slot:
                        conflict += 1
            #如果在同一时间中一个教师有好几门课
                    # check same course for one class in same day
                    if p[i].classId == p[j].classId and p[i].courseId == p[j].courseId and p[i].weekDay == p[j].weekDay:
                        conflict += 1
            #在同一天一个教室有相同的课

            conflicts.append(conflict)
#conflicts中包含的是每一个population中的conficts
        index = np.array(conflicts).argsort()
#对conficts进行排序
        return index[: elite], conflicts[index[0]]
#返回的是elite个数的index，并返回conlicts的值

import copy
import numpy as np

from schedule import schedule_cost

#考虑3个班级数/6个课程数/6个教师/3个教室数
class GeneticOptimize:
    """Genetic Algorithm.
    """
#采用GA算法
    def __init__(self, popsize=30, mutprob=0.3, elite=5, maxiter=100):
        # size of population
        self.popsize = popsize  #种群数量
        # prob of mutation
        self.mutprob = mutprob  #变异概率
         # number of elite
        self.elite = elite      #子结果数量
        # iter times
        self.maxiter = maxiter  #迭代次数

    def init_population(self, schedules, roomRange):
        """Init population   用于初始化种群
        Arguments:
            schedules: List, population of class schedules.  课表的种群
            roomRange: int, number of classrooms.   教室的数量
        """
        self.population = []   # ？？？

        for i in range(self.popsize):
            entity = []

            for s in schedules:  #对于每一个Schedule的实例s来说
                s.random_init(roomRange)   #对这个实例的单个教室进行初始化
                entity.append(copy.deepcopy(s))

            self.population.append(entity)   #得到初始化的种群

    def mutate(self, eiltePopulation, roomRange):
        """Mutation Operation
        #变异操作
        Arguments:
            eiltePopulation: List, population of elite schedules.
            #精英子类
            roomRange: int, number of classrooms.
            #教室数目
        Returns:
            ep: List, population after mutation.
        """
        #返回变异后的种群数目
        e = np.random.randint(0, self.elite, 1)[0]
        #e表示的是int,指的是从elite 5 中选出一个值
        pos = np.random.randint(0, 2, 1)[0]
        #pos表示 从0到2之间选出一个值

        ep = copy.deepcopy(eiltePopulation[e])
        #挑选出ep,也就是种群中的一个entity

        for p in ep:
            pos = np.random.randint(0, 3, 1)[0]   #对一个entity的一个课程而言,pos是0到3之间的一个数
            operation = np.random.rand()          #operation的值是0到1之间的小数

            if pos == 0:
                p.roomId = self.addSub(p.roomId, operation, roomRange)  #如果pos等于0的话，那么对roomID进行变异
            if pos == 1:
                p.weekDay = self.addSub(p.weekDay, operation, 5)   #如果pos等于1的话，那么对weekDay进行变异
            if pos == 2:
                p.slot = self.addSub(p.slot, operation, 5)    #如果pos等于2的话，那么对slot进行变异，对时间进行变异

        return ep
#返回的是种群的一个实体，返回值是ep
    #如果op大于0.5
    def addSub(self, value, op, valueRange):
        if op > 0.5:
            #如果value值小于valueRange，那么就给value+1
            if value < valueRange:
                value += 1
            else:
            #否则给value-1
                value -= 1
        else:
            #如果op<0.5，那么如果value>1，value值就-1
            if value - 1 > 0:
                value -= 1
            else:
                value += 1
            #否则value+1

        return value
#变异方式是，对entity中的每一个实体中的schedule，随机的变化房间数，星期数，时间数。
#因为课程名称/班级号/教室号都是固定值。
#房间数变化/星期数变化/时间数变化
    def crossover(self, eiltePopulation):
    #交叉方式
        """Crossover Operation
        Arguments:
            eiltePopulation: List, population of elite schedules.
    #返回的是population中的列表
        Returns:
            ep: List, population after crossover.
        """
    #返回的是交叉后的种群
        e1 = np.random.randint(0, self.elite, 1)[0]
    #elite是最佳种群数目，self.elite
    #从最佳种群数中选出一个值
        e2 = np.random.randint(0, self.elite, 1)[0]
    #e2也是从最佳种群数中选出一个值
        pos = np.random.randint(0, 2, 1)[0]
    #pos是0，1之间的一个值
        ep1 = copy.deepcopy(eiltePopulation[e1])
    #ep1也是entity的一个实体
        ep2 = eiltePopulation[e2]
    #ep2也是entity的一个实体
        for p1, p2 in zip(ep1, ep2):
    #形成了一个迭代器，ep1和ep2进行循环
            if pos == 0:
                p1.weekDay = p2.weekDay
                p1.slot = p2.slot
            if pos == 1:
                p1.roomId = p2.roomId
    #如果pos=0，那么将p1中的星期数和p2的星期数进行交换，否则将房间号进行交换
        return ep1
    #返回的是要改变的ep1，也就是说，交换后保留了其中一个实体，ep2保持不变

#定义进化函数，输入的是schedules和房间的个数，schedules是用于优化的类
    def evolution(self, schedules, roomRange):
        """evolution

        Arguments:
            schedules: class schedules for optimization.
            elite: int, number of best result.
        Returns:
            index of best result.
            best conflict score.
        """
#主循环中，用于计算最高分bestscore和找到最好的安排方式,
        # Main loop .
        bestScore = 0
        bestSchedule = None

        self.init_population(schedules, roomRange)
#对种群进行初始化，得到初始化后的种群population
        for i in range(self.maxiter):
            eliteIndex, bestScore = schedule_cost(self.population, self.elite)
#进行maxiter次数的迭代，计算当前的分数，采用函数schedule_cost进行计算
            print('Iter: {} | conflict: {}'.format(i + 1, bestScore))
#输出的是conflict
            if bestScore == 0:
                bestSchedule = self.population[eliteIndex[0]]
                break
#如果bestScore等于0，那么就结束循环，否则就继续
            # Start with the pure winners
            newPopulation = [self.population[index] for index in eliteIndex]
#得出的是新的population
            # Add mutated and bred forms of the winners
            while len(newPopulation) < self.popsize:
                if np.random.rand() < self.mutprob:
                    # Mutation
                    newp = self.mutate(newPopulation, roomRange)
                else:
                    # Crossover
                    newp = self.crossover(newPopulation)

                newPopulation.append(newp)

            self.population = newPopulation
#得出新的population。
        return bestSchedule
#输出bestSchedule


import prettytable

from schedule import Schedule
from genetic import GeneticOptimize

#可视化schedule
def vis(schedule):
    """visualization Class Schedule.
    Arguments:
        schedule: List, Class Schedule
    """
    col_labels = ['week/slot', '1', '2', '3', '4', '5']
    table_vals = [[i + 1, '', '', '', '', ''] for i in range(5)]

    table = prettytable.PrettyTable(col_labels, hrules=prettytable.ALL)

    for s in schedule:
        weekDay = s.weekDay
        slot = s.slot
        text = 'course: {} \n class: {} \n room: {} \n teacher: {}'.format(s.courseId, s.classId, s.roomId, s.teacherId)
        table_vals[weekDay - 1][slot] = text

    for row in table_vals:
        table.add_row(row)

    print(table)


if __name__ == '__main__':
    schedules = []

    # add schedule
    schedules.append(Schedule(201, 1201, 11101))
    schedules.append(Schedule(201, 1201, 11101))
    schedules.append(Schedule(202, 1201, 11102))
    schedules.append(Schedule(202, 1201, 11102))
    schedules.append(Schedule(203, 1201, 11103))
    schedules.append(Schedule(203, 1201, 11103))
    schedules.append(Schedule(206, 1201, 11106))
    schedules.append(Schedule(206, 1201, 11106))

    schedules.append(Schedule(202, 1202, 11102))
    schedules.append(Schedule(202, 1202, 11102))
    schedules.append(Schedule(204, 1202, 11104))
    schedules.append(Schedule(204, 1202, 11104))
    schedules.append(Schedule(206, 1202, 11106))
    schedules.append(Schedule(206, 1202, 11106))

    schedules.append(Schedule(203, 1203, 11103))
    schedules.append(Schedule(203, 1203, 11103))
    schedules.append(Schedule(204, 1203, 11104))
    schedules.append(Schedule(204, 1203, 11104))
    schedules.append(Schedule(205, 1203, 11105))
    schedules.append(Schedule(205, 1203, 11105))
    schedules.append(Schedule(206, 1203, 11106))
    schedules.append(Schedule(206, 1203, 11106))
#schedules是初始化种群列表，schedules中包含了22种课程安排
    # optimization
    ga = GeneticOptimize(popsize=50, elite=10, maxiter=500)   #调用GA算法
    res = ga.evolution(schedules, 3)

    # visualization
    vis_res = []
    for r in res:
        if r.classId == 1203:
            vis_res.append(r)
    vis(vis_res)



