#Case number 1:
from CodeLibrary import Simulation
import matplotlib.pyplot as plt


"""Created on the 24.05.2022
@author: Richard ten Hagen
@author contact: Richardxtenxhagen@gmail.com



Case Example Nr 1: In this code we will loop through a list of different Stagenumbers and record what influence that has on the duty, temp and split fraction
The feedstage will be set to be the middle stage. It is a very simple example which shows how it is possible to test a large number of cases for a process design.


1. Proves the capabilty to cycle through a list of values for a input variable.
2. Outputs are extracted for each case.
3. Outputs are plotted to show the influence of the inputs on the design
"""


#This is the list of the Stagenumbers which will be applied
StagenumberList1 = [4,5,6,7,8,9,10,11,12,13]
ColumnName1 = "B3"



#lets first just initalize some stuff

sim = Simulation(AspenFileName= "CaseExample1.bkp", WorkingDirectoryPath= r"c:/Users/s2371014/Desktop/AspenPythonInterface" ,VISIBILITY=False)
        #These are just instanciation of empty lists
OutputList = []
ReboilerTempList = []
ReboilerHeatDutyList = []
CondenserTemperatureList = []
CondenserHeatDutyList = []
SplitfractionTopList = []
SplitfractionBottomList = []




#First we will loop through a list of different Stagenumbers
for Stagenumber1 in StagenumberList1:
    #Change Stagenumber in Aspen
    sim.BLK_RADFRAC_Set_NSTAGE(ColumnName1, Stagenumber1)
    print("\n \n \n Stagenumber was set to be: ", Stagenumber1)
    Feedstage = round(Stagenumber1/2, 0)
    sim.BLK_RADFRAC_Set_FeedStage(ColumnName1,Feedstage, "FEED")
    
    
    
    #Run simulation
    convergence = sim.Run()         #This will run the Simulation
    print("the simulation ran")
    #Suppress dialog
    sim.DialogSuppression(TrueOrFalse= False)
    

    
    #get and print ReboilerTemp
    ReboilerTempList.append(sim.BLK_RADFRAC_Get_Reboiler_Temperature(ColumnName1))
    print("The Reboiler Temp in the Radfrac of B3 ", ReboilerTempList[-1])
    #get and print ReboilerHeatDuty
    ReboilerHeatDutyList.append(sim.BLK_RADFRAC_Get_Reboiler_HeatDuty(ColumnName1))
    print("The ReboilerHeatDuty in the Radfrac of B3 ", ReboilerHeatDutyList[-1])
    #get and print Condenser Temperature
    CondenserTemperatureList.append(sim.BLK_RADFRAC_Get_Condenser_Temperature(ColumnName1))
    print("The CondenserTemperatrue of B3 ", CondenserTemperatureList[-1])
    #get and print Condenser HeatDuty
    CondenserHeatDutyList.append(sim.BLK_RADFRAC_Get_Condenser_HeatingDuty(ColumnName1))
    print("The Condenser Heat Duty of B3 ", CondenserHeatDutyList[-1])
    #Get and print the Splitfraction Top and Bottom
    SplitfractionTop = sim.BLK_RADFRAC_Get_SplitFraction_List(ColumnName1, "S3")
    SplitfractionTopList.append(SplitfractionTop)
    print("The Splitfractioni in the Top flow is: ", SplitfractionTop)
    SplitfractionBottom = sim.BLK_RADFRAC_Get_SplitFraction_List(ColumnName1, "S7")
    SplitfractionBottomList.append(SplitfractionBottom)
    print("The Splitfractioni in the Bottom flow is: ", SplitfractionBottom)
    #Getting the list of compound names 
    CompoundLister = sim.BLK.Elements(ColumnName1).Elements("Output").Elements("MASS_CONC").Elements
    CompoundNameList = []
    for compound in CompoundLister:
        Compoundname = compound.Name
        CompoundNameList.append(Compoundname)
    print(CompoundNameList)









print("\n \n \n \n Everything in the code ran except printing")

plt.figure(1)
plt.title("Reboiler Temperature")
plt.plot(StagenumberList1, ReboilerTempList)
plt.xlabel('Stagenumber')
plt.ylabel('Reboiler temperature')

plt.figure(2)
plt.title("Reboiler Heat duty")
plt.plot(StagenumberList1, ReboilerHeatDutyList)
plt.xlabel('Stagenumber')
plt.ylabel('Reboiler Heat Duty')

plt.figure(3)
plt.title("Condenser Temperature")
plt.plot(StagenumberList1, CondenserTemperatureList)
plt.xlabel('Stagenumber')
plt.ylabel('Reboiler temperature')

plt.figure(4)
plt.title("Condenser Heat Duty")
plt.plot(StagenumberList1, CondenserHeatDutyList)
plt.xlabel('Stagenumber')
plt.ylabel('Condenser Heat Duty')

plt.figure(5)
plt.title("Splitfraction in Top")
plt.plot(StagenumberList1, SplitfractionTopList)
plt.legend(CompoundNameList)
plt.xlabel('Stagenumber')
plt.ylabel('Splitfraction')

plt.figure(6)
plt.title("Splitfraction in Bottom")
plt.plot(StagenumberList1, SplitfractionBottomList)
plt.legend(CompoundNameList)
plt.xlabel('Stagenumber')
plt.ylabel('Splitfraction')




sim.CloseAspen()
plt.show()