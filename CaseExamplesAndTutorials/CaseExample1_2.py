#Case number 1:
from CodeLibrary import Simulation
import matplotlib.pyplot as plt


"""Created on the 24.05.2022
@author: Richard ten Hagen
@author contact: Richardxtenxhagen@gmail.com



Case Example Nr 1: In this code we will loop through a list of Stagenumbers in two different columns and record what influence that has on the duty, temp and split fraction
The feedstage will be set to be the middle stage. This shows the power of doing extensive searches in aspen since the same procedure can be used to loop through even more variables to find a wanted optimum.
This process will be automated even further in CaseExample2_1 where the set of possible variables becomes so large that it can no longer be effectivly tested.

1. loop through each column
2. for each column loop through Stagenumbers
3. set the Stagenumber and run the simulation
4. extract output variables
5. plot them to show differences in each column
"""


#This is the list of the Stagenumbers which will be applied
StagenumberList1 = [5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21]
ColumnnameList = ["B3","B4"]
FeedStreamList = ["FEED", "S3"]
TopStreamList = ["S3","S9"]
BottomStreamList = ["S7","S8"]


#lets first just initalize some stuff
sim = Simulation(AspenFileName= "CaseExample1.bkp", WorkingDirectoryPath= r"c:/Users/s2371014/Desktop/AspenPythonInterface" ,VISIBILITY=False)
        #These are just instanciation of empty lists
n = 0


for ColumnName1 in ColumnnameList:
    #First we will loop through a list of different Stagenumbers
    OutputList = []
    ReboilerTempList = []
    ReboilerHeatDutyList = []
    CondenserTemperatureList = []
    CondenserHeatDutyList = []
    SplitfractionTopList = []
    SplitfractionBottomList = []
    
    for Stagenumber1 in StagenumberList1:
        #Change Stagenumber in Aspen
        sim.BLK_RADFRAC_Set_NSTAGE(ColumnName1, Stagenumber1)
        print("\n \n \n Stagenumber was set to be: ", Stagenumber1)
        Feedstage = round(Stagenumber1/2, 0)
        sim.BLK_RADFRAC_Set_FeedStage(ColumnName1,Feedstage, FeedStreamList[n])
        
        
        
        #Run simulation
        convergence = sim.Run()         #This will run the Simulation
        print("the simulation ran")
        #Suppress dialog
        sim.DialogSuppression(TrueOrFalse= True)
        

        
        #get and print ReboilerTemp
        ReboilerTempList.append(sim.BLK_RADFRAC_Get_Reboiler_Temperature(ColumnName1))
        print("The Reboiler Temp in the Radfrac of ",ColumnName1, ReboilerTempList[-1])
        #get and print ReboilerHeatDuty
        ReboilerHeatDutyList.append(sim.BLK_RADFRAC_Get_Reboiler_HeatDuty(ColumnName1))
        print("The ReboilerHeatDuty in the Radfrac of ",ColumnName1, ReboilerHeatDutyList[-1])
        #get and print Condenser Temperature
        CondenserTemperatureList.append(sim.BLK_RADFRAC_Get_Condenser_Temperature(ColumnName1))
        print("The CondenserTemperatrue of ",ColumnName1, CondenserTemperatureList[-1])
        #get and print Condenser HeatDuty
        CondenserHeatDutyList.append(sim.BLK_RADFRAC_Get_Condenser_HeatingDuty(ColumnName1))
        print("The Condenser Heat Duty of ",ColumnName1, CondenserHeatDutyList[-1])
        #Get and print the Splitfraction Top and Bottom
        SplitfractionTop = sim.BLK_RADFRAC_Get_SplitFraction_List(ColumnName1, TopStreamList[n])
        SplitfractionTopList.append(SplitfractionTop)
        print("The Splitfractioni in the Top flow is: ", SplitfractionTop)
        SplitfractionBottom = sim.BLK_RADFRAC_Get_SplitFraction_List(ColumnName1, BottomStreamList[n])
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
    titel = "Reboiler Temperature  " + ColumnName1
    plt.figure(1+(6*n))
    plt.title(titel)
    plt.plot(StagenumberList1, ReboilerTempList)
    plt.xlabel('Stagenumber')
    plt.ylabel('Reboiler temperature')

    titel = "Reboiler Heat duty  " + ColumnName1
    plt.figure(2+(6*n))
    plt.title(titel)
    plt.plot(StagenumberList1, ReboilerHeatDutyList)
    plt.xlabel('Stagenumber')
    plt.ylabel('Reboiler Heat Duty')

    titel = "Condenser Temperature  " + ColumnName1
    plt.figure(3+(6*n))
    plt.title(titel)
    plt.plot(StagenumberList1, CondenserTemperatureList)
    plt.xlabel('Stagenumber')
    plt.ylabel('Reboiler temperature')

    titel = "Condenser Heat Duty " + ColumnName1
    plt.figure(4+(6*n))
    plt.title(titel)
    plt.plot(StagenumberList1, CondenserHeatDutyList)
    plt.xlabel('Stagenumber')
    plt.ylabel('Condenser Heat Duty')

    titel = "Splitfraction in Top " +ColumnName1
    plt.figure(5+(6*n))
    plt.title(titel)
    plt.plot(StagenumberList1, SplitfractionTopList)
    plt.legend(CompoundNameList)
    plt.xlabel('Stagenumber')
    plt.ylabel('Splitfraction')

    titel = "Splitfraction in Bottom  " +ColumnName1
    plt.figure(6+(6*n))
    plt.title(titel)
    plt.plot(StagenumberList1, SplitfractionBottomList)
    plt.legend(CompoundNameList)
    plt.xlabel('Stagenumber')
    plt.ylabel('Splitfraction')



    #This counter is there to make sure that the figure numbering is correct 
    n= n+1


sim.CloseAspen()

plt.show()


