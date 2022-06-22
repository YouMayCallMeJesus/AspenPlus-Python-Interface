#from ast import AugAssign
from CodeLibrary import Simulation


#############################################################################################################################################



#TTTTTTTTTTTTTTTT       U           U   #TTTTTTTTTTTTTTTT   OOOOOOOOOOOOOOOOO       RRRRRRRRRRRRR       I           A
        #               U           U           #           O               O       R           R       I          A A
        #               U           U           #           O               O       R           R       I         A   A
        #               U           U           #           O               O       R           R       I        A     A
        #               U           U           #           O               O       RRRRRRRRRRRRR       I       A       A
        #               U           U           #           O               O       R   R               I       AAAAAAAAAA
        #               U           U           #           O               O       R      R            I      A          A
        #               U           U           #           O               O       R         R         I     A            A
        #               UUUUUUUUUUUU            #           OOOOOOOOOOOOOOOOO       R           R       I   A               A


#########################################################################################################################################

#       To use the tutorial just run this program and read the Terminal

#Contents:
        #1. Connecting Aspen to Python
        #2. Retrieving inputs from CISTRS, DSTWU, RPLUG as dictionaries
        #3. Running simulations + Dialog suppression
        #4. Extracting results from CISTR, DSTWU, RPLUG as dictionaries
        #5. Extracting results about Stream as dictionaries
        #6. Extracting singluar values from the results
        #7. Changing singlular values in Equipment
        #8. Errorhandeling in case of non convergence
        #9. Adding new process units
        #10. Adding new streams
        #11. Connecting streams
        #12. Using dictionaries to set necessary inputs
        #13. Creating reports
        #14. Saving Aspen







print("\nThe Library ran without any Syntax Error \n")

#1. instanciate the class and set the aspen name, file path and visibilty
input("To open Aspen and instanciate the Simulation Class: Press any Enter to continue  \n")
sim = Simulation(AspenFileName= "AspenTutorial.bkp", WorkingDirectoryPath= r"c:/Users/s2371014/Desktop/AspenPythonInterface" ,VISIBILITY=True)

#Look at aspen
print("Aspen should have opened now. Please take a look at it  \n \n")
input("Now we will start to work with the interface. Press enter to continue \n")
print("First we will try to retrieve some data about the different reactors which we are working with. \nFor this we can use the sim.Functions(), In this case we will use sim.BLK_CISTR_GET_ME_ALL_INPUTS_BACK(B1). \n")

#2. CISTR input summary
input("We will now retrieve the inputs of the CISTR which were already set by me and then print it, Press enter")
CISTRInputDictionary = sim.BLK_CISTR_GET_ME_ALL_INPUTS_BACK("RCSTR")
print(" \n \n The inputs which were made for RCSTR are summarized below: \n ")
sim.print_dictionary2(CISTRInputDictionary)

# RPLUG input summary
input("\n\nAbove you can read the CISTRs inputs and now we will also do the same for the RPLUG, press enter ")
RPLUGInputDictionary = sim.BLK_RPLUG_GET_ME_ALL_INPUTS_BACK("RPLUG")
print(" \n  \n The inputs which were made for RPLUG are summarized below: \n ")
sim.print_dictionary(RPLUGInputDictionary)
print(" \n \n \n As you can see most variabels are not actually needed for the simulation to run and remain --None-- \n They are be used for more detailed descriptions of the reactor. \n")

#3. Run simulation
input("Now lets see if we can run the simulation: Press enter to continue \n")
sim.EngineRun()         #generally speaking it is advised to only use sim.Run() since that is more reliable and it contains error handeling
print("\n        it ran without error \n")

#Dialog suppression
input("As you can see there is a message in the Aspen program which informs you that the simulation ran sucessfully. Please click this pop up away for now. \n \n To suppress future dialog sim.DialogSuppression(True) is used, press enter to continue\n")
sim.DialogSuppression(TrueOrFalse= True)
print("This DialogSuppression is necessary otherwise Aspen will get stuck \n")

#4. Output Summary for RPLUG
input("\n After running an aspen simulation it is common that one will try to find out what the calculations yielded,\nThis is done by a sim.BLK_RPLUG_GET_OUTPUTS(RPLUG) command. \n Please press enter to continue \n\n ")
RPLUGOutputDictionary = sim.BLK_RPLUG_GET_OUTPUTS("RPLUG")
sim.print_dictionary(RPLUGOutputDictionary)

# Output Summary for RCISTR
input("\n Now we will get all the outputs from the RCSTR \n Please press enter \n \n ")
RCSTROutputDictionary = sim.BLK_RCSTR_GET_OUTPUTS("RCSTR")
sim.print_dictionary(RCSTROutputDictionary)

#5. Output Summary for the Product Stream of RPLUG
input(" \n  \n Until now we have only read the inputs and outputs of an block but for compositions we will need to extract them from a stream.\nThis will be done via sim.STRM_GET_OUTPUTS. The output stream of the RPLUG is summarized below: \n Please press enter \n \n ")
RPLUGStreamDictionary = sim.STRM_GET_OUTPUTS("RPLUGOUT")
sim.print_dictionary(RPLUGStreamDictionary)

# Output Summary for the Product Stream of CISTR
input(" \n  \n The output stream of the RCISTR is summarized below: \n  Please press enter \n \n ")
CISTRStreamDicitonary = sim.STRM_GET_OUTPUTS("RCSTROUT")
sim.print_dictionary(CISTRStreamDicitonary)

#6. Extracting singlular value ouputs
input("\n\nThese output dictionaries which we have seen until now are collections of functions but in some cases it might be useful to not extract all the different variables when we are only intersted in one.\nFor this we can for example use the sim.BLK_RCSTR_Get_HeatDuty(RCSTR). Each value inside of the dictionaries also has a corresponding single value function,\nPlease press enter")
HeatDuty = sim.BLK_RCSTR_Get_HeatDuty(Blockname="RCSTR")
print("This allows us to extract only the Heatduty:    ", HeatDuty, "\n\n")


#7. CHANGE INPUT for one value
input("Lets imagine that we have noticed a problem and we would like to change the lightkey recovery in the destillation column \n Press enter \n")
print("We shall set the lightkey recovery from 0.95 to only 0.06 \nThis is done with sim.BLK_DSTWU_Set_LightkeyRecovery(B1, 0.06)\nThe documentation to this library can be used to find the function names to every variable in AspenPlus\n")
sim.BLK_DSTWU_Set_LightkeyRecovery("B1", 0.06)

#8. Run the simulation and let it fail
input("Now we shall run the simulation again using --convergence=sim.Run()-- (which should fail to converge with such obsurde inputs), Press enter \n")
convergence = sim.Run()
print("The convergence variable which is returned by the Run function tells you if the simulation was successful. \n")
print("In this case the convergence variable is: ", convergence, "\n This is very useful since aspen has the tendency to not converge and this needs to be dealt with by your errorhandler")

#change inputs back to normal
input("\nNow that we saw that it failed lets change the inputs back to the original, Press enter")
sim.BLK_DSTWU_Set_LightkeyRecovery("B1", 0.95)


#9. Add a new block
input("\nUntil now we have learned how to retrieve inputs and output, change inputs, run the simulation and handle errors. The next step is to learn how to edit the flowsheet.\n\nDownstream of the reactor I would like to add another new DSTWU destillation column, this will be done with sim.BlockPlace(B6, DSTWU) \n Press enter")
sim.BlockPlace("B6","DSTWU")


#10. place stream 
input("\nWe now need to place the streams on the flowsheet using the sim.StreamPlace(S19, MATERIAL) \nPlease press enter ")
sim.StreamPlace(Streamname="S1", Streamtype= "MATERIAL")
sim.StreamPlace(Streamname="S2", Streamtype= "MATERIAL")


#11. connect streams
input("\nThe next step is connecting the streams. For this we will use the sim.StreamConnect(B6, NewDestillTop, D(OUT)), This is done for the top bottom and feed, \n Please press enter")
        #Connect the outlet of RPLUG to the Destillation column
sim.StreamConnect(Blockname="B6",Streamname="RPLUGOUT", Portname="F(IN)")
        #Connect the Top and bottom
sim.StreamConnect(Blockname="B6", Streamname="S1", Portname="D(OUT)")
sim.StreamConnect(Blockname="B6", Streamname="S2", Portname="B(OUT)")



#12. use the dictionary to set the inputs(Refluxratio, lightkey recovery.....) for the new column
input("\nNow that we have placed the column and connected all the streams there is only one thing which is missing and that is to set the inputs of the DSTWU \nThis could be done by going through the documentation and setting each value but I am lazy, which means we will just use the same settings as the first column.\nThis is very easy since the BLK_DSTWU_GET_ME_ALL_INPUTS returns a dictionary which can be used as the input for the BLK_DSTWU_SET_INPUTS\nPress enter")
        #extract the inputs of the first DSTWU as a dictionary
OldDSTWUinputDictionary = sim.BLK_DSTWU_GET_ME_ALL_INPUTS_BACK("B1")
        #Use this dictionary to set the NewDestill
sim.BLK_DSTWU_SET_ALL_INPUTS("B6", OldDSTWUinputDictionary)



#Run the simulation and print convergence state:
input("\nWe now made the second column more or less a -clone- of the first one. Lets test if it will converge by running the simulation, \nPlease press enter")
converged = sim.Run()
print("Was the convergence successful? ", converged , " \n")


#13. Create some reports
input("\nWe are now done with editing, we have learned how to add new equipment and streams, how to connect them and how to set the inputs for these blocks.\n\nThe next step in the process would be the creation of some reports such that we can remember this specific design which we have created.\nFor this we will save a Summary, Report and InputFile into the directory where we are currently working\nPlease press enter")
sim.ExportReportFile("TutorialReportFile")
sim.ExportInputFile("TutorialInputFile")
sim.ExportRunMessagesFile("TutorialRunMessageFile")
sim.ExportSummaryFile("TutorialSummaryFile")
sim.ExportInputFileWithGraphics("TutorialInputGraphics")

input("\n\nPlease take the time to look at the exported files, the most important ones being the TutorialReportFile and TutorialInputFile\nThese can be used to understand what design your optimization algorithm has found without needing to open it in Aspen.\nThe input file can also be loaded into aspen and it is comparable to a backupfile in that sense(except that a human can read it)\nPlease press enter to continue")

#14. Save it
input("\nAs a final step for this tutorial we will save the current Aspen file as AspenfileAfterTutorial.bkp\nPlease press enter to continue")
sim.SaveAs("AspenfileAfterTutorial.bkp", True)






print(" \n\n\n              END OF TUTORIAL \n\n\n")

sim.CloseAspen()