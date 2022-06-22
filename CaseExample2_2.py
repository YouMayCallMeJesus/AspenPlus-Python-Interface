#Case number 2:
from ast import Break
from CodeLibrary import Simulation
import scipy
from scipy import optimize
import time
import matplotlib.pyplot as plt
import numpy

"""Created on the 24.05.2022
@author: Richard ten Hagen
@author contact: Richardxtenxhagen@gmail.com



Case Example Nr 2: This code will make use of the brute force optimization algorithm to find the optimal profit for the given flowsheet by varying the following parameters:
- Stagenumber of Column 1
- Reboiler Duty of Column 1
- Stagenumber of Column 1
- Reboiler Duty of Column 1

For the optimization alorithm to be able to function we will need to rewrite our previous process into a function that is called with the variable values as inputs and which returns the profit for the given case.
This function is called: funcToMin and it will return the negative profit.

It consists of multiple substeps:
1. Unpacking the variables(the scipy library wants it that way)
2. Setting the variables into the flowsheet
3. Running the simulation
4. Retrieving the data needed for cost analysis
5. Cost analysis
6. Saving data into global arrays for later plotting and data analysis


The Stagenumber and Reboiler duties will be varies between given maximum and minimum boundries. Since there is a near infinite number of different combinations of these 4 values, which will each have a different expected profit, it will be necessary to find a mechanism by which we can find the maximum profit with minimal number of computations.
This problem is well known in computer science (they call it "non differentiable root finding") and they have developed different algorithms that can solve this. 
In this case we will be using the Brute force method. It functions by taking the minimum and maximum bound of each variable and selecting a given number of values in between (aka Ns = 3) for each variable and then going through the different permutations of these combinations.
It is also possible that the process is repeated multiple times where each finished search reduces the bounds to a smaller section until no further optimization is possible.
This method is usually slow but very reliable in its convergence on the minimum. Unlike most other algorithms it does not make use of stochastic which is a major disadvantage.
"""



#lets first just initalize some stuff

sim = Simulation(AspenFileName= "CaseExample2_2.bkp", WorkingDirectoryPath= r"c:/Users/s2371014/Desktop/AspenPythonInterface" ,VISIBILITY=False)







plottingcounterList = []
BreakEvenYearsForInvestmentList = []
AnnualProfitWithInvestmentCostsList = []
AnnualRevenueList = []
TotalAnnualUtilityCostList = []
vList = []
AnnualInvestmentCostsList = []





#Lets do some optimizing depending on some variables. For this we will need to make a function which will be minimized

def funcToMin(v):
    """ This function changes some Variables in Aspen and returns the number of years until investment is paid off    
    """
    funcToMin.plottingcounter +=1
    ProductStreamnameList = ["S3","S4","S5"]
    ColumnNameList = ["B1", "B2"]


    # Lets first unpack the the variable 
    Blockname1 = ColumnNameList[0]
    Blockname2 = ColumnNameList[1]
    StagenumberColumn1, ReboilerDuty1, StagenumberColumn2, ReboilerDuty2 = v        #These are the variables which the optimizer is allowed to change
    print("The value of v is ", v)



        #Setting the first columns variabels, these are changed by the optimizer
    sim.BLK_RADFRAC_Set_ReboilerDuty(Blockname1 ,ReboilerDuty1)
    sim.BLK_RADFRAC_Set_NSTAGE(Blockname1 ,StagenumberColumn1)
    sim.BLK_RADFRAC_Set_FeedStage(Blockname1,round(StagenumberColumn1/2,0),"S1")
        #Setting the second column
    sim.BLK_RADFRAC_Set_ReboilerDuty(Blockname2 ,ReboilerDuty2)
    sim.BLK_RADFRAC_Set_NSTAGE(Blockname2 ,StagenumberColumn2)
    sim.BLK_RADFRAC_Set_FeedStage(Blockname2,round(StagenumberColumn2/2,0), "S2")




    # Now we run the simulation
    convergence = sim.Run() 
    sim.DialogSuppression(TrueOrFalse= True)
    if convergence == False:
        input("Hey the Convergence failed... why?")                            


    # Get the outputs and print them:
    ##OutputDictColumn1 = sim.BLK_RADFRAC_GET_OUTPUTS(Blockname1)
    ##OutputDictColumn2 = sim.BLK_RADFRAC_GET_OUTPUTS(Blockname2)
    ##print('\n \n Output of first Column \n \n ')
    ##sim.print_dictionary(OutputDictColumn1)
    ##print('\n \n Output of second Column \n \n ')
    ##sim.print_dictionary(OutputDictColumn2)

    #Get inputs for Cost analysis
    Columnpressure1 = sim.BLK_Get_Pressure(Blockname1)
    n_stages1 =sim.BLK_Get_NStages(Blockname1)
    condenser_duty1 = sim.BLK_RADFRAC_Get_Condenser_HeatingDuty(Blockname1)
    reboiler_temperature1 = sim.BLK_RADFRAC_Get_Reboiler_Temperature(Blockname1)
    reboiler_duty1 = sim.BLK_RADFRAC_Get_Reboiler_HeatDuty(Blockname1)
    tops_temperature1 =sim.BLK_RADFRAC_Get_Condenser_Temperature(Blockname1)
    vapor_flows1 =sim.BLK_Get_Column_Stage_Vapor_Flows(Blockname1)
    stage_mw1 = sim.BLK_Get_Column_Stage_Molar_Weights(Blockname1)
    stage_temp1 = sim.BLK_Get_Column_Stage_Temperatures(Blockname1)


    Columnpressure2 =  sim.BLK_Get_Pressure(Blockname2)
    n_stages2=sim.BLK_Get_NStages(Blockname2)
    condenser_duty2= sim.BLK_RADFRAC_Get_Condenser_HeatingDuty(Blockname2)
    reboiler_temperature2 = sim.BLK_RADFRAC_Get_Reboiler_Temperature(Blockname2)
    reboiler_duty2=sim.BLK_RADFRAC_Get_Reboiler_HeatDuty(Blockname2)
    tops_temperature2= sim.BLK_RADFRAC_Get_Condenser_Temperature(Blockname2)
    vapor_flows2=sim.BLK_Get_Column_Stage_Vapor_Flows(Blockname2)
    stage_mw2=sim.BLK_Get_Column_Stage_Molar_Weights(Blockname2)
    stage_temp2=sim.BLK_Get_Column_Stage_Temperatures(Blockname2)



    # Do the Cost analysis
    InvestcostColumn1 = sim.CAL_InvestmentCost(Columnpressure1, n_stages1, condenser_duty1, reboiler_temperature1, reboiler_duty1, tops_temperature1, vapor_flows1, stage_mw1, stage_temp1)
    InvestcostColumn2 = sim.CAL_InvestmentCost(Columnpressure2, n_stages2, condenser_duty2, reboiler_temperature2, reboiler_duty2, tops_temperature2, vapor_flows2, stage_mw2, stage_temp2)
    TotalInvestmentCost = InvestcostColumn1 + InvestcostColumn2
    print("The investment cost of col 1 is: ", InvestcostColumn1, "  The investment cost of col 2 is: ", InvestcostColumn2)

    AnnualUtilityCostColumn1 = sim.CAL_Annual_OperatingCost(reboiler_duty1, condenser_duty1)
    AnnualUtilityCostColumn2 = sim.CAL_Annual_OperatingCost(reboiler_duty2, condenser_duty2)
    TotalAnnualUtilityCost =  AnnualUtilityCostColumn1 + AnnualUtilityCostColumn2
    print("Total annual cost in col 1 is: ", AnnualUtilityCostColumn1,"  Total annual cost in col 2 is: ", AnnualUtilityCostColumn2)

        #Check all streams to find the value of each stream
    AnnualRevenue = 0
    for ProductStreamname in ProductStreamnameList:
        StreamDictionary = sim.STRM_GET_OUTPUTS(ProductStreamname)
        MoleFlowList = StreamDictionary["MoleFlowList"]
        product_specification = 0.95
        total_stream_value, component_purities = sim.CAL_stream_value( MoleFlowList, product_specification)        
        if total_stream_value != 0: print("For ", ProductStreamname, " the total stream value is: ", total_stream_value)
        AnnualRevenue = AnnualRevenue + total_stream_value

    AnnualProfit = AnnualRevenue - TotalAnnualUtilityCost
    if AnnualProfit >0: print("The total Annual Profit is: ", AnnualProfit)
    BreakEvenYearsForInvestment = TotalInvestmentCost/AnnualProfit
    if BreakEvenYearsForInvestment >0: print("The Return on investment is: ", BreakEvenYearsForInvestment)
    
    AnnualInvestmentCosts = TotalInvestmentCost/20
    AnnualProfitWithInvestmentCosts = AnnualRevenue - TotalAnnualUtilityCost - AnnualInvestmentCosts




#Tests to make sure the units are correct    
    if TotalAnnualUtilityCost <0: 
        print("Hold on Utility costs are negative... that should not be the case... lets punish with 30")
        return 30
    if AnnualRevenue <0:
        print("Hold on AnnualRevenue is negative... that should not be the case")
        return 30
    
    
    


    #Saving the internal function Data into the Global list variables
    BreakEvenYearsForInvestmentList.append(BreakEvenYearsForInvestment)
    AnnualRevenueList.append(AnnualRevenue)
    TotalAnnualUtilityCostList.append(TotalAnnualUtilityCost)
    AnnualInvestmentCostsList.append(AnnualInvestmentCosts)
    vList.append(v)

    AnnualProfitWithInvestmentCostsList.append(-AnnualProfitWithInvestmentCosts)
    plottingcounterList.append(funcToMin.plottingcounter)



    #plt.figure(1)
    #plt.clf()    
    #plt.plot(plottingcounterList, AnnualProfitWithInvestmentCostsList,"*")
    #plt.title("Negative Profit(including investment costs)")
    #plt.draw()
    #plt.pause(0.001)




    return -AnnualProfitWithInvestmentCosts
    
funcToMin.plottingcounter = 0       #Instanciate the function attribute such that it zero the first time it is called.

"""


    plt.figure(2)
    plt.clf()
    RunningMean = sim.running_mean(BreakEvenYearsForInvestmentList,20)
    plt.plot(plottingcounterList, RunningMean,"*")
    plt.title("Running mean of ROI")
    plt.draw()
    plt.pause(0.1)
"""

## THIS FUNCTION DOES OPTIMIZATIONS..... 


# define the bounds on the search of #StagenumberColumn1, ReboilerDuty1, StagenumberColumn2, ReboilerDuty2
bounds = [[2, 20], [100, 100000],[2,20],[100,100000]]

#If you want to use brute force
results = optimize.brute(funcToMin,bounds,Ns=3)
#If you want evolutionary strategy
#results = optimize.differential_evolution(funcToMin, bounds, args=(), strategy='best1bin', maxiter=10, popsize=10, tol=0.01, mutation=(0.5, 1), recombination=0.7, seed=None, callback=None, disp=False, polish=True, init='latinhypercube', atol=0, updating='immediate', workers=1, constraints=(), x0=None)
        #Maximum number of function calls is: (maxiter + 1) * popsize * len(x)





#print the results and values:
print("\n\n\n\n\nThe plottingcounterList is : ",plottingcounterList,"\n\n\n\n")
print("\n\n\n\n\nThe AnnualProfitWithInvestmentCostsList is : ",AnnualProfitWithInvestmentCostsList,"\n\n\n\n")
print("\n\n\n\n\nThe AnnualRevenueList is : ",AnnualRevenueList,"\n\n\n\n")
print("\n\n\n\n\nThe AnnualInvestmentCostsList is : ",AnnualInvestmentCostsList,"\n\n\n\n")
print("\n\n\n\n\nThe BreakEvenYearsForInvestmentList is : ",BreakEvenYearsForInvestmentList,"\n\n\n\n")
print("\n\n\n\n\nThe TotalAnnualUtilityCostList is : ",TotalAnnualUtilityCostList,"\n\n\n\n")
print("\n\n\n\n\nThe vList is : ",vList,"\n\n\n\n")




plt.figure(1)
   
plt.plot(plottingcounterList, AnnualProfitWithInvestmentCostsList,"*")
plt.title("Negative Profit(including investment costs)")
plt.show()
plt.savefig("NegativeProfitBrute")
plt.clf() 
plt.plot(plottingcounterList, AnnualRevenueList,"*")
plt.title("Annual Revenue")
plt.show()
plt.savefig("AnnualRevenueBrute")
plt.clf() 
plt.plot(plottingcounterList, AnnualInvestmentCostsList,"*")
plt.title("Annual Revenue")
plt.show()
plt.savefig("AnnualInvestmentCostsBrute")
plt.clf() 
plt.plot(plottingcounterList, BreakEvenYearsForInvestmentList,"*")
plt.title("Return on Investment years")
plt.show()
plt.savefig("ROIyearsBrute")
plt.clf() 
plt.plot(plottingcounterList, TotalAnnualUtilityCostList,"*")
plt.title("Annual utility costs")
plt.show()
plt.savefig("AnnualUtilityCostsBrute")
plt.clf() 

print("Hey the results are:")
print(results)
input("Hey are you happy with life?")

#print("\n\n\nThe total runtime was: ", runtimetotal)

#print("Number of Stages in Column 1")
#print(results["StagenumberColumn1"])
#print("Number of Stages in Column 2")
#print(results["StagenumberColumn2"])
#print("ReboilerDuty1")
#print(results["ReboilerDuty1"])
#print("ReboilerDuty2")
#print(results["ReboilerDuty1"])


"""
# objective function
def objective(v):
	x, y = v
	return -20.0 * exp(-0.2 * sqrt(0.5 * (x**2 + y**2))) - exp(0.5 * (cos(2 * pi * x) + cos(2 * pi * y))) + e + 20
 
# define range for input
r_min, r_max = -5.0, 5.0
# define the bounds on the search
bounds = [[r_min, r_max], [r_min, r_max]]
# perform the differential evolution search
result = differential_evolution(objective, bounds)
# summarize the result
print('Status : %s' % result['message'])
print('Total Evaluations: %d' % result['nfev'])
# evaluate solution
solution = result['x']
evaluation = objective(solution)
print('Solution: f(%s) = %.5f' % (solution, evaluation))





plt.ion()
for i in range(100):
    x = range(i)
    y = range(i)
    # plt.gca().cla() # optionally clear axes
    

plt.show(block=True)








"""










def print_dictionary(dct):
    """ Takes Dictionary input with two items inside and prints them"""
    print("Items held:")
    for item, amount in dct.items():  # dct.iteritems() in Python 2
        print("{} ({})".format(item, amount))




sim.CloseAspen()
