from deap import base, creator, gp, tools, algorithms
from FactorModule.FactorShow import FactorShow
from DataReaderModule.Constants import ALIAS_RESPONSE as alr
from DataReaderModule.Constants import ALIAS_INDICATORS as ali
from CalculatorModule import  OperatorPool
from FactorModule.FactorUpdate import update_factors
import pandas as pd
import numpy
import random
import gc
import _thread
factorDefPath = r'..\FactorPool\factors_mqh'  # 因子定义路径
factorDataPath = r'..\FactorPool\factors_mqh_data'  # 因子数据路径
factorRiskPath = r'..\FactorPool\risk_factors_data'# 风险因子数据路径

field = { "ARG0": "needData[t.OPEN]",              #定义变量
    "ARG1" : "needData[t.HIGH]",
    "ARG2" : "needData[t.LOW]",
    "ARG3" : "needData[t.CLOSE]",
    "ARG4" : "needData[t.VOLUME]",
    "ARG5" : "needData[t.AMOUNT]",
    "ARG6" : "needData[t.PCTCHG]",
    "ARG7" : "needData[t.PRCCHG]",
    "ARG8" : "needData[t.VWAP]",
    "ARG9": "needData[t.ADJOPEN]",
    "ARG10" : "needData[t.ADJCLOSE]",
    "ARG11" : "needData[t.MKTCAP]",
    "ARG12" : "needData[t.MKTCAPFL]",
    "ARG13" : "needData[t.SHR]",
    "ARG14" : "needData[t.SHRFREE]",
    "ARG15" : "needData[t.TURN]",
    "ARG16" : "needData[t.NETASSET]",
    "ARG17" : "needData[t.OPERREVTTM]",
    "ARG18" : "needData[t.OPERREVLYR]",
    "ARG19" : "needData[t.NETPCMTTM]",
    "ARG20" : "needData[t.NETCASHLYR]",
    "ARG21" : "needData[t.INCRCASHTTM]",
    "ARG22" : "needData[t.INCRCASHLYR]",
    "ARG23" : "needData[t.PE]",
    "ARG24" : "needData[t.PETTM]",
    "ARG25" : "needData[t.PB]",
    "ARG26" : "needData[t.PCFOCF]",
    "ARG27" : "needData[t.PCFOCFTTM]",
    "ARG28" : "needData[t.PS]",
    "ARG29" : "needData[t.PSTTM]",
    "ARG30" : "needData[t.PDD]"}

def create_needfield(individual):  #输出因子文件中的needfield
    dic=gp.graph(individual)[2]
    needfield="["
    for key in dic.keys():
        if "needData" in dic[key]:
            needfield+=dic[key][9:-1]+","
    needfield=needfield[0:-1]+"]"
    for x in locals().keys():  #清除局部变量
        del locals()[x]
    gc.collect()
    return needfield

def exp2fctpy(expression, needfield): #写入因子文件
    s = "#!/usr/bin/env Python\n# -*- coding:utf-8 -*-\n# author: mqh\nimport time\nimport numpy as np\nimport pandas as pd\nimport math\n\
from FactorModule.mqhBase import FactorBase\nfrom DataReaderModule.Constants import ALIAS_FIELDS as t\n\
from CalculatorModule.OperatorPool import *\n\
class Factor(FactorBase):\n\tdef __init__(self):\n\t\tsuper(Factor, self).__init__()\n\
\t\tself.neutral = True\n\
\t\tself.factorName = __name__.split('.')[-1]\n\
\t\tself.needFields = list(set("+needfield+"))# 设置需要的字段\n\
\tdef factor_definition(self):\n\t\ts = time.time()\n\t\tneedData = self.needData  # 计算所需数据\n\
\t\tfactor="+expression+"\n\
\t\tprint('factor {0} done with {1} seconds'.format(self.factorName, time.time() - s))\n\t\treturn factor\n\tdef run_factor(self):\n\t\tself.run()\nfct = Factor()\nfct.run_factor()"
    for x in locals().keys(): #清除局部变量
        del locals()[x]
    gc.collect()
    return s

def cal_fitness(genmark):  #计算适应度：0.8*sharp-0.2*turnover
    fctname = "genticT" + genmark
    path = r'factors_mqh//' + fctname + ".py"
    failures = update_factors(factorList=[fctname], #通过update计算sharp
                              factorDefPath=factorDefPath,
                              factorDataPath=factorDataPath,
                              factorRiskPath=factorRiskPath,
                              startOver=True,
                              indexFactor=False,
                              preDateNum=90)
    obj = FactorShow(fctDataPath=r'..\FactorPool\factors_mqh_data',
                     fctRiskPath=r'..\FactorPool\risk_factors_data')
    headDate = 20080101
    tailDate = None
    sharp=obj.show_statistics(factorName=fctname, #通过show读取sharp
                        headDate=headDate,
                        tailDate=tailDate,
                        responses=[alr.OC1,alr.CCG1],
                        indicators=[ali.TBDF])
    #[alr.OC1, alr.OCG1, alr.OCG2, alr.CCG1, alr.CCG2]
    sharpfit=[]
    for key in sharp.keys():
        sharpfit.append(float(sharp[key].iloc[:,1].min()))
    turnover = obj.show_turnover(factorName=fctname, #通过show计算turnover
                        headDate=headDate,
                        tailDate=tailDate).iloc[0,0]
    for fit in sharpfit:
        fit=0.8*fit-0.2*turnover
    fitness=tuple(sharpfit)
    #fitness=0.8*sharpfit-0.2*turnover
    for x in locals().keys(): #清除局部变量
        del locals()[x]
    gc.collect()
    return fitness
def writefct(individual,genmark):
    expression = str((individual))
    needfield=create_needfield(individual)
    fct = exp2fctpy(expression,needfield)
    fctname = "genticT"+genmark
    path = r'factors_mqh//' + fctname + ".py"
    f = open(path,'w',encoding='UTF-8')
    f.write(fct)
    f.close()
    for x in locals().keys(): #清除局部变量
        del locals()[x]
    gc.collect()
if __name__ == "__main__":
    df=pd.core.frame.DataFrame
    pset=gp.PrimitiveSetTyped("main",[df for i in range(9)],df) #deap注册变量
    pset.renameArguments(**field)
    operator = dir(OperatorPool)[9:]  #读取OperatorPool中的操作函数
    operator.remove("np")
    for i in range(len(operator)): #deap注册操作函数
        func="OperatorPool."+operator[i]
        para = list(eval(func).__code__.co_varnames)
        for j in range(len(para)):
            if para[j]=="cond":
                para[j]=bool
            else:
                para[j]=df
        if "cond" in func:
            ret=bool
        else:
            ret=df
        pset.addPrimitive(eval(func),para,ret)
    #pset.addEphemeralConstant("randnum", lambda: random.randint(1,30) , int)
    creator.create("FitnessMax", base.Fitness, weights=(1.0,1.0)) #deap注册适应度
    creator.create("Individual", gp.PrimitiveTree, fitness=creator.FitnessMax,genmark="0_0")#deap注册个体
    toolbox = base.Toolbox()
    toolbox.register("expr", gp.genHalfAndHalf, pset=pset, min_=3, max_=6) #toolbox注册个体生成函数
    toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.expr) #toolbox注册个体
    toolbox.register("population", tools.initRepeat, list, toolbox.individual) #toolbox注册群体
    toolbox.register("compile", gp.compile, pset=pset) #toolbox注册编译函数
    toolbox.register("evaluate",cal_fitness) #toolbox注册适应度函数
    toolbox.register("select", tools.selTournament, tournsize=3) #toolbox注册选择函数
    toolbox.register("mate", gp.cxOnePoint) #toolbox注册交叉函数
    toolbox.register("expr_mut", gp.genFull, min_=1, max_=3) #toolbox注册生成变异函数
    toolbox.register("mutate", gp.mutUniform, expr=toolbox.expr_mut, pset=pset) #toolbox注册变异函数
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", numpy.mean,axis=0) #获得统计信息
    stats.register("std", numpy.std,axis=0)
    stats.register("min", numpy.min,axis=0)
    stats.register("max", numpy.max,axis=0)
    cxpb, mutpb, ngen = 0.5, 0.2, 8 #设定交叉概率、变异概率、世代数量
    fits = []
    gen = 0
    pop = toolbox.population(n=10)  #生成含有n个个体的群体
    for ind in pop: #计算个体适应度
        genmark = str(gen) + "_" + str(pop.index(ind))
        ind.genmark=genmark  #生成进化标签，以供写入因子文件函数使用
        writefct(ind, genmark)
    for ind in pop:
        fitvalue = toolbox.evaluate(ind.genmark) #计算适应度
        ind.fitness.values = fitvalue
    gen += 1
    print(stats.compile(pop))
    for g in range(ngen): #开始进化
        offspring = toolbox.select(pop, k=len(pop))
        offspring = list(map(toolbox.clone, offspring))
        for child1, child2 in zip(offspring[::2], offspring[1::2]): #进行交叉
            if random.random() < cxpb:
                toolbox.mate(child1, child2)
                del child1.fitness.values
                del child2.fitness.values
        gc.collect()
        for mutant in offspring: #进行变异
            if random.random() < mutpb:
                toolbox.mutate(mutant)
                del mutant.fitness.values
        gc.collect()
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitness = []
        for ind in invalid_ind: #计算个体适应度（经过交叉或者变异操作的个体）
            genmark = str(gen) + "_" + str(offspring.index(ind))
            ind.genmark = genmark
            writefct(ind, genmark)
        for ind in invalid_ind:
            fitvalue = toolbox.evaluate(ind.genmark)
            ind.fitness.values = fitvalue
        pop[:] = offspring #得到新一代
        gen += 1
        print(stats.compile(pop)) #打印统计信息