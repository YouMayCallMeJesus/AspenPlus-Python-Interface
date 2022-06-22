from fileinput import filename
import os
from re import A
from tokenize import String
from typing import Union, Dict, Literal
import win32com.client as win32
import numpy as np
import time
#from scripy import optimize


"""Created on the 24.05.2022
@author: Richard ten Hagen
@author contact: Richardxtenxhagen@gmail.com



API for controlling the Aspen Python Interface automatically

If you change it, update it, fix something just email me such that I can also update my version to keep it as coherent as possible
"""



class Simulation():
    """Class which starts a Simulation interface instance
    
    Args:
        AspenFileName: Name of the Aspenfile on which you are working with
        WorkingDirectoryPath: Path to the Folder where we will be working
        VISIBITLITY: Toggles the opening and interactive running of the Aspen simulation
    """
    AspenSimulation = win32.gencache.EnsureDispatch("Apwn.Document")

    def __init__(self, AspenFileName:str, WorkingDirectoryPath:str, VISIBILITY:bool = True):
        print("The current Directory is :  ")
        print(os.getcwd())                      #Returns the Directory where it is currently working
        os.chdir(WorkingDirectoryPath)          #Changes the Directory to  ..../AspenSimulation
        print("The new Directory where you should also have your Aspen file is : ")
        print(os.getcwd())          
        self.AspenSimulation.InitFromArchive2(os.path.abspath(AspenFileName))
        print("The Aspen is active now. If you dont want to see aspen open again take VISIBITLY as False \n")
        self.AspenSimulation.Visible = VISIBILITY

    def CloseAspen(self):
        AspenFileName = self.Give_AspenDocumentName()
        print(AspenFileName)
        self.AspenSimulation.Close(os.path.abspath(AspenFileName))
        print("\nAspen should be closed now")

#This just shortens the path you need to call for Streams and Blocks

    @property
    def BLK(self):
        """Property: Defines Path to the Block node in Aspen File system. 
            
        Aspendocument is defined in the Class Simulation initialization
        """
        return self.AspenSimulation.Tree.Elements("Data").Elements("Blocks") 



    @property
    def STRM(self):
        """Property: Defines Path to the Streamnode node in Aspen File system. 
            
        Aspendocument is defined in the Class Simulation initialization
        """
        return self.AspenSimulation.Tree.Elements("Data").Elements("Streams")



    #Type definition to simplify the type hinting:
    Phnum = Literal[1,2,3]
    Ph = Literal["L", "V", "S"]








##############################################################################################################################


#PPPPPPPPPPPPP          OOOOOOOOOoOOOO  W                 W     Eeeeeeeeeeeeeee     RRRRRRRRRRRRRRR
#               P       O            O   W                W     E                   R               R
#               P       O            O    W               W     E                   R               R
#               P       O            O    W       W      W      E                   R               R
#            P          O            O     W      W      w      E                   RRRRRRRRRRRRRRRR
#PPPPPPPPPPPP           O            O     W      W      W      Eeeeeeeeeeeeeee     RR
#                       O            O     W      W      W      E                   R   R
#                       O            O      W    W  W    W      E                   R       R
#                       O            O       W   W  W   W       E                   R           R
#                       O            O        W W    W W        E                   R             R
#                       OOOOOOOOOOOOOOO        W      W         Eeeeeeeeeeeeeee     R               R


###################################################################################################################################




####Generalized Powerfunctions:

#Related to Placing Blocks, connecting, removing and such things:
    def BlockDelete(self, Blockname:str) ->None:
        """Removes Block with given Name from the Aspen Simulation 
            
        All data (Input+Outputs+Simulationdata+InitialValues) connected to this Block will be deleted in Aspen.  
        """
        self.BLK.Elements.Remove(Blockname)
        
    def BlockPlace(self, Blockname:str, EquipmentType: Literal["RCSTR", "RPlug", "DSTWU", "Flash2", "Mixer", "Heater", "Radfrac", "Splitter", "RYield"])-> None:
        """Adds only a BLOCK with given Name on the Aspen Simulation Sheet.
            
            No data (Input+Outputs+Simulationdata+InitialValues) are added yet. The Block is "empty".
            
            Args:
                Blockname: which contains the Name of the Stream in Aspen
                EquipmentType: Name of Equipment in Aspen. Can be: "RCSTR", "RPlug", "DSTWU", "Flash2", "Mixer", "Heater", "Radfrac", "Splitter", "RYield", 
        """
        compositstring = Blockname + "!" + EquipmentType
        print(compositstring)
        self.BLK.Elements.Add(compositstring)

    def StreamPlace(self, Streamname:str, Streamtype: Literal["MATERIAL", "HEAT", ""]) -> None:  #Stream types are: "MATERIAL", "HEAT" or ""
        """Adds only a STREAM with given Name on the Aspen Simulation Sheet.
            
            No data (Input+Outputs+Simulationdata+InitialValues) are added yet. The Stream is "empty"
            
            Args:
                Streamname: String which contains the Name of the Stream in Aspen
                Streamtype: Can be "MATERIAL", "HEAT" or ""
        """
        compositstring = Streamname + "!" + Streamtype
        print(compositstring)
        self.STRM.Elements.Add(compositstring)

        
    def StreamDelete(self, Streamname:str) -> None: 
        """Removes STREAM with given Name from the Aspen Simulation 
            
            All data (Input+Outputs+Simulationdata+InitialValues) connected to this STREAM will be deleted in Aspen.  
            
            Args:
                Streamname: String which contains the Name of the Stream in Aspen
        """
        self.STRM.Elements.Remove(Streamname)
        
    def StreamConnect(self, Blockname:str, Streamname:str, Portname:str) -> None:        #Portnames for destillation column is: "D(OUT)" , "B(OUT)", "F(IN)"
        """Connects Block with given Stream
        
        Args:
            Blockname: String which contains the Name of the Block in Aspen
            Streamname: String which contains the Name of the Stream in Aspen
            Portnames: String which could be for example: "D(OUT)" , "B(OUT)", "F(IN)
        """
        self.BLK.Elements(Blockname).Elements("Ports").Elements(Portname).Elements.Add(Streamname)
                
    def StreamDisconnect(self, Blockname:str, Streamname:str, Portname:str) -> None:        #Portnames for destillation column is: "D(OUT)" , "B(OUT)", "F(IN)"
        """Disconnects Block from given Stream
        
        Args:
            Blockname: String which contains the Name of the Block in Aspen
            Streamname: String which contains the Name of the Stream in Aspen
            Portnames: String which could be for example: "D(OUT)" , "B(OUT)", "F(IN)
        """
        
        self.BLK.Elements(Blockname).Elements("Ports").Elements(Portname).Elements.Remove(Streamname)
    
    def StreamDeleteALL(self) -> None:
        """Removes ALL STREAMS from the Aspen Simulation 
            
            All data (Input+Outputs+Simulationdata+InitialValues) connected to this Block will be deleted in Aspen.  
        """
        self.STRM.RemoveAll
        
    def BlockDeleteALL(self) -> None:
        """Removes ALL BLOCKS from the Aspen Simulation 
            
            All data (Input+Outputs+Simulationdata+InitialValues) connected to this Block will be deleted in Aspen.  
        """
        self.BLK.RemoveAll

#POWERFUNCTION for Running the Simulation:
    def VisibilityChange(self,VISIBILITY: bool) -> None:
        """ De/Activates Aspensheet graphics from being rendered. 
        
        Args:
            Visibility: String "FALSE" for more speed or "TRUE" for manual usage of Aspen
        """
        self.AspenSimulation.Visible = VISIBILITY
    
    def SheetCheckIfInputsAreComplete(self) -> bool:
        """Check if all Inputs are given on the entire Sheet, returns "0x00002081 = HAP_RESULTS_SUCCESS|HAP_INPUT_COMPLETE|HAP_ENABLED"
        
        Checks if the Aspen Expert system thinks all necessary Inputs are given and the Simulation can be run
        
        Args:
            Blockname: String which contains the Name of the Block in Aspen
            return: TRUE or FALSE????????????
        """
        return self.AspenSimulation.COMPSTATUS

    def BlockCheckIfInputsAreComplete(self, Blockname: str) -> bool:
        """
        Checks if the Aspen Expert system thinks all necessary Inputs are given and the Simulation can be run
        
        Args:
            Blockname: String which contains the Name of the Block in Aspen
            return: TRUE or FALSE????????????
        """
        return self.BLK.Elements(Blockname).COMPSTATUS

    def StreamCheckIfInputsAreComplete(self, Streamname:str) -> bool:
        """
        Checks if the Aspen Expert system thinks all necessary Inputs are given and the Simulation can be run
        
        Args:
            Streamname: String which contains the Name of the Block in Aspen
            return: TRUE or FALSE????????????
        """
        return self.STRM.Elements(Streamname).COMPSTATUS



    def Give_AspenDocumentName(self) -> String:
        """Returns name of Aspen document"""
        return self.AspenSimulation.FullName
    def DialogSuppression(self, TrueOrFalse: bool) -> None:
        """Supresses Aspen Popups
        
        Args: 
            TrueOrFalse: can be True or False """
        self.AspenSimulation.SuppressDialogs = TrueOrFalse
        
    def EngineRun(self) -> None:
        """Runs Simulation, synonymous with pressing the playbutton"""
        self.AspenSimulation.Run2()
    def EngineStop(self) -> None:
        """Stops Simulation, synonymous to pressing the red square button"""
        self.AspenSimulation.Stop()
        
    def EngineReinit(self) -> None:
        """Reinitalizes the Entire Simulation, synonymous to pressing the Reset button

        Other possible functions you might need are: BlockReinit(Blockname), StreamReinit(Streamname)
        """
        self.AspenSimulation.Reinit()
    
    def BlockReinit(self, Blockname:str) -> None:
        """Reinitalizes the Block with given Name,
        
        Synonymous to pressing the Reset button, Other possible functions you might need are: BlockReinit(Blockname), StreamReinit(Streamname), EngineReinit()
        
        Args:
            Blockname: String which contains the Name of the Block in Aspen
        """
        self.BLK.Elements(Blockname).Reinit()
     
        
    def StreamReinit(self, Streamname:str) -> None:
        """Reinitalizes the Stream with given Name,
        
        Synonymous to pressing the Reset button, Other possible functions you might need are: BlockReinit(Blockname), StreamReinit(Streamname), EngineReinit()

        Args:
            Streamname: String which contains the Name of the Stream in Aspen
        """
        self.STRM.Elements(Streamname).Reinit()
        
    #def EngineGiveSettings(self):
    #    return self.AspenSimulation.EngineFilesSettings????
    
    
#POWERFUNCTION for Saving Reports and such things
    def Save(self) -> None:
        """Saves Current Simulation (.apw), Inputs and all Values connected to it."""
        self.AspenSimulation.Save()
    def SaveAs(self, Filename:str, overwrite:bool = True) -> None:
        """Saves the current Aspen Simulation,(.apw) with a new name with/out overwritting.
        
        Args:
            Filename: String which gives the File name. 
            overwrite: Should file be overwritten when the File already exists? True or False, standard is True
        """
        self.AspenSimulation.SaveAs(Filename, overwrite)
    
    def ExportBackupFile(self, filename:str) -> None:
        """Saves BackupFile (.bkp) of Aspen Simulation with a given name.
        
        Args:
            Filename: String which gives the File name. 
        """
        self.AspenSimulation.Export(1, filename)
    def ExportReportFile(self, filename:str) -> None:
        """Saves ReportFile (.rep or .txt) of Aspen Simulation with a given name.
        
        Args:
            Filename: String which gives the File name. 
        """
        self.AspenSimulation.Export(2, filename)


    def ExportSummaryFile(self, filename:str) -> None:
        """Saves SummaryFile (.sum) of Aspen Simulation with a given name.
        
        Args:
            Filename: String which gives the File name. 
        """
        self.AspenSimulation.Export(3, filename)
    def ExportInputFile(self, filename:str) -> None:
        """Saves InputFile (.inp aka txt) of Aspen Simulation with a given name.
        
        Args:
            Filename: String which gives the File name. 
        """
        self.AspenSimulation.Export(4, filename) #"HAPEXP_INPUT"
    
    def ExportInputFileWithGraphics(self, filename:str) -> None:
        """Saves InputFile (.inp aka txt) of Aspen Simulation with a given name.
        
        Args:
            Filename: String which gives the File name. 
        """
        self.AspenSimulation.Export(5, filename) 


    def ExportRunMessagesFile(self, filename:str) -> None:
        """Saves Messages, Errors, Warnings and diagnostics from running the Simulation for each run.
        
        Args:
            Filename: String which gives the File name. 
        """
        self.AspenSimulation.Export(6, filename)
    
    def ExportFlowDrivenDynamicSimulationFile(self, filename:str) -> None:
        """Export a Flowdriven simulation report
        
        Args:
            Filename: String which gives the File name. 
        """
        self.AspenSimulation.Export(9, filename)  

    def ExportPressureDrivenDynamicSimulationFile(self, filename:str) -> None:
        """Export a Pressure driven simulation report
        
        Args:
            Filename: String which gives the File name. 
        """
        self.AspenSimulation.Export(10, filename)  
  
    
    
    def ExportFlowsheetdrawingFile(self, filename:str) -> None:
        """Export a Drawing of the Flowsheet
        
        Args:
            Filename: String which gives the File name. 
        """
        self.AspenSimulation.Export(11, filename)   #"HAPEXP_DXF"






















########################################################################################################################################


###########         N               N       PPPPPPPPPPP         U               U       TTTTTTTTTTTTTTTTTTTTTTTT
    #               N  N            N       P           P       U               U                   T
    #               N    N          N       P           P       U               U                   T
    #               N      N        N       P           P       U               U                   T
    #               N       N       N       PPPPPPPPPPP         U               U                   T
    #               N         N     N       P                   U               U                   T
    #               N           N   N       P                   U               U                   T
    #               N             N N       P                   U               U                   T
###########         N               N       P                   UUUUUUUUUUUUUUUUU                   T


############################################################################################################################################


###DSTWU
    def BLK_DSTWU_GET_ME_ALL_INPUTS_BACK(self, Blockname:str) -> Dict[str, Union[str,float,int]]:
        """Retrieves all the Inputs and returns Dictionary with Values 
        
        Does not include all aspects of a Aspen Simulationsheet, for this look at Exports
        
        Args:
            Blockname: String which gives the name of Block.         
        """
        
        StageRefluxOption = self.BLK.Elements(Blockname).Elements("Input").Elements("OPT_NTRR").Value
        NumberOfStages = self.BLK.Elements(Blockname).Elements("Input").Elements("NSTAGE").Value
        RefluxRatio = self.BLK.Elements(Blockname).Elements("Input").Elements("RR").Value
        CondenserPressure = self.BLK.Elements(Blockname).Elements("Input").Elements("PTOP").Value
        ReboilerPressure = self.BLK.Elements(Blockname).Elements("Input").Elements("PBOT").Value
        LightkeyComponent = self.BLK.Elements(Blockname).Elements("Input").Elements("LIGHTKEY").Value
        HeavykeyComponent = self.BLK.Elements(Blockname).Elements("Input").Elements("HEAVYKEY").Value
        LightkeyRecovery = self.BLK.Elements(Blockname).Elements("Input").Elements("RECOVL").Value
        HeavykeyRecovery = self.BLK.Elements(Blockname).Elements("Input").Elements("RECOVH").Value
        CondenserOption = self.BLK.Elements(Blockname).Elements("Input").Elements("OPT_RDV").Value
        DestillVaporFraction = self.BLK.Elements(Blockname).Elements("Input").Elements("RDV").Value
        GenerateTableOption = self.BLK.Elements(Blockname).Elements("Input").Elements("PLOT").Value
        GenerateTable_FirstStage = self.BLK.Elements(Blockname).Elements("Input").Elements("LOWER").Value
        GenerateTable_LastStage = self.BLK.Elements(Blockname).Elements("Input").Elements("UPPER").Value
        GenerateTable_StageNumber = self.BLK.Elements(Blockname).Elements("Input").Elements("NPOINT").Value
        CalculateHeightequivalentHETP_Option = self.BLK.Elements(Blockname).Elements("Input").Elements("OPT_CALHETP").Value
        CalculateHeightequivalentHETP_PackedHeight = self.BLK.Elements(Blockname).Elements("Input").Elements("PACK_HEIGHT").Value
        FreewaterOption = self.BLK.Elements(Blockname).Elements("Input").Elements("BLKOPFREWAT").Value
        MaxNumberFlashIterations = self.BLK.Elements(Blockname).Elements("Input").Elements("MAXIT").Value
        FlashConvergenceTolerance =self.BLK.Elements(Blockname).Elements("Input").Elements("FLASH_TOL").Value
        MaxNumberMinStageIterations = self.BLK.Elements(Blockname).Elements("Input").Elements("MAXIT").Value
        KvalueTolerance = self.BLK.Elements(Blockname).Elements("Input").Elements("K_TOL").Value
        ProductTempTolerance = self.BLK.Elements(Blockname).Elements("Input").Elements("TEMP_TOL").Value
        Dictionary = {
        "StageRefluxOption": StageRefluxOption,
        "NumberOfStages" : NumberOfStages,
        "RefluxRatio":RefluxRatio,
        "CondenserPressure":CondenserPressure,
        "ReboilerPressure":ReboilerPressure,
        "LightkeyComponent":LightkeyComponent,
        "HeavykeyComponent":HeavykeyComponent,
        "LightkeyRecovery":LightkeyRecovery,
        "HeavykeyRecovery":HeavykeyRecovery,
        "CondenserOption":CondenserOption,
        "DestillVaporFraction":DestillVaporFraction,
        "GenerateTableOption":GenerateTableOption,
        "GenerateTable_FirstStage":GenerateTable_FirstStage,
        "GenerateTable_LastStage":GenerateTable_LastStage,
        "GenerateTable_StageNumber":GenerateTable_StageNumber,
        "CalculateHeightequivalentHETP_Option" : CalculateHeightequivalentHETP_Option,
        "alculateHeightequivalentHETP_CPackedHeight":CalculateHeightequivalentHETP_PackedHeight,
        "FreewaterOption":FreewaterOption,
        "MaxNumberFlashIterations":MaxNumberFlashIterations,
        "FlashConvergenceTolerance":FlashConvergenceTolerance,
        "MaxNumberMinStageIterations":MaxNumberMinStageIterations,
        "KvalueTolerance":KvalueTolerance,
        "ProductTempTolerance":ProductTempTolerance,
        }
        return Dictionary
    def BLK_DSTWU_SET_ALL_INPUTS(self, Blockname:str, Dictionary: Dict[str, Union[str,float,int]] ) ->None:
        """Takes Dictionary with Values set the ones which are given in Aspen. 
        
        The Original Dictionary with its specific format can be found via "BLK_DSTWU_GET_ME_ALL_INPUTS_BACK"
        
        Args:
            Blockname: String which gives the name of Block.  
            Dictionary: Dictionary which contains all the Input variables.       
        """
        try:
            self.BLK.Elements(Blockname).Elements("Input").Elements("OPT_NTRR").Value = Dictionary.get("StageRefluxOption")
            try:
                self.BLK.Elements(Blockname).Elements("Input").Elements("NSTAGE").Value = Dictionary.get("NumberOfStages")
            except Exception:
                pass
            try:
                self.BLK.Elements(Blockname).Elements("Input").Elements("RR").Value = Dictionary.get("RefluxRatio")
            except Exception:
                pass
            self.BLK.Elements(Blockname).Elements("Input").Elements("PTOP").Value = Dictionary.get("CondenserPressure")
            self.BLK.Elements(Blockname).Elements("Input").Elements("PBOT").Value = Dictionary.get("ReboilerPressure")
            self.BLK.Elements(Blockname).Elements("Input").Elements("LIGHTKEY").Value = Dictionary.get("LightkeyComponent")
            self.BLK.Elements(Blockname).Elements("Input").Elements("HEAVYKEY").Value = Dictionary.get("HeavykeyComponent")
            self.BLK.Elements(Blockname).Elements("Input").Elements("RECOVL").Value = Dictionary.get("LightkeyRecovery")
            self.BLK.Elements(Blockname).Elements("Input").Elements("RECOVH").Value = Dictionary.get("HeavykeyRecovery")
            self.BLK.Elements(Blockname).Elements("Input").Elements("OPT_RDV").Value = Dictionary.get("CondenserOption")
            self.BLK.Elements(Blockname).Elements("Input").Elements("RDV").Value = Dictionary.get("DestillVaporFraction")
            self.BLK.Elements(Blockname).Elements("Input").Elements("PLOT").Value = Dictionary.get("GenerateTableOption")
            try:   
                self.BLK.Elements(Blockname).Elements("Input").Elements("LOWER").Value = Dictionary.get("GenerateTable_FirstStage")
                self.BLK.Elements(Blockname).Elements("Input").Elements("UPPER").Value = Dictionary.get("GenerateTable_LastStage")
            except Exception:
                pass            
            self.BLK.Elements(Blockname).Elements("Input").Elements("NPOINT").Value = Dictionary.get("GenerateTable_StageNumber")
            self.BLK.Elements(Blockname).Elements("Input").Elements("OPT_CALHETP").Value = Dictionary.get("CalculateHeightequivalentHETP_Option")
            try:
                self.BLK.Elements(Blockname).Elements("Input").Elements("PACK_HEIGHT").Value = Dictionary.get("CalculateHeightequivalentHETP_PackedHeight")
            except Exception:
                pass
            self.BLK.Elements(Blockname).Elements("Input").Elements("BLKOPFREWAT").Value = Dictionary.get("FreewaterOption")
            self.BLK.Elements(Blockname).Elements("Input").Elements("FLASH_MAXIT").Value = Dictionary.get("MaxNumberFlashIterations")
            self.BLK.Elements(Blockname).Elements("Input").Elements("FLASH_TOL").Value = Dictionary.get("FlashConvergenceTolerance")
            self.BLK.Elements(Blockname).Elements("Input").Elements("MAXIT").Value = Dictionary.get("MaxNumberMinStageIterations")
            self.BLK.Elements(Blockname).Elements("Input").Elements("K_TOL").Value = Dictionary.get("KvalueTolerance")
            self.BLK.Elements(Blockname).Elements("Input").Elements("TEMP_TOL").Value = Dictionary.get("ProductTempTolerance")
        except Exception:
            pass
                  
###DSTWU
#PAGE 1         Specification:
    #Choice between giving Number of Stages or Refluxratio:
    def BLK_DSTWU_Set_StageRefluxOption(self,Blockname:str, StageRefluxOption: Literal["NSTAGE", "RR"]) -> None:     #you can chose NSTAGE or RR
        self.BLK.Elements(Blockname).Elements("Input").Elements("OPT_NTRR").Value = StageRefluxOption
        #if you chose: NSTAGE
    def BLK_DSTWU_Set_NumberOfStages(self,Blockname, nstages):
        self.BLK.Elements(Blockname).Elements("Input").Elements("NSTAGE").Value = nstages
        #if you chose: RR
    def BLK_DSTWU_Set_Refluxratio(self,Blockname, Refluxratio):
        self.BLK.Elements(Blockname).Elements("Input").Elements("RR").Value = Refluxratio
    def BLK_DSTWU_Set_CondenserPressure(self, Blockname, CondenserPressure):
        self.BLK.Elements(Blockname).Elements("Input").Elements("PTOP").Value = CondenserPressure
        
    def BLK_DSTWU_Set_ReboilerPressure(self, Blockname, ReboilerPressure):
        self.BLK.Elements(Blockname).Elements("Input").Elements("PBOT").Value = ReboilerPressure
    def BLK_DSTWU_Set_LightkeyComponent(self, Blockname,LightkeyComponent):
        self.BLK.Elements(Blockname).Elements("Input").Elements("LIGHTKEY").Value = LightkeyComponent
    def BLK_DSTWU_Set_HeavykeyComponent(self, Blockname,HeavykeyComponent):
        self.BLK.Elements(Blockname).Elements("Input").Elements("HEAVYKEY").Value = HeavykeyComponent
    def BLK_DSTWU_Set_LightkeyRecovery(self, Blockname,LightkeyRecovery):
        self.BLK.Elements(Blockname).Elements("Input").Elements("RECOVL").Value = LightkeyRecovery
    def BLK_DSTWU_Set_HeavykeyRecovery(self, Blockname,HeavykeyRecovery):
        self.BLK.Elements(Blockname).Elements("Input").Elements("RECOVH").Value = HeavykeyRecovery
    #Choice between Condenser specification
    def BLK_DSTWU_Set_CondenserOption(self, Blockname:str, CondenserOption: Literal["LIQUID", "VAPOR", "VAPLIQ"]):        #LIQUID VAPOR or VAPLIQ
        self.BLK.Elements(Blockname).Elements("Input").Elements("OPT_RDV").Value = CondenserOption
        #if you chose: LIQUID or VAPOR:
            #you dont need to add anything 

        #if you chose: VAPLIQ:
    def BLK_DSTWU_Set_VAPLIQ_DestillVaporFraction(self, Blockname, DestillVaporFraction):
        self.BLK.Elements(Blockname).Elements("Input").Elements("RDV").Value = DestillVaporFraction
    

#PAGE 2         Calculation Options:
    def BLK_DSTWU_Set_GenerateTableOption(self, Blockname:str, GenerateTableOption: Literal["YES", "NO"]) -> None:    #YES or NO
        self.BLK.Elements(Blockname).Elements("Input").Elements("PLOT").Value = GenerateTableOption
        #if you chose YES then you need to input this:
    def BLK_DSTWU_Set_GenerateTable_FirstStage(self, Blockname, FirstStage):
        self.BLK.Elements(Blockname).Elements("Input").Elements("LOWER").Value = FirstStage
    def BLK_DSTWU_Set_GenerateTable_LastStage(self, Blockname, LastStage):
        self.BLK.Elements(Blockname).Elements("Input").Elements("UPPER").Value = LastStage
    def BLK_DSTWU_Set_GenerateTable_StageNumber(self, Blockname, StageNumber):
        self.BLK.Elements(Blockname).Elements("Input").Elements("NPOINT").Value = StageNumber
    
    def BLK_DSTWU_Set_CalculateHeightequivalentHETP_Option(self, Blockname:str, CalculateHeightequivalentHETP_Option: Literal["YES", "NO"]) -> None:      #YES or NO
        self.BLK.Elements(Blockname).Elements("Input").Elements("OPT_CALHETP").Value = CalculateHeightequivalentHETP_Option
        #if you chose YES then you need to input this:
    def BLK_DSTWU_Set_CalculateHeightequivalentHETP_PackedHeight(self, Blockname:str, PackedHeight: Literal["YES", "NO"]) -> None:      #YES or NO
        self.BLK.Elements(Blockname).Elements("Input").Elements("PACK_HEIGHT").Value = PackedHeight


#PAGE 3         Convergence:
    def BLK_DSTWU_Set_FreewaterOption(self, Blockname:str, FreewaterOption: Literal["YES", "NO", "DIRTY"]) -> None:        #This can be YES, NO, DIRTY
        self.BLK.Elements(Blockname).Elements("Input").Elements("BLKOPFREWAT").Value = FreewaterOption
    def BLK_DSTWU_Set_MaxNumberFlashIterations(self, Blockname, MaxNumberFlashIterations):
        self.BLK.Elements(Blockname).Elements("Input").Elements("FLASH_MAXIT").Value = MaxNumberFlashIterations
    def BLK_DSTWU_Set_FlashConvergenceTolerance(self, Blockname, FlashConvergenceTolerance):
        self.BLK.Elements(Blockname).Elements("Input").Elements("FLASH_TOL").Value = FlashConvergenceTolerance
    def BLK_DSTWU_Set_MaxNumberMinStageIterations(self, Blockname, MaxNumberMinStageIterations):
        self.BLK.Elements(Blockname).Elements("Input").Elements("MAXIT").Value = MaxNumberMinStageIterations
    def BLK_DSTWU_Set_KvalueTolerance(self, Blockname, KvalueTolerance):
        self.BLK.Elements(Blockname).Elements("Input").Elements("K_TOL").Value = KvalueTolerance
    def BLK_DSTWU_Set_ProductTempTolerance(self, Blockname, ProductTempTolerance):
        self.BLK.Elements(Blockname).Elements("Input").Elements("TEMP_TOL").Value = ProductTempTolerance



















    def BLK_MIXER_GET_ME_ALL_INPUTS_BACK(self, Blockname:str) -> Dict[str, Union[str,float,int]]:
        """Retrieves all the Inputs and returns Dictionary with Values 
        
        Does not include all aspects of a Aspen Simulationsheet, for this look at Exports
        
        Args:
            Blockname: String which gives the name of Block.         
        """
        
        Pressure = self.BLK.Elements(Blockname).Elements("Input").Elements("PRES").Value 
        Phase = self.BLK.Elements(Blockname).Elements("Input").Elements("Phase").Value  #This can be V L or S
        Nphase = self.BLK.Elements(Blockname).Elements("Input").Elements("NPhase").Value 
        TemperatureEstimation = self.BLK.Elements(Blockname).Elements("Input").Elements("T_EST").Value 
        MaximumIterations = self.BLK.Elements(Blockname).Elements("Input").Elements("MAXIT").Value 
        ErrorTolerance =  self.BLK.Elements(Blockname).Elements("Input").Elements("TOL").Value
        
        Dictionary = {
        "Pressure": Pressure    ,
        "Phase" :  Phase  , 
        "Nphase":   Nphase,
        "TemperatureEstimate": TemperatureEstimation    ,
        "MaximumIterations":    MaximumIterations  ,
        "ErrorTolerance":  ErrorTolerance    ,
        }
        return Dictionary
    def BLK_MIXER_SET_ALL_INPUTS(self, Blockname:str, Dictionary: Dict[str, Union[str,float,int]]) -> None:
        """Takes Dictionary with Values set the ones which are given in Aspen. 
        
        The Original Dictionary with its specific format can be found via "BLK_DSTWU_GET_ME_ALL_INPUTS_BACK"
        
        Args:
            Blockname: String which gives the name of Block.  
            Dictionary: Dictionary which contains all the Input variables.       
        """

        self.BLK.Elements(Blockname).Elements("Input").Elements("PRES").Value = Dictionary.get("Pressure")
        self.BLK.Elements(Blockname).Elements("Input").Elements("Phase").Value = Dictionary.get("Phase") #This can be V L or S
        self.BLK.Elements(Blockname).Elements("Input").Elements("NPhase").Value = Dictionary.get("Nphase")
        self.BLK.Elements(Blockname).Elements("Input").Elements("T_EST").Value = Dictionary.get("TemperatureEstimate")
        self.BLK.Elements(Blockname).Elements("Input").Elements("MAXIT").Value = Dictionary.get("MaximumIteration")
        self.BLK.Elements(Blockname).Elements("Input").Elements("TOL").Value = Dictionary.get("ErrorTolerance")

##MIXER:
    def BLK_MIXER_Set_Pressure(self, Blockname:str, Pressure:float):
        self.BLK.Elements(Blockname).Elements("Input").Elements("PRES").Value = Pressure
    def BLK_MIXER_Set_Phases(self, Blockname:str, Phase: Ph, Phasenumber: Phnum):
        self.BLK.Elements(Blockname).Elements("Input").Elements("Phase").Value = Phase #This can be V L or S
        self.BLK.Elements(Blockname).Elements("Input").Elements("NPhase").Value = Phasenumber
    def BLK_MIXER_Set_TemperatureEstimate(self, Blockname:str, TempEstimate:float):      #OPTIONAL
        self.BLK.Elements(Blockname).Elements("Input").Elements("T_EST").Value = TempEstimate
    def BLK_MIXER_Set_MaximumIteration(self, Blockname:str, MaximumIteration:int):       #OPTIONAL
        self.BLK.Elements(Blockname).Elements("Input").Elements("MAXIT").Value = MaximumIteration
    def BLK_MIXER_Set_ErrorTolerance(self, Blockname:str, ErrorTolerance:float):           #OPTIONAL
        self.BLK.Elements(Blockname).Elements("Input").Elements("TOL").Value = ErrorTolerance


















    def BLK_HEATER_GET_ME_ALL_INPUTS_BACK(self, Blockname:str) -> Dict[str, Union[str,float,int]]:
        """Retrieves all the Inputs and returns Dictionary with Values 
        
        Does not include all aspects of a Aspen Simulationsheet, for this look at Exports
        
        Args:
            Blockname: String which gives the name of Block.         
        """
        FlashTypeOption =self.BLK.Elements(Blockname).Elements("Input").Elements("SPEC_OPT").Value 
        Temperature =self.BLK.Elements(Blockname).Elements("Input").Elements("TEMP").Value 
        TemperatureChange =self.BLK.Elements(Blockname).Elements("Input").Elements("DELT").Value 
        DegreesSuperheating =self.BLK.Elements(Blockname).Elements("Input").Elements("DEGSUP").Value 
        DegreesSubcooling =self.BLK.Elements(Blockname).Elements("Input").Elements("DEGSUB").Value 
        Pressure =self.BLK.Elements(Blockname).Elements("Input").Elements("PRES").Value 
        Duty =self.BLK.Elements(Blockname).Elements("Input").Elements("DUTY").Value 
        Vaporfraction =self.BLK.Elements(Blockname).Elements("Input").Elements("VFRAC").Value 
        PressureDropCorrelation =self.BLK.Elements(Blockname).Elements("Input").Elements("DPPARM").Value 
        Phase =self.BLK.Elements(Blockname).Elements("Input").Elements("Phase").Value  #This can be V L or S
        Phasenumber =self.BLK.Elements(Blockname).Elements("Input").Elements("NPhase").Value    #This can be 1,2,3
        TemperatureEstimation =self.BLK.Elements(Blockname).Elements("Input").Elements("T_EST").Value 
        PressureEstimation =self.BLK.Elements(Blockname).Elements("Input").Elements("P_EST").Value 
        MaximumIteration =self.BLK.Elements(Blockname).Elements("Input").Elements("MAXIT").Value 
        ErrorTolerance = self.BLK.Elements(Blockname).Elements("Input").Elements("TOL").Value 

        Dictionary = {
        "FlashTypeOption": FlashTypeOption    ,
        "Temperature" :  Temperature  , 
        "TemperatureChange":   TemperatureChange,
        "DegreesSuperheating": DegreesSuperheating    ,
        "DegreesSubcooling":     DegreesSubcooling  ,
        "Pressure":  Pressure    ,
        "Duty": Duty  ,
        "Vaporfraction": Vaporfraction  ,
        "PressureDropCorrelation":  PressureDropCorrelation ,
        "Phase": Phase  ,
        "Phasenumber": Phasenumber  ,
        "TemperatureEstimation":  TemperatureEstimation ,
        "PressureEstimation": PressureEstimation  ,
        "MaximumIteration": MaximumIteration  ,
        "ErrorTolerance": ErrorTolerance,
        }
        return Dictionary
    def BLK_HEATER_SET_ALL_INPUTS(self, Blockname:str, Dictionary: Dict[str, Union[str,float,int]]) -> None:
        """Takes Dictionary with Values set the ones which are given in Aspen. 
        
        The Original Dictionary with its specific format can be found via "BLK_DSTWU_GET_ME_ALL_INPUTS_BACK"
        
        Args:
            Blockname: String which gives the name of Block.  
            Dictionary: Dictionary which contains all the Input variables.       
        """

        self.BLK.Elements(Blockname).Elements("Input").Elements("SPEC_OPT").Value = Dictionary.get("FlashTypeOption")
        self.BLK.Elements(Blockname).Elements("Input").Elements("TEMP").Value = Dictionary.get("Temperature")
        self.BLK.Elements(Blockname).Elements("Input").Elements("DELT").Value = Dictionary.get("TemperatureChange")
        self.BLK.Elements(Blockname).Elements("Input").Elements("DEGSUP").Value = Dictionary.get("DegreesSuperheating")
        self.BLK.Elements(Blockname).Elements("Input").Elements("DEGSUB").Value = Dictionary.get("DegreesSubcooling")
        self.BLK.Elements(Blockname).Elements("Input").Elements("PRES").Value = Dictionary.get("Pressure")
        self.BLK.Elements(Blockname).Elements("Input").Elements("DUTY").Value = Dictionary.get("Duty")
        self.BLK.Elements(Blockname).Elements("Input").Elements("VFRAC").Value = Dictionary.get("Vaporfraction")
        self.BLK.Elements(Blockname).Elements("Input").Elements("DPPARM").Value = Dictionary.get("PressureDropCorrelation")
        self.BLK.Elements(Blockname).Elements("Input").Elements("Phase").Value = Dictionary.get("Phase") #This can be V L or S
        self.BLK.Elements(Blockname).Elements("Input").Elements("NPhase").Value = Dictionary.get("Phasenumber")   #This can be 1,2,3
        self.BLK.Elements(Blockname).Elements("Input").Elements("T_EST").Value = Dictionary.get("TemperatureEstimation")
        self.BLK.Elements(Blockname).Elements("Input").Elements("P_EST").Value = Dictionary.get("PressureEstimation")
        self.BLK.Elements(Blockname).Elements("Input").Elements("MAXIT").Value = Dictionary.get("MaximumIteration")
        self.BLK.Elements(Blockname).Elements("Input").Elements("TOL").Value = Dictionary.get("ErrorTolerance")


##  HEATER

#Page 1         Flash specification
    def BLK_HEATER_Set_FlashTypeOption(self, Blockname:str, FlashTypeOption: Literal["TP", "TD", "TV", "TDPPARM", "PD", "PV", "PDT" , "PDEGSUP", "PDEGSUB", "DDPPARM", "VDPPARM", "DEGSUPDPPARM", "DEGSUBDPPARM", "DTV", "DTD", "DTDPPARM"]) -> None:           #You can chose between: TP, TD, TV, TDPPARM, PD, PV, PDT,PDEGSUP, PDEGSUB, DDPPARM, VDPPARM, DEGSUPDPPARM, DEGSUBDPPARM, DTV, DTD, DTDPPARM
        self.BLK.Elements(Blockname).Elements("Input").Elements("SPEC_OPT").Value = FlashTypeOption
    def BLK_HEATER_Set_Temperature(self, Blockname, Temperature):
        self.BLK.Elements(Blockname).Elements("Input").Elements("TEMP").Value = Temperature
    def BLK_HEATER_Set_TemperatureChange(self, Blockname, TemperatureChange):
        self.BLK.Elements(Blockname).Elements("Input").Elements("DELT").Value =TemperatureChange
    def BLK_HEATER_Set_DegreesSuperheating(self, Blockname, DegreesSuperheating):
        self.BLK.Elements(Blockname).Elements("Input").Elements("DEGSUP").Value = DegreesSuperheating
    def BLK_HEATER_Set_DegreesSubcooling(self, Blockname, DegreesSubcooling):
        self.BLK.Elements(Blockname).Elements("Input").Elements("DEGSUB").Value = DegreesSubcooling
    def BLK_HEATER_Set_Pressure(self, Blockname, Pressure):
        self.BLK.Elements(Blockname).Elements("Input").Elements("PRES").Value = Pressure
    def BLK_HEATER_Set_Duty(self, Blockname, Duty):
        self.BLK.Elements(Blockname).Elements("Input").Elements("DUTY").Value = Duty
    def BLK_HEATER_Set_Vaporfraction(self, Blockname, Vaporfraction):
        self.BLK.Elements(Blockname).Elements("Input").Elements("VFRAC").Value = Vaporfraction
    def BLK_HEATER_Set_PressureDropCorrelation(self, Blockname, PressureDropCorrelation):
        self.BLK.Elements(Blockname).Elements("Input").Elements("DPPARM").Value = PressureDropCorrelation

    def BLK_HEATER_Set_Phases(self, Blockname:str, Phase: Ph, Phasenumber: Phnum) -> None:
        self.BLK.Elements(Blockname).Elements("Input").Elements("Phase").Value = Phase #This can be V L or S
        self.BLK.Elements(Blockname).Elements("Input").Elements("NPhase").Value = Phasenumber   #This can be 1,2,3


#Page 2         Flash Option
    def BLK_HEATER_Set_TemperatureEstimation(self, Blockname, TemperatureEstimation):
        self.BLK.Elements(Blockname).Elements("Input").Elements("T_EST").Value = TemperatureEstimation
    def BLK_HEATER_Set_PressureEstimation(self, Blockname, PressureEstimation):
        self.BLK.Elements(Blockname).Elements("Input").Elements("P_EST").Value = PressureEstimation
    def BLK_HEATER_Set_MaximumIteration(self, Blockname, MaximumIteration):       #OPTIONAL
        self.BLK.Elements(Blockname).Elements("Input").Elements("MAXIT").Value = MaximumIteration
    def BLK_HEATER_Set_ErrorTolerance(self, Blockname, ErrorTolerance):           #OPTIONAL
        self.BLK.Elements(Blockname).Elements("Input").Elements("TOL").Value = ErrorTolerance



















    def BLK_CISTR_GET_ME_ALL_INPUTS_BACK(self, Blockname:str): #-> Dict[str, Union[str,float,int]]
        """Retrieves all the Inputs and returns Dictionary with Values 
        
        Does not include all aspects of a Aspen Simulationsheet, for this look at Exports
        
        Args:
            Blockname: String which gives the name of Block.         
        """
        SpecificationOption = self.BLK.Elements(Blockname).Elements("Input").Elements("SPEC_OPT").Value
        Pressure = self.BLK.Elements(Blockname).Elements("Input").Elements("PRES").Value
        Temperature =self.BLK.Elements(Blockname).Elements("Input").Elements("TEMP").Value 
        Duty = self.BLK.Elements(Blockname).Elements("Input").Elements("DUTY").Value
        VaporFraction=self.BLK.Elements(Blockname).Elements("Input").Elements("VFRAC").Value 
        Phase =self.BLK.Elements(Blockname).Elements("Input").Elements("PHASE").Value  #This can be V L or S
        Phasenumber= self.BLK.Elements(Blockname).Elements("Input").Elements("NPHASE").Value  #This can be 1,2,3
        Specification_type= self.BLK.Elements(Blockname).Elements("Input").Elements("SPEC_TYPE").Value  #This selects what input is needed:
        VolumeReactor= self.BLK.Elements(Blockname).Elements("Input").Elements("VOL").Value 
        ResidencetimeReactor = self.BLK.Elements(Blockname).Elements("Input").Elements("RES_TIME").Value 
        Specification_PhaseHoldup= self.BLK.Elements(Blockname).Elements("Input").Elements("SPEC_PHASE").Value 
        VolumeFrac_of_PhaseHoldup = self.BLK.Elements(Blockname).Elements("Input").Elements("REACT_VOL_FR").Value 
        Volume_of_PhaseHoldup = self.BLK.Elements(Blockname).Elements("Input").Elements("REACT_VOL").Value
        Residencetime_of_PhaseHoldup = self.BLK.Elements(Blockname).Elements("Input").Elements("PH_RES_TIME").Value 

        StreamnameNode = self.BLK.Elements(Blockname).Elements("Ports").Elements("F(IN)").Elements

        ActivateReactions_or_not = self.BLK.Elements(Blockname).Elements("Input").Elements("REACSYS").Value 
        ActivateCrystalization_or_not = self.BLK.Elements(Blockname).Elements("Input").Elements("CRYSTSYS").Value 
        ActivateAgitation_or_not = self.BLK.Elements(Blockname).Elements("Input").Elements("AGITATOR").Value 
        AgitatorRotationrate = self.BLK.Elements(Blockname).Elements("Input").Elements("AGITRATE").Value 
        AgitatorImpellerDiameter = self.BLK.Elements(Blockname).Elements("Input").Elements("IMPELLR_DIAM").Value 
        AgitatorPowernumber = self.BLK.Elements(Blockname).Elements("Input").Elements("POWERNUMBER").Value 

        PSDCalculation_Option = self.BLK.Elements(Blockname).Elements("Input").Elements("OPT_PSD").Value
        PSDParticalGrowthModel = self.BLK.Elements(Blockname).Elements("Input").Elements("CONST_METHOD").Value 
    
        CatalystPresentOption = self.BLK.Elements(Blockname).Elements("Input").Elements("CAT_PRESENT").Value
        IgnoreCatalystVolume = self.BLK.Elements(Blockname).Elements("Input").Elements("IGN_CAT_VOL").Value 
        WeightOfCatalystLoaded = self.BLK.Elements(Blockname).Elements("Input").Elements("CATWT").Value 
        ParticleDensity = self.BLK.Elements(Blockname).Elements("Input").Elements("CAT_RHO").Value 
        BedVoidage = self.BLK.Elements(Blockname).Elements("Input").Elements("BED_VOIDAGE").Value 
        
        Dictionary = {
        "SpecificationOption":SpecificationOption,
        "Pressure":Pressure,
        "Temperature":Temperature,
        "Duty":Duty,
        "VaporFraction":VaporFraction,
        "Phase":Phase,
        "Phasenumber":Phasenumber,
        "Specification_type":Specification_type,
        "VolumeReactor":VolumeReactor,
        "ResidencetimeReactor":ResidencetimeReactor,
        "Specification_PhaseHoldup":Specification_PhaseHoldup,
        "VolumeFrac_of_PhaseHoldup": VolumeFrac_of_PhaseHoldup,
        "Volume_of_PhaseHoldup":Volume_of_PhaseHoldup,
        "Residencetime_of_PhaseHoldup":Residencetime_of_PhaseHoldup,

        "Activate_Reaction":ActivateReactions_or_not,
        "Activate_Crystalization":ActivateCrystalization_or_not,
        "Activate_Agitation":ActivateAgitation_or_not,
        "AgitatorRotationrate":AgitatorRotationrate,
        "AgitatorImpellerDiameter":AgitatorImpellerDiameter,
        "AgitatorPowernumber":AgitatorPowernumber,

        "PSDCalculation_Option":PSDCalculation_Option,
        "PSDParticalGrowthModel":PSDParticalGrowthModel,

        "CatalystPresentOption":CatalystPresentOption,
        "IgnoreCatalystVolume":IgnoreCatalystVolume,
        "WeightOfCatalystLoaded":WeightOfCatalystLoaded,
        "ParticleDensity":ParticleDensity,
        "BedVoidage":BedVoidage
        }
        return Dictionary

    def BLK_CISTR_SET_ALL_INPUTS(self, Blockname:str, Dictionary: Dict[str, Union[str,float,int]]) -> None:
        """Takes Dictionary with Values set the ones which are given in Aspen. 
        
        The Original Dictionary with its specific format can be found via "BLK_DSTWU_GET_ME_ALL_INPUTS_BACK"
        
        Args:
            Blockname: String which gives the name of Block.  
            Dictionary: Dictionary which contains all the Input variables.       
        """

        self.BLK.ELements(Blockname).Elements("Input").Elements("SPEC_OPT").Value = Dictionary.get("SpecificationOption")
        self.BLK.Elements(Blockname).Elements("Input").Elements("PRES").Value = Dictionary.get("Pressure")
        self.BLK.Elements(Blockname).Elements("Input").Elements("TEMP").Value = Dictionary.get("Temperature")    
        self.BLK.Elements(Blockname).Elements("Input").Elements("DUTY").Value = Dictionary.get("Duty")
        self.BLK.Elements(Blockname).Elements("Input").Elements("VFRAC").Value = Dictionary.get("VaporFraction")
        self.BLK.Elements(Blockname).Elements("Input").Elements("PHASE").Value = Dictionary.get("Phase") #This can be V L or S
        self.BLK.Elements(Blockname).Elements("Input").Elements("NPHASE").Value = Dictionary.get("Phasenumber") #This can be 1,2,3
        self.BLK.Elements(Blockname).Elements("Input").Elements("SPEC_TYPE").Value = Dictionary.get("Specification_type") #This selects what input is needed:
        self.BLK.Elements(Blockname).Elements("Input").Elements("VOL").Value = Dictionary.get("VolumeReactor")
        self.BLK.Elements(Blockname).Elements("Input").Elements("RES_TIME").Value = Dictionary.get("ResidencetimeReactor")
        self.BLK.Elements(Blockname).Elements("Input").Elements("SPEC_PHASE").Value = Dictionary.get("Specification_Phase")
        self.BLK.Elements(Blockname).Elements("Input").Elements("REACT_VOL_FR").Value = Dictionary.get("VolumeFrac_of_Phase")
        self.BLK.Elements(Blockname).Elements("Input").Elements("REACT_VOL").Value = Dictionary.get("Volume_of_Phase")
        self.BLK.Elements(Blockname).Elements("Input").Elements("PH_RES_TIME").Value = Dictionary.get("Residencetime_of_Holdup")
        
        StreamnameNode = self.BLK.Elements(Blockname).Elements("Ports").Elements("F(IN)").Elements
        for Streamname in StreamnameNode:
            self.BLK.Elements(Blockname).Elements("Input").Elements("PROD_PHASE").Elements(Streamname).Value = Dictionary.get("Streamphase")
        
        self.BLK.Elements(Blockname).Elements("Input").Elements("REACSYS").Value = Dictionary.get("ActivateReactions_or_not")
        self.BLK.Elements(Blockname).Elements("Input").Elements("CRYSTSYS").Value = Dictionary.get("ActivateCrystalization_or_not")
        self.BLK.Elements(Blockname).Elements("Input").Elements("AGITATOR").Value = Dictionary.get("ActivateAgitation_or_not")
        self.BLK.Elements(Blockname).Elements("Input").Elements("AGITRATE").Value = Dictionary.get("Rotationrate")
        self.BLK.Elements(Blockname).Elements("Input").Elements("IMPELLR_DIAM").Value = Dictionary.get("ImpellerDiameter")
        self.BLK.Elements(Blockname).Elements("Input").Elements("POWERNUMBER").Value = Dictionary.get("Powernumber")
        self.BLK.Elements(Blockname).Elements("Input").Elements("OPT_PSD").Value = Dictionary.get("CalculationOption")
        self.BLK.Elements(Blockname).Elements("Input").Elements("CONST_METHOD").Value = Dictionary.get("ParticalGrowthModel")
        self.BLK.Elements(Blockname).Elements("Input").Elements("CAT_PRESENT").Value = Dictionary.get("CatalystPresentOption")
        self.BLK.Elements(Blockname).Elements("Input").Elements("IGN_CAT_VOL").Value = Dictionary.get("IgnoreCatalystVolume")
        self.BLK.Elements(Blockname).Elements("Input").Elements("CATWT").Value = Dictionary.get("WeightOfCatalystLoaded")
        self.BLK.Elements(Blockname).Elements("Input").Elements("CAT_RHO").Value = Dictionary.get("ParticleDensity")
        self.BLK.Elements(Blockname).Elements("Input").Elements("BED_VOIDAGE").Value = Dictionary.get("BedVoidage")


##CISTR:
#PAGE 1         Specifications
    def BLK_CISTR_Set_Pressure(self, Blockname, Pressure):
        self.BLK.Elements(Blockname).Elements("Input").Elements("PRES").Value = Pressure
    def BLK_CISTR_Set_Temperature(self, Blockname, Temperature):
        self.BLK.ELements(Blockname).Elements("Input").Elements("SPEC_OPT").Value = "TEMP"
        self.BLK.Elements(Blockname).Elements("Input").Elements("TEMP").Value = Temperature    
    def BLK_CISTR_Set_Duty(self, Blockname ,Duty):
        self.BLK.ELements(Blockname).Elements("Input").Elements("SPEC_OPT").Value = "DUTY"
        self.BLK.Elements(Blockname).Elements("Input").Elements("DUTY").Value = Duty
    def BLK_CISTR_Set_VaporFraction(self, Blockname, VaporFraction):
        self.BLK.ELements(Blockname).Elements("Input").Elements("SPEC_OPT").Value = "VFRAC"
        self.BLK.Elements(Blockname).Elements("Input").Elements("VFRAC").Value = VaporFraction
    def BLK_CISTR_Set_Phases(self, Blockname:str, Phase:Ph, Phasenumber:Phnum) -> None:
        self.BLK.Elements(Blockname).Elements("Input").Elements("PHASE").Value = Phase #This can be V L 
        self.BLK.Elements(Blockname).Elements("Input").Elements("NPHASE").Value = Phasenumber #This can be 1,2,3

    def BLK_CISTR_Set_Specification_type(self,Blockname:str, Specification_type: Literal["TOT-VOL", "RES-TIME", "TOT-VOL-PH-VOL", "TOT-VOL-PH-VOL-FRAC", "TOT-VOL-PH-RES-TIME", "RES-TIME-PH-VOL-FRAC"]) -> None:
        self.BLK.Elements(Blockname).Elements("Input").Elements("SPEC_TYPE").Value = Specification_type #This selects what input is needed:
            #The easy ones are: "TOT-VOL" or "RES-TIME" 
            #If there is only one Phase then you can chose these:
            #"TOT-VOL-PH-VOL" "TOT-VOL-PH-VOL-FRAC" "TOT-VOL-PH-RES-TIME" "RES-TIME-PH-VOL-FRAC"
    def BLK_CISTR_Set_Volume(self,Blockname, VolumeReactor):
        self.BLK.Elements(Blockname).Elements("Input").Elements("VOL").Value = VolumeReactor
    def BLK_CISTR_Set_ResidenceTime(self,Blockname, ResidencetimeReactor):
        self.BLK.Elements(Blockname).Elements("Input").Elements("RES_TIME").Value = ResidencetimeReactor
    def BLK_CISTR_Set_Specification_PhaseHoldup(self, Blockname, Specification_Phase):
        self.BLK.Elements(Blockname).Elements("Input").Elements("SPEC_PHASE").Value = Specification_Phase
    def BLK_CISTR_Set_VolumeFrac_of_PhaseHoldup(self, Blockname, VolumeFrac_of_Phase):
        self.BLK.Elements(Blockname).Elements("Input").Elements("REACT_VOL_FR").Value = VolumeFrac_of_Phase
    def BLK_CISTR_Set_Volume_of_PhaseHoldup(self, Blockname, Volume_of_Phase):
        self.BLK.Elements(Blockname).Elements("Input").Elements("REACT_VOL").Value = Volume_of_Phase
    def BLK_CISTR_Set_Residencetime_of_PhaseHoldup(self, Blockname, Residencetime_of_Holdup):
        self.BLK.Elements(Blockname).Elements("Input").Elements("PH_RES_TIME").Value = Residencetime_of_Holdup


###PAGE 2       Streams
    def BLK_CISTR_Set_Productstream_phase(self, Blockname, Streamname, Streamphase):
        self.BLK.Elements(Blockname).Elements("Input").Elements("PROD_PHASE").Elements(Streamname).Value = Streamphase


###PAGE 3       Kinetics
    def BLK_CISTR_Set_Activate_Reaction(self, Blockname:str, ActivateReactions_or_not: Literal["YES", "NO"]):
        self.BLK.Elements(Blockname).Elements("Input").Elements("REACSYS").Value = ActivateReactions_or_not
    ########    KINETICS IS STILL MISSING!!!!!!    #######
    def BLK_CISTR_Set_Activate_Crystalization(self, Blockname:str, ActivateCrystalization_or_not: Literal["YES", "NO"]):
        self.BLK.Elements(Blockname).Elements("Input").Elements("CRYSTSYS").Value = ActivateCrystalization_or_not
    def BLK_CISTR_Set_Activate_Agitation(self, Blockname:str, ActivateAgitation_or_not: Literal["YES", "NO"], Rotationrate:float, ImpellerDiameter:float, Powernumber:float):
        self.BLK.Elements(Blockname).Elements("Input").Elements("AGITATOR").Value = ActivateAgitation_or_not
        self.BLK.Elements(Blockname).Elements("Input").Elements("AGITRATE").Value = Rotationrate
        self.BLK.Elements(Blockname).Elements("Input").Elements("IMPELLR_DIAM").Value = ImpellerDiameter
        self.BLK.Elements(Blockname).Elements("Input").Elements("POWERNUMBER").Value = Powernumber


###PAGE 4       Particle Size Determination PSD
    def BLK_CISTR_Set_Calculation_Option(self, Blockname:str, CalculationOption: Literal["COPY" ,"CONSTANT"]) -> None:
        self.BLK.Elements(Blockname).Elements("Input").Elements("OPT_PSD").Value = CalculationOption
    def BLK_CISTR_Set_ParticalGrowthModel(self, Blockname:str, ParticalGrowthModel: Literal["DELTAD-NUM", "DELTAD-MASS", "DELTAV-NUM", "EQUI-MASS", "EQUI-SURFACE", "EQUI_NUMBER"]) -> None:
        self.BLK.Elements(Blockname).Elements("Input").Elements("CONST_METHOD").Value = ParticalGrowthModel
        
###PAGE 5       Component Attributes

###PAGE 6       Utilites

###PAGE 7       Catalysts
    def BLK_CISTR_Set_CatalystPresent(self, Blockname:str, CatalystPresentOption: Literal["YES" ,"NO"]) -> None:
        self.BLK.Elements(Blockname).Elements("Input").Elements("CAT_PRESENT").Value = CatalystPresentOption
    def BLK_CISTR_Set_IgnoreCatalystVolume(self, Blockname:str, IgnoreCatalystVolume: Literal["YES" ,"NO"]) -> None:
        self.BLK.Elements(Blockname).Elements("Input").Elements("IGN_CAT_VOL").Value = IgnoreCatalystVolume

    def BLK_CISTR_Set_WeightOfCatalystLoaded(self, Blockname, WeightOfCatalystLoaded):
        self.BLK.Elements(Blockname).Elements("Input").Elements("CATWT").Value = WeightOfCatalystLoaded
    def BLK_CISTR_Set_ParticleDensity(self, Blockname, ParticleDensity):
        self.BLK.Elements(Blockname).Elements("Input").Elements("CAT_RHO").Value = ParticleDensity
    def BLK_CISTR_Set_BedVoidage(self, Blockname, BedVoidage):
        self.BLK.Elements(Blockname).Elements("Input").Elements("BED_VOIDAGE").Value = BedVoidage

    






























    def BLK_RPLUG_GET_ME_ALL_INPUTS_BACK(self, Blockname:str) -> Dict[str, Union[str,float,int]]:
        """Retrieves all the Inputs and returns Dictionary with Values 
        
        Does not include all aspects of a Aspen Simulationsheet, for this look at Exports
        
        Args:
            Blockname: String which gives the name of Block.         
        """
    
        TYPE = self.BLK.Elements(Blockname).Elements("Input").Elements("TYPE").Value 
        Operating_conditions = self.BLK.Elements(Blockname).Elements("Input").Elements("OPT_TSPEC").Value    #Chose between INLET-TEMP, CONST-TEMP, TEMP-PROF
        ReactorTemperature = self.BLK.Elements(Blockname).Elements("Input").Elements("REAC_TEMP").Value 
        
        
        Constant_Temp = self.BLK.Elements(Blockname).Elements("Input").Elements("CTEMP").Value
        OutletTemp = self.BLK.Elements(Blockname).Elements("Input").Elements("TEMP").Value 
        U = self.BLK.Elements(Blockname).Elements("Input").Elements("U").Value
        Activate_YES_NO = self.BLK.Elements(Blockname).Elements("Input").Elements("CHK_NTUBE").Value 
        Number_of_Tubes = self.BLK.Elements(Blockname).Elements("Input").Elements("NTUBE").Value 
        TubeLength = self.BLK.Elements(Blockname).Elements("Input").Elements("LENGTH").Value 
        TubeDiameter = self.BLK.Elements(Blockname).Elements("Input").Elements("DIAM").Value
        Phase = self.BLK.Elements(Blockname).Elements("Input").Elements("PHASE").Value  #This can be V L or S
        Phasenumber = self.BLK.Elements(Blockname).Elements("Input").Elements("NPHASE").Value #This can be 1,2,3    
        ThermFluidPhase = self.BLK.Elements(Blockname).Elements("Input").Elements("CPHASE").Value   #"V" or "L"
        ThermFluidPhaseNumber = self.BLK.Elements(Blockname).Elements("Input").Elements("CNPHASE").Value     # 1 ,2 ,3 
        
        StreaminPortList = self.BLK.Elements(Blockname).Elements("Ports").Elements("P(OUT)").Elements
        ListingOfStreamnamesinProductphase = []
        for Streams in StreaminPortList:
            ListingOfStreamnamesinProductphase.append(Streams.Name)

        Streamphase = self.BLK.Elements(Blockname).Elements("Input").Elements("PROD_PHASE").Elements(ListingOfStreamnamesinProductphase[0]).Value
        ActivateReaction_YES_NO = self.BLK.Elements(Blockname).Elements("Input").Elements("REACSYS").Value 
        InletProcessflowPressure = self.BLK.Elements(Blockname).Elements("Input").Elements("PRES").Value
        InletThermalfluidPressure = self.BLK.Elements(Blockname).Elements("Input").Elements("CPRES").Value 
        PressuredropCalulationOption = self.BLK.Elements(Blockname).Elements("Input").Elements("OPT_PDROP").Value
        ThermalfluidPressureDrop = self.BLK.Elements(Blockname).Elements("Input").Elements("CPDROP").Value
        ProcessflowPressureDrop = self.BLK.Elements(Blockname).Elements("Input").Elements("PDROP").Value 
        Roughnessvalue = self.BLK.Elements(Blockname).Elements("Input").Elements("ROUGHNESS").Value 
        PressuredropCorrelation = self.BLK.Elements(Blockname).Elements("Input").Elements("DP_FCOR").Value
        CorrectionFactor = self.BLK.Elements(Blockname).Elements("Input").Elements("DP_MULT").Value 
        HoldupCalculationOption = self.BLK.Elements(Blockname).Elements("Input").Elements("OPT_HOLDUP").Value 
        HoldupCorrelation  = self.BLK.Elements(Blockname).Elements("Input").Elements("DP_HCOR").Value
        CatalystPresentOption = self.BLK.Elements(Blockname).Elements("Input").Elements("CAT_PRESENT").Value
        IgnoreCatalystVolume = self.BLK.Elements(Blockname).Elements("Input").Elements("IGN_CAT_VOL").Value
        WeightOfCatalystLoaded = self.BLK.Elements(Blockname).Elements("Input").Elements("CATWT").Value
        ParticleDensity = self.BLK.Elements(Blockname).Elements("Input").Elements("CAT_RHO").Value
        BedVoidage = self.BLK.Elements(Blockname).Elements("Input").Elements("BED_VOIDAGE").Value 

        Dictionary = {
        "TYPE":TYPE,
        "Operating_conditions":Operating_conditions ,
        "ReactorTemperature":ReactorTemperature ,
        "Constant_Temp":Constant_Temp ,
        "OutletTemp":OutletTemp ,
        "U":U ,
        "Activate_YES_NO":Activate_YES_NO ,
        "Number_of_Tubes":Number_of_Tubes ,
        "TubeLength":TubeLength ,
        "TubeDiameter":TubeDiameter ,
        "Phase":Phase ,
        "Phasenumber":Phasenumber ,
        "ThermFluidPhase":ThermFluidPhase ,
        "ThermFluidPhaseNumber":ThermFluidPhaseNumber ,
        "Streamphase":Streamphase ,
        "ActivateReaction_YES_NO":ActivateReaction_YES_NO ,
        "InletProcessflowPressure":InletProcessflowPressure ,
        "InletThermalfluidPressure":InletThermalfluidPressure ,
        "PressuredropCalulationOption":PressuredropCalulationOption ,
        "ThermalfluidPressureDrop":ThermalfluidPressureDrop ,
        "ProcessflowPressureDrop":ProcessflowPressureDrop ,
        "Roughnessvalue":Roughnessvalue ,
        "ThermalfluidPressureDrop":ThermalfluidPressureDrop ,
        "PressuredropCorrelation":PressuredropCorrelation ,
        "CorrectionFactor":CorrectionFactor ,
        "HoldupCalculationOption":HoldupCalculationOption , 
        "HoldupCorrelation":HoldupCorrelation ,
        "CatalystPresentOption":CatalystPresentOption , 
        "IgnoreCatalystVolume":IgnoreCatalystVolume ,
        "WeightOfCatalystLoaded":WeightOfCatalystLoaded ,
        "ParticleDensity":ParticleDensity ,
        "BedVoidage":BedVoidage
        }
        return Dictionary
    def BLK_RPLUG_SET_ALL_INPUTS(self, Blockname:str, Dictionary: Dict[str, Union[str,float,int]]) -> None:
        """Takes Dictionary with Values set the ones which are given in Aspen. 
        
        The Original Dictionary with its specific format can be found via "BLK_DSTWU_GET_ME_ALL_INPUTS_BACK"
        
        Args:
            Blockname: String which gives the name of Block.  
            Dictionary: Dictionary which contains all the Input variables.       
        """

        self.BLK.Elements(Blockname).Elements("Input").Elements("TYPE").Value = Dictionary.get("TYPE")
        self.BLK.Elements(Blockname).Elements("Input").Elements("OPT_TSPEC").Value = Dictionary.get("Operating_conditions")   #Chose between INLET-TEMP, CONST-TEMP, TEMP-PROF
        self.BLK.Elements(Blockname).Elements("Input").Elements("REAC_TEMP").Value = Dictionary.get("ReactorTemperature")
        self.BLK.Elements(Blockname).Elements("Input").Elements("U").Value = Dictionary.get("U")
        self.BLK.Elements(Blockname).Elements("Input").Elements("CTEMP").Value = Dictionary.get("Constant_Temp")
        self.BLK.Elements(Blockname).Elements("Input").Elements("TEMP").Value = Dictionary.get("OutletTemp")
        #PAGE 2     General Reactor Config
        self.BLK.Elements(Blockname).Elements("Input").Elements("CHK_NTUBE").Value = Dictionary.get("Activate_YES_NO")
        self.BLK.Elements(Blockname).Elements("Input").Elements("NTUBE").Value = Dictionary.get("Number_of_Tubes")
        self.BLK.Elements(Blockname).Elements("Input").Elements("LENGTH").Value = Dictionary.get("TubeLength")
        self.BLK.Elements(Blockname).Elements("Input").Elements("DIAM").Value = Dictionary.get("TubeDiameter")
        self.BLK.Elements(Blockname).Elements("Input").Elements("PHASE").Value = Dictionary.get("Phase") #This can be V L or S
        self.BLK.Elements(Blockname).Elements("Input").Elements("NPHASE").Value = Dictionary.get("Phasenumber") #This can be 1,2,3    
        self.BLK.Elements(Blockname).Elements("Input").Elements("CPHASE").Value = Dictionary.get("ThermFluidPhase")   #"V" or "L"
        self.BLK.Elements(Blockname).Elements("Input").Elements("CNPHASE").Value = Dictionary.get("ThermFluidPhaseNumber")    # 1 ,2 ,3 
        #PAGE 3     Streams
        StreaminPortList = self.BLK.Elements(Blockname).Elements("Ports").Elements("P(OUT)").Elements
        ListingOfStreamnamesinProductphase = []
        for Streams in StreaminPortList:
            ListingOfStreamnamesinProductphase.append(Streams.Name)
                #if there is a error here you need to have connected all the Streams before you can use this function...
        self.BLK.Elements(Blockname).Elements("Input").Elements("PROD_PHASE").Elements(ListingOfStreamnamesinProductphase[0]).Value = Dictionary.get("Streamphase")
        #PAGE 4     Reaction
        self.BLK.Elements(Blockname).Elements("Input").Elements("REACSYS").Value = Dictionary.get("ActivateReaction_YES_NO")
        #PAGE 5     Pressurespecification
        self.BLK.Elements(Blockname).Elements("Input").Elements("PRES").Value = Dictionary.get("InletProcessflowPressure")
        self.BLK.Elements(Blockname).Elements("Input").Elements("CPRES").Value = Dictionary.get("InletThermalfluidPressure")
        self.BLK.Elements(Blockname).Elements("Input").Elements("OPT_PDROP").Value = Dictionary.get("PressuredropCalulationOption")
        self.BLK.Elements(Blockname).Elements("Input").Elements("CPDROP").Value = Dictionary.get("ThermalfluidPressureDrop")
        self.BLK.Elements(Blockname).Elements("Input").Elements("PDROP").Value = Dictionary.get("ProcessflowPressureDrop")
        self.BLK.Elements(Blockname).Elements("Input").Elements("ROUGHNESS").Value = Dictionary.get("Roughnessvalue")
        self.BLK.Elements(Blockname).Elements("Input").Elements("CPDROP").Value = Dictionary.get("ThermalfluidPressureDrop")
        self.BLK.Elements(Blockname).Elements("Input").Elements("DP_FCOR").Value = Dictionary.get("PressuredropCorrelation")
        self.BLK.Elements(Blockname).Elements("Input").Elements("DP_MULT").Value = Dictionary.get("CorrectionFactor")
        #PAGE 6     Reactor holdup
        self.BLK.Elements(Blockname).Elements("Input").Elements("OPT_HOLDUP").Value = Dictionary.get("HoldupCalculationOption")
        self.BLK.Elements(Blockname).Elements("Input").Elements("DP_HCOR").Value = Dictionary.get("HoldupCorrelation")
        #PAGE 7     CATALYST
        self.BLK.Elements(Blockname).Elements("Input").Elements("CAT_PRESENT").Value = Dictionary.get("CatalystPresentOption")
        self.BLK.Elements(Blockname).Elements("Input").Elements("IGN_CAT_VOL").Value = Dictionary.get("IgnoreCatalystVolume")
        self.BLK.Elements(Blockname).Elements("Input").Elements("CATWT").Value = Dictionary.get("WeightOfCatalystLoaded")
        self.BLK.Elements(Blockname).Elements("Input").Elements("CAT_RHO").Value = Dictionary.get("ParticleDensity")
        self.BLK.Elements(Blockname).Elements("Input").Elements("BED_VOIDAGE").Value = Dictionary.get("BedVoidage")

 
##RPLUG

#PAGE 1     Reactor Type

    def BLK_RPLUG_Set_TYPE(self, Blockname:str, TYPE: Literal["T-SPEC", "ADIABATIC", "TCOOL-SPEC", "CO-COOL", "TCOOL-PROF", "QFLUX-PROF"]) -> None:
        '''defining the typ of Reactor which changes the necessary Inputs to make it run. Possibilities are: “T-SPEC” ”ADIABATIC” ”TCOOL-SPEC” “CO-COOL” “TCOOL-PROF” “QFLUX-PROF” '''
        self.BLK.Elements(Blockname).Elements("Input").Elements("TYPE").Value = TYPE

    #You chose Reactor with specific temperature:   	
    def BLK_RPLUG_Set_T_SPEC_Operating_condition(self, Blockname:str, Operating_conditions: Literal["INLET-TEMP", "CONST-TEMP", "TEMP-PROF"]) -> None:
        self.BLK.Elements(Blockname).Elements("Input").Elements("OPT_TSPEC").Value = Operating_conditions   #Chose between INLET-TEMP, CONST-TEMP, TEMP-PROF
        #if you chose INLET-TEMP:
            #Nothing is needed
        #if you chose CONST-TEMP:
    def BLK_RPLUG_Set_T_SPEC_Constant_Temp(self, Blockname, ReactorTemperature):   
        self.BLK.Elements(Blockname).Elements("Input").Elements("REAC_TEMP").Value = ReactorTemperature
        #if you chose Temperature Profile:
    #def BLK_RPLUG_Set_T_SPEC_TemperatureProfil(self, Blockname:str, TemperatureList: list[float], LocationList: list[float]) -> None:
    def BLK_RPLUG_Set_T_SPEC_TemperatureProfil(self, Blockname, TemperatureList, LocationList):
        """Sets the Temperature Profile in side of the Column
        
        Args:
            Blockname: String which gives the name of Block.  
            LocationList: List of location values which define where what temperature is found in the column
            TemperatureList: List of temperature values
        """
        #Check to see if it is the same size
        if len(TemperatureList) != len(LocationList):
            raise Exception('TemperatureList and LocationList need to have the same length! PList:{} LList: {}'.format(len(TemperatureList), len(LocationList)))
        i = 0
        for Temp in TemperatureList:
            listpositionname = "#" + str(i)
            self.BLK.Elements(Blockname).Elements("Input").Elements("SPEC_TEMP").Elements(listpositionname).Value = Temp
            i = i + 1
        i = 0
        for Location in LocationList:
            listpositionname = "#" + str(i)
            self.BLK.Elements(Blockname).Elements("Input").Elements("LOC").Elements(listpositionname).Value = Location
            i = i + 1
        i = 0

    #You chose Adiabetic reactor:
        #Nothing is needed
    
    #You chose TCOOL-SPEC (constant thermal fluid temperature
    def BLK_RPLUG_Set_TCOOL_SPEC_HeattransferU(self, Blockname, U):
        self.BLK.Elements(Blockname).Elements("Input").Elements("U").Value = U
    def BLK_RPLUG_Set_TCOOL_SPEC_ConstantTemp(self, Blockname, Constant_Temp):
        self.BLK.Elements(Blockname).Elements("Input").Elements("CTEMP").Value = Constant_Temp

    #You chose CO-COOL (co-current thermal fluid)
    def BLK_RPLUG_Set_CO_COOL_HeattransferU(self, Blockname, U):
        self.BLK.Elements(Blockname).Elements("Input").Elements("U").Value = U
    
    #You chose COUNTER-COOL (counter current thermal fluid)
    def BLK_RPLUG_COUNTER_COOL_HeattransferU(self, Blockname, U):
        self.BLK.Elements(Blockname).Elements("Input").Elements("U").Value = U
    def BLK_RPLUG_Set_COUNTER_COOL_OutletTemp(self, Blockname, OutletTemp):
        self.BLK.Elements(Blockname).Elements("Input").Elements("TEMP").Value = OutletTemp

    #You chose TCOOL-PROF (specific thermal fluid profile)
    def BLK_RPLUG_Set_TCOOL_PROF_HeattransferU(self, Blockname, U):
        self.BLK.Elements(Blockname).Elements("Input").Elements("U").Value = U
    def BLK_RPLUG_Set_TCOOL_PROF_TemperatureProfil(self, Blockname, TemperatureList: list, LocationList: list):
        """Sets the Temperature Profile in side of the Column
        
        Args:
            Blockname: String which gives the name of Block.  
            LocationList: List of location values which define where what temperature is found in the column
            TemperatureList: List of temperature values
        """
        #Check to see if it is the same size
        if len(TemperatureList) != len(LocationList):
            raise Exception('TemperatureList and LocationList need to have the same length! PList:{} LList: {}'.format(len(TemperatureList), len(LocationList)))

        i = 0
        for Temp in TemperatureList:
            listpositionname = "#" + str(i)
            self.BLK.Elements(Blockname).Elements("Input").Elements("TCOOL").Elements(listpositionname).Value = Temp
            i = i + 1
        i = 0
        for Location in LocationList:
            listpositionname = "#" + str(i)
            self.BLK.Elements(Blockname).Elements("Input").Elements("TCOOL_LOC").Elements(listpositionname).Value = Location
            i = i + 1
        i = 0

    #You chose QFLUX-PROF (defined Heatflux profile)
    def BLK_RPLUG_Set_QFLUX_PROF_HeatFluxProfil(self, Blockname:str , HeatFluxList: list, LocationList:list)-> None:
        """Sets the HeatFlux Profile in side of the Column
        
        Args:
            Blockname: String which gives the name of Block.  
            LocationList: List of location values which define where what temperature is found in the column
            HeatFluxList: List of Heatflux values
        """
        #Check to see if it is the same size
        if len(HeatFluxList) != len(LocationList):
            raise Exception('HeatFluxList and LocationList need to have the same length! PList:{} LList: {}'.format(len(HeatFluxList), len(LocationList)))

        i = 0
        for HeatFlux in HeatFluxList:
            listpositionname = "#" + str(i)
            self.BLK.Elements(Blockname).Elements("Input").Elements("QFLUX").Elements(listpositionname).Value = HeatFlux
            i = i + 1
        i = 0
        for Location in LocationList:
            listpositionname = "#" + str(i)
            self.BLK.Elements(Blockname).Elements("Input").Elements("QFLUX_LOC").Elements(listpositionname).Value = Location
            i = i + 1
        i = 0


#PAGE 2     General Reactor Config
    def BLK_RPLUG_Set_Activate_Multitube_Reactor(self, Blockname:str, Activate_YES_NO: Literal["YES", "NO"], Number_of_Tubes: int):    #Optional
        self.BLK.Elements(Blockname).Elements("Input").Elements("CHK_NTUBE").Value = Activate_YES_NO
        self.BLK.Elements(Blockname).Elements("Input").Elements("NTUBE").Value = Number_of_Tubes

    def BLK_RPLUG_Set_TubeLength(self, Blockname, TubeLength):
        self.BLK.Elements(Blockname).Elements("Input").Elements("LENGTH").Value = TubeLength
    def BLK_RPLUG_Set_TubeDiameter(self, Blockname,TubeDiameter):
        self.BLK.Elements(Blockname).Elements("Input").Elements("DIAM").Value = TubeDiameter
    def BLK_RPLUG_Set_Phases(self, Blockname:str, Phase:Ph, Phasenumber:Phnum):
        self.BLK.Elements(Blockname).Elements("Input").Elements("PHASE").Value = Phase #This can be V L or S
        self.BLK.Elements(Blockname).Elements("Input").Elements("NPHASE").Value = Phasenumber #This can be 1,2,3    
    def BLK_RPLUG_Set_Thermalfluid_ValidPhases(self, Blockname:str,ThermFluidPhase: Literal["V", "L"], ThermFluidPhaseNumber: Literal[1,2,3]) -> None:
        self.BLK.Elements(Blockname).Elements("Input").Elements("CPHASE").Value = ThermFluidPhase   #"V" or "L"
        self.BLK.Elements(Blockname).Elements("Input").Elements("CNPHASE").Value = ThermFluidPhaseNumber    # 1 ,2 ,3 


#PAGE 3     Streams
    def BLK_RPLUG_Set_Productstream_phase(self, Blockname, Streamname, Streamphase):
        self.BLK.Elements(Blockname).Elements("Input").Elements("PROD_PHASE").Elements(Streamname).Value = Streamphase


#PAGE 4     Reaction
    def BLK_RPLUG_Set_ActivateReactions(self, Blockname:str, ActivateReaction_YES_NO: Literal["YES", "NO"]) -> None:
        self.BLK.Elements(Blockname).Elements("Input").Elements("REACSYS").Value = ActivateReaction_YES_NO
    

                    ##MISSING THE MOVING THE REACTION THING OVER###
    def BLK_RPLUG_Set_ReactionActivities(self, Blockname:str, ActivityList: list, ActivityNameList:list) -> None:
        """Sets the Reaction Activities 
        
        Args:
            Blockname: String which gives the name of Block.  
            ActivityList: List of location values which define where what temperature is found in the column
            ActivityNameList: List of Heatflux values
        """
        #Check to see if it is the same size
        if len(ActivityList) != len(ActivityNameList):
            raise Exception('ActivityList and ActivityNameList need to have the same length! PList:{} LList: {}'.format(len(ActivityList), len(ActivityNameList)))

        i = 0
        for Activity in ActivityList:
            listpositionname = "#" + str(i)
            self.BLK.Elements(Blockname).Elements("Input").Elements("ACT_VALUE").Elements(listpositionname).Value = Activity
            i = i + 1
        i = 0
        for ActivityName in ActivityNameList:
            listpositionname = "#" + str(i)
            self.BLK.Elements(Blockname).Elements("Input").Elements("???????????????").Elements(listpositionname).Value = ActivityName
            i = i + 1
        i = 0


#PAGE 5     Pressurespecification
    def BLK_RPLUG_Set_InletProcessflowPressure(self, Blockname, InletProcessflowPressure):
        self.BLK.Elements(Blockname).Elements("Input").Elements("PRES").Value = InletProcessflowPressure
    def BLK_RPLUG_Set_InletThermalfluidPressure(self, Blockname, InletThermalfluidPressure):
        self.BLK.Elements(Blockname).Elements("Input").Elements("CPRES").Value = InletThermalfluidPressure
        #Chose Option for the Pressure drop calculation
    def BLK_RPLUG_Set_PressuredropCalulationOption(self, Blockname:str, PressuredropCalulationOption: Literal["SPECIFIED", "USER-SUBR", "CORRELATION"]) -> None:       #Possibilites are: “SPECIFIED“, “USER-SUBR“, “CORRELATION“:
        self.BLK.Elements(Blockname).Elements("Input").Elements("OPT_PDROP").Value = PressuredropCalulationOption
    
    #if you chose “SPECIFIED“
    def BLK_RPLUG_Set_SPECIFIED_ThermalfluidPressureDrop(self, Blockname,ThermalfluidPressureDrop):
        self.BLK.Elements(Blockname).Elements("Input").Elements("CPDROP").Value = ThermalfluidPressureDrop
    def BLK_RPLUG_Set_SPECIFIED_ProcessflowPressureDrop(self, Blockname, ProcessflowPressureDrop):
        self.BLK.Elements(Blockname).Elements("Input").Elements("PDROP").Value = ProcessflowPressureDrop
    
    #if you chose “USER-SUBR“
    def BLK_RPLUG_Set_USERSUBR_Roughnessvalue(self, Blockname, Roughnessvalue):
        self.BLK.Elements(Blockname).Elements("Input").Elements("ROUGHNESS").Value = Roughnessvalue
    
    #if you chose “CORRELATION“:
    def BLK_RPLUG_Set_CORRELATION_ThermalfluidPressureDrop(self, Blockname, ThermalfluidPressureDrop):
        self.BLK.Elements(Blockname).Elements("Input").Elements("CPDROP").Value = ThermalfluidPressureDrop
    def BLK_RPLUG_Set_CORRELATION_PressuredropCorrelation(self, Blockname,PressuredropCorrelation):     #You can chose between: BEGGS-BRILL DUKLER SLACK ORKI AWR LOCK-MART H-BROWN DARCY ERGUN HTFS		
        self.BLK.Elements(Blockname).Elements("Input").Elements("DP_FCOR").Value = PressuredropCorrelation
    def BLK_RPLUG_Set_CORRELATION_CorrectionFactor(self, Blockname, CorrectionFactor):
        self.BLK.Elements(Blockname).Elements("Input").Elements("DP_MULT").Value = CorrectionFactor


#PAGE 6     Reactor holdup
    def BLK_RPLUG_Set_HoldupCalculationOption(self, Blockname:str, HoldupCalculationOption: Literal["NO-SLIP", "CALCULATED", "SPECIFIED"]):            #You can chose between NO-SLIP, CALCULATED, SPECIFIED
        self.BLK.Elements(Blockname).Elements("Input").Elements("OPT_HOLDUP").Value = HoldupCalculationOption
    
    #if you chose NO-SLIP
        #Nothing is needed as Input

    #if you chose CALCULATED
    def BLK_RPLUG_Set_CALCULATED_HoldupCorrelation(self, Blockname,HoldupCorrelation):              #You can chose between BEGGS-BRILL FLANIGAN EATON HOOG HUGH SLACK ORKI AWR LOCK-MART H-BROWN USER-SUBR HTFS	
        self.BLK.Elements(Blockname).Elements("Input").Elements("DP_HCOR").Value = HoldupCorrelation

    #if you chose SPECIFIED
    def BLK_RPLUG_Set_SPECIFIED_HoldupProfilSOLID(self, Blockname:str, HoldupList: list, LocationList: list) -> None:
        """Sets the Solid HoldupProfile
        
        Args:
            Blockname: String which gives the name of Block.  
            HoldupList: List of location values which define where what temperature is found in the column
            LocationList: List of Heatflux values
        """
        #Check to see if it is the same size
        if len(HoldupList) != len(LocationList):
            raise Exception('HoldupList and LocationList need to have the same length! PList:{} LList: {}'.format(len(HoldupList), len(LocationList)))

        i = 0
        for Holdup in HoldupList:
            listpositionname = "#" + str(i)
            self.BLK.Elements(Blockname).Elements("Input").Elements("SHOLDUP").Elements(listpositionname).Value = Holdup
            i = i + 1
        i = 0
        for Location in LocationList:
            listpositionname = "#" + str(i)
            self.BLK.Elements(Blockname).Elements("Input").Elements("SHLOC").Elements(listpositionname).Value = Location
            i = i + 1
        i = 0
        
    def BLK_RPLUG_Set_SPECIFIED_HoldupProfilLIQUID(self, Blockname:str, HoldupList: list, LocationList: list):
        """Sets the Liquid HoldupProfile
        
        Args:
            Blockname: String which gives the name of Block.  
            HoldupList: List of location values which define where what temperature is found in the column
            LocationList: List of Heatflux values
        """
        #Check to see if it is the same size
        if len(HoldupList) != len(LocationList):
            raise Exception('HoldupList and LocationList need to have the same length! PList:{} LList: {}'.format(len(HoldupList), len(LocationList)))

        i = 0
        for Holdup in HoldupList:
            listpositionname = "#" + str(i)
            self.BLK.Elements(Blockname).Elements("Input").Elements("HOLDUP").Elements(listpositionname).Value = Holdup
            i = i + 1
        i = 0
        for Location in LocationList:
            listpositionname = "#" + str(i)
            self.BLK.Elements(Blockname).Elements("Input").Elements("HLOCK").Elements(listpositionname).Value = Location
            i = i + 1
        i = 0
        
#PAGE 7     CATALYST
    def BLK_RPLUG_Set_CatalystPresent(self, Blockname:str, CatalystPresentOption: Literal["YES", "NO"]):
        self.BLK.Elements(Blockname).Elements("Input").Elements("CAT_PRESENT").Value = CatalystPresentOption
    def BLK_RPLUG_Set_IgnoreCatalystVolume(self, Blockname:str, IgnoreCatalystVolume: Literal["YES", "NO"]):
        self.BLK.Elements(Blockname).Elements("Input").Elements("IGN_CAT_VOL").Value = IgnoreCatalystVolume

    def BLK_RPLUG_Set_WeightOfCatalystLoaded(self, Blockname, WeightOfCatalystLoaded):
        self.BLK.Elements(Blockname).Elements("Input").Elements("CATWT").Value = WeightOfCatalystLoaded
    def BLK_RPLUG_Set_ParticleDensity(self, Blockname, ParticleDensity):
        self.BLK.Elements(Blockname).Elements("Input").Elements("CAT_RHO").Value = ParticleDensity
    def BLK_RPLUG_Set_BedVoidage(self, Blockname, BedVoidage):
        self.BLK.Elements(Blockname).Elements("Input").Elements("BED_VOIDAGE").Value = BedVoidage




























    def BLK_RADFRAC_GET_ME_ALL_INPUTS_BACK(self, Blockname:str)-> Dict[str, Union[str,float,int]]:
        """Retrieves all the Inputs and returns Dictionary with Values 
        
        Does not include all aspects of a Aspen Simulationsheet, for this look at Exports
        
        Args:
            Blockname: String which gives the name of Block.         
        """
        
                    #PAGE 1         Configuration
        CalculationType = self.BLK.Elements(Blockname).Elements("Input").Elements("CALC_MODE").Value
        NStage = self.BLK.Elements(Blockname).Elements("Input").Elements("NSTAGE").Value 
        CondenserType = self.BLK.Elements(Blockname).Elements("Input").Elements("CONDENSER").Value
        ReboilerType = self.BLK.Elements(Blockname).Elements("Input").Elements("REBOILER").Value 
        Phase = self.BLK.Elements(Blockname).Elements("Input").Elements("Phase").Value #This can be V L or S
        Phasenumber = self.BLK.Elements(Blockname).Elements("Input").Elements("NPhase").Value  #This can be 1,2,3    
        ConvergenceMethod  = self.BLK.Elements(Blockname).Elements("Input").Elements("CONV_METH").Value 
        Refluxratio = self.BLK.Elements(Blockname).Elements("Input").Elements("BASIS_RR").Value 
        Refluxrate = self.BLK.Elements(Blockname).Elements("Input").Elements("BASIS_L1").Value
        BoilupRate = self.BLK.Elements(Blockname).Elements("Input").Elements("BASIS_VN").Value
        BoilupRatio = self.BLK.Elements(Blockname).Elements("Input").Elements("BASIS_BR").Value
        CondenserDuty = self.BLK.Elements(Blockname).Elements("Input").Elements("Q1").Value 
        ReboilerDuty = self.BLK.Elements(Blockname).Elements("Input").Elements("QN").Value
        TotalDestillateFlowrate = self.BLK.Elements(Blockname).Elements("Input").Elements("BASIS_D").Value 
        LiquidBottomRate = self.BLK.Elements(Blockname).Elements("Input").Elements("BASIS_B").Value
        DestillateToFeedRatio = self.BLK.Elements(Blockname).Elements("Input").Elements("BASIS_D:F").Value
        BottomToFeedRatio = self.BLK.Elements(Blockname).Elements("Input").Elements("BASIS_B:F").Value
                #Page 2     Streams
        FeedStreamNameNode = self.BLK.Elements(Blockname).Elements("Ports").Elements("F(IN)").Element
        for FeedStreamName in FeedStreamNameNode:
            FeedStage = self.BLK.Elements(Blockname).Elements("Input").Elements("FEED_STAGE").Elements(FeedStreamName).Value 
            FeedStageLocation = self.BLK.Elements(Blockname).Elements("Input").Elements("FEED_CONVE2").Elements(FeedStreamName).Value 

        CompleteProductStreamNameList = []
        ProductStreamNameList4LiquidDestillate = self.BLK.Elements(Blockname).Elements("Ports").Elements("LD(OUT)").Element
        for ProductStreamName in ProductStreamNameList4LiquidDestillate:
            CompleteProductStreamNameList.append(ProductStreamName)
        ProductStreamNameList4Bottoms = self.BLK.Elements(Blockname).Elements("Ports").Elements("B(OUT)").Element
        for ProductStreamName in ProductStreamNameList4Bottoms:
            CompleteProductStreamNameList.append(ProductStreamName)
            
        ProductStageLocationList = []
        ProductPhaseList = []
        for ProductStreamName in CompleteProductStreamNameList:
            ProductStageLocationList.append(self.BLK.Elements(Blockname).Elements("Input").Elements("PROD_STAGE").Elements(ProductStreamName).Value)
            ProductPhaseList.append(self.BLK.Elements(Blockname).Elements("Input").Elements("PROD_PHASE").Elements(ProductStreamName).Value)
        
               #Page 3     PRESSURE
        PressurePerspectiveOption = self.BLK.Elements(Blockname).Elements("Input").Elements("VIEW_PRES").Value
        CondenserPressure = self.BLK.Elements(Blockname).Elements("Input").Elements("PRES1").Value
        CondenserPressureDrop = self.BLK.Elements(Blockname).Elements("Input").Elements("PRES2").Value
        StagePressureDrop = self.BLK.Elements(Blockname).Elements("Input").Elements("DP_STAGE").Value 
                #PAGE 4         Condenser
        CoolRefluxandDestillate = self.BLK.Elements(Blockname).Elements("Input").Elements("SC_OPTION").Value
        CondenserTempOption = self.BLK.Elements(Blockname).Elements("Input").Elements("OPT_SUBCOOL").Value
        SubcooledTemp = self.BLK.Elements(Blockname).Elements("Input").Elements("SC_TEMP").Value
        DegreeSubcooled = self.BLK.Elements(Blockname).Elements("Input").Elements("DEGSUB").Value
        CondenserOption = self.BLK.Elements(Blockname).Elements("Input").Elements("OPT_COND").Value
        VaporTemp = self.BLK.Elements(Blockname).Elements("Input").Elements("T1").Value
        VaporFraction = self.BLK.Elements(Blockname).Elements("Input").Elements("BASIS_RDV").Value 
        ThermosyphonOption = self.BLK.Elements(Blockname).Elements("Input").Elements("OPT_TH_REB").Value
        ReboilerCirculationFlow = self.BLK.Elements(Blockname).Elements("Input").Elements("TH_FLOW").Value
        OutletTemperature = self.BLK.Elements(Blockname).Elements("Input").Elements("TH_TEMP").Value 
        ReboilerOutletPressure = self.BLK.Elements(Blockname).Elements("Input").Elements("TH_PRES").Value 
        ReboilerReturnLocation = self.BLK.Elements(Blockname).Elements("Input").Elements("RETURN_CONV").Value 
        ReboilerConfiguration = self.BLK.Elements(Blockname).Elements("Input").Elements("TSR_CONFIG").Value

        Dictionary = {
            #Page 1:
            "CalculationType":CalculationType,
            "NStage":NStage,
            "CondenserType":CondenserType,
            "ReboilerType":ReboilerType,
            "Phase":Phase,
            "Phasenumber":Phasenumber,
            "ConvergenceMethod":ConvergenceMethod,
            "Refluxratio":Refluxratio,
            "Refluxrate":Refluxrate,
            "BoilupRate":BoilupRate,
            "BoilupRatio":BoilupRatio,
            "CondenserDuty":CondenserDuty,
            "ReboilerDuty":ReboilerDuty,
            "TotalDestillateFlowrate":TotalDestillateFlowrate,
            "LiquidBottomRate":LiquidBottomRate,
            "DestillateToFeedRatio":DestillateToFeedRatio,
            "BottomToFeedRatio":BottomToFeedRatio,
            #Page 2       
            "FeedStage":FeedStage,
            "FeedStageLocation":FeedStageLocation,
            "ProductStageLocation":ProductStageLocationList,
            "ProductPhaseList":ProductPhaseList,
            #Page 3
            "PressurePerspectiveOption":PressurePerspectiveOption,
            "CondenserPressure":CondenserPressure,
            "CondenserPressureDrop":CondenserPressureDrop,
            "StagePressureDrop":StagePressureDrop,
            #Page 4
            "CondenserTempOption":CondenserTempOption,
            "CoolRefluxandDestillate":CoolRefluxandDestillate,
            "CondenserTempOption":CondenserTempOption,
            "SubcooledTemp":SubcooledTemp,
            "DegreeSubcooled":DegreeSubcooled,
            "CoolRefluxandDestillate":CoolRefluxandDestillate,
            "CondenserOption":CondenserOption,
            "VaporTemp":VaporTemp,
            "VaporFraction":VaporFraction,
            "ThermosyphonOption":ThermosyphonOption,
            "ReboilerCirculationFlow":ReboilerCirculationFlow,
            "OutletTemperature":OutletTemperature,
            "ReboilerOutletPressure":ReboilerOutletPressure,
            "ReboilerReturnLocation":ReboilerReturnLocation,
            "ReboilerConfiguration":ReboilerConfiguration,
        }
        return Dictionary
    def BLK_RADFRAC_SET_ALL_INPUTS(self, Blockname:str, Dictionary: Dict[str, Union[str,float,int]]) -> None:
        """Takes Dictionary with Values set the ones which are given in Aspen. 
        
        The Original Dictionary with its specific format can be found via "BLK_DSTWU_GET_ME_ALL_INPUTS_BACK"
        
        Args:
            Blockname: String which gives the name of Block.  
            Dictionary: Dictionary which contains all the Input variables.       
        """

        self.BLK.Elements(Blockname).Elements("Input").Elements("CALC_MODE").Value = Dictionary.get("CalculationType")
        self.BLK.Elements(Blockname).Elements("Input").Elements("NSTAGE").Value = Dictionary.get("NStage")
        self.BLK.Elements(Blockname).Elements("Input").Elements("CONDENSER").Value = Dictionary.get("CondenserType")
        self.BLK.Elements(Blockname).Elements("Input").Elements("REBOILER").Value = Dictionary.get("ReboilerType")
        self.BLK.Elements(Blockname).Elements("Input").Elements("Phase").Value = Dictionary.get("Phase") #This can be V L or S
        self.BLK.Elements(Blockname).Elements("Input").Elements("NPhase").Value = Dictionary.get("Phasenumber") #This can be 1,2,3    
        self.BLK.Elements(Blockname).Elements("Input").Elements("CONV_METH").Value = Dictionary.get("ConvergenceMethod")
        self.BLK.Elements(Blockname).Elements("Input").Elements("BASIS_RR").Value = Dictionary.get("Refluxratio")
        self.BLK.Elements(Blockname).Elements("Input").Elements("BASIS_L1").Value = Dictionary.get("Refluxrate")
        self.BLK.Elements(Blockname).Elements("Input").Elements("BASIS_VN").Value = Dictionary.get("BoilupRate")
        self.BLK.Elements(Blockname).Elements("Input").Elements("BASIS_BR").Value = Dictionary.get("BoilupRatio")
        self.BLK.Elements(Blockname).Elements("Input").Elements("Q1").Value = Dictionary.get("CondenserDuty")
        self.BLK.Elements(Blockname).Elements("Input").Elements("QN").Value = Dictionary.get("ReboilerDuty")
        self.BLK.Elements(Blockname).Elements("Input").Elements("BASIS_D").Value = Dictionary.get("TotalDestillateFlowrate")
        self.BLK.Elements(Blockname).Elements("Input").Elements("BASIS_B").Value = Dictionary.get("LiquidBottomRate")
        self.BLK.Elements(Blockname).Elements("Input").Elements("BASIS_D:F").Value = Dictionary.get("DestillateToFeedRatio")
        self.BLK.Elements(Blockname).Elements("Input").Elements("BASIS_B:F").Value = Dictionary.get("BottomToFeedRatio")
        #Page 2     Streams    
        
        
        
        FeedStreamNameNode = self.BLK.Elements(Blockname).Elements("Ports").Elements("F(IN)").Element
        for FeedStreamName in FeedStreamNameNode:
            self.BLK.Elements(Blockname).Elements("Input").Elements("FEED_STAGE").Elements(FeedStreamName).Value = Dictionary.get("FeedStage")
            self.BLK.Elements(Blockname).Elements("Input").Elements("FEED_CONVE2").Elements(FeedStreamName).Value = Dictionary.get("FeedStageLocation")

        CompleteProductStreamNameList = []
        ProductStreamNameList4LiquidDestillate = self.BLK.Elements(Blockname).Elements("Ports").Elements("LD(OUT)").Element
        for ProductStreamName in ProductStreamNameList4LiquidDestillate:
            CompleteProductStreamNameList.append(ProductStreamName)
        ProductStreamNameList4Bottoms = self.BLK.Elements(Blockname).Elements("Ports").Elements("B(OUT)").Element
        for ProductStreamName in ProductStreamNameList4Bottoms:
            CompleteProductStreamNameList.append(ProductStreamName)
        
        ProductStageLocationList = Dictionary.get("ProductStageLocationList")
        ProductPhase = Dictionary.get("ProductPhase")
        i = 0  
        for ProductStreamName in CompleteProductStreamNameList:
            self.BLK.Elements(Blockname).Elements("Input").Elements("PROD_STAGE").Elements(ProductStreamName).Value = ProductStageLocationList[i]
            self.BLK.Elements(Blockname).Elements("Input").Elements("PROD_PHASE").Elements(ProductStreamName).Value = ProductPhase[i]
            i = i + 1
    
        #Page 3     PRESSURE
        self.BLK.Elements(Blockname).Elements("Input").Elements("VIEW_PRES").Value = Dictionary.get("PressurePerspectiveOption")
        self.BLK.Elements(Blockname).Elements("Input").Elements("PRES1").Value = Dictionary.get("CondenserPressure")
        self.BLK.Elements(Blockname).Elements("Input").Elements("PRES2").Value = Dictionary.get("CondenserPressureDrop")
        self.BLK.Elements(Blockname).Elements("Input").Elements("DP_STAGE").Value = Dictionary.get("StagePressureDrop")
        self.BLK.Elements(Blockname).Elements("Input").Elements("PRES1").Value = Dictionary.get("TopStagePressure")
        #PAGE 4         Condenser
        self.BLK.Elements(Blockname).Elements("Input").Elements("OPT_SUBCOOL").Value = Dictionary.get("CondenserTempOption")
        self.BLK.Elements(Blockname).Elements("Input").Elements("SC_TEMP").Value = Dictionary.get("SubcooledTemp")
        self.BLK.Elements(Blockname).Elements("Input").Elements("DEGSUB").Value = Dictionary.get("DegreeSubcooled")
        self.BLK.Elements(Blockname).Elements("Input").Elements("SC_OPTION").Value = Dictionary.get("CoolRefluxandDestillate")
        self.BLK.Elements(Blockname).Elements("Input").Elements("OPT_SUBCOOL").Value = Dictionary.get("CondenserTempOption")
        self.BLK.Elements(Blockname).Elements("Input").Elements("SC_TEMP").Value = Dictionary.get("SubcooledTemp")
        self.BLK.Elements(Blockname).Elements("Input").Elements("DEGSUB").Value = Dictionary.get("DegreeSubcooled")
        self.BLK.Elements(Blockname).Elements("Input").Elements("SC_OPTION").Value = Dictionary.get("CoolRefluxandDestillate")
        self.BLK.Elements(Blockname).Elements("Input").Elements("OPT_COND").Value = Dictionary.get("CondenserOption") 
        self.BLK.Elements(Blockname).Elements("Input").Elements("T1").Value = Dictionary.get("VaporTemp")
        self.BLK.Elements(Blockname).Elements("Input").Elements("BASIS_RDV").Value = Dictionary.get("VaporFraction")
        #PAGE 5 Reboiler
        self.BLK.Elements(Blockname).Elements("Input").Elements("OPT_TH_REB").Value = Dictionary.get("ThermosyphonOption")
        self.BLK.Elements(Blockname).Elements("Input").Elements("TH_FLOW").Value = Dictionary.get("ReboilerCirculationFlow")
        self.BLK.Elements(Blockname).Elements("Input").Elements("TH_TEMP").Value = Dictionary.get("OutletTemperature")
        self.BLK.Elements(Blockname).Elements("Input").Elements("TH_FLOW").Value = Dictionary.get("ReboilerCirculationFlow")
        self.BLK.Elements(Blockname).Elements("Input").Elements("TH_TEMP").Value = Dictionary.get("OutletTemperature")
        self.BLK.Elements(Blockname).Elements("Input").Elements("TH_PRES").Value = Dictionary.get("ReboilerOutletPressure")
        self.BLK.Elements(Blockname).Elements("Input").Elements("RETURN_CONV").Value = Dictionary.get("ReboilerReturnLocation")
        self.BLK.Elements(Blockname).Elements("Input").Elements("TSR_CONFIG").Value = Dictionary.get("ReboilerConfiguration")
    


##RADFRAC

#PAGE 1         Configuration
    def BLK_RADFRAC_Set_CalculationType(self, Blockname:str , CalculationType: Literal["RIG-RATE", "EQUILIBRIUM"]) -> None:       #This can be RIG-RATE,  EQUILIBRIUM
        self.BLK.Elements(Blockname).Elements("Input").Elements("CALC_MODE").Value = CalculationType
    def BLK_RADFRAC_Set_NSTAGE(self, Blockname, NStage):
        self.BLK.Elements(Blockname).Elements("Input").Elements("NSTAGE").Value = NStage
    def BLK_RADFRAC_Set_CondenserType(self, Blockname:str, CondenserType: Literal["NONE", "TOTAL", "PARTIAL-V", "PARTIAL-V-L"]) -> None:          #THIS can be NONE, TOTAL, PARTIAL-V, PARTIAL-V-L        Very important for Page 4
        self.BLK.Elements(Blockname).Elements("Input").Elements("CONDENSER").Value = CondenserType
    def BLK_RADFRAC_Set_ReboilerType(self, Blockname:str, ReboilerType: Literal["NONE", "KETTLE", "THERMOSYPHON"]):            #Can be NONE, KETTLE, THERMOSYPHON, This is important for Page 5
        self.BLK.Elements(Blockname).Elements("Input").Elements("REBOILER").Value = ReboilerType
    def BLK_RADFRAC_Set_Phases(self, Blockname:str, Phase:Ph, Phasenumber:Phnum):
        self.BLK.Elements(Blockname).Elements("Input").Elements("Phase").Value = Phase #This can be V L or S
        self.BLK.Elements(Blockname).Elements("Input").Elements("NPhase").Value = Phasenumber #This can be 1,2,3    
    def BLK_RADFRAC_Set_ConvergenceMethod(self, Blockname:str, ConvergenceMethod: Literal["STANDARD", "PETROLEUM", "NONIDEAL", "AZEOTROPIC", "CRYOGENIX", "OTHERS"]) -> None:      #This can be STANDARD, PETROLEUM, NONIDEAL, AZEOTROPIC, CRYOGENIX, OTHERS
        self.BLK.Elements(Blockname).Elements("Input").Elements("CONV_METH").Value = ConvergenceMethod 
    def BLK_RADFRAC_Set_Refluxratio(self, Blockname, Refluxratio):
        self.BLK.Elements(Blockname).Elements("Input").Elements("BASIS_RR").Value = Refluxratio
    def BLK_RADFRAC_Set_Refluxrate(self, Blockname, Refluxrate):
        self.BLK.Elements(Blockname).Elements("Input").Elements("BASIS_L1").Value = Refluxrate
    def BLK_RADFRAC_Set_BoilupRate(self, Blockname, BoilupRate):
        self.BLK.Elements(Blockname).Elements("Input").Elements("BASIS_VN").Value = BoilupRate
    def BLK_RADFRAC_Set_BoilupRatio(self, Blockname, BoilupRatio):
        self.BLK.Elements(Blockname).Elements("Input").Elements("BASIS_BR").Value = BoilupRatio
    def BLK_RADFRAC_Set_CondenserDuty(self, Blockname,CondenserDuty):
        self.BLK.Elements(Blockname).Elements("Input").Elements("Q1").Value = CondenserDuty
    def BLK_RADFRAC_Set_ReboilerDuty(self, Blockname,ReboilerDuty):
        self.BLK.Elements(Blockname).Elements("Input").Elements("QN").Value = ReboilerDuty
    def BLK_RADFRAC_Set_TotalDestillateFlowrate(self, Blockname, TotalDestillateFlowrate):
        self.BLK.Elements(Blockname).Elements("Input").Elements("BASIS_D").Value = TotalDestillateFlowrate
    def BLK_RADFRAC_Set_LiquidBottomRate(self, Blockname, LiquidBottomRate):
        self.BLK.Elements(Blockname).Elements("Input").Elements("BASIS_B").Value = LiquidBottomRate
    def BLK_RADFRAC_Set_DestillateToFeedRatio(self, Blockname, DestillateToFeedRatio):
        self.BLK.Elements(Blockname).Elements("Input").Elements("BASIS_D:F").Value = DestillateToFeedRatio
    def BLK_RADFRAC_Set_BottomToFeedRatio(self, Blockname, BottomToFeedRatio):
        self.BLK.Elements(Blockname).Elements("Input").Elements("BASIS_B:F").Value = BottomToFeedRatio
    

#Page 2     Streams    
    def BLK_RADFRAC_Set_FeedStage(self, Blockname,FeedStage, FeedstreamName):
        self.BLK.Elements(Blockname).Elements("Input").Elements("FEED_STAGE").Elements(FeedstreamName).Value = FeedStage
    def BLK_RADFRAC_Set_FeedStageLocation(self, Blockname, FeedStageLocation: Literal["ON-STAGE", "ABOVE-STAGE", "ON-STAGE-VAP", "ON-STAGE-LIQ"], FeedstreamName: str) -> None:      #Location can be ON-STAGE, ABOVE-STAGE, ON-STAGE-VAP, ON-STAGE-LIQ
        self.BLK.Elements(Blockname).Elements("Input").Elements("FEED_CONVE2").Elements(FeedstreamName).Value = FeedStageLocation
    def BLK_RADFRAC_Set_ProductStreamStage(self, Blockname, ProductStageLocation, ProductstreamName):
        self.BLK.Elements(Blockname).Elements("Input").Elements("FEED_CONVE2").Elements(ProductstreamName).Value = ProductStageLocation
    def BLK_RADFRAC_Set_ProductPhase(self, Blockname:str, ProductPhase: Literal["L", "L1", "L2", "W", "V", "TL", "TV"], ProductStreamName: str) -> None:         #ProductPhases: L, L1, L2, W, V, TL, TV
        self.BLK.Elements(Blockname).Elements("Input").Elements("PROD_PHASE").Elements(ProductStreamName).Value = ProductPhase 


#Page 3     PRESSURE
    def BLK_RADFRAC_Set_PressurePerspectiveOption(self, Blockname:str, PressurePerspectiveOption: Literal["TOP/BOTTOM", "PROFILE", "PDROP"]) -> None:   #You can chose TOP/BOTTOM, PROFILE, PDROP
        self.BLK.Elements(Blockname).Elements("Input").Elements("VIEW_PRES").Value = PressurePerspectiveOption
    
    #if you chose TOP/BOTTOM
    def BLK_RADFRAC_Set_TOPBOTTOM_CondenserPressure(self, Blockname, CondenserPressure):
        self.BLK.Elements(Blockname).Elements("Input").Elements("PRES1").Value = CondenserPressure
    def BLK_RADFRAC_Set_TOPBOTTOM_CondenserPressureDrop(self, Blockname, CondenserPressureDrop):
        self.BLK.Elements(Blockname).Elements("Input").Elements("PRES2").Value = CondenserPressureDrop
    def BLK_RADFRAC_Set_TOPBOTTOM_StagePressureDrop(self, Blockname, StagePressureDrop):
        self.BLK.Elements(Blockname).Elements("Input").Elements("DP_STAGE").Value = StagePressureDrop
    
    #if you chose PROFILE
    def BLK_RADFRAC_Set_PROFILE_Pressure(self, Blockname:str, PressureList: list, LocationList:list) -> None:
        """Sets the Pressure Profile in side of the Column
        
        Args:
            Blockname: String which gives the name of Block.  
            LocationList: List of location values which define what pressure is found in the column
            PressureList: List of pressure values
        """
        #Check to see if it is the same size
        if len(PressureList) != len(LocationList):
            raise Exception('PressureList and LocationList need to have the same length! PList:{} LList: {}'.format(len(PressureList), len(LocationList)))
        
        i = 0    
        for Pressure in PressureList:
            listpositionname = LocationList[i]
            self.BLK.Elements(Blockname).Elements("Input").Elements("STAGE_PRES").Elements(listpositionname).Value = Pressure
            i = i + 1
        i = 0

    #if you chose PDROP 
    def BLK_RADFRAC_Set_PDROP_TopStagePressure(self, Blockname, TopStagePressure):
        self.BLK.Elements(Blockname).Elements("Input").Elements("PRES1").Value = TopStagePressure
    
    def BLK_RADFRAC_Set_PDROP_StagePDROP_Profile(self, Blockname:str, LocationList: list, StartingStageList: list, EndingStageList: list, PressureDropList: list) -> None:    
        """Sets the Pressure Profile in side of the Column
        
        Args:
            Blockname: String which gives the name of Block.  
            LocationList: List for numbering the sections
            PressureDropList: List of pressure drop values per section
            StartingStageList: List of Stages where sections begin
            EndingStageList: List of Stages where sections end
        """
        #Check to see if it is the same size
        if len(PressureDropList) != len(LocationList):
            raise Exception('PressureDropList and LocationList need to have the same length! PList:{} LList: {}'.format(len(PressureDropList), len(LocationList)))
        if len(StartingStageList) != len(LocationList):
            raise Exception('StartingStageList and LocationList need to have the same length! PList:{} LList: {}'.format(len(StartingStageList), len(LocationList)))
        if len(EndingStageList) != len(LocationList):
            raise Exception('EndingStageList and LocationList need to have the same length! PList:{} LList: {}'.format(len(EndingStageList), len(LocationList)))
        
        i = 0
        for StartingStage in StartingStageList:
            listpositionname = LocationList[i]
            self.BLK.Elements(Blockname).Elements("Input").Elements("PRES_STAGE1").Elements(listpositionname).Value = StartingStage
            self.BLK.Elements(Blockname).Elements("Input").Elements("PRES_STAGE2").Elements(listpositionname).Value = EndingStageList[i]
            self.BLK.Elements(Blockname).Elements("Input").Elements("PDROP_SEC").Elements(listpositionname).Value = PressureDropList[i]
            i = i + 1
        i = 0
#PAGE 4         Condenser
    
    #if NONE was chosen on Page 1 for the Condenser type aka    BLK_RADFRAC_CondenserType()
        #Nothing is needed for this input.
    
    #if TOTAL or PARTIAL-V was chosen
        #Choice between Condenser Temperature and Degrees subcooled
    def BLK_RADFRAC_Set_TOTALorPARTIALV_CondenserTempOption(self, Blockname:str, CondenserTempOption: Literal["TEMP", "SUBCOOL"]) -> None:      #You can chose between TEMP for Subcooled temperature, or SUBCOOL for degrees subcooled
        self.BLK.Elements(Blockname).Elements("Input").Elements("OPT_SUBCOOL").Value = CondenserTempOption
        #if you chose TEMP
    def BLK_RADFRAC_Set_TOTALorPARTIALV_TEMP(self, Blockname, SubcooledTemp):
        self.BLK.Elements(Blockname).Elements("Input").Elements("SC_TEMP").Value = SubcooledTemp
        #if you chose SUBCOOL
    def BLK_RADFRAC_Set_TOTALorPARTIALV_SUBCOOL(self, Blockname, DegreeSubcooled):
        self.BLK.Elements(Blockname).Elements("Input").Elements("DEGSUB").Value = DegreeSubcooled
    def BLK_RADFRAC_Set_TOTALorPARTIALV_CoolRefluxandDestillate(self, Blockname: str, CoolRefluxandDestillate: Literal["REFLUX-AND-DESTILLATE", "REFLUX-ONLY"]) -> None:     #You can chose REFLUX-AND-DESTILLATE or REFLUX-ONLY
        self.BLK.Elements(Blockname).Elements("Input").Elements("SC_OPTION").Value = CoolRefluxandDestillate
    
    #if PARTIAL_V_L
    def BLK_RADFRAC_Set_PARTIAL_V_L_CondenserTempOption(self, Blockname:str, CondenserTempOption: Literal["TEMP", "SUBCOOL"]) -> None:      #You can chose between TEMP for Subcooled temperature, or SUBCOOL for degrees subcooled
        self.BLK.Elements(Blockname).Elements("Input").Elements("OPT_SUBCOOL").Value = CondenserTempOption
        #if you chose TEMP
    def BLK_RADFRAC_Set_PARTIAL_V_L_TEMP(self, Blockname, SubcooledTemp):
        self.BLK.Elements(Blockname).Elements("Input").Elements("SC_TEMP").Value = SubcooledTemp
        #if you chose SUBCOOL   
    def BLK_RADFRAC_Set_PARTIAL_V_L_SUBCOOL(self, Blockname, DegreeSubcooled):
        self.BLK.Elements(Blockname).Elements("Input").Elements("DEGSUB").Value = DegreeSubcooled
    def BLK_RADFRAC_Set_PARTIAL_V_L_CoolRefluxandDestillate(self, Blockname:str, CoolRefluxandDestillate: Literal["REFLUX-AND-DESTILLATE", "REFLUX-ONLY"]) -> None:     #You can chose REFLUX-AND-DESTILLATE or REFLUX-ONLY
        self.BLK.Elements(Blockname).Elements("Input").Elements("SC_OPTION").Value = CoolRefluxandDestillate

    #Chose between specifying the Destillate Vapor fraction or the Temperature
    def BLK_RADFRAC_Set_PARTIAL_V_L_CondenserOption(self, Blockname:str, CondenserOption: Literal["TEMP", "VFRAC"]) -> None:      #you can chose between TEMP and VFRAC
        self.BLK.Elements(Blockname).Elements("Input").Elements("OPT_COND").Value = CondenserOption 
        #if you chose TEMP
    def BLK_RADFRAC_Set_PARTIAL_V_L_TEMP_VaporTemp(self, Blockname,VaporTemp):
        self.BLK.Elements(Blockname).Elements("Input").Elements("T1").Value = VaporTemp
        #if you chose VFRAC
    def BLK_RADFRAC_Set_PARTIAL_V_L_TEMP_VaporFraction(self, Blockname, VaporFraction):
        self.BLK.Elements(Blockname).Elements("Input").Elements("BASIS_RDV").Value = VaporFraction
    

#PAGE 5 Reboiler
    #Similar to the Condenser it all depends on the selection on Page 1         BLK_RADFRAC_ReboilerType(
    #if you chose NONE or KETTLE:
            #Nothing is needed
    #if you chose THERMOSYPHON
    def BLK_RADFRAC_Set_THERMOSYPHON_OPTIONS(self, Blockname:str, ThermosyphonOption: Literal["FLOW", "OUTLET", "FLOW+OUTLET"]) -> None:       #You can chose between FLOW, OUTLET, FLOW+OUTLET
        self.BLK.Elements(Blockname).Elements("Input").Elements("OPT_TH_REB").Value = ThermosyphonOption
        #if Flow was selected:
    def BLK_RADFRAC_Set_THERMOSYPHON_FLOW(self, Blockname, ReboilerCirculationFlow):
        self.BLK.Elements(Blockname).Elements("Input").Elements("TH_FLOW").Value = ReboilerCirculationFlow
        #if OUTLET was selected:
    def BLK_RADFRAC_Set_THERMOSYPHON_OUTLET(self, Blockname, OutletTemperature):
        self.BLK.Elements(Blockname).Elements("Input").Elements("TH_TEMP").Value = OutletTemperature
        #if FLOW+OUTLET was selected:
    def BLK_RADFRAC_Set_THERMOSYPHON_FLOW(self, Blockname, ReboilerCirculationFlow):
        self.BLK.Elements(Blockname).Elements("Input").Elements("TH_FLOW").Value = ReboilerCirculationFlow
    def BLK_RADFRAC_Set_THERMOSYPHON_OUTLET(self, Blockname, OutletTemperature):
        self.BLK.Elements(Blockname).Elements("Input").Elements("TH_TEMP").Value = OutletTemperature
        
    #More Optional Parameters:
    def BLK_RADFRAC_Set_ReboilerOutletPressure(self, Blockname, ReboilerOutletPressure):
        self.BLK.Elements(Blockname).Elements("Input").Elements("TH_PRES").Value = ReboilerOutletPressure
    def BLK_RADFRAC_Set_ReboilerReturnLocation(self, Blockname:str, ReboilerReturnLocation: Literal["ABOVE-STAGE", "ON-STAGE"]) -> None:    #IT can be ABOVE-STAGE or ON-STAGE
        self.BLK.Elements(Blockname).Elements("Input").Elements("RETURN_CONV").Value = ReboilerReturnLocation
    def BLK_RADFRAC_Set_ReboilerConfiguration(self, Blockname, ReboilerConfiguration: Literal[1,2,3]):      #This can be 1 or 2 or 3. 
        self.BLK.Elements(Blockname).Elements("Input").Elements("TSR_CONFIG").Value = ReboilerConfiguration
    
    
    
    


















    def BLK_FLASH2_GET_ME_ALL_INPUTS_BACK(self, Blockname:str)-> Dict[str, Union[str,float,int]]:
        """Retrieves all the Inputs and returns Dictionary with Values 
        
        Does not include all aspects of a Aspen Simulationsheet, for this look at Exports
        
        Args:
            Blockname: String which gives the name of Block.         
        """
        
        FlashTypeOption = self.BLK.Elements(Blockname).Elements("Input").Elements("SPEC_OPT").Value
        Temperature = self.BLK.Elements(Blockname).Elements("Input").Elements("TEMP").Value 
        Pressure = self.BLK.Elements(Blockname).Elements("Input").Elements("PRES").Value
        Duty = self.BLK.Elements(Blockname).Elements("Input").Elements("DUTY").Value 
        Vapor_fraction = self.BLK.Elements(Blockname).Elements("Input").Elements("VFRAC").Value
        Phase = self.BLK.Elements(Blockname).Elements("Input").Elements("Phase").Value #This can be V L
        Phasenumber = self.BLK.Elements(Blockname).Elements("Input").Elements("NPhase").Value #This can be 1,2,3    
        TemperatureEstimation = self.BLK.Elements(Blockname).Elements("Input").Elements("T_EST").Value 
        PressureEstimation = self.BLK.Elements(Blockname).Elements("Input").Elements("P_EST").Value
        MaximumIteration = self.BLK.Elements(Blockname).Elements("Input").Elements("MAXIT").Value
        ErrorTolerance = self.BLK.Elements(Blockname).Elements("Input").Elements("TOL").Value
        Liquid_Entrainment = self.BLK.Elements(Blockname).Elements("Input").Elements("ENTRN").Value
        Solid_Entrainment = self.BLK.Elements(Blockname).Elements("Input").Elements("VAPOR").Elements("MIXED").Value
        CalculationOption = self.BLK.Elements(Blockname).Elements("Input").Elements("OPT_PSD").Value
        ParticalGrowthModel = self.BLK.Elements(Blockname).Elements("Input").Elements("CONST_METHOD").Value
        
        Dictionary = {
            "FlashTypeOption":FlashTypeOption,
            "Temperature":Temperature,
            "Pressure":Pressure,
            "Duty":Duty,
            "Vapor_fraction":Vapor_fraction,
            "Phase":Phase,
            "Phasenumber":Phasenumber,
            "TemperatureEstimation":TemperatureEstimation,
            "PressureEstimation":PressureEstimation,
            "MaximumIteration":MaximumIteration,
            "ErrorTolerance":ErrorTolerance,
            "Liquid_Entrainment":Liquid_Entrainment,
            "Solid_Entrainment":Solid_Entrainment,
            "CalculationOption":CalculationOption,
            "ParticalGrowthModel":ParticalGrowthModel,
        }
        return Dictionary
    def BLK_FLASH2_SET_ALL_INPUTS(self,Blockname:str, Dictionary: Dict[str, Union[str,float,int]]) -> None:
        """Takes Dictionary with Values set the ones which are given in Aspen. 
        
        The Original Dictionary with its specific format can be found via "BLK_DSTWU_GET_ME_ALL_INPUTS_BACK"
        
        Args:
            Blockname: String which gives the name of Block.  
            Dictionary: Dictionary which contains all the Input variables.       
        """

        #PAGE 1 Specification
        self.BLK.Elements(Blockname).Elements("Input").Elements("SPEC_OPT").Value = Dictionary.get("FlashTypeOption")
        self.BLK.Elements(Blockname).Elements("Input").Elements("TEMP").Value = Dictionary.get("Temperature")
        self.BLK.Elements(Blockname).Elements("Input").Elements("PRES").Value = Dictionary.get("Pressure")
        self.BLK.Elements(Blockname).Elements("Input").Elements("DUTY").Value = Dictionary.get("Duty")
        self.BLK.Elements(Blockname).Elements("Input").Elements("VFRAC").Value = Dictionary.get("Vapor_fraction")
        self.BLK.Elements(Blockname).Elements("Input").Elements("Phase").Value = Dictionary.get("Phase") #This can be V L
        self.BLK.Elements(Blockname).Elements("Input").Elements("NPhase").Value = Dictionary.get("Phasenumber") #This can be 1,2,3    
        #PAGE 2 FLASH OPTION
        self.BLK.Elements(Blockname).Elements("Input").Elements("T_EST").Value = Dictionary.get("TemperatureEstimation")
        self.BLK.Elements(Blockname).Elements("Input").Elements("P_EST").Value = Dictionary.get("PressureEstimation")
        self.BLK.Elements(Blockname).Elements("Input").Elements("MAXIT").Value = Dictionary.get("MaximumIteration")
        self.BLK.Elements(Blockname).Elements("Input").Elements("TOL").Value = Dictionary.get("ErrorTolerance")
        #PAGE 3 ENTRAINMENT:
        self.BLK.Elements(Blockname).Elements("Input").Elements("ENTRN").Value = Dictionary.get("Liquid_Entrainment")
        self.BLK.Elements(Blockname).Elements("Input").Elements("VAPOR").Elements("MIXED").Value = Dictionary.get("Solid_Entrainment")
        #PAGE 4 Particle Size Determination PSD:
        self.BLK.Elements(Blockname).Elements("Input").Elements("OPT_PSD").Value = Dictionary.get("CalculationOption")
        self.BLK.Elements(Blockname).Elements("Input").Elements("CONST_METHOD").Value = Dictionary.get("ParticalGrowthModel")
    

#### FLASH2
#PAGE 1 Specification
    def BLK_FLASH2_Set_Flash_Type_Option(self, Blockname:str, FlashTypeOption: Literal["TP","TD","TV","TQ","PD","PV","PQ"]) -> None:          #This can be TP,TD,TV,TQ,PD,PV,PQ
        self.BLK.Elements(Blockname).Elements("Input").Elements("SPEC_OPT").Value = FlashTypeOption
    def BLK_FLASH2_Set_Temperature(self, Blockname,Temperature):
        self.BLK.Elements(Blockname).Elements("Input").Elements("TEMP").Value = Temperature
    def BLK_FLASH2_Set_Pressure(self, Blockname, Pressure):
        self.BLK.Elements(Blockname).Elements("Input").Elements("PRES").Value = Pressure
    def BLK_FLASH2_Set_Duty(self, Blockname, Duty):
        self.BLK.Elements(Blockname).Elements("Input").Elements("DUTY").Value = Duty
    def BLK_FLASH2_Set_Vapor_fraction(self, Blockname,Vapor_fraction):
        self.BLK.Elements(Blockname).Elements("Input").Elements("VFRAC").Value = Vapor_fraction
    def BLK_FLASH2_Set_Phases(self, Blockname, Phase: Ph, Phasenumber:Phnum):
        self.BLK.Elements(Blockname).Elements("Input").Elements("Phase").Value = Phase #This can be V L
        self.BLK.Elements(Blockname).Elements("Input").Elements("NPhase").Value = Phasenumber #This can be 1,2,3    


#PAGE 2 FLASH OPTION
    def BLK_FLASH2_Set_TemperatureEstimation(self, Blockname, TemperatureEstimation):
        self.BLK.Elements(Blockname).Elements("Input").Elements("T_EST").Value = TemperatureEstimation
    def BLK_FLASH2_Set_PressureEstimation(self, Blockname, PressureEstimation):
        self.BLK.Elements(Blockname).Elements("Input").Elements("P_EST").Value = PressureEstimation
    def BLK_FLASH2_Set_MaximumIteration(self, Blockname, MaximumIteration):       #OPTIONAL
        self.BLK.Elements(Blockname).Elements("Input").Elements("MAXIT").Value = MaximumIteration
    def BLK_FLASH2_Set_ErrorTolerance(self, Blockname, ErrorTolerance):           #OPTIONAL
        self.BLK.Elements(Blockname).Elements("Input").Elements("TOL").Value = ErrorTolerance


#PAGE 3 ENTRAINMENT:
    def BLK_FLASH2_Set_Liquid_Entrainment(self, Blockname, Liquid_Entrainment):
        self.BLK.Elements(Blockname).Elements("Input").Elements("ENTRN").Value = Liquid_Entrainment
    def BLK_FLASH2_Set_Solid_Entrainment(self, Blockname, Solid_Entrainment):
        self.BLK.Elements(Blockname).Elements("Input").Elements("VAPOR").Elements("MIXED").Value = Solid_Entrainment


#PAGE 4 Particle Size Determination PSD:
    def BLK_FLASH2_Set_Calculation_Option(self, Blockname:str, CalculationOption: Literal["COPY", "CONSTANT"]) -> None:      #This can be COPY or CONSTANT
        self.BLK.Elements(Blockname).Elements("Input").Elements("OPT_PSD").Value = CalculationOption
    def BLK_FLASH2_Set_ParticalGrowthModel(self, Blockname, ParticalGrowthModel: Literal["DELTAD-NUM", "DELTAD-MASS", "DELTAV-NUM", "EQUI-MASS", "EQUI-SURFACE", "EQUI_NUMBER"]) -> None:       #if you chose Constant you chose model: DELTAD-NUM, DELTAD-MASS, DELTAV-NUM, EQUI-MASS, EQUI-SURFACE, EQUI_NUMBER
        self.BLK.Elements(Blockname).Elements("Input").Elements("CONST_METHOD").Value = ParticalGrowthModel
            ## USER SPECIFIED PSD


    #PAGE 5 Utilities
    ##MISSING


















    def BLK_SPLITTER_GET_ME_ALL_INPUTS_BACK(self, Blockname: str) -> Dict[str, Union[str,float,int]]:
        """Retrieves all the Inputs and returns Dictionary with Values 
        
        Does not include all aspects of a Aspen Simulationsheet, for this look at Exports
        
        Args:
            Blockname: String which gives the name of Block.         
        """
        
        ProductStreamNameNode = self.BLK.Elements(Blockname).Elements("Ports").Elements("P(OUT)").Element
        ProductStreamNameList = []
        SplitFractionList = []
        FlowList = []
        ActualVolumeFlowList = []
        LimitFlowList = []
        VolumeLimitFlowList = []
        CumLimitFlowList = []
        CumVolumeLimitFlowList = []
        ResidualFractionList = []
        
        for ProductStreamName in ProductStreamNameNode:
            ProductStreamNameList.append(ProductStreamName)
            SplitFractionList.append(self.BLK.Elements(Blockname).Elements("Input").Elements("FRAC").Elements(ProductStreamName).Value)
            FlowList.append(self.BLK.Elements(Blockname).Elements("Input").Elements("BASIS_FLOW").Elements(ProductStreamName).Value)
            ActualVolumeFlowList.append(self.BLK.Elements(Blockname).Elements("Input").Elements("VOL_FLOW").Elements(ProductStreamName).Value)
            LimitFlowList.append(self.BLK.Elements(Blockname).Elements("Input").Elements("BASIS_LIMIT").Elements(ProductStreamName).Value)
            VolumeLimitFlowList.append(self.BLK.Elements(Blockname).Elements("Input").Elements("VOL_LIMIT").Elements(ProductStreamName).Value)
            CumLimitFlowList.append(self.BLK.Elements(Blockname).Elements("Input").Elements("BASIS_C_LIM").Elements(ProductStreamName).Value)
            CumVolumeLimitFlowList.append(self.BLK.Elements(Blockname).Elements("Input").Elements("VOL_C_LIM").Elements(ProductStreamName).Value)
            ResidualFractionList.append(self.BLK.Elements(Blockname).Elements("Input").Elements("R_FRAC").Elements(ProductStreamName).Value)
        Pressure = self.BLK.Elements(Blockname).Elements("Input").Elements("PRES1").Value
        Phase = self.BLK.Elements(Blockname).Elements("Input").Elements("Phase").Value #This can be V L or S
        Phasenumber = self.BLK.Elements(Blockname).Elements("Input").Elements("NPhase").Value   #This can be 1,2,3
        MaximumIteration = self.BLK.Elements(Blockname).Elements("Input").Elements("MAXIT").Value 
        ErrorTolerance = self.BLK.Elements(Blockname).Elements("Input").Elements("TOL").Value
        
        Dictionary = {
            "ProductStreamNameList":ProductStreamNameList,
            "SplitFractionList":SplitFractionList,
            "FlowList":FlowList,
            "ActualVolumeFlowList":ActualVolumeFlowList,
            "LimitFlowList":LimitFlowList,
            "VolumeLimitFlowList":VolumeLimitFlowList,
            "CumLimitFlowList":CumLimitFlowList,
            "CumVolumeLimitFlowList":CumVolumeLimitFlowList,
            "ResidualFractionList":ResidualFractionList,
            "Pressure":Pressure,
            "Phase":Phase,
            "Phasenumber":Phasenumber,
            "MaximumIteration":MaximumIteration,
            "ErrorTolerance":ErrorTolerance,
        }
        return Dictionary
    def BLK_SPLITTER_SET_ALL_INPUTS(self, Blockname:str, Dictionary: Dict[str, Union[str,float,int]]) -> None:
        """Takes Dictionary with Values set the ones which are given in Aspen. 
        
        The Original Dictionary with its specific format can be found via "BLK_DSTWU_GET_ME_ALL_INPUTS_BACK"
        
        Args:
            Blockname: String which gives the name of Block.  
            Dictionary: Dictionary which contains all the Input variables.       
        """
        
        #PAGE 1 Specification        
        ProductStreamNameList = Dictionary.get("ProductStreamNameList")
        SplitFractionList = Dictionary.get("SplitFractionList")
        FlowList = Dictionary.get("FlowList")
        ActualVolumeFlowList = Dictionary.get("ActualVolumeFlowList")
        LimitFlowList = Dictionary.get("LimitFlowList")
        VolumeLimitFlowList = Dictionary.get("VolumeLimitFlowList")
        CumLimitFlowList = Dictionary.get("CumLimitFlowList")
        CumVolumeLimitFlowList = Dictionary.get("CumVolumeLimitFlowList")
        ResidualFractionList = Dictionary.get("ResidualFractionList")
        i = 0
        for ProductStreamName in ProductStreamNameList:                 # You need to loop through all the ProductStreamNames
            self.BLK.Elements(Blockname).Elements("Input").Elements("FRAC").Elements(ProductStreamName).Value = SplitFractionList[i]
            self.BLK.Elements(Blockname).Elements("Input").Elements("BASIS_FLOW").Elements(ProductStreamName).Value =FlowList[i]
            self.BLK.Elements(Blockname).Elements("Input").Elements("VOL_FLOW").Elements(ProductStreamName).Value =ActualVolumeFlowList[i]
            self.BLK.Elements(Blockname).Elements("Input").Elements("BASIS_LIMIT").Elements(ProductStreamName).Value = LimitFlowList[i]
            self.BLK.Elements(Blockname).Elements("Input").Elements("VOL_LIMIT").Elements(ProductStreamName).Value = VolumeLimitFlowList[i]
            self.BLK.Elements(Blockname).Elements("Input").Elements("BASIS_C_LIM").Elements(ProductStreamName).Value =CumLimitFlowList[i]
            self.BLK.Elements(Blockname).Elements("Input").Elements("VOL_C_LIM").Elements(ProductStreamName).Value =CumVolumeLimitFlowList[i]
            self.BLK.Elements(Blockname).Elements("Input").Elements("R_FRAC").Elements(ProductStreamName).Value =ResidualFractionList[i]
            i = i+1
        i = 0
        
        #PAGE 2 Flash Option:
        self.BLK.Elements(Blockname).Elements("Input").Elements("PRES1").Value = Dictionary.get("Pressure")
        self.BLK.Elements(Blockname).Elements("Input").Elements("Phase").Value = Dictionary.get("Phase") #This can be V L or S
        self.BLK.Elements(Blockname).Elements("Input").Elements("NPhase").Value = Dictionary.get("Phasenumber")   #This can be 1,2,3
        self.BLK.Elements(Blockname).Elements("Input").Elements("MAXIT").Value = Dictionary.get("MaximumIteration")
        self.BLK.Elements(Blockname).Elements("Input").Elements("TOL").Value = Dictionary.get("ErrorTolerance")
      
      
      

#SPLITTER
#PAGE 1 Specification
#There are many options available for how to split the streams:
    def BLK_SPLITTER_Set_By_SplitFraction(self, Blockname, Streamname, SplitFraction):
        self.BLK.Elements(Blockname).Elements("Input").Elements("FRAC").Elements(Streamname).Value = SplitFraction
    def BLK_SPLITTER_Set_By_Flow(self, Blockname,Streamname, Flow):
        self.BLK.Elements(Blockname).Elements("Input").Elements("BASIS_FLOW").Elements(Streamname).Value = Flow
    def BLK_SPLITTER_Set_By_ActualVolumeFlow(self, Blockname,Streamname, ActualVolumeFlow):
        self.BLK.Elements(Blockname).Elements("Input").Elements("VOL_FLOW").Elements(Streamname).Value = ActualVolumeFlow
    def BLK_SPLITTER_Set_By_LimitFlow(self, Blockname,Streamname, LimitFlow):
        self.BLK.Elements(Blockname).Elements("Input").Elements("BASIS_LIMIT").Elements(Streamname).Value = LimitFlow
    def BLK_SPLITTER_Set_By_VolumeLimitFlow(self, Blockname,Streamname, VolumeLimitFlow):
        self.BLK.Elements(Blockname).Elements("Input").Elements("VOL_LIMIT").Elements(Streamname).Value = VolumeLimitFlow
    def BLK_SPLITTER_Set_By_CumLimitFlow(self, Blockname,Streamname, CumLimitFlow):
        self.BLK.Elements(Blockname).Elements("Input").Elements("BASIS_C_LIM").Elements(Streamname).Value = CumLimitFlow
    def BLK_SPLITTER_Set_By_CumVolumeLimitFlow(self, Blockname,Streamname, CumVolumeLimitFlow):
        self.BLK.Elements(Blockname).Elements("Input").Elements("VOL_C_LIM").Elements(Streamname).Value = CumVolumeLimitFlow
    def BLK_SPLITTER_Set_By_ResidualFraction(self, Blockname,Streamname, ResidualFraction):
        self.BLK.Elements(Blockname).Elements("Input").Elements("R_FRAC").Elements(Streamname).Value = ResidualFraction


#PAGE 2 Flash Option:
    def BLK_SPLITTER_Set_Pressure(self, Blockname, Pressure):
        self.BLK.Elements(Blockname).Elements("Input").Elements("PRES1").Value = Pressure
    def BLK_SPLITTER_Set_Phases(self, Blockname:str, Phase:Ph, Phasenumber:Phnum) -> None:
        self.BLK.Elements(Blockname).Elements("Input").Elements("Phase").Value = Phase #This can be V L or S
        self.BLK.Elements(Blockname).Elements("Input").Elements("NPhase").Value = Phasenumber   #This can be 1,2,3
    def BLK_SPLITTER_Set_MaximumIteration(self, Blockname, MaximumIteration):       #OPTIONAL
        self.BLK.Elements(Blockname).Elements("Input").Elements("MAXIT").Value = MaximumIteration
    def BLK_SPLITTER_Set_ErrorTolerance(self, Blockname, ErrorTolerance):           #OPTIONAL
        self.BLK.Elements(Blockname).Elements("Input").Elements("TOL").Value = ErrorTolerance

#PAGE 3 Key Component
        ###MISSIGN



















    def BLK_RYIELD_GET_ME_ALL_INPUTS_BACK(self, Blockname) -> Dict[str, Union[str,float,int]]:
        """Retrieves all the Inputs and returns Dictionary with Values 
        
        Does not include all aspects of a Aspen Simulationsheet, for this look at Exports
        
        Args:
            Blockname: String which gives the name of Block.         
        """
        
        FlashTypeOption = self.BLK.Elements(Blockname).Elements("Input").Elements("SPEC_OPT").Value
        Temperature = self.BLK.Elements(Blockname).Elements("Input").Elements("TEMP").Value 
        TemperatureChange = self.BLK.Elements(Blockname).Elements("Input").Elements("DELT").Value
        Pressure = self.BLK.Elements(Blockname).Elements("Input").Elements("PRES").Value
        Duty= self.BLK.Elements(Blockname).Elements("Input").Elements("DUTY").Value 
        Vaporfraction = self.BLK.Elements(Blockname).Elements("Input").Elements("VFRAC").Value 
        Phase = self.BLK.Elements(Blockname).Elements("Input").Elements("Phase").Value #This can be V L or S
        Phasenumber = self.BLK.Elements(Blockname).Elements("Input").Elements("NPhase").Value     #This can be 1,2,3
        
        PhaseOfProductStreamNode = self.BLK.Elements(Blockname).Elements("Input").Elements("PROD_PHASE").Elements
        PhaseOfProductStreamList = []
        PhaseOfProductStreamnameList = []
        for ProductStreamname in PhaseOfProductStreamNode:
            PhaseOfProductStream = self.BLK.Elements(Blockname).Elements("Input").Elements("PROD_PHASE").Elements(ProductStreamname).Value 
            PhaseOfProductStreamList.append(PhaseOfProductStream)
            PhaseOfProductStreamnameList.append(ProductStreamname)
        
        YieldCalcOption = self.BLK.Elements(Blockname).Elements("Input").Elements("USER_YIELD").Value

        NewBasisList = []        
        YieldPerFlowList = []
        YieldPerFlowCompoundList = []
        YieldPerFlowNode = self.BLK.Elements(Blockname).Elements("Input").Elements("MOLE_YIELD").Elements
        for YieldPerFlowCompound in YieldPerFlowNode:
            YieldPerFlow = self.BLK.Elements(Blockname).Elements("Input").Elements("MOLE_YIELD").Elements(YieldPerFlowCompound).Value 
            YieldPerFlowList.append(YieldPerFlow)
            YieldPerFlowCompoundList.append(YieldPerFlowCompound)
            Basis = self.BLK.Elements(Blockname).Elements("Input").Elements("BASIS").Elements(YieldPerFlowCompound).Value
            NewBasisList.append(Basis)

        InertNumberList = []
        InertComponentList = []
        InertNumberNode = self.BLK.Elements(Blockname).Elements("Input").Elements("COMP_LIST").Elements
        for InertNumber in InertNumberNode:
            InertNumberList.append(InertNumber)
            InertComponent = self.BLK.Elements(Blockname).Elements("Input").Elements("COMP_LIST").Elements(InertNumber).Value
            InertComponentList.append(InertComponent)
        
        TemperatureEstimation = self.BLK.Elements(Blockname).Elements("Input").Elements("T_EST").Value
        PressureEstimation = self.BLK.Elements(Blockname).Elements("Input").Elements("P_EST").Value
        MaximumIteration = self.BLK.Elements(Blockname).Elements("Input").Elements("MAXIT").Value
        ErrorTolerance = self.BLK.Elements(Blockname).Elements("Input").Elements("TOL").Value
        CalculationOption = self.BLK.Elements(Blockname).Elements("Input").Elements("OPT_PSD").Value
        ParticalGrowthModel = self.BLK.Elements(Blockname).Elements("Input").Elements("CONST_METHOD").Value
        Dictionary = {
            "FlashTypeOption":FlashTypeOption,
            "Temperature":Temperature,
            "TemperatureChange":TemperatureChange,
            "Pressure":Pressure,
            "Duty":Duty,
            "Vaporfraction":Vaporfraction,
            "Phase":Phase,
            "Phasenumber":Phasenumber,
            "PhaseOfProductStreamList":PhaseOfProductStreamList,
            "PhaseOfProductStreamnameList":PhaseOfProductStreamnameList,
            "YieldCalcOption":YieldCalcOption,
            "YieldPerFlowList":YieldPerFlowList,
            "YieldPerFlowCompoundList":YieldPerFlowCompoundList,
            "NewBasisList":NewBasisList,
            "InertNumberList":InertNumberList,
            "InertComponentList":InertComponentList,
            "TemperatureEstimation":TemperatureEstimation,
            "PressureEstimation":PressureEstimation,
            "MaximumIteration":MaximumIteration,
            "ErrorTolerance":ErrorTolerance,
            "CalculationOption":CalculationOption,
            "ParticalGrowthModel":ParticalGrowthModel,

        }
        return Dictionary
    def BLK_RYIELD_SET_ALL_INPUTS(self, Blockname:str, Dictionary: Dict[str, Union[str,float,int]]) -> None:
        """Takes Dictionary with Values set the ones which are given in Aspen. 
        
        The Original Dictionary with its specific format can be found via "BLK_DSTWU_GET_ME_ALL_INPUTS_BACK"
        
        Args:
            Blockname: String which gives the name of Block.  
            Dictionary: Dictionary which contains all the Input variables.       
        """

        #PAGE 1 Specification:
        self.BLK.Elements(Blockname).Elements("Input").Elements("SPEC_OPT").Value = Dictionary.get("FlashTypeOption")
        self.BLK.Elements(Blockname).Elements("Input").Elements("TEMP").Value = Dictionary.get("Temperature")
        self.BLK.Elements(Blockname).Elements("Input").Elements("DELT").Value = Dictionary.get("TemperatureChange")
        self.BLK.Elements(Blockname).Elements("Input").Elements("PRES").Value = Dictionary.get("Pressure")
        self.BLK.Elements(Blockname).Elements("Input").Elements("DUTY").Value = Dictionary.get("Duty")
        self.BLK.Elements(Blockname).Elements("Input").Elements("VFRAC").Value = Dictionary.get("Vaporfraction")
        self.BLK.Elements(Blockname).Elements("Input").Elements("Phase").Value = Dictionary.get("Phase") #This can be V L or S
        self.BLK.Elements(Blockname).Elements("Input").Elements("NPhase").Value = Dictionary.get("Phasenumber")   #This can be 1,2,3
        #PAGE 2 Streams:
        PhaseOfProductStreamnameList = Dictionary.get("PhaseOfProductStreamnameList")
        PhaseOfProductStreamList = Dictionary.get("PhaseOfProductStreamList")
        i = 0
        for PhaseOfProductStreamname in PhaseOfProductStreamnameList:
            self.BLK.Elements(Blockname).Elements("Input").Elements("PROD_PHASE").Elements(PhaseOfProductStreamname).Value = PhaseOfProductStreamList[i]
            i = i + 1
        i = 0    
        #PAGE 3 Yields:
        self.BLK.Elements(Blockname).Elements("Input").Elements("USER_YIELD").Value = Dictionary.get("YieldCalcOption")

        YieldPerFlowList = Dictionary.get("YieldPerFlowList")
        YieldPerFlowCompoundList = Dictionary.get("YieldPerFlowCompoundList")
        NewBasisList = Dictionary.get("NewBasisList")
        i = 0
        for YieldPerFlowCompound in YieldPerFlowCompoundList:
            self.BLK.Elements(Blockname).Elements("Input").Elements("MOLE_YIELD").Elements(YieldPerFlowCompound).Value = YieldPerFlowList[i]
            self.BLK.Elements(Blockname).Elements("Input").Elements("BASIS").Elements(YieldPerFlowCompound).Value = NewBasisList[i]
            i = i + 1
        i = 0
        
        InertNumberList = Dictionary.get("InertNumberList")
        InertComponentList = Dictionary.get("InertComponentList")
        i = 0
        for InertNumber in InertNumberList:
            self.BLK.Elements(Blockname).Elements("Input").Elements("COMP_LIST").Elements(InertNumber).Value = InertComponentList[i]
            i = i + 1
        i = 0           
        #PAGE 4 FLASH OPTION:
        self.BLK.Elements(Blockname).Elements("Input").Elements("T_EST").Value = Dictionary.get("TemperatureEstimation")
        self.BLK.Elements(Blockname).Elements("Input").Elements("P_EST").Value = Dictionary.get("PressureEstimation")
        self.BLK.Elements(Blockname).Elements("Input").Elements("MAXIT").Value = Dictionary.get("MaximumIteration")
        self.BLK.Elements(Blockname).Elements("Input").Elements("TOL").Value = Dictionary.get("ErrorTolerance")
        #PAGE 5 Particle Size Determination, PSD
        self.BLK.Elements(Blockname).Elements("Input").Elements("OPT_PSD").Value = Dictionary.get("CalculationOption")
        self.BLK.Elements(Blockname).Elements("Input").Elements("CONST_METHOD").Value = Dictionary.get("ParticalGrowthModel")



#RYIELD

#PAGE 1 Specification:
    def BLK_RYIELD_Set_FlashTypeOption(self, Blockname:str, FlashTypeOption: Literal["TP", "TD", "TV", "PD", "PV", "DTV", "DTD", "DTP", "DTQ"]) -> None:           #You can chose between: TP, TD, TV, PD, PV, DTV, DTD, DTP, DTQ
        self.BLK.Elements(Blockname).Elements("Input").Elements("SPEC_OPT").Value = FlashTypeOption
    def BLK_RYIELD_Set_Temperature(self, Blockname, Temperature):
        self.BLK.Elements(Blockname).Elements("Input").Elements("TEMP").Value = Temperature
    def BLK_RYIELD_Set_TemperatureChange(self, Blockname, TemperatureChange):
        self.BLK.Elements(Blockname).Elements("Input").Elements("DELT").Value =TemperatureChange
    def BLK_RYIELD_Set_Pressure(self, Blockname, Pressure):
        self.BLK.Elements(Blockname).Elements("Input").Elements("PRES").Value = Pressure
    def BLK_RYIELD_Set_Duty(self, Blockname, Duty):
        self.BLK.Elements(Blockname).Elements("Input").Elements("DUTY").Value = Duty
    def BLK_RYIELD_Set_Vaporfraction(self, Blockname, Vaporfraction):
        self.BLK.Elements(Blockname).Elements("Input").Elements("VFRAC").Value = Vaporfraction
    def BLK_RYIELD_Set_Phases(self, Blockname, Phase:Ph, Phasenumber:Phnum):
        self.BLK.Elements(Blockname).Elements("Input").Elements("Phase").Value = Phase #This can be V L or S
        self.BLK.Elements(Blockname).Elements("Input").Elements("NPhase").Value = Phasenumber   #This can be 1,2,3


#PAGE 2 Streams:
    def BLK_RYIELD_Set_PhaseOfProductStream(self, Blockname:str, PhaseOfProductStream: Literal["V", "L", "L1","L2", "W", "VL", "VL1", "LW", "L1L2"], Streamname:str):      #This can be V, L, L1,L2,W,VL,VL1,LW,L1L2
        self.BLK.Elements(Blockname).Elements("Input").Elements("PROD_PHASE").Elements(Streamname).Value = PhaseOfProductStream


#PAGE 3 Yields:

    def BLK_RYIELD_Set_YieldCalcOption(self, Blockname:str, YieldCalcOption: Literal["NO", "YES", "NO2", "NO3"]):    #This can be NO, YES, NO2, NO3
        self.BLK.Elements(Blockname).Elements("Input").Elements("USER_YIELD").Value = YieldCalcOption
        #if you chose: NO (Component yields)
    def BLK_RYIELD_Set_ComponentYield_YieldPerFlow(self, Blockname,YieldPerFlow, CompoundName):     #Compoundname should be "ETHAN-01 MIXED"
        self.BLK.Elements(Blockname).Elements("Input").Elements("MOLE_YIELD").Elements(CompoundName).Value = YieldPerFlow
    def BLK_RYIELD_Set_ComponentYield_ChangeBasis(self, Blockname,CompoundName, NewBasis: Literal["MASS" , "MOLE"]) -> None:             #Compoundname should be like: "ETHAN-01 MIXED", BaseOptions are "MASS" , "MOLE"
        self.BLK.Elements(Blockname).Elements("Input").Elements("BASIS").Elements(CompoundName).Value = NewBasis
    def BLK_RYIELD_Set_ComponentYield_InertComponent(self, Blockname, InertComponent, InertNumber):     #InertNumber should be either #0 or 0 ??? not sure..        InertComponent could be WATER
        self.BLK.Elements(Blockname).Elements("Input").Elements("COMP_LIST").Elements(InertNumber).Value = InertComponent
        #if you chose: YES (User Subroutine)
                ##MISSING
        #if you chose: NO2 (Component mapping)
                ##MISSING
        #if you chose: NO3 (Petro characterization)
            #No data needed

#PAGE 4 FLASH OPTION:
    def BLK_RYIELD_Set_TemperatureEstimation(self, Blockname, TemperatureEstimation):
        self.BLK.Elements(Blockname).Elements("Input").Elements("T_EST").Value = TemperatureEstimation
    def BLK_RYIELD_Set_PressureEstimation(self, Blockname, PressureEstimation):
        self.BLK.Elements(Blockname).Elements("Input").Elements("P_EST").Value = PressureEstimation
    def BLK_RYIELD_Set_MaximumIteration(self, Blockname, MaximumIteration):       #OPTIONAL
        self.BLK.Elements(Blockname).Elements("Input").Elements("MAXIT").Value = MaximumIteration
    def BLK_RYIELD_Set_ErrorTolerance(self, Blockname, ErrorTolerance):           #OPTIONAL
        self.BLK.Elements(Blockname).Elements("Input").Elements("TOL").Value = ErrorTolerance


#PAGE 5 Particle Size Determination, PSD
    def BLK_RYIELD_Set_Calculation_Option(self, Blockname:str, CalculationOption: Literal["COPY", "CONSTANT" ,"SPEC"]) -> None:      #This can be COPY or CONSTANT or SPEC
        self.BLK.Elements(Blockname).Elements("Input").Elements("OPT_PSD").Value = CalculationOption
            #if you chose Keep PSD,    COPY
                    #nothing needed
            #if you chose Particle growth model,  CONSTANT
    def BLK_RYIELD_Set_ParticalGrowthModel(self, Blockname, ParticalGrowthModel: Literal["DELTAD-NUM", "DELTAD-MASS", "DELTAV-NUM", "EQUI-MASS", "EQUI-SURFACE", "EQUI_NUMBER"]):       #if you chose Constant you chose model: DELTAD-NUM, DELTAD-MASS, DELTAV-NUM, EQUI-MASS, EQUI-SURFACE, EQUI_NUMBER
        self.BLK.Elements(Blockname).Elements("Input").Elements("CONST_METHOD").Value = ParticalGrowthModel
            #if you chose User specified PSD 
                   #MISSING
#PAGE 6 Component Attribute
        #MISSING
#PAGE 7 Component mapping
        #MISSING






 















    def STRM_GET_ME_ALL_INPUTS_BACK(self, Streamname:str) -> Dict[str, Union[str,float,int]]:
        """Retrieves all the Inputs and returns Dictionary with Values 
        
        Does not include all aspects of a Aspen Simulationsheet, for this look at Exports
        
        Args:
            Blockname: String which gives the name of Block.         
        """
        FlashtypeChoice = self.STRM.Elements(Streamname).Elements("Input").Elements("MIXED_SPEC").Elements("MIXED").Value        
        Temp = self.STRM.Elements(Streamname).Elements("Input").Elements("TEMP").Elements("MIXED").Value
        Pressure = self.STRM.Elements(Streamname).Elements("Input").Elements("PRES").Elements("MIXED").Value
        VaporFraction = self.STRM.Elements(Streamname).Elements("Input").Elements("VFRAC").Elements("MIXED").Value 
        TotalFlowRate = self.STRM.Elements(Streamname).Elements("Input").Elements("TOTFLOW").Value
        
        CompoundNameList = []
        TotalFlowBasisList = []
        ComponentFlowRateList = []
        CompoundNameNode = self.STRM.Elements(Streamname).Elements("Input").Elements("FLOW").Elements("MIXED").Elements
        for CompoundName in CompoundNameNode:
            CompoundNameList.append(CompoundName)
            TotalFlowBasisList.append(self.STRM.Elements(Streamname).Elements("Input").Elements("FLOW").Elements("MIXED").Elements(CompoundName).Value)
            ComponentFlowRateList.append(self.STRM.Elements(Streamname).Elements("Input").Elements("FLOW").Elements("MIXED").Elements(CompoundName).Value)
        
        CalculateStreamPropertiesOption = self.STRM.Elements(Streamname).Elements("Input").Elements("FL_OPTION").Elements("MIXED").Value 
        RemoveComponentOption = self.STRM.Elements(Streamname).Elements("Input").Elements("AUTO_COMPS").Value
        ComponentTolerance = self.STRM.Elements(Streamname).Elements("Input").Elements("AUTO_COMPS_T").Value 
        ChooseAdditionalOptions = self.STRM.Elements(Streamname).Elements("Input").Elements("EO_COMPS").Value 
        SolutionMethod = self.STRM.Elements(Streamname).Elements("Input").Elements("SOL_METHOD").Value
        OpenDerivationMethod = self.STRM.Elements(Streamname).Elements("Input").Elements("DERIV_METHOD").Value 
        PassthroughOption = self.STRM.Elements(Streamname).Elements("Input").Elements("PASS_THROUGH").Value 
        NegativeComponentCheckTol = self.STRM.Elements(Streamname).Elements("Input").Elements("NEG_COMP_CHK").Value
        NegativeFlowCheckTol  = self.STRM.Elements(Streamname).Elements("Input").Elements("NEG_FLOW_CHK").Value
        AlwaysInstantiate = self.STRM.Elements(Streamname).Elements("Input").Elements("").Value
        Sparcity = self.STRM.Elements(Streamname).Elements("Input").Elements("SPARCITY").Value
        Lightkey = self.STRM.Elements(Streamname).Elements("Input").Elements("EO_LIGHT_KEY").Value 
        Heavykey = self.STRM.Elements(Streamname).Elements("Input").Elements("EO_HEAVY_KEY").Value
        WaterOnlyCheck= self.STRM.Elements(Streamname).Elements("Input").Elements("CHECK_FREE_W").Value
        AutoPhaseOption = self.STRM.Elements(Streamname).Elements("Input").Elements("AUTO_PHASE").Value
        PhaseTolerance = self.STRM.Elements(Streamname).Elements("Input").Elements("AUTO_PHASE_T").Value
        FlashFormulation = self.STRM.Elements(Streamname).Elements("Input").Elements("FLASH_FORM").Value
        VfracXTol = self.STRM.Elements(Streamname).Elements("Input").Elements("VFRACX_TOL").Value
        VfracTol = self.STRM.Elements(Streamname).Elements("Input").Elements("VFRAC_TOL").Value
        SfracTol = self.STRM.Elements(Streamname).Elements("Input").Elements("SFRAC_TOL").Value
        CompositionTol = self.STRM.Elements(Streamname).Elements("Input").Elements("COMP_TOL").Value
        TemperatureTol = self.STRM.Elements(Streamname).Elements("Input").Elements("EO_TEMP_TOL").Value
        PricePerUnit = self.STRM.Elements(Streamname).Elements("Input").Elements("PRICE").Value
        PriceUnit = self.STRM.Elements(Streamname).Elements("Input").Elements("PRICE").Basis
        
        Dictionary = {
            "FlashtypeChoice":FlashtypeChoice,
            "Temp":Temp,
            "Pressure":Pressure,
            "VaporFraction":VaporFraction,
            "TotalFlowRate":TotalFlowRate,
            "CompoundNameList":CompoundNameList,
            "TotalFlowBasisList":TotalFlowBasisList,
            "ComponentFlowRateList":ComponentFlowRateList,
            "CalculateStreamPropertiesOption":CalculateStreamPropertiesOption,
            "RemoveComponentOption":RemoveComponentOption,
            "ComponentTolerance":ComponentTolerance,
            "ChooseAdditionalOptions":ChooseAdditionalOptions,
            "SolutionMethod":SolutionMethod,
            "OpenDerivationMethod":OpenDerivationMethod,
            "PassthroughOption":PassthroughOption,
            "NegativeComponentCheckTol":NegativeComponentCheckTol,
            "NegativeFlowCheckTol":NegativeFlowCheckTol,
            "AlwaysInstantiate":AlwaysInstantiate,
            "Sparcity":Sparcity,
            "Lightkey":Lightkey,
            "Heavykey":Heavykey,
            "WaterOnlyCheck":WaterOnlyCheck,
            "AutoPhaseOption":AutoPhaseOption,
            "PhaseTolerance":PhaseTolerance,
            "FlashFormulation":FlashFormulation,
            "VfracXTol":VfracXTol,
            "VfracTol":VfracTol,
            "SfracTol":SfracTol,
            "CompositionTol":CompositionTol,
            "TemperatureTol":TemperatureTol,
            "PricePerUnit":PricePerUnit,
            "PriceUnit":PriceUnit,
        }
        return Dictionary
    def STRM_SET_ALL_INPUTS(self, Streamname:str, Dictionary: Dict[str, Union[str,float,int]]) -> None:
        """Takes Dictionary with Values set the ones which are given in Aspen. 
        
        The Original Dictionary with its specific format can be found via "BLK_DSTWU_GET_ME_ALL_INPUTS_BACK"
        
        Args:
            Blockname: String which gives the name of Block.  
            Dictionary: Dictionary which contains all the Input variables.       
        """

        #Specifications: PAGE 1
        self.STRM.Elements(Streamname).Elements("Input").Elements("MIXED_SPEC").Elements("MIXED").Value = Dictionary.get("FlashtypeChoice")    
        self.STRM.Elements(Streamname).Elements("Input").Elements("TEMP").Elements("MIXED").Value = Dictionary.get("Temp")
        self.STRM.Elements(Streamname).Elements("Input").Elements("PRES").Elements("MIXED").Value = Dictionary.get("Pressure")
        self.STRM.Elements(Streamname).Elements("Input").Elements("VFRAC").Elements("MIXED").Value = Dictionary.get("VaporFraction")
        self.STRM.Elements(Streamname).Elements("Input").Elements("TOTFLOW").Value = Dictionary.get("TotalFlowRate")
        
        CompoundNameList = Dictionary.get("CompoundNameList")
        TotalFlowBasisList = Dictionary.get("TotalFlowBasisList")
        ComponentFlowRateList = Dictionary.get("ComponentFlowRateList")
        i = 0
        for Compoundname in CompoundNameList:
            self.STRM.Elements(Streamname).Elements("Input").Elements("FLOW").Elements("MIXED").Elements(Compoundname).Value = TotalFlowBasisList[i]
            self.STRM.Elements(Streamname).Elements("Input").Elements("FLOW").Elements("MIXED").Elements(Compoundname).Value = ComponentFlowRateList[i]
            i = i + 1
        i = 0
        #Page 2    CI Solid
        #PAGE 3     NC Solid
        #PAGE 4     Flash Option
        self.STRM.Elements(Streamname).Elements("Input").Elements("FL_OPTION").Elements("MIXED").Value = Dictionary.get("CalculateStreamPropertiesOption")
        #PAGE 5 EO OPTIONS
        self.STRM.Elements(Streamname).Elements("Input").Elements("AUTO_COMPS").Value = Dictionary.get("RemoveComponentOption")
        self.STRM.Elements(Streamname).Elements("Input").Elements("AUTO_COMPS_T").Value = Dictionary.get("ComponentTolerance")
        self.STRM.Elements(Streamname).Elements("Input").Elements("EO_COMPS").Value = Dictionary.get("ChooseAdditionalOptions")
        self.STRM.Elements(Streamname).Elements("Input").Elements("SOL_METHOD").Value = Dictionary.get("SolutionMethod")
        self.STRM.Elements(Streamname).Elements("Input").Elements("DERIV_METHOD").Value = Dictionary.get("OpenDerivationMethod")
        self.STRM.Elements(Streamname).Elements("Input").Elements("PASS_THROUGH").Value = Dictionary.get("YesOrNO")
        self.STRM.Elements(Streamname).Elements("Input").Elements("NEG_COMP_CHK").Value = Dictionary.get("NegativeComponentCheckTol")
        self.STRM.Elements(Streamname).Elements("Input").Elements("NEG_FLOW_CHK").Value = Dictionary.get("NegativeFlowCheckTol")
        self.STRM.Elements(Streamname).Elements("Input").Elements("").Value = Dictionary.get("AlwaysInstantiate")
        self.STRM.Elements(Streamname).Elements("Input").Elements("SPARCITY").Value = Dictionary.get("Sparcity")
        self.STRM.Elements(Streamname).Elements("Input").Elements("EO_LIGHT_KEY").Value = Dictionary.get("Lightkey")
        self.STRM.Elements(Streamname).Elements("Input").Elements("EO_HEAVY_KEY").Value = Dictionary.get("Heavykey")
        self.STRM.Elements(Streamname).Elements("Input").Elements("CHECK_FREE_W").Value = Dictionary.get("WaterOnlyCheck")
        self.STRM.Elements(Streamname).Elements("Input").Elements("AUTO_PHASE").Value = Dictionary.get("YesOrNo")
        self.STRM.Elements(Streamname).Elements("Input").Elements("AUTO_PHASE_T").Value = Dictionary.get("PhaseTolerance")
        self.STRM.Elements(Streamname).Elements("Input").Elements("FLASH_FORM").Value = Dictionary.get("FlashFormulation")
        self.STRM.Elements(Streamname).Elements("Input").Elements("VFRACX_TOL").Value = Dictionary.get("VfracXTol")
        self.STRM.Elements(Streamname).Elements("Input").Elements("VFRAC_TOL").Value = Dictionary.get("VfracTol")
        self.STRM.Elements(Streamname).Elements("Input").Elements("SFRAC_TOL").Value = Dictionary.get("SfracTol")
        self.STRM.Elements(Streamname).Elements("Input").Elements("COMP_TOL").Value = Dictionary.get("CompositionTol")
        self.STRM.Elements(Streamname).Elements("Input").Elements("EO_TEMP_TOL").Value = Dictionary.get("TemperatureTol")
        #PAGE 6   Costing
        self.STRM.Elements(Streamname).Elements("Input").Elements("PRICE").Value = Dictionary.get("PricePerUnit")
        self.STRM.Elements(Streamname).Elements("Input").Elements("PRICE").Basis = Dictionary.get("PriceUnit")






#### INPUT FOR STREAMS

#Specifications: PAGE 1
    def STRM_Set_FlashTypeOption(self, Streamname:str, FlashtypeChoice: Literal["TP", "TV", "PV"]) -> None:        #   This choses the Inputs: can take TP, TV, PV
        self.STRM.Elements(Streamname).Elements("Input").Elements("MIXED_SPEC").Elements("MIXED").Value = FlashtypeChoice        
    def STRM_Set_Temperature(self, Streamname, Temp):
        self.STRM.Elements(Streamname).Elements("Input").Elements("TEMP").Elements("MIXED").Value = Temp
    def STRM_Set_Pressure(self, Streamname, Pressure):
        self.STRM.Elements(Streamname).Elements("Input").Elements("PRES").Elements("MIXED").Value = Pressure
    def STRM_Set_VaporFraction(self, Streamname, VaporFraction):
        self.STRM.Elements(Streamname).Elements("Input").Elements("VFRAC").Elements("MIXED").Value = VaporFraction
    def STRM_Set_TotalFlowRate(self, Streamname, TotalFlowRate):
        self.STRM.Elements(Streamname).Elements("Input").Elements("TOTFLOW").Value = TotalFlowRate
    def STRM_Set_TotalFlowBasis(self, Streamname, TotalFlowBasis, Compoundname):
        self.STRM.Elements(Streamname).Elements("Input").Elements("FLOW").Elements("MIXED").Elements(Compoundname).Value = TotalFlowBasis
    def STRM_Set_ComponentFlowRate(self, Streamname, ComponentFlowRate, Compoundname):
        self.STRM.Elements(Streamname).Elements("Input").Elements("FLOW").Elements("MIXED").Elements(Compoundname).Value = ComponentFlowRate
#Page 2    CI Solid
    ###MISSING
#PAGE 3     NC Solid
    ##MISSING

#PAGE 4     Flash Option
    def STRM_Set_CalculateStreamPropertiesOption(self, Streamname:str, CalculateStreamPropertiesOption: Literal["NOFLASH", "" ]):        #This can be either "NOFLASH" or "" (nothing)
        self.STRM.Elements(Streamname).Elements("Input").Elements("FL_OPTION").Elements("MIXED").Value = CalculateStreamPropertiesOption 

#PAGE 5 EO OPTIONS
 #   def STRM_ModelComponent(self, Streamname, ):
  #      self.STRM.Elements(Streamname).Elements("Input").Elements("").Elements("MIXED").Value = 
#                   I DONT KNOW HOW TO DO THIS
    def STRM_Set_RemoveComponentOption(self, Streamname:str, RemoveComponentOption: Literal["ALWAYS", "IF-NO-COMPS", "NEVER"]) -> None:        #THIS can be ALWAYS, IF-NO-COMPS, NEVER
        self.STRM.Elements(Streamname).Elements("Input").Elements("AUTO_COMPS").Value = RemoveComponentOption
    def STRM_Set_ComponentTolerance(self, Streamname, ComponentTolerance):
        self.STRM.Elements(Streamname).Elements("Input").Elements("AUTO_COMPS_T").Value = ComponentTolerance
    def STRM_Set_ChooseAdditionalOptions(self, Streamname, ChooseAdditionalOptions):
        self.STRM.Elements(Streamname).Elements("Input").Elements("EO_COMPS").Value = ChooseAdditionalOptions

        #ADDITIONAL OPTIONS:
    def STRM_Set_AddOptSolutionMethod(self, Streamname: str, SolutionMethod: Literal["OPEN-PERT-IN","OPEN-PERT-WA", "OPEN-NOPERT","PERTUBATION", "DO-NOT-CREAT"]) -> None:        #Choices are:	OPEN-PERT-IN   OPEN-PERT-WA    OPEN-NOPERT    PERTUBATION   DO-NOT-CREAT
        self.STRM.Elements(Streamname).Elements("Input").Elements("SOL_METHOD").Value = SolutionMethod
    def STRM_Set_AddOptOpenDerivationMethod(self, Streamname:str, OpenDerivationMethod: Literal["ANALYTICAL", "NUMERICAL", "UPDATE-ANALY", "UPDATE-NUMER"]):        #ANALYTICAL, NUMERICAL, UPDATE-ANALY, UPDATE-NUMER
        self.STRM.Elements(Streamname).Elements("Input").Elements("DERIV_METHOD").Value = OpenDerivationMethod
    def STRM_Set_AddOptPassThrough(self, Streamname:str, YesOrNO: Literal["YES", "NO"]) -> None:
        self.STRM.Elements(Streamname).Elements("Input").Elements("PASS_THROUGH").Value = YesOrNO
    def STRM_Set_AddOptNegativeComponentCheckTol(self, Streamname, NegativeComponentCheckTol):
        self.STRM.Elements(Streamname).Elements("Input").Elements("NEG_COMP_CHK").Value = NegativeComponentCheckTol
    def STRM_Set_AddOptNegativeFlowCheckTol(self, Streamname,NegativeFlowCheckTol):
        self.STRM.Elements(Streamname).Elements("Input").Elements("NEG_FLOW_CHK").Value = NegativeFlowCheckTol
    def STRM_Set_AddOptAlwaysInstantiate(self, Streamname, AlwaysInstantiate):
        self.STRM.Elements(Streamname).Elements("Input").Elements("").Value = AlwaysInstantiate
    def STRM_Set_AddOptSparcity(self, Streamname, Sparcity):
        self.STRM.Elements(Streamname).Elements("Input").Elements("SPARCITY").Value =Sparcity
#    def STRM_AddOptSparcityComponents(self, Streamname, SparcityComponents):
#        self.STRM.Elements(Streamname).Elements("Input").Elements("????").Value = SparcityComponents
                #cant do this yet....
    def STRM_Set_AddOptLightkey(self, Streamname, Lightkey):
        self.STRM.Elements(Streamname).Elements("Input").Elements("EO_LIGHT_KEY").Value = Lightkey
    def STRM_Set_AddOptHeavykey(self, Streamname,Heavykey):
        self.STRM.Elements(Streamname).Elements("Input").Elements("EO_HEAVY_KEY").Value = Heavykey
    def STRM_Set_AddOptWaterOnlyCheck(self, Streamname, WaterOnlyCheck):
        self.STRM.Elements(Streamname).Elements("Input").Elements("CHECK_FREE_W").Value = WaterOnlyCheck
    def STRM_Set_AddOptRemoveMissingPhase(self, Streamname:str, YesOrNo: Literal["YES", "NO"]) -> None:
        self.STRM.Elements(Streamname).Elements("Input").Elements("AUTO_PHASE").Value = YesOrNo
    def STRM_Set_AddOptPhaseTolerance(self, Streamname, PhaseTolerance):
        self.STRM.Elements(Streamname).Elements("Input").Elements("AUTO_PHASE_T").Value = PhaseTolerance
    def STRM_Set_AddOptFlashFormulation(self, Streamname:str ,FlashFormulation: Literal["PML", "SMOOTHING"]) -> None:     #Option is "PML", "SMOOTHING"
        self.STRM.Elements(Streamname).Elements("Input").Elements("FLASH_FORM").Value = FlashFormulation
    def STRM_Set_AddOptSmoothingVfracXTol(self, Streamname,VfracXTol):
        self.STRM.Elements(Streamname).Elements("Input").Elements("VFRACX_TOL").Value = VfracXTol
    def STRM_Set_AddOptSmoothingVfracTol(self, Streamname, VfracTol):
        self.STRM.Elements(Streamname).Elements("Input").Elements("VFRAC_TOL").Value = VfracTol
    def STRM_Set_AddOptSmoothingSfracTol(self, Streamname,SfracTol):
        self.STRM.Elements(Streamname).Elements("Input").Elements("SFRAC_TOL").Value = SfracTol
    def STRM_Set_AddOptSmoothingCompositionTol(self, Streamname, CompositionTol):
        self.STRM.Elements(Streamname).Elements("Input").Elements("COMP_TOL").Value = CompositionTol
    def STRM_Set_AddOptSmoothingTemperatureTol(self, Streamname, TemperatureTol):
        self.STRM.Elements(Streamname).Elements("Input").Elements("EO_TEMP_TOL").Value =TemperatureTol


#PAGE 6   Costing
    def STRM_Set_PricePerUnit(self, Streamname, PricePerUnit):
        self.STRM.Elements(Streamname).Elements("Input").Elements("PRICE").Value = PricePerUnit
    def STRM_Set_ChangePriceUnit(self, Streamname, PriceUnit):
        self.STRM.Elements(Streamname).Elements("Input").Elements("PRICE").Basis = PriceUnit

























###########################################################################################################################################



#ooooooooooooo   UU           U      tttttttttttttttttt         PPPPPPPPPPP         U               U       TTTTTTTTTTTTTTTTTTTTTTTT
#o           o   UU           U              TT                 P           P       U               U                   T
#o           o   UU           U              TT                 P           P       U               U                   T
#o           o   UU           U              TT                 P           P       U               U                   T
#o           o   UU           U              TT                 PPPPPPPPPPP         U               U                   T
#o           o   UU           U              TT                 P                   U               U                   T
#ooooooooooooo   UUUUUUUUUUUUUU              TT                 P                   U               U                   T
                                                               #P                   UUUUUUUUUUUUUUUUU                   T


############################################################################################################################################


#############   OUTPUTS

    def BLK_DSTWU_GET_OUTPUTS(self, Blockname:str) -> Dict[str, Union[str,float,int]]:
        """Retrieves all Output variables for given Block and returns Dictionary of Values
            
            Args:
                Blockname: String which gives the name of Block.         
        """
        #Page 1
        MinimumRefluxRatio = self.BLK.Elements(Blockname).Elements("Output").Elements("MIN_REFLUX").Value        
        ActualRefluxRatio = self.BLK.Elements(Blockname).Elements("Output").Elements("ACT_REFLUX").Value        
        MinimumNStage = self.BLK.Elements(Blockname).Elements("Output").Elements("MIN_STAGES").Value        
        ActualNStage = self.BLK.Elements(Blockname).Elements("Output").Elements("ACT_STAGES").Value        
        FeedStage = self.BLK.Elements(Blockname).Elements("Output").Elements("FEED_LOCATN").Value 
        ActualNumberOfStagesAboveFeed = self.BLK.Elements(Blockname).Elements("Output").Elements("RECT_STAGE").Value        
        ReboilerHeatingRequired = self.BLK.Elements(Blockname).Elements("Output").Elements("REB_DUTY").Value        
        CondenserCoolingRequired = self.BLK.Elements(Blockname).Elements("Output").Elements("COND_DUTY").Value        
        DestillateTemperature = self.BLK.Elements(Blockname).Elements("Output").Elements("DISTIL_TEMP").Value        
        BottomTemperature = self.BLK.Elements(Blockname).Elements("Output").Elements("BOTTOM_TEMP").Value        
        DestillateFeedFraction = self.BLK.Elements(Blockname).Elements("Output").Elements("DIST_VS_FEED").Value        
        HETP = self.BLK.Elements(Blockname).Elements("Output").Elements("HETP").Value        
        #Page 2
        MoleFlowBalanceIN = self.BLK.Elements(Blockname).Elements("Output").Elements("BAL_MOLI_TFL").Value              
        MoleFlowBalanceOUT = self.BLK.Elements(Blockname).Elements("Output").Elements("BAL_MOLO_TFL").Value        
        MoleFlowBalanceRelDifference = self.BLK.Elements(Blockname).Elements("Output").Elements("BAL_MOLR_TFL").Value        
        MassFlowBalanceIN = self.BLK.Elements(Blockname).Elements("Output").Elements("BAL_MASI_TFL").Value              
        MassFlowBalanceOUT = self.BLK.Elements(Blockname).Elements("Output").Elements("BAL_MASO_TFL").Value              
        MassFlowBalanceRelDifference = self.BLK.Elements(Blockname).Elements("Output").Elements("BAL_MASR_TFL").Value              
        EnthalpyBalanceIN = self.BLK.Elements(Blockname).Elements("Output").Elements("TOT_ENTH_ABS").Value              
        EnthalpyBalanceOUT = self.BLK.Elements(Blockname).Elements("Output").Elements("BAL_ENTH_OUT").Value              
        EnthalpyBalanceRelDifference = self.BLK.Elements(Blockname).Elements("Output").Elements("TOT_ENTH_REL").Value              
        #PAGE 3
        StagenumberList = []
        RefluxratioValueList = []
        for Stage in self.BLK.Elements(Blockname).Elements("Output").Elements("RR"):
            StagenumberList.append(Stage)
            RefluxratioValueList.append(self.BLK.Elements(Blockname).Elements("Output").Elements("RR").Elements(Stage).Value)
        #PAGE 4
        ConvergenceStatus = self.BLK.Elements(Blockname).Elements("Output").Elements("BLKSTAT").Value  
        ConvergenceMessage = self.BLK.Elements(Blockname).Elements("Output").Elements("BLKMSG").Value
        PropertyStatus= self.BLK.Elements(Blockname).Elements("Output").Elements("PROPSTAT").Value  
          
        Dictionary = {
            "MinimumRefluxRatio":MinimumRefluxRatio,
            "ActualRefluxRatio":ActualRefluxRatio,
            "MinimumNStage":MinimumNStage,
            "ActualNStage":ActualNStage,
            "FeedStage":FeedStage,
            "ActualNumberOfStagesAboveFeed":ActualNumberOfStagesAboveFeed,
            "ReboilerHeatingRequired":ReboilerHeatingRequired,
            "CondenserCoolingRequired":CondenserCoolingRequired,
            "DestillateTemperature":DestillateTemperature,
            "BottomTemperature":BottomTemperature,
            "DestillateFeedFraction":DestillateFeedFraction,
            "HETP":HETP,
            "MoleFlowBalanceIN":MoleFlowBalanceIN,
            "MoleFlowBalanceOUT":MoleFlowBalanceOUT,
            "MoleFlowBalanceRelDifference":MoleFlowBalanceRelDifference,
            "MassFlowBalanceIN":MassFlowBalanceIN,
            "MassFlowBalanceOUT":MassFlowBalanceOUT,
            "MassFlowBalanceRelDifference":MassFlowBalanceRelDifference,
            "EnthalpyBalanceIN":EnthalpyBalanceIN,
            "EnthalpyBalanceOUT":EnthalpyBalanceOUT,
            "EnthalpyBalanceRelDifference":EnthalpyBalanceRelDifference,
            "StagenumberList":StagenumberList,
            "RefluxratioValueList":RefluxratioValueList,
            "ConvergenceStatus":ConvergenceStatus,
            "ConvergenceMessage":ConvergenceMessage,
            "PropertyStatus":PropertyStatus,
        }
        return Dictionary

## OUTPUTS FOR DSTWU
#PAGE 1:        Summary
    def BLK_DSTWU_Get_MinimumRefluxRatio(self, Blockname):
        return self.BLK.Elements(Blockname).Elements("Output").Elements("MIN_REFLUX").Value
    def BLK_DSTWU_Get_ActualRefluxRatio(self, Blockname):
        return self.BLK.Elements(Blockname).Elements("Output").Elements("ACT_REFLUX").Value   
    def BLK_DSTWU_Get_MinimumNStage(self, Blockname):
        return self.BLK.Elements(Blockname).Elements("Output").Elements("MIN_STAGES").Value 
    def BLK_DSTWU_Get_ActualNStage(self, Blockname):
        return self.BLK.Elements(Blockname).Elements("Output").Elements("ACT_STAGES").Value   
    def BLK_DSTWU_Get_FeedStage(self, Blockname):
        return self.BLK.Elements(Blockname).Elements("Output").Elements("FEED_LOCATN").Value
    def BLK_DSTWU_Get_ActualNumberOfStagesAboveFeed(self, Blockname):
        return self.BLK.Elements(Blockname).Elements("Output").Elements("RECT_STAGE").Value     
    def BLK_DSTWU_Get_ReboilerHeatingRequired(self, Blockname):
        return self.BLK.Elements(Blockname).Elements("Output").Elements("REB_DUTY").Value       
    def BLK_DSTWU_Get_CondenserCoolingRequired(self, Blockname):
        return self.BLK.Elements(Blockname).Elements("Output").Elements("COND_DUTY").Value     
    def BLK_DSTWU_Get_DestillateTemperature(self, Blockname):
        return self.BLK.Elements(Blockname).Elements("Output").Elements("DISTIL_TEMP").Value      
    def BLK_DSTWU_Get_BottomTemperature(self, Blockname):
        return self.BLK.Elements(Blockname).Elements("Output").Elements("BOTTOM_TEMP").Value     
    def BLK_DSTWU_Get_DestillateFeedFraction(self, Blockname):
        return self.BLK.Elements(Blockname).Elements("Output").Elements("DIST_VS_FEED").Value     
    def BLK_DSTWU_Get_HETP(self, Blockname):
        return self.BLK.Elements(Blockname).Elements("Output").Elements("HETP").Value      

#Page 2       Balance
    def BLK_DSTWU_Get_MoleFlowBalanceIN(self, Blockname):
        return self.BLK.Elements(Blockname).Elements("Output").Elements("BAL_MOLI_TFL").Value         
    def BLK_DSTWU_Get_MoleFlowBalanceOUT(self, Blockname):
        return self.BLK.Elements(Blockname).Elements("Output").Elements("BAL_MOLO_TFL").Value      
    def BLK_DSTWU_Get_MoleFlowBalanceRelDifference(self, Blockname):
        return self.BLK.Elements(Blockname).Elements("Output").Elements("BAL_MOLR_TFL").Value     
    def BLK_DSTWU_Get_MassFlowBalanceIN(self, Blockname):
        return self.BLK.Elements(Blockname).Elements("Output").Elements("BAL_MASI_TFL").Value          
    def BLK_DSTWU_Get_MassFlowBalanceOUT(self, Blockname):
        return self.BLK.Elements(Blockname).Elements("Output").Elements("BAL_MASO_TFL").Value           
    def BLK_DSTWU_Get_MassFlowBalanceRelDifference(self, Blockname):
        return self.BLK.Elements(Blockname).Elements("Output").Elements("BAL_MASR_TFL").Value             
    def BLK_DSTWU_Get_EnthalpyBalanceIN(self, Blockname):
        return self.BLK.Elements(Blockname).Elements("Output").Elements("TOT_ENTH").Value          
    def BLK_DSTWU_Get_EnthalpyBalanceOUT(self, Blockname):
        return self.BLK.Elements(Blockname).Elements("Output").Elements("BAL_ENTH_OUT").Value           
    def BLK_DSTWU_Get_EnthalpyBalanceRelDifference(self, Blockname):
        return self.BLK.Elements(Blockname).Elements("Output").Elements("TOT_ENTH_REL").Value             

#PAGE 3     Reflux Ratio Profile
    def BLK_DSTWU_Get_RefluxRatioProfile(self, Blockname:str) -> list:    
        StagenumberList = []
        RefluxratioValueList = []
        for Stage in self.BLK.Elements(Blockname).Elements("Output").Elements("RR"):
            StagenumberList.append(Stage)
            RefluxratioValueList.append(self.BLK.Elements(Blockname).Elements("Output").Elements("RR").Elements(Stage).Value)
        return StagenumberList, RefluxratioValueList
#PAGE 4     Status
    def BLK_DSTWU_Get_ConvergenceStatus(self, Blockname):
        return self.BLK.Elements(Blockname).Elements("Output").Elements("BLKSTAT").Value  
    def BLK_DSTWU_Get_ConvergenceMessage(self, Blockname):
        return self.BLK.Elements(Blockname).Elements("Output").Elements("BLKMSG").Value 
    def BLK_DSTWU_Get_PropertyStatus(self, Blockname):
        return self.BLK.Elements(Blockname).Elements("Output").Elements("PROPSTAT").Value 

        















    def BLK_FLASH2_GET_OUTPUTS(self, Blockname:str) -> Dict[str, Union[str,float,int]]:
        """Retrieves all Output variables for given Block and returns Dictionary of Values
            
            Args:
                Blockname: String which gives the name of Block.         
        """
        #Page 1
        OutletTemperature = self.BLK.Elements(Blockname).Elements("Output").Elements("B_TEMP").Value
        OutletPressure = self.BLK.Elements(Blockname).Elements("Output").Elements("B_PRES").Value
        VaporFractionMole = self.BLK.Elements(Blockname).Elements("Output").Elements("B_VFRAC").Value
        VaporFractionMass = self.BLK.Elements(Blockname).Elements("Output").Elements("MVFRAC").Value
        HeatingDuty = self.BLK.Elements(Blockname).Elements("Output").Elements("QCALC").Value
        NetDuty = self.BLK.Elements(Blockname).Elements("Output").Elements("QNET").Value
        FirstLiquidtoTotalLiquidRatio = self.BLK.Elements(Blockname).Elements("Output").Elements("LIQ_RATIO").Value
        PressureDrop = self.BLK.Elements(Blockname).Elements("Output").Elements("PDROP").Value

        #Page 2
        MoleFlowBalanceIN = self.BLK.Elements(Blockname).Elements("Output").Elements("BAL_MOLI_TFL").Value              
        MoleFlowBalanceOUT = self.BLK.Elements(Blockname).Elements("Output").Elements("BAL_MOLO_TFL").Value        
        MoleFlowBalanceRelDifference = self.BLK.Elements(Blockname).Elements("Output").Elements("BAL_MOLR_TFL").Value        
        MassFlowBalanceIN = self.BLK.Elements(Blockname).Elements("Output").Elements("BAL_MASI_TFL").Value              
        MassFlowBalanceOUT = self.BLK.Elements(Blockname).Elements("Output").Elements("BAL_MASO_TFL").Value              
        MassFlowBalanceRelDifference = self.BLK.Elements(Blockname).Elements("Output").Elements("BAL_MASR_TFL").Value              
        EnthalpyBalanceIN = self.BLK.Elements(Blockname).Elements("Output").Elements("TOT_ENTH_ABS").Value              
        EnthalpyBalanceOUT = self.BLK.Elements(Blockname).Elements("Output").Elements("BAL_ENTH_OUT").Value              
        EnthalpyBalanceRelDifference = self.BLK.Elements(Blockname).Elements("Output").Elements("TOT_ENTH_REL").Value     

        #PAGE 3
        CompoundLister = self.BLK.Elements(Blockname).Elements("Output").Elements("F").Elements
        TotalFlowFractionList = []
        LiquidConcentrationList = []
        VaporConcentrationList = []
        EquilibriumConstantList = []
        CompoundNameList = []
        for compound in CompoundLister:
            Compoundname = compound.Name
            TotalFlowFractionList.append(self.BLK.Elements(Blockname).Elements("Output").Elements("F").Elements(Compoundname).Value)
            LiquidConcentrationList.append(self.BLK.Elements(Blockname).Elements("Output").Elements("X").Elements(Compoundname).Value)
            VaporConcentrationList.append(self.BLK.Elements(Blockname).Elements("Output").Elements("Y").Elements(Compoundname).Value)            
            EquilibriumConstantList.append(self.BLK.Elements(Blockname).Elements("Output").Elements("B_K").Elements(Compoundname).Value)      
            CompoundNameList.append(Compoundname)
        #PAGE 4


        #PAGE 5:
        ConvergenceStatus = self.BLK.Elements(Blockname).Elements("Output").Elements("BLKSTAT").Value  
        ConvergenceMessage = self.BLK.Elements(Blockname).Elements("Output").Elements("BLKMSG").Value
        PropertyStatus= self.BLK.Elements(Blockname).Elements("Output").Elements("PROPSTAT").Value  
          
        Dictionary = {
            "OutletTemperature":OutletTemperature,
            "OutletPressure":OutletPressure,
            "VaporFractionMole":VaporFractionMole,
            "VaporFractionMass":VaporFractionMass,
            "HeatingDuty":HeatingDuty,
            "NetDuty":NetDuty,
            "FirstLiquidtoTotalLiquidRatio":FirstLiquidtoTotalLiquidRatio,
            "PressureDrop":PressureDrop,

            "MoleFlowBalanceIN":MoleFlowBalanceIN,
            "MoleFlowBalanceOUT":MoleFlowBalanceOUT,
            "MoleFlowBalanceRelDifference":MoleFlowBalanceRelDifference,
            "MassFlowBalanceIN":MassFlowBalanceIN,
            "MassFlowBalanceOUT":MassFlowBalanceOUT,
            "MassFlowBalanceRelDifference":MassFlowBalanceRelDifference,
            "EnthalpyBalanceIN":EnthalpyBalanceIN,
            "EnthalpyBalanceOUT":EnthalpyBalanceOUT,
            "EnthalpyBalanceRelDifference":EnthalpyBalanceRelDifference,

            "CompoundNameList":CompoundNameList,
            "TotalFlowFractionList":TotalFlowFractionList,
            "LiquidConcentrationList":LiquidConcentrationList,
            "VaporConcentrationList":VaporConcentrationList,
            "EquilibriumConstantList":EquilibriumConstantList,

            "ConvergenceStatus":ConvergenceStatus,
            "ConvergenceMessage":ConvergenceMessage,
            "PropertyStatus":PropertyStatus,
        }
        return Dictionary


## OUTPUTS FOR FLASH2
#PAGE 1:        Summary
    def BLK_FLASH2_Get_OutletTemperature(self, Blockname):
        return self.BLK.Elements(Blockname).Elements("Output").Elements("B_TEMP").Value
    def BLK_FLASH2_Get_OutletPressure(self, Blockname):
        return self.BLK.Elements(Blockname).Elements("Output").Elements("B_PRES").Value
    def BLK_FLASH2_Get_VaporFractionMole(self, Blockname):
        return self.BLK.Elements(Blockname).Elements("Output").Elements("B_VFRAC").Value
    def BLK_FLASH2_Get_VaporFractionMass(self, Blockname):
        return self.BLK.Elements(Blockname).Elements("Output").Elements("MVFRAC").Value
    def BLK_FLASH2_Get_HeatingDuty(self, Blockname):
        return self.BLK.Elements(Blockname).Elements("Output").Elements("QCALC").Value
    def BLK_FLASH2_Get_NetDuty(self, Blockname):
        return self.BLK.Elements(Blockname).Elements("Output").Elements("QNET").Value
    def BLK_FLASH2_Get_FirstLiquidtoTotalLiquidRatio(self, Blockname):
        return self.BLK.Elements(Blockname).Elements("Output").Elements("LIQ_RATIO").Value
    def BLK_FLASH2_Get_PressureDrop(self, Blockname):
        return self.BLK.Elements(Blockname).Elements("Output").Elements("PDROP").Value

#PAGE 2:        Balances:
    def BLK_FLASH2_Get_MoleFlowBalanceIN(self, Blockname):
        return self.BLK.Elements(Blockname).Elements("Output").Elements("BAL_MOLI_TFL").Value         
    def BLK_FLASH2_Get_MoleFlowBalanceOUT(self, Blockname):
        return self.BLK.Elements(Blockname).Elements("Output").Elements("BAL_MOLO_TFL").Value      
    def BLK_FLASH2_Get_MoleFlowBalanceRelDifference(self, Blockname):
        return self.BLK.Elements(Blockname).Elements("Output").Elements("BAL_MOLR_TFL").Value     
    def BLK_FLASH2_Get_MassFlowBalanceIN(self, Blockname):
        return self.BLK.Elements(Blockname).Elements("Output").Elements("BAL_MASI_TFL").Value          
    def BLK_FLASH2_Get_MassFlowBalanceOUT(self, Blockname):
        return self.BLK.Elements(Blockname).Elements("Output").Elements("BAL_MASO_TFL").Value           
    def BLK_FLASH2_Get_MassFlowBalanceRelDifference(self, Blockname):
        return self.BLK.Elements(Blockname).Elements("Output").Elements("BAL_MASR_TFL").Value             
    def BLK_FLASH2_Get_EnthalpyBalanceIN(self, Blockname):
        return self.BLK.Elements(Blockname).Elements("Output").Elements("TOT_ENTH").Value          
    def BLK_FLASH2_Get_EnthalpyBalanceOUT(self, Blockname):
        return self.BLK.Elements(Blockname).Elements("Output").Elements("BAL_ENTH_OUT").Value           
    def BLK_FLASH2_Get_EnthalpyBalanceRelDifference(self, Blockname):
        return self.BLK.Elements(Blockname).Elements("Output").Elements("TOT_ENTH_REL").Value             

#PAGE 3:        Phase Equilibium:
    def BLK_FLASH2_Get_TotalFlowFraction_F(self, Blockname,Compoundname):
        return self.BLK.Elements(Blockname).Elements("Output").Elements("F").Elements(Compoundname).Value
    def BLK_FLASH2_Get_LiquidConcentration_X(self, Blockname, Compoundname):
        return self.BLK.Elements(Blockname).Elements("Output").Elements("X").Elements(Compoundname).Value
    def BLK_FLASH2_Get_VaporConcentration_Y(self, Blockname,Compoundname):
        return self.BLK.Elements(Blockname).Elements("Output").Elements("Y").Elements(Compoundname).Value
    def BLK_FLASH2_Get_EquilinriumConstant_K(self, Blockname, Compoundname):
        return self.BLK.Elements(Blockname).Elements("Output").Elements("B_K").Elements(Compoundname).Value

#PAGE 4:        Utility Usage:

    #I CAN not ACTIVATE THIS....

#PAGE 5:        Status:
    def BLK_FLASH2_Get_ConvergenceStatus(self, Blockname):
        return self.BLK.Elements(Blockname).Elements("Output").Elements("BLKSTAT").Value  
    def BLK_FLASH2_Get_ConvergenceMessage(self, Blockname):
        return self.BLK.Elements(Blockname).Elements("Output").Elements("BLKMSG").Value 
    def BLK_FLASH2_Get_PropertyStatus(self, Blockname):
        return self.BLK.Elements(Blockname).Elements("Output").Elements("PROPSTAT").Value 

        

























    def BLK_RADFRAC_GET_OUTPUTS(self, Blockname:str) -> Dict[str, Union[str,float,int]]:
        """Retrieves all Output variables for given Block and returns Dictionary of Values
            
            Args:
                Blockname: String which gives the name of Block.         
        """
        Condenser_Temperature = self.BLK.Elements(Blockname).Elements("Output").Elements("TOP_TEMP").Value
        Condenser_SubcooledTemp = self.BLK.Elements(Blockname).Elements("Output").Elements("SCTEMP").Value
        Condenser_HeatingDuty = self.BLK.Elements(Blockname).Elements("Output").Elements("COND_DUTY").Value
        Condenser_SubcooledDuty = self.BLK.Elements(Blockname).Elements("Output").Elements("SCDUTY").Value
        Condenser_DistillateRate = self.BLK.Elements(Blockname).Elements("Output").Elements("MOLE_D").Value
        Condenser_RefluxRate = self.BLK.Elements(Blockname).Elements("Output").Elements("MOLE_L1").Value
        Condenser_FreeWaterDistillateRate = self.BLK.Elements(Blockname).Elements("Output").Elements("MOLE_DW").Value
        Condenser_FreeWaterRefluxRatio = self.BLK.Elements(Blockname).Elements("Output").Elements("RW").Value
        Condenser_DistillateToFeedRatio = self.BLK.Elements(Blockname).Elements("Output").Elements("MOLE_DFR").Value

        Reboiler_Temperature = self.BLK.Elements(Blockname).Elements("Output").Elements("BOTTOM_TEMP").Value
        Reboiler_HeatDuty = self.BLK.Elements(Blockname).Elements("Output").Elements("REB_DUTY").Value
        Reboiler_BottomsRate = self.BLK.Elements(Blockname).Elements("Output").Elements("MOLE_B").Value
        Reboiler_BoilupRate = self.BLK.Elements(Blockname).Elements("Output").Elements("MOLE_VN").Value
        Reboiler_BoilupRatio = self.BLK.Elements(Blockname).Elements("Output").Elements("CMF_MAMX").Value
        Reboiler_BottomsToFeedRatio = self.BLK.Elements(Blockname).Elements("Output").Elements("MOLE_BFR").Value

        MoleFlowBalanceIN = self.BLK.Elements(Blockname).Elements("Output").Elements("BAL_MOLI_TFL").Value              
        MoleFlowBalanceOUT = self.BLK.Elements(Blockname).Elements("Output").Elements("BAL_MOLO_TFL").Value        
        MoleFlowBalanceRelDifference = self.BLK.Elements(Blockname).Elements("Output").Elements("BAL_MOLR_TFL").Value        
        MassFlowBalanceIN = self.BLK.Elements(Blockname).Elements("Output").Elements("BAL_MASI_TFL").Value              
        MassFlowBalanceOUT = self.BLK.Elements(Blockname).Elements("Output").Elements("BAL_MASO_TFL").Value              
        MassFlowBalanceRelDifference = self.BLK.Elements(Blockname).Elements("Output").Elements("BAL_MASR_TFL").Value              
        EnthalpyBalanceIN = self.BLK.Elements(Blockname).Elements("Output").Elements("TOT_ENTH_ABS").Value              
        EnthalpyBalanceOUT = self.BLK.Elements(Blockname).Elements("Output").Elements("BAL_ENTH_OUT").Value              
        EnthalpyBalanceRelDifference = self.BLK.Elements(Blockname).Elements("Output").Elements("TOT_ENTH_REL").Value   


        CompoundLister = self.BLK.Elements(Blockname).Elements("Output").Elements("MASS_CONC").Elements
        SplitFractionInS1List = []
        SplitFractionInS2List = []
        ReboilerMoleFractionInLiquidList = []
        ReboilerMoleFractionInVaporList = []
        CompoundNameList = []
        for compound in CompoundLister:
            Compoundname = compound.Name
            StreamnodeLister = self.BLK.Elements(Blockname).Elements("Output").Elements("MASS_CONC").Elements(Compoundname).Elements
            for StreamnameNode in StreamnodeLister:
                Streamname = StreamnameNode.Name
                SplitFractionInS1List.append(self.BLK.Elements(Blockname).Elements("Output").Elements("MASS_CONC").Elements(Compoundname).Elements(Streamname).Value)
                SplitFractionInS2List.append(self.BLK.Elements(Blockname).Elements("Output").Elements("MASS_CONC").Elements(Compoundname).Elements(Streamname).Value)
            try:
                ReboilerMoleFractionInLiquidList.append(self.BLK.Elements(Blockname).Elements("Output").Elements("TH_X").Elements(Compoundname).Value)            
                ReboilerMoleFractionInVaporList.append(self.BLK.Elements(Blockname).Elements("Output").Elements("TH_Y").Elements(Compoundname).Value)      
            except Exception:
                pass
            CompoundNameList.append(Compoundname)
        try:
            Thermosiphon_Pressure = self.BLK.Elements(Blockname).Elements("Output").Elements("TH_PRES_OUT").Value
            Thermosiphon_Temperature = self.BLK.Elements(Blockname).Elements("Output").Elements("TH_TEMP_OUT").Value
            Thermosiphon_MolarVaporFraction = self.BLK.Elements(Blockname).Elements("Output").Elements("TH_VFRAC_OUT").Value
            Thermosiphon_MolarFlow = self.BLK.Elements(Blockname).Elements("Output").Elements("TH_MOLEFLOW").Value
            Thermosiphon_MassFlow = self.BLK.Elements(Blockname).Elements("Output").Elements("TH_MASSFLOW").Value
            Thermosiphon_HeatDuty = self.BLK.Elements(Blockname).Elements("Output").Elements("TH_DUTY").Value
            Thermosiphon_FirstliquidByTotalLiquidRatio = self.BLK.Elements(Blockname).Elements("Output").Elements("LIQ_RATIO").Value
        except Exception:
            pass

        ConvergenceStatus = self.BLK.Elements(Blockname).Elements("Output").Elements("BLKSTAT").Value 
        ConvergenceMessage = self.BLK.Elements(Blockname).Elements("Output").Elements("BLKMSG").Value 
        PropertyStatus = self.BLK.Elements(Blockname).Elements("Output").Elements("PROPSTAT").Value
        if Thermosiphon_Pressure == None:
            Thermosiphon_Temperature = None
            Thermosiphon_MolarVaporFraction=None
            Thermosiphon_MolarFlow=None
            Thermosiphon_MassFlow=None
            Thermosiphon_HeatDuty=None
            Thermosiphon_FirstliquidByTotalLiquidRatio=None

        Dictionary = {
            "Condenser_Temperature":Condenser_Temperature,
            "Condenser_SubcooledTemp":Condenser_SubcooledTemp,
            "Condenser_HeatingDuty":Condenser_HeatingDuty,
            "Condenser_SubcooledDuty":Condenser_SubcooledDuty,
            "Condenser_DistillateRate":Condenser_DistillateRate,
            "Condenser_RefluxRate":Condenser_RefluxRate,
            "Condenser_FreeWaterDistillateRate":Condenser_FreeWaterDistillateRate,
            "Condenser_FreeWaterRefluxRatio":Condenser_FreeWaterRefluxRatio,
            "Condenser_DistillateToFeedRatio":Condenser_DistillateToFeedRatio,

            "Reboiler_Temperature":Reboiler_Temperature,
            "Reboiler_HeatDuty":Reboiler_HeatDuty,
            "Reboiler_BottomsRate":Reboiler_BottomsRate,
            "Reboiler_BoilupRate":Reboiler_BoilupRate,
            "Reboiler_BoilupRatio":Reboiler_BoilupRatio,
            "Reboiler_BottomsToFeedRatio":Reboiler_BottomsToFeedRatio,

            "MoleFlowBalanceIN":MoleFlowBalanceIN,
            "MoleFlowBalanceOUT":MoleFlowBalanceOUT,
            "MoleFlowBalanceRelDifference":MoleFlowBalanceRelDifference,
            "MassFlowBalanceIN":MassFlowBalanceIN,
            "MassFlowBalanceOUT":MassFlowBalanceOUT,
            "MassFlowBalanceRelDifference":MassFlowBalanceRelDifference,
            "EnthalpyBalanceIN":EnthalpyBalanceIN,
            "EnthalpyBalanceOUT":EnthalpyBalanceOUT,
            "EnthalpyBalanceRelDifference":EnthalpyBalanceRelDifference,

            "CompoundNameList":CompoundNameList,
            "SplitFractionInS1List":SplitFractionInS1List,
            "SplitFractionInS2List":SplitFractionInS2List,
            "ReboilerMoleFractionInLiquidList":ReboilerMoleFractionInLiquidList,
            "ReboilerMoleFractionInVaporList":ReboilerMoleFractionInVaporList,
            
            "Thermosiphon_Pressure":Thermosiphon_Pressure,
            "Thermosiphon_Temperature":Thermosiphon_Temperature,
            "Thermosiphon_MolarVaporFraction":Thermosiphon_MolarVaporFraction,
            "Thermosiphon_MolarFlow":Thermosiphon_MolarFlow,
            "Thermosiphon_MassFlow":Thermosiphon_MassFlow,
            "Thermosiphon_HeatDuty":Thermosiphon_HeatDuty,
            "Thermosiphon_FirstliquidByTotalLiquidRatio":Thermosiphon_FirstliquidByTotalLiquidRatio,

            "ConvergenceStatus":ConvergenceStatus,
            "ConvergenceMessage":ConvergenceMessage,        
            "PropertyStatus":PropertyStatus,
            
        }
        return Dictionary


#RADFRAC OUTPUTS

#PAGE 1 Summary
    #Condenser data
    def BLK_RADFRAC_Get_Condenser_Temperature(self, Blockname):
        return self.BLK.Elements(Blockname).Elements("Output").Elements("TOP_TEMP").Value
    def BLK_RADFRAC_Get_Condenser_SubcooledTemp(self, Blockname):
        return self.BLK.Elements(Blockname).Elements("Output").Elements("SCTEMP").Value
    def BLK_RADFRAC_Get_Condenser_HeatingDuty(self, Blockname):
        return self.BLK.Elements(Blockname).Elements("Output").Elements("COND_DUTY").Value
    def BLK_RADFRAC_Get_Condenser_SubcooledDuty(self, Blockname):
        return self.BLK.Elements(Blockname).Elements("Output").Elements("SCDUTY").Value
    def BLK_RADFRAC_Get_Condenser_DistillateRate(self, Blockname):
        return self.BLK.Elements(Blockname).Elements("Output").Elements("MOLE_D").Value
    def BLK_RADFRAC_Get_Condenser_RefluxRate(self, Blockname):
        return self.BLK.Elements(Blockname).Elements("Output").Elements("MOLE_L1").Value
    def BLK_RADFRAC_Get_Condenser_FreeWaterDistillateRate(self, Blockname):
        return self.BLK.Elements(Blockname).Elements("Output").Elements("MOLE_DW").Value
    def BLK_RADFRAC_Get_Condenser_FreeWaterRefluxRatio(self, Blockname):
        return self.BLK.Elements(Blockname).Elements("Output").Elements("RW").Value
    def BLK_RADFRAC_Get_Condenser_DistillateToFeedRatio(self, Blockname):
        return self.BLK.Elements(Blockname).Elements("Output").Elements("MOLE_DFR").Value
    #Reboiler data
    def BLK_RADFRAC_Get_Reboiler_Temperature(self, Blockname):
        return self.BLK.Elements(Blockname).Elements("Output").Elements("BOTTOM_TEMP").Value
    def BLK_RADFRAC_Get_Reboiler_HeatDuty(self, Blockname):
        return self.BLK.Elements(Blockname).Elements("Output").Elements("REB_DUTY").Value
    def BLK_RADFRAC_Get_Reboiler_BottomsRate(self, Blockname):
        return self.BLK.Elements(Blockname).Elements("Output").Elements("MOLE_B").Value
    def BLK_RADFRAC_Get_Reboiler_BoilupRate(self, Blockname):
        return self.BLK.Elements(Blockname).Elements("Output").Elements("MOLE_VN").Value
    def BLK_RADFRAC_Get_Reboiler_BoilupRatio(self, Blockname):
        return self.BLK.Elements(Blockname).Elements("Output").Elements("CMF_MAMX").Value
    def BLK_RADFRAC_Get_Reboiler_BottomsToFeedRatio(self, Blockname):
        return self.BLK.Elements(Blockname).Elements("Output").Elements("MOLE_BFR").Value


    #PAGE 2 Balance:
    def BLK_RADFRAC_Get_MoleFlowBalanceIN(self, Blockname):
        return self.BLK.Elements(Blockname).Elements("Output").Elements("BAL_MOLI_TFL").Value         
    def BLK_RADFRAC_Get_MoleFlowBalanceOUT(self, Blockname):
        return self.BLK.Elements(Blockname).Elements("Output").Elements("BAL_MOLO_TFL").Value      
    def BLK_RADFRAC_Get_MoleFlowBalanceRelDifference(self, Blockname):
        return self.BLK.Elements(Blockname).Elements("Output").Elements("BAL_MOLR_TFL").Value     
    def BLK_RADFRAC_Get_MassFlowBalanceIN(self, Blockname):
        return self.BLK.Elements(Blockname).Elements("Output").Elements("BAL_MASI_TFL").Value          
    def BLK_RADFRAC_Get_MassFlowBalanceOUT(self, Blockname):
        return self.BLK.Elements(Blockname).Elements("Output").Elements("BAL_MASO_TFL").Value           
    def BLK_RADFRAC_Get_MassFlowBalanceRelDifference(self, Blockname):
        return self.BLK.Elements(Blockname).Elements("Output").Elements("BAL_MASR_TFL").Value             
    def BLK_RADFRAC_Get_EnthalpyBalanceIN(self, Blockname):
        return self.BLK.Elements(Blockname).Elements("Output").Elements("TOT_ENTH").Value          
    def BLK_RADFRAC_Get_EnthalpyBalanceOUT(self, Blockname):
        return self.BLK.Elements(Blockname).Elements("Output").Elements("BAL_ENTH_OUT").Value           
    def BLK_RADFRAC_Get_EnthalpyBalanceRelDifference(self, Blockname):
        return self.BLK.Elements(Blockname).Elements("Output").Elements("TOT_ENTH_REL").Value             

    
    #PAGE 3 SPLIT FRACTION:
    def BLK_RADFRAC_Get_SplitFraction(self, Blockname, Compoundname, OutputStreamname):
        return self.BLK.Elements(Blockname).Elements("Output").Elements("MASS_CONC").Elements(Compoundname).Elements(OutputStreamname).Value
    def BLK_RADFRAC_Get_SplitFraction_List(self, Blockname:str, OutputStreamName:str) -> list:
        CompoundLister = self.BLK.Elements(Blockname).Elements("Output").Elements("MASS_CONC").Elements
        SplitFractionInS1List = []
        CompoundNameList = []
        for compound in CompoundLister:
            Compoundname = compound.Name
            SplitFractionInS1List.append(self.BLK.Elements(Blockname).Elements("Output").Elements("MASS_CONC").Elements(Compoundname).Elements(OutputStreamName).Value)
            CompoundNameList.append(Compoundname)
        return SplitFractionInS1List

    #PAGE 4 Reboiler:
    def BLK_RADFRAC_Get_Thermosiphon_Pressure(self, Blockname):
        return self.BLK.Elements(Blockname).Elements("Output").Elements("TH_PRES_OUT").Value
    def BLK_RADFRAC_Get_Thermosiphon_Temperature(self, Blockname):
        return self.BLK.Elements(Blockname).Elements("Output").Elements("TH_TEMP_OUT").Value
    def BLK_RADFRAC_Get_Thermosiphon_MolarVaporFraction(self, Blockname):
        return self.BLK.Elements(Blockname).Elements("Output").Elements("TH_VFRAC_OUT").Value
    def BLK_RADFRAC_Get_Thermosiphon_MolarFlow(self, Blockname):
        return self.BLK.Elements(Blockname).Elements("Output").Elements("TH_MOLEFLOW").Value
    def BLK_RADFRAC_Get_Thermosiphon_MassFlow(self, Blockname):
        return self.BLK.Elements(Blockname).Elements("Output").Elements("TH_MASSFLOW").Value
    def BLK_RADFRAC_Get_Thermosiphon_HeatDuty(self, Blockname):
        return self.BLK.Elements(Blockname).Elements("Output").Elements("TH_DUTY").Value
    def BLK_RADFRAC_Get_Thermosiphon_FirstliquidByTotalLiquidRatio(self, Blockname):
        return self.BLK.Elements(Blockname).Elements("Output").Elements("LIQ_RATIO").Value
    def BLK_RADFRAC_Get_ReboilerMoleFractionInLiquid(self, Blockname, Compoundname):
        return self.BLK.Elements(Blockname).Elements("Output").Elements("TH_X").Elements(Compoundname).Value
    def BLK_RADFRAC_Get_ReboilerMoleFractionInVapor(self, Blockname, Compoundname):
        return self.BLK.Elements(Blockname).Elements("Output").Elements("TH_Y").Elements(Compoundname).Value

#PAGE 5 Utilities:
        #missing    

#PAGE 6 STAGE UTILITIES:
        #MISSING

#PAGE 7 STATUS:
    def BLK_RADFRAC_Get_ConvergenceStatus(self, Blockname):
        return self.BLK.Elements(Blockname).Elements("Output").Elements("BLKSTAT").Value  
    def BLK_RADFRAC_Get_ConvergenceMessage(self, Blockname):
        return self.BLK.Elements(Blockname).Elements("Output").Elements("BLKMSG").Value 
    def BLK_RADFRAC_Get_PropertyStatus(self, Blockname):
        return self.BLK.Elements(Blockname).Elements("Output").Elements("PROPSTAT").Value 

























    def BLK_MIXER_GET_OUTPUTS(self, Blockname:str) -> Dict[str, Union[str,float,int]]:
        """Retrieves all Output variables for given Block and returns Dictionary of Values
            
            Args:
                Blockname: String which gives the name of Block.         
        """
        OutletTemperature = self.BLK.Elements(Blockname).Elements("Output").Elements("B_TEMP").Value
        OutletPressure = self.BLK.Elements(Blockname).Elements("Output").Elements("B_PRES").Value
        VaporFraction = self.BLK.Elements(Blockname).Elements("Output").Elements("B_VFRAC").Value
        FirstLiquidbyTotalLiquid = self.BLK.Elements(Blockname).Elements("Output").Elements("LIQ_RATIO").Value
        PressureDrop = self.BLK.Elements(Blockname).Elements("Output").Elements("PDROP").Value

        MoleFlowBalanceIN = self.BLK.Elements(Blockname).Elements("Output").Elements("BAL_MOLI_TFL").Value              
        MoleFlowBalanceOUT = self.BLK.Elements(Blockname).Elements("Output").Elements("BAL_MOLO_TFL").Value        
        MoleFlowBalanceRelDifference = self.BLK.Elements(Blockname).Elements("Output").Elements("BAL_MOLR_TFL").Value        
        MassFlowBalanceIN = self.BLK.Elements(Blockname).Elements("Output").Elements("BAL_MASI_TFL").Value              
        MassFlowBalanceOUT = self.BLK.Elements(Blockname).Elements("Output").Elements("BAL_MASO_TFL").Value              
        MassFlowBalanceRelDifference = self.BLK.Elements(Blockname).Elements("Output").Elements("BAL_MASR_TFL").Value              
        EnthalpyBalanceIN = self.BLK.Elements(Blockname).Elements("Output").Elements("TOT_ENTH_ABS").Value              
        EnthalpyBalanceOUT = self.BLK.Elements(Blockname).Elements("Output").Elements("BAL_ENTH_OUT").Value              
        EnthalpyBalanceRelDifference = self.BLK.Elements(Blockname).Elements("Output").Elements("TOT_ENTH_REL").Value   

        ConvergenceStatus = self.BLK.Elements(Blockname).Elements("Output").Elements("BLKSTAT").Value 
        ConvergenceMessage = self.BLK.Elements(Blockname).Elements("Output").Elements("BLKMSG").Value 
        PropertyStatus = self.BLK.Elements(Blockname).Elements("Output").Elements("PROPSTAT").Value

        Dictionary = {
            "OutletTemperature":OutletTemperature,
            "OutletPressure":OutletPressure,
            "VaporFraction":VaporFraction,
            "FirstLiquidbyTotalLiquid":FirstLiquidbyTotalLiquid,
            "PressureDrop":PressureDrop,

            "MoleFlowBalanceIN":MoleFlowBalanceIN,
            "MoleFlowBalanceOUT":MoleFlowBalanceOUT,
            "MoleFlowBalanceRelDifference":MoleFlowBalanceRelDifference,
            "MassFlowBalanceIN":MassFlowBalanceIN,
            "MassFlowBalanceOUT":MassFlowBalanceOUT,
            "MassFlowBalanceRelDifference":MassFlowBalanceRelDifference,
            "EnthalpyBalanceIN":EnthalpyBalanceIN,
            "EnthalpyBalanceOUT":EnthalpyBalanceOUT,
            "EnthalpyBalanceRelDifference":EnthalpyBalanceRelDifference,

            "ConvergenceStatus":ConvergenceStatus,
            "ConvergenceMessage":ConvergenceMessage,        
            "PropertyStatus":PropertyStatus,
        }
        return Dictionary

#MIXER
#  PAGE 1 Summary
    def BLK_MIXER_Get_OutletTemperature(self, Blockname):
        return self.BLK.Elements(Blockname).Elements("Output").Elements("B_TEMP").Value
    def BLK_MIXER_Get_OutletPressure(self, Blockname):
        return self.BLK.Elements(Blockname).Elements("Output").Elements("B_PRES").Value
    def BLK_MIXER_Get_VaporFraction(self, Blockname):
        return self.BLK.Elements(Blockname).Elements("Output").Elements("B_VFRAC").Value
    def BLK_MIXER_Get_FirstLiquidbyTotalLiquid(self, Blockname):
        return self.BLK.Elements(Blockname).Elements("Output").Elements("LIQ_RATIO").Value
    def BLK_MIXER_Get_PressureDrop(self, Blockname):
        return self.BLK.Elements(Blockname).Elements("Output").Elements("PDROP").Value

#Page 2: Balance
    def BLK_MIXER_Get_MoleFlowBalanceIN(self, Blockname):
        return self.BLK.Elements(Blockname).Elements("Output").Elements("BAL_MOLI_TFL").Value         
    def BLK_MIXER_Get_MoleFlowBalanceOUT(self, Blockname):
        return self.BLK.Elements(Blockname).Elements("Output").Elements("BAL_MOLO_TFL").Value      
    def BLK_MIXER_Get_MoleFlowBalanceRelDifference(self, Blockname):
        return self.BLK.Elements(Blockname).Elements("Output").Elements("BAL_MOLR_TFL").Value     
    def BLK_MIXER_Get_MassFlowBalanceIN(self, Blockname):
        return self.BLK.Elements(Blockname).Elements("Output").Elements("BAL_MASI_TFL").Value          
    def BLK_MIXER_Get_MassFlowBalanceOUT(self, Blockname):
        return self.BLK.Elements(Blockname).Elements("Output").Elements("BAL_MASO_TFL").Value           
    def BLK_MIXER_Get_MassFlowBalanceRelDifference(self, Blockname):
        return self.BLK.Elements(Blockname).Elements("Output").Elements("BAL_MASR_TFL").Value             
    def BLK_MIXER_Get_EnthalpyBalanceIN(self, Blockname):
        return self.BLK.Elements(Blockname).Elements("Output").Elements("TOT_ENTH").Value          
    def BLK_MIXER_Get_EnthalpyBalanceOUT(self, Blockname):
        return self.BLK.Elements(Blockname).Elements("Output").Elements("BAL_ENTH_OUT").Value           
    def BLK_MIXER_Get_EnthalpyBalanceRelDifference(self, Blockname):
        return self.BLK.Elements(Blockname).Elements("Output").Elements("TOT_ENTH_REL").Value             


#Page 3 Status:
    def BLK_MIXER_Get_ConvergenceStatus(self, Blockname):
        return self.BLK.Elements(Blockname).Elements("Output").Elements("BLKSTAT").Value  
    def BLK_MIXER_Get_ConvergenceMessage(self, Blockname):
        return self.BLK.Elements(Blockname).Elements("Output").Elements("BLKMSG").Value 
    def BLK_MIXER_Get_PropertyStatus(self, Blockname):
        return self.BLK.Elements(Blockname).Elements("Output").Elements("PROPSTAT").Value 

























    def BLK_RCSTR_GET_OUTPUTS(self, Blockname:str) -> Dict[str, Union[str,float,int]]:
        """Retrieves all Output variables for given Block and returns Dictionary of Values
            
            Args:
                Blockname: String which gives the name of Block.         
        """
        #Page 1
        OutletTemperature = self.BLK.Elements(Blockname).Elements("Output").Elements("B_TEMP").Value
        OutletPressure = self.BLK.Elements(Blockname).Elements("Output").Elements("B_PRES").Value
        OutletVaporFraction = self.BLK.Elements(Blockname).Elements("Output").Elements("B_VFRAC").Value
        HeatDuty = self.BLK.Elements(Blockname).Elements("Output").Elements("QCALC").Value
        NetHeatDuty = self.BLK.Elements(Blockname).Elements("Output").Elements("QNET").Value
        ReactorVolume = self.BLK.Elements(Blockname).Elements("Output").Elements("TOT_VOL").Value
        VaporPhaseVolume = self.BLK.Elements(Blockname).Elements("Output").Elements("VAP_VOL").Value
        LiquidPhaseVolume = self.BLK.Elements(Blockname).Elements("Output").Elements("LIQ_VOL").Value
        Liquid1PhaseVolume = self.BLK.Elements(Blockname).Elements("Output").Elements("LIQ1_VOL").Value
        SaltPhaseVolume = self.BLK.Elements(Blockname).Elements("Output").Elements("SALT_VOL").Value
        CondensedPhaseVolume = self.BLK.Elements(Blockname).Elements("Output").Elements("COND_VOL").Value
        ReactorResidenceTime = self.BLK.Elements(Blockname).Elements("Output").Elements("TOT_RES_TIME").Value
        VaporPhaseResidenceTime = self.BLK.Elements(Blockname).Elements("Output").Elements("VAP_RES_TIME").Value
        CondensedPhaseResidenceTime = self.BLK.Elements(Blockname).Elements("Output").Elements("COND_RES_TIM").Value

        #Page 2
        MoleFlowBalanceIN = self.BLK.Elements(Blockname).Elements("Output").Elements("BAL_MOLI_TFL").Value         
        MoleFlowBalanceOUT = self.BLK.Elements(Blockname).Elements("Output").Elements("BAL_MOLO_TFL").Value      
        MoleFlowBalanceRelDifference = self.BLK.Elements(Blockname).Elements("Output").Elements("BAL_MOLR_TFL").Value     
        MoleFlowBalanceGenerated = self.BLK.Elements(Blockname).Elements("Output").Elements("BAL_MOLG_TFL").Value     
        MassFlowBalanceIN = self.BLK.Elements(Blockname).Elements("Output").Elements("BAL_MASI_TFL").Value          
        MassFlowBalanceOUT = self.BLK.Elements(Blockname).Elements("Output").Elements("BAL_MASO_TFL").Value           
        MassFlowBalanceRelDifference = self.BLK.Elements(Blockname).Elements("Output").Elements("BAL_MASR_TFL").Value             
        MassFlowBalanceGenerated = self.BLK.Elements(Blockname).Elements("Output").Elements("BAL_MASG_TFL").Value    
        EnthalpyBalanceIN = self.BLK.Elements(Blockname).Elements("Output").Elements("TOT_ENTH_ABS").Value 
        EnthalpyBalanceOUT = self.BLK.Elements(Blockname).Elements("Output").Elements("BAL_ENTH_OUT").Value           
        EnthalpyBalanceRelDifference = self.BLK.Elements(Blockname).Elements("Output").Elements("TOT_ENTH_REL").Value             
        EnthalpyBalanceGenerated = self.BLK.Elements(Blockname).Elements("Output").Elements("BAL_ENTH_GEN").Value                        
    
        #Page 7
        ConvergenceStatus = self.BLK.Elements(Blockname).Elements("Output").Elements("BLKSTAT").Value  
        ConvergenceMessage = self.BLK.Elements(Blockname).Elements("Output").Elements("BLKMSG").Value 
        PropertyStatus = self.BLK.Elements(Blockname).Elements("Output").Elements("PROPSTAT").Value 

        Dictionary = {
            "OutletTemperature":OutletTemperature,
            "OutletPressure":OutletPressure,
            "OutletVaporFraction":OutletVaporFraction,
            "HeatDuty":HeatDuty,
            "NetHeatDuty":NetHeatDuty,
            "ReactorVolume":ReactorVolume,
            "VaporPhaseVolume":VaporPhaseVolume,
            "LiquidPhaseVolume":LiquidPhaseVolume,
            "Liquid1PhaseVolume":Liquid1PhaseVolume,
            "SaltPhaseVolume":SaltPhaseVolume,
            "CondensedPhaseVolume":CondensedPhaseVolume,
            "ReactorResidenceTime":ReactorResidenceTime,
            "VaporPhaseResidenceTime":VaporPhaseResidenceTime,
            "CondensedPhaseResidenceTime":CondensedPhaseResidenceTime,

            "MoleFlowBalanceIN":MoleFlowBalanceIN,
            "MoleFlowBalanceOUT":MoleFlowBalanceOUT,
            "MoleFlowBalanceRelDifference":MoleFlowBalanceRelDifference,
            "MoleFlowBalanceGenerated":MoleFlowBalanceGenerated,
            "MassFlowBalanceIN":MassFlowBalanceIN,
            "MassFlowBalanceOUT":MassFlowBalanceOUT,
            "MassFlowBalanceRelDifference":MassFlowBalanceRelDifference,
            "MassFlowBalanceGenerated":MassFlowBalanceGenerated,
            "EnthalpyBalanceIN":EnthalpyBalanceIN,
            "EnthalpyBalanceOUT":EnthalpyBalanceOUT,
            "EnthalpyBalanceRelDifference":EnthalpyBalanceRelDifference,
            "EnthalpyBalanceGenerated":EnthalpyBalanceGenerated,

            "ConvergenceStatus":ConvergenceStatus,
            "ConvergenceMessage":ConvergenceMessage,
            "PropertyStatus":PropertyStatus,
        }
        return Dictionary
   

#RCSTR:
#PAGE 1 SUMMARY:
    def BLK_RCSTR_Get_OutletTemperature(self,Blockname):
        return self.BLK.Elements(Blockname).Elements("Output").Elements("B_TEMP").Value
    def BLK_RCSTR_Get_OutletPressure(self,Blockname):
        return self.BLK.Elements(Blockname).Elements("Output").Elements("B_PRES").Value
    def BLK_RCSTR_Get_OutletVaporFraction(self,Blockname):
        return self.BLK.Elements(Blockname).Elements("Output").Elements("B_VFRAC").Value
    def BLK_RCSTR_Get_HeatDuty(self,Blockname):
        return self.BLK.Elements(Blockname).Elements("Output").Elements("QCALC").Value
    def BLK_RCSTR_Get_NetHeatDuty(self,Blockname):
        return self.BLK.Elements(Blockname).Elements("Output").Elements("QNET").Value
    def BLK_RCSTR_Get_ReactorVolume(self,Blockname):
        return self.BLK.Elements(Blockname).Elements("Output").Elements("TOT_VOL").Value
    def BLK_RCSTR_Get_VaporPhaseVolume(self,Blockname):
        return self.BLK.Elements(Blockname).Elements("Output").Elements("VAP_VOL").Value
    def BLK_RCSTR_Get_LiquidPhaseVolume(self,Blockname):
        return self.BLK.Elements(Blockname).Elements("Output").Elements("LIQ_VOL").Value
    def BLK_RCSTR_Get_Liquid1PhaseVolume(self,Blockname):
        return self.BLK.Elements(Blockname).Elements("Output").Elements("LIQ1_VOL").Value
    def BLK_RCSTR_Get_SaltPhaseVolume(self,Blockname):
        return self.BLK.Elements(Blockname).Elements("Output").Elements("SALT_VOL").Value
    def BLK_RCSTR_Get_CondensedPhaseVolume(self,Blockname):
        return self.BLK.Elements(Blockname).Elements("Output").Elements("COND_VOL").Value
    def BLK_RCSTR_Get_ReactorResidenceTime(self,Blockname):
        return self.BLK.Elements(Blockname).Elements("Output").Elements("TOT_RES_TIME").Value
    def BLK_RCSTR_Get_VaporPhaseResidenceTime(self,Blockname):
        return self.BLK.Elements(Blockname).Elements("Output").Elements("VAP_RES_TIME").Value
    def BLK_RCSTR_Get_CondensedPhaseResidenceTime(self,Blockname):
        return self.BLK.Elements(Blockname).Elements("Output").Elements("COND_RES_TIME").Value

#Page 2: Balance
    def BLK_RCSTR_Get_MoleFlowBalanceIN(self, Blockname):
        return self.BLK.Elements(Blockname).Elements("Output").Elements("BAL_MOLI_TFL").Value         
    def BLK_RCSTR_Get_MoleFlowBalanceOUT(self, Blockname):
        return self.BLK.Elements(Blockname).Elements("Output").Elements("BAL_MOLO_TFL").Value      
    def BLK_RCSTR_Get_MoleFlowBalanceRelDifference(self, Blockname):
        return self.BLK.Elements(Blockname).Elements("Output").Elements("BAL_MOLR_TFL").Value     
    def BLK_RCSTR_Get_MoleFlowBalanceGenerated(self,Blockname):
        return self.BLK.Elements(Blockname).Elements("Output").Elements("BAL_MOLG_TFL").Value     
    def BLK_RCSTR_Get_MassFlowBalanceIN(self, Blockname):
        return self.BLK.Elements(Blockname).Elements("Output").Elements("BAL_MASI_TFL").Value          
    def BLK_RCSTR_Get_MassFlowBalanceOUT(self, Blockname):
        return self.BLK.Elements(Blockname).Elements("Output").Elements("BAL_MASO_TFL").Value           
    def BLK_RCSTR_Get_MassFlowBalanceRelDifference(self, Blockname):
        return self.BLK.Elements(Blockname).Elements("Output").Elements("BAL_MASR_TFL").Value             
    def BLK_RCSTR_Get_MassFlowBalanceGenerated(self, Blockname):
        return self.BLK.Elements(Blockname).Elements("Output").Elements("BAL_MASG_TFL").Value    
    def BLK_RCSTR_Get_EnthalpyBalanceIN(self, Blockname):
        return self.BLK.Elements(Blockname).Elements("Output").Elements("TOT_ENTH").Value          
    def BLK_RCSTR_Get_EnthalpyBalanceOUT(self, Blockname):
        return self.BLK.Elements(Blockname).Elements("Output").Elements("BAL_ENTH_OUT").Value           
    def BLK_RCSTR_Get_EnthalpyBalanceRelDifference(self, Blockname):
        return self.BLK.Elements(Blockname).Elements("Output").Elements("TOT_ENTH_REL").Value             
    def BLK_RCSTR_Get_EnthalpyBalanceGenerated(self, Blockname):
        return self.BLK.Elements(Blockname).Elements("Output").Elements("BAL_ENTH_GEN").Value             

#Page 3 Reaction Kinetics:

#Page 4 Component Generation Rates:

#Page 5 Custom Reaction Variables:

#Page 6 Utility Usage: 

#Page 7 Distribution

#Page 8 Polymer Attributes:

#Page 9 Crystallization:

#Page 10 Status:
    def BLK_RCSTR_Get_ConvergenceStatus(self, Blockname):
        return self.BLK.Elements(Blockname).Elements("Output").Elements("BLKSTAT").Value  
    def BLK_RCSTR_Get_ConvergenceMessage(self, Blockname):
        return self.BLK.Elements(Blockname).Elements("Output").Elements("BLKMSG").Value 
    def BLK_RCSTR_Get_PropertyStatus(self, Blockname):
        return self.BLK.Elements(Blockname).Elements("Output").Elements("PROPSTAT").Value 



























    def BLK_RPLUG_GET_OUTPUTS(self, Blockname:str) -> Dict[str, Union[str,float,int]]:
        """Retrieves all Output variables for given Block and returns Dictionary of Values
            
            Args:
                Blockname: String which gives the name of Block.         
        """
        #Page 1
        Heatduty = self.BLK.Elements(Blockname).Elements("Output").Elements("QCALC").Value
        MinimumReactorTemperature = self.BLK.Elements(Blockname).Elements("Output").Elements("TMIN").Value
        MaximumReactorTemperature = self.BLK.Elements(Blockname).Elements("Output").Elements("TMAX").Value
        ResidenceTime = self.BLK.Elements(Blockname).Elements("Output").Elements("RES_TIME").Value
        ThermalFluidInletTemperature = self.BLK.Elements(Blockname).Elements("Output").Elements("COOLANT_TIN").Value
        ThermalFluidInletVaporFraction = self.BLK.Elements(Blockname).Elements("Output").Elements("COOLANT_VIN").Value

        #Page 2
        MoleFlowBalanceIN = self.BLK.Elements(Blockname).Elements("Output").Elements("BAL_MOLI_TFL").Value         
        MoleFlowBalanceOUT = self.BLK.Elements(Blockname).Elements("Output").Elements("BAL_MOLO_TFL").Value      
        MoleFlowBalanceRelDifference = self.BLK.Elements(Blockname).Elements("Output").Elements("BAL_MOLR_TFL").Value     
        MoleFlowBalanceGenerated = self.BLK.Elements(Blockname).Elements("Output").Elements("BAL_MOLG_TFL").Value     
        MassFlowBalanceIN = self.BLK.Elements(Blockname).Elements("Output").Elements("BAL_MASI_TFL").Value          
        MassFlowBalanceOUT = self.BLK.Elements(Blockname).Elements("Output").Elements("BAL_MASO_TFL").Value           
        MassFlowBalanceRelDifference = self.BLK.Elements(Blockname).Elements("Output").Elements("BAL_MASR_TFL").Value             
        MassFlowBalanceGenerated = self.BLK.Elements(Blockname).Elements("Output").Elements("BAL_MASG_TFL").Value    
        EnthalpyBalanceIN = self.BLK.Elements(Blockname).Elements("Output").Elements("TOT_ENTH_ABS").Value 
        EnthalpyBalanceOUT = self.BLK.Elements(Blockname).Elements("Output").Elements("BAL_ENTH_OUT").Value           
        EnthalpyBalanceRelDifference = self.BLK.Elements(Blockname).Elements("Output").Elements("TOT_ENTH_REL").Value             
        EnthalpyBalanceGenerated = self.BLK.Elements(Blockname).Elements("Output").Elements("BAL_ENTH_GEN").Value                        
    
        #Page 7
        ConvergenceStatus = self.BLK.Elements(Blockname).Elements("Output").Elements("BLKSTAT").Value  
        ConvergenceMessage = self.BLK.Elements(Blockname).Elements("Output").Elements("BLKMSG").Value 
        PropertyStatus = self.BLK.Elements(Blockname).Elements("Output").Elements("PROPSTAT").Value 

        Dictionary = {
            "Heatduty":Heatduty,
            "MinimumReactorTemperature":MinimumReactorTemperature,
            "MaximumReactorTemperature":MaximumReactorTemperature,
            "ResidenceTime":ResidenceTime,
            "ThermalFluidInletTemperature":ThermalFluidInletTemperature,
            "ThermalFluidInletVaporFraction":ThermalFluidInletVaporFraction,

            "MoleFlowBalanceIN":MoleFlowBalanceIN,
            "MoleFlowBalanceOUT":MoleFlowBalanceOUT,
            "MoleFlowBalanceRelDifference":MoleFlowBalanceRelDifference,
            "MoleFlowBalanceGenerated":MoleFlowBalanceGenerated,
            "MassFlowBalanceIN":MassFlowBalanceIN,
            "MassFlowBalanceOUT":MassFlowBalanceOUT,
            "MassFlowBalanceRelDifference":MassFlowBalanceRelDifference,
            "MassFlowBalanceGenerated":MassFlowBalanceGenerated,
            "EnthalpyBalanceIN":EnthalpyBalanceIN,
            "EnthalpyBalanceOUT":EnthalpyBalanceOUT,
            "EnthalpyBalanceRelDifference":EnthalpyBalanceRelDifference,
            "EnthalpyBalanceGenerated":EnthalpyBalanceGenerated,

            "ConvergenceStatus":ConvergenceStatus,
            "ConvergenceMessage":ConvergenceMessage,
            "PropertyStatus":PropertyStatus,
        }
        return Dictionary

#RPLUG:
#PAGE 1 Summary:
    def BLK_RPLUG_Get_Heatduty(self,Blockname):
        return self.BLK.Elements(Blockname).Elements("Output").Elements("QCALC").Value
    def BLK_RPLUG_Get_MinimumReactorTemperature(self,Blockname):
        return self.BLK.Elements(Blockname).Elements("Output").Elements("TMIN").Value
    def BLK_RPLUG_Get_MaximumReactorTemperature(self,Blockname):
        return self.BLK.Elements(Blockname).Elements("Output").Elements("TMAX").Value
    def BLK_RPLUG_Get_ResidenceTime(self,Blockname):
        return self.BLK.Elements(Blockname).Elements("Output").Elements("RES_TIME").Value
    def BLK_RPLUG_Get_ThermalFluidInletTemperature(self,Blockname):
        return self.BLK.Elements(Blockname).Elements("Output").Elements("COOLANT_TIN").Value
    def BLK_RPLUG_Get_ThermalFluidInletVaporFraction(self,Blockname):
        return self.BLK.Elements(Blockname).Elements("Output").Elements("COOLANT_VIN").Value

#PAGE 2 Balance:
    def BLK_RPLUG_Get_MoleFlowBalanceIN(self, Blockname):
        return self.BLK.Elements(Blockname).Elements("Output").Elements("BAL_MOLI_TFL").Value         
    def BLK_RPLUG_Get_MoleFlowBalanceOUT(self, Blockname):
        return self.BLK.Elements(Blockname).Elements("Output").Elements("BAL_MOLO_TFL").Value      
    def BLK_RPLUG_Get_MoleFlowBalanceRelDifference(self, Blockname):
        return self.BLK.Elements(Blockname).Elements("Output").Elements("BAL_MOLR_TFL").Value     
    def BLK_RPLUG_Get_MoleFlowBalanceGenerated(self,Blockname):
        return self.BLK.Elements(Blockname).Elements("Output").Elements("BAL_MOLG_TFL").Value     
    def BLK_RPLUG_Get_MassFlowBalanceIN(self, Blockname):
        return self.BLK.Elements(Blockname).Elements("Output").Elements("BAL_MASI_TFL").Value          
    def BLK_RPLUG_Get_MassFlowBalanceOUT(self, Blockname):
        return self.BLK.Elements(Blockname).Elements("Output").Elements("BAL_MASO_TFL").Value           
    def BLK_RPLUG_Get_MassFlowBalanceRelDifference(self, Blockname):
        return self.BLK.Elements(Blockname).Elements("Output").Elements("BAL_MASR_TFL").Value             
    def BLK_RPLUG_Get_MassFlowBalanceGenerated(self, Blockname):
        return self.BLK.Elements(Blockname).Elements("Output").Elements("BAL_MASG_TFL").Value    
    def BLK_RPLUG_Get_EnthalpyBalanceIN(self, Blockname):
        return self.BLK.Elements(Blockname).Elements("Output").Elements("TOT_ENTH").Value          
    def BLK_RPLUG_Get_EnthalpyBalanceOUT(self, Blockname):
        return self.BLK.Elements(Blockname).Elements("Output").Elements("BAL_ENTH_OUT").Value           
    def BLK_RPLUG_Get_EnthalpyBalanceRelDifference(self, Blockname):
        return self.BLK.Elements(Blockname).Elements("Output").Elements("TOT_ENTH_REL").Value             
    def BLK_RPLUG_Get_EnthalpyBalanceGenerated(self, Blockname):
        return self.BLK.Elements(Blockname).Elements("Output").Elements("BAL_ENTH_GEN").Value             


#PAGE 3 Distribution:


#Page 4 Polymer Attributes:


#Page 5 Status:
    def BLK_RPLUG_Get_ConvergenceStatus(self, Blockname):
        return self.BLK.Elements(Blockname).Elements("Output").Elements("BLKSTAT").Value  
    def BLK_RPLUG_Get_ConvergenceMessage(self, Blockname):
        return self.BLK.Elements(Blockname).Elements("Output").Elements("BLKMSG").Value 
    def BLK_RPLUG_Get_PropertyStatus(self, Blockname):
        return self.BLK.Elements(Blockname).Elements("Output").Elements("PROPSTAT").Value 





























    def BLK_RYIELD_GET_OUTPUTS(self, Blockname:str) -> Dict[str, Union[str,float,int]]:
        """Retrieves all Output variables for given Block and returns Dictionary of Values
            
            Args:
                Blockname: String which gives the name of Block.         
        """
        #Page 1
        OutletTemperature =  self.BLK.Elements(Blockname).Elements("Output").Elements("B_TEMP").Value
        OutletPressure = self.BLK.Elements(Blockname).Elements("Output").Elements("B_PRES").Value
        HeatDuty = self.BLK.Elements(Blockname).Elements("Output").Elements("QCALC").Value
        NetHeatDuty = self.BLK.Elements(Blockname).Elements("Output").Elements("QNET").Value
        VaporFraction = self.BLK.Elements(Blockname).Elements("Output").Elements("B_VFRAC").Value
        FirstLiquidbyTotalLiquidFraction = self.BLK.Elements(Blockname).Elements("Output").Elements("LIQ_RATIO").Value    
        #Page 2
        MoleFlowBalanceIN = self.BLK.Elements(Blockname).Elements("Output").Elements("BAL_MOLI_TFL").Value         
        MoleFlowBalanceOUT = self.BLK.Elements(Blockname).Elements("Output").Elements("BAL_MOLO_TFL").Value      
        MoleFlowBalanceRelDifference = self.BLK.Elements(Blockname).Elements("Output").Elements("BAL_MOLR_TFL").Value     
        MoleFlowBalanceGenerated = self.BLK.Elements(Blockname).Elements("Output").Elements("BAL_MOLG_TFL").Value     
        MassFlowBalanceIN = self.BLK.Elements(Blockname).Elements("Output").Elements("BAL_MASI_TFL").Value          
        MassFlowBalanceOUT = self.BLK.Elements(Blockname).Elements("Output").Elements("BAL_MASO_TFL").Value           
        MassFlowBalanceRelDifference = self.BLK.Elements(Blockname).Elements("Output").Elements("BAL_MASR_TFL").Value             
        MassFlowBalanceGenerated = self.BLK.Elements(Blockname).Elements("Output").Elements("BAL_MASG_TFL").Value    
        EnthalpyBalanceIN = self.BLK.Elements(Blockname).Elements("Output").Elements("TOT_ENTH_ABS").Value 
        EnthalpyBalanceOUT = self.BLK.Elements(Blockname).Elements("Output").Elements("BAL_ENTH_OUT").Value           
        EnthalpyBalanceRelDifference = self.BLK.Elements(Blockname).Elements("Output").Elements("TOT_ENTH_REL").Value             
        EnthalpyBalanceGenerated = self.BLK.Elements(Blockname).Elements("Output").Elements("BAL_ENTH_GEN").Value                        
        #Page 3
        CompoundLister = self.BLK.Elements(Blockname).Elements("Output").Elements("F").Elements
        TotalFlowFractionList = []
        LiquidConcentrationList = []
        VaporConcentrationList = []
        EquilibriumConstantList = []
        CompoundNameList = []
        for compound in CompoundLister:
            Compoundname = compound.Name
            TotalFlowFractionList.append(self.BLK.Elements(Blockname).Elements("Output").Elements("F").Elements(Compoundname).Value)
            LiquidConcentrationList.append(self.BLK.Elements(Blockname).Elements("Output").Elements("X").Elements(Compoundname).Value)
            VaporConcentrationList.append(self.BLK.Elements(Blockname).Elements("Output").Elements("Y").Elements(Compoundname).Value)            
            EquilibriumConstantList.append(self.BLK.Elements(Blockname).Elements("Output").Elements("B_K").Elements(Compoundname).Value)      
            CompoundNameList.append(Compoundname)
            
        #Page 7
        ConvergenceStatus = self.BLK.Elements(Blockname).Elements("Output").Elements("BLKSTAT").Value  
        ConvergenceMessage = self.BLK.Elements(Blockname).Elements("Output").Elements("BLKMSG").Value 
        PropertyStatus = self.BLK.Elements(Blockname).Elements("Output").Elements("PROPSTAT").Value 

        Dictionary = {
            "OutletTemperature":OutletTemperature,
            "OutletPressure":OutletPressure,
            "HeatDuty":HeatDuty,
            "NetHeatDuty":NetHeatDuty,
            "VaporFraction":VaporFraction,
            "FirstLiquidbyTotalLiquidFraction":FirstLiquidbyTotalLiquidFraction,

            "MoleFlowBalanceIN":MoleFlowBalanceIN,
            "MoleFlowBalanceOUT":MoleFlowBalanceOUT,
            "MoleFlowBalanceRelDifference":MoleFlowBalanceRelDifference,
            "MoleFlowBalanceGenerated":MoleFlowBalanceGenerated,
            "MassFlowBalanceIN":MassFlowBalanceIN,
            "MassFlowBalanceOUT":MassFlowBalanceOUT,
            "MassFlowBalanceRelDifference":MassFlowBalanceRelDifference,
            "MassFlowBalanceGenerated":MassFlowBalanceGenerated,
            "EnthalpyBalanceIN":EnthalpyBalanceIN,
            "EnthalpyBalanceOUT":EnthalpyBalanceOUT,
            "EnthalpyBalanceRelDifference":EnthalpyBalanceRelDifference,
            "EnthalpyBalanceGenerated":EnthalpyBalanceGenerated,

            "CompoundNameList":CompoundNameList,
            "TotalFlowFractionList":TotalFlowFractionList,
            "LiquidConcentrationList":LiquidConcentrationList,
            "VaporConcentrationList":VaporConcentrationList,
            "EquilibriumConstantList":EquilibriumConstantList,

            "ConvergenceStatus":ConvergenceStatus,
            "ConvergenceMessage":ConvergenceMessage,
            "PropertyStatus":PropertyStatus,
        }
        return Dictionary
   
#RYIELD:

#PAGE 1 Summary:
    def BLK_RYIELD_Get_OutletTemperature(self,Blockname):
        return self.BLK.Elements(Blockname).Elements("Output").Elements("B_TEMP").Value
    def BLK_RYIELD_Get_OutletPressure(self,Blockname):
        return self.BLK.Elements(Blockname).Elements("Output").Elements("B_PRES").Value
    def BLK_RYIELD_Get_HeatDuty(self,Blockname):
        return self.BLK.Elements(Blockname).Elements("Output").Elements("QCALC").Value
    def BLK_RYIELD_Get_NetHeatDuty(self,Blockname):
        return self.BLK.Elements(Blockname).Elements("Output").Elements("QNET").Value
    def BLK_RYIELD_Get_VaporFraction(self,Blockname):
        return self.BLK.Elements(Blockname).Elements("Output").Elements("B_VFRAC").Value
    def BLK_RYIELD_Get_FirstLiquidbyTotalLiquidFraction(self,Blockname):
        return self.BLK.Elements(Blockname).Elements("Output").Elements("LIQ_RATIO").Value

#PAGE 2 Balance:
    def BLK_RYIELD_Get_MoleFlowBalanceIN(self, Blockname):
        return self.BLK.Elements(Blockname).Elements("Output").Elements("BAL_MOLI_TFL").Value         
    def BLK_RYIELD_Get_MoleFlowBalanceOUT(self, Blockname):
        return self.BLK.Elements(Blockname).Elements("Output").Elements("BAL_MOLO_TFL").Value      
    def BLK_RYIELD_Get_MoleFlowBalanceRelDifference(self, Blockname):
        return self.BLK.Elements(Blockname).Elements("Output").Elements("BAL_MOLR_TFL").Value     
    def BLK_RYIELD_Get_MoleFlowBalanceGenerated(self,Blockname):
        return self.BLK.Elements(Blockname).Elements("Output").Elements("BAL_MOLG_TFL").Value     
    def BLK_RYIELD_Get_MassFlowBalanceIN(self, Blockname):
        return self.BLK.Elements(Blockname).Elements("Output").Elements("BAL_MASI_TFL").Value          
    def BLK_RYIELD_Get_MassFlowBalanceOUT(self, Blockname):
        return self.BLK.Elements(Blockname).Elements("Output").Elements("BAL_MASO_TFL").Value           
    def BLK_RYIELD_Get_MassFlowBalanceRelDifference(self, Blockname):
        return self.BLK.Elements(Blockname).Elements("Output").Elements("BAL_MASR_TFL").Value             
    def BLK_RYIELD_Get_MassFlowBalanceGenerated(self, Blockname):
        return self.BLK.Elements(Blockname).Elements("Output").Elements("BAL_MASG_TFL").Value    
    def BLK_RYIELD_Get_EnthalpyBalanceIN(self, Blockname):
        return self.BLK.Elements(Blockname).Elements("Output").Elements("TOT_ENTH").Value          
    def BLK_RYIELD_Get_EnthalpyBalanceOUT(self, Blockname):
        return self.BLK.Elements(Blockname).Elements("Output").Elements("BAL_ENTH_OUT").Value           
    def BLK_RYIELD_Get_EnthalpyBalanceRelDifference(self, Blockname):
        return self.BLK.Elements(Blockname).Elements("Output").Elements("TOT_ENTH_REL").Value             
    def BLK_RYIELD_Get_EnthalpyBalanceGenerated(self, Blockname):
        return self.BLK.Elements(Blockname).Elements("Output").Elements("BAL_ENTH_GEN").Value             

#PAGE 3 Phase Equilibrium
    def BLK_RYIELD_Get_TotalFlowFraction(self, Blockname, Compoundname):
        return self.BLK.Elements(Blockname).Elements("Output").Elements("F").Elements(Compoundname).Value             
    def BLK_RYIELD_Get_Liquidconcentrations(self, Blockname, Compoundname):
        return self.BLK.Elements(Blockname).Elements("Output").Elements("X").Elements(Compoundname).Value              
    def BLK_RYIELD_Get_Vaporconcentrations(self, Blockname, Compoundname):
        return self.BLK.Elements(Blockname).Elements("Output").Elements("Y").Elements(Compoundname).Value             
    def BLK_RYIELD_Get_EquilibriumConstant(self, Blockname, Compoundname):
        return self.BLK.Elements(Blockname).Elements("Output").Elements("B_K").Elements(Compoundname).Value            

#PAGE 4 Weight distribution

#Page 5 Pseudocomp Breakdown:

#Page 6 Utility usage:

#Page 7 Status
    def BLK_RYIELD_Get_ConvergenceStatus(self, Blockname):
        return self.BLK.Elements(Blockname).Elements("Output").Elements("BLKSTAT").Value  
    def BLK_RYIELD_Get_ConvergenceMessage(self, Blockname):
        return self.BLK.Elements(Blockname).Elements("Output").Elements("BLKMSG").Value 
    def BLK_RYIELD_Get_PropertyStatus(self, Blockname):
        return self.BLK.Elements(Blockname).Elements("Output").Elements("PROPSTAT").Value 
















































    def BLK_FSPLITTER_GET_OUTPUTS(self, Blockname:str) -> Dict[str, Union[str,float,int]]:
        """Retrieves all Output variables for given Block and returns Dictionary of Values
            
            Args:
                Blockname: String which gives the name of Block.         
        """
        SplitFractionElementList = self.BLK.Elements(Blockname).Elements("Output").Elements("STREAMFRAC").Element
        SplitFractionList = []
        StreamOrderList = []
        CompoundNameList = []
        for compound in SplitFractionElementList:
            Compoundname = compound.Name
            SplitFractionList.append(self.BLK.Elements(Blockname).Elements("Output").Elements("STREAMFRAC").Elements(Compoundname).Value)
            StreamOrderList.append(self.BLK.Elements(Blockname).Elements("Output").Elements("STREAM_ORDER").Elements(Compoundname).Value)
            CompoundNameList.append(Compoundname)
        
        MoleFlowBalanceIN = self.BLK.Elements(Blockname).Elements("Output").Elements("BAL_MOLI_TFL").Value              
        MoleFlowBalanceOUT = self.BLK.Elements(Blockname).Elements("Output").Elements("BAL_MOLO_TFL").Value        
        MoleFlowBalanceRelDifference = self.BLK.Elements(Blockname).Elements("Output").Elements("BAL_MOLR_TFL").Value        
        MassFlowBalanceIN = self.BLK.Elements(Blockname).Elements("Output").Elements("BAL_MASI_TFL").Value              
        MassFlowBalanceOUT = self.BLK.Elements(Blockname).Elements("Output").Elements("BAL_MASO_TFL").Value              
        MassFlowBalanceRelDifference = self.BLK.Elements(Blockname).Elements("Output").Elements("BAL_MASR_TFL").Value              
        EnthalpyBalanceIN = self.BLK.Elements(Blockname).Elements("Output").Elements("TOT_ENTH_ABS").Value              
        EnthalpyBalanceOUT = self.BLK.Elements(Blockname).Elements("Output").Elements("BAL_ENTH_OUT").Value              
        EnthalpyBalanceRelDifference = self.BLK.Elements(Blockname).Elements("Output").Elements("TOT_ENTH_REL").Value   

        ConvergenceStatus = self.BLK.Elements(Blockname).Elements("Output").Elements("BLKSTAT").Value 
        ConvergenceMessage = self.BLK.Elements(Blockname).Elements("Output").Elements("BLKMSG").Value 
        PropertyStatus = self.BLK.Elements(Blockname).Elements("Output").Elements("PROPSTAT").Value

        Dictionary = {
            "CompoundNameList":CompoundNameList,
            "SplitFractionList":SplitFractionList,
            "StreamOrderList":StreamOrderList,

            "MoleFlowBalanceIN":MoleFlowBalanceIN,
            "MoleFlowBalanceOUT":MoleFlowBalanceOUT,
            "MoleFlowBalanceRelDifference":MoleFlowBalanceRelDifference,
            "MassFlowBalanceIN":MassFlowBalanceIN,
            "MassFlowBalanceOUT":MassFlowBalanceOUT,
            "MassFlowBalanceRelDifference":MassFlowBalanceRelDifference,
            "EnthalpyBalanceIN":EnthalpyBalanceIN,
            "EnthalpyBalanceOUT":EnthalpyBalanceOUT,
            "EnthalpyBalanceRelDifference":EnthalpyBalanceRelDifference,

            "ConvergenceStatus":ConvergenceStatus,
            "ConvergenceMessage":ConvergenceMessage,        
            "PropertyStatus":PropertyStatus,
        }
        return Dictionary

#SPLITTER
#  PAGE 1 Summary
    def BLK_FSPLITTER_Get_SplitFraction(self, Blockname, Streamname):
        return self.BLK.Elements(Blockname).Elements("Output").Elements("STREAMFRAC").Element(Streamname).Value
    def BLK_FSPLITTER_Get_StreamOrder(self, Blockname, Streamname):
        return self.BLK.Elements(Blockname).Elements("Output").Elements("STREAM_ORDER").Element(Streamname).Value

#Page 2: Balance
    def BLK_FSPLITTER_Get_MoleFlowBalanceIN(self, Blockname):
        return self.BLK.Elements(Blockname).Elements("Output").Elements("BAL_MOLI_TFL").Value         
    def BLK_FSPLITTER_Get_MoleFlowBalanceOUT(self, Blockname):
        return self.BLK.Elements(Blockname).Elements("Output").Elements("BAL_MOLO_TFL").Value      
    def BLK_FSPLITTER_Get_MoleFlowBalanceRelDifference(self, Blockname):
        return self.BLK.Elements(Blockname).Elements("Output").Elements("BAL_MOLR_TFL").Value     
    def BLK_FSPLITTER_Get_MassFlowBalanceIN(self, Blockname):
        return self.BLK.Elements(Blockname).Elements("Output").Elements("BAL_MASI_TFL").Value          
    def BLK_FSPLITTER_Get_MassFlowBalanceOUT(self, Blockname):
        return self.BLK.Elements(Blockname).Elements("Output").Elements("BAL_MASO_TFL").Value           
    def BLK_FSPLITTER_Get_MassFlowBalanceRelDifference(self, Blockname):
        return self.BLK.Elements(Blockname).Elements("Output").Elements("BAL_MASR_TFL").Value             
    def BLK_FSPLITTER_Get_EnthalpyBalanceIN(self, Blockname):
        return self.BLK.Elements(Blockname).Elements("Output").Elements("TOT_ENTH").Value          
    def BLK_FSPLITTER_Get_EnthalpyBalanceOUT(self, Blockname):
        return self.BLK.Elements(Blockname).Elements("Output").Elements("BAL_ENTH_OUT").Value           
    def BLK_FSPLITTER_Get_EnthalpyBalanceRelDifference(self, Blockname):
        return self.BLK.Elements(Blockname).Elements("Output").Elements("TOT_ENTH_REL").Value             


#Page 3 Status:
    def BLK_FSPLITTER_Get_ConvergenceStatus(self, Blockname):
        return self.BLK.Elements(Blockname).Elements("Output").Elements("BLKSTAT").Value  
    def BLK_FSPLITTER_Get_ConvergenceMessage(self, Blockname):
        return self.BLK.Elements(Blockname).Elements("Output").Elements("BLKMSG").Value 
    def BLK_FSPLITTER_Get_PropertyStatus(self, Blockname):
        return self.BLK.Elements(Blockname).Elements("Output").Elements("PROPSTAT").Value 





























#Outputs for Streams

    def STRM_GET_OUTPUTS(self, Streamname:str) -> Dict[str, Union[str,float,int]]:
        """Retrieves all Output variables for given Block and returns Dictionary of Values
            
            Args:
                Blockname: String which gives the name of Block.         
        """
        Compoundlist = self.STRM.Elements(Streamname).Elements("Output").Elements("MOLEFRAC").Elements("MIXED").Elements
        CompoundNameList = []
        MoleFlowList = []
        MassFlowList = []
        MoleFracList = []
        MassFracList = []
        LiquidConcentrationList = []
        VaporConcentrationList = []
        
        for compound in Compoundlist:
            Compoundname = compound.Name
            CompoundNameList.append(Compoundname)
            MoleFlowList.append(self.STRM.Elements(Streamname).Elements("Output").Elements("STR_MAIN").Elements("MOLEFLOW").Elements("MIXED").Elements(Compoundname).Value)
            MassFlowList.append(self.STRM.Elements(Streamname).Elements("Output").Elements("STR_MAIN").Elements("MASSFLOW").Elements("MIXED").Elements(Compoundname).Value)
            MoleFracList.append(self.STRM.Elements(Streamname).Elements("Output").Elements("MOLEFRAC").Elements("MIXED").Elements(Compoundname).Value)
            MassFracList.append(self.STRM.Elements(Streamname).Elements("Output").Elements("MASSFRAC").Elements("MIXED").Elements(Compoundname).Value)
            LiquidConcentrationList.append(self.STRM.Elements(Streamname).Elements("Output").Elements("X").Elements(Compoundname).Value)
            VaporConcentrationList.append(self.STRM.Elements(Streamname).Elements("Output").Elements("Y").Elements(Compoundname).Value)

        Source = self.STRM.Elements(Streamname).Elements("Output").Elements("STR_MAIN").Elements("SOURCE").Value 
        Destination = self.STRM.Elements(Streamname).Elements("Output").Elements("STR_MAIN").Elements("DESTINATION").Value 
        Phase = self.STRM.Elements(Streamname).Elements("Output").Elements("STR_MAIN").Elements("COMPTYPE").Value 
        PropertySet = self.STRM.Elements(Streamname).Elements("Output").Elements("STR_MAIN").Elements("PPOPSET").Value 
        VolumeFlow =  self.STRM.Elements(Streamname).Elements("Output").Elements("STR_MAIN").Elements("VOLFLMX").Elements("MIXED").Value 
        
        VaporFraction = self.STRM.Elements(Streamname).Elements("Output").Elements("STR_MAIN").Elements("VFRAC").Value 
        LiquidFraction = self.STRM.Elements(Streamname).Elements("Output").Elements("STR_MAIN").Elements("LFRAC").Value 
        SolidFraction = self.STRM.Elements(Streamname).Elements("Output").Elements("STR_MAIN").Elements("SFRAC").Value 
    
        Dictionary = {
            "Source":Source,
            "Destination":Destination,
            "Phase":Phase,
            "PropertySet":PropertySet,
            "VolumeFlow":VolumeFlow,
            
            "CompoundNameList":CompoundNameList,
            "MoleFlowList":MoleFlowList,
            "MassFlowList":MassFlowList,
            "MoleFracList":MoleFracList,
            "MassFracList":MassFracList,
            "LiquidConcentrationList":LiquidConcentrationList,
            "VaporConcentrationList":VaporConcentrationList,

            "VaporFraction":VaporFraction,
            "LiquidFraction":LiquidFraction,        
            "SolidFraction":SolidFraction,
        }
        return Dictionary




    def STRM_Get_Source(self, Streamname):
        return self.STRM.Elements(Streamname).Elements("Output").Elements("STR_MAIN").Elements("SOURCE").Value 
    def STRM_Get_Destination(self, Streamname):
        return self.STRM.Elements(Streamname).Elements("Output").Elements("STR_MAIN").Elements("DESTINATION").Value 
    def STRM_Get_Phase(self, Streamname):
        return self.STRM.Elements(Streamname).Elements("Output").Elements("STR_MAIN").Elements("COMPTYPE").Value 
    def STRM_Get_PropertySet(self, Streamname):
        return self.STRM.Elements(Streamname).Elements("Output").Elements("STR_MAIN").Elements("PROPSET").Value 
    
    def STRM_Get_MoleFlowPerCompound(self, Streamname, Compoundname):
        return self.STRM.Elements(Streamname).Elements("Output").Elements("STR_MAIN").Elements("MOLEFLOW").Elements("MIXED").Elements(Compoundname).Value 
    def STRM_Get_MassFlowPerCompound(self, Streamname, Compoundname):
        return self.STRM.Elements(Streamname).Elements("Output").Elements("STR_MAIN").Elements("MASSFLOW").Elements("MIXED").Elements(Compoundname).Value 
    def STRM_Get_VolumeFlow(self, Streamname):
        return self.STRM.Elements(Streamname).Elements("Output").Elements("STR_MAIN").Elements("VOLFLMX").Elements("MIXED").Value 
    def STRM_Get_Temperature(self, Streamname):
        return self.STRM.Elements(Streamname).Elements("Output").Elements("STR_MAIN").Elements("TEMP").Elements("MIXED").Value 
    def STRM_Get_Pressure(self, Streamname):
        return self.STRM.Elements(Streamname).Elements("Output").Elements("STR_MAIN").Elements("PRES").Elements("MIXED").Value 
    def STRM_Get_MoleFracPerCompound(self, Streamname, Compoundname):
        return self.STRM.Elements(Streamname).Elements("Output").Elements("MOLEFRAC").Elements("MIXED").Elements(Compoundname).Value 
    def STRM_Get_MassFracPerCompound(self, Streamname, Compoundname):
        return self.STRM.Elements(Streamname).Elements("Output").Elements("MASSFRAC").Elements("MIXED").Elements(Compoundname).Value 
    def STRM_Get_LiquidConcentrationPerCompound(self, Streamname, Compoundname):
        return self.STRM.Elements(Streamname).Elements("Output").Elements("X").Elements(Compoundname).Value 
    def STRM_Get_VaporConcentrationPerCompound(self, Streamname, Compoundname):
        return self.STRM.Elements(Streamname).Elements("Output").Elements("Y").Elements(Compoundname).Value 
    def STRM_Get_VaporFraction(self, Streamname):
        return self.STRM.Elements(Streamname).Elements("Output").Elements("STR_MAIN").Elements("VFRAC").Value 
    def STRM_Get_LiquidFraction(self, Streamname):
        return self.STRM.Elements(Streamname).Elements("Output").Elements("STR_MAIN").Elements("LFRAC").Value 
    def STRM_Get_SolidFraction(self, Streamname):
        return self.STRM.Elements(Streamname).Elements("Output").Elements("STR_MAIN").Elements("SFRAC").Value 
    



































############################################################################################################################################3


###############     H           H       RRRRRRRRRR      II     SSSSSSSSSSS
##                  H           H       R        R      II     S
#                   H           H       R       R       II     S
#                   HHHHHHHHHHHHH       RRRRRRRRR       II     SSSSSSSSSSS
#                   H           H       R   R           II               S
#                   H           H       R      R        II               S
###############     H           H       R          R    II    SSSSSSSSSSSS


############################################################################################################################################
    def STRM_Get_Outputs(self, Streamname, Chemical):
        STRM_COMP = self.STRM.Elements(Streamname).Elements("Output").Elements("MOLEFLOW").Elements("MIXED")
        COMP_1 = STRM_COMP.Elements(Chemical).Value
        return COMP_1

    def STRM_Get_Temperature(self, Streamname):
        return self.STRM.Elements(Streamname).Elements("Output").Elements("TEMP_OUT").Elements("MIXED").Value

    def STRM_Get_Pressure(self, Streamname):
        return self.STRM.Elements(Streamname).Elements("Output").Elements("PRES_OUT").Elements("MIXED").Value



    def BLK_Get_NStages(self,Blockname):
        return self.BLK.Elements(Blockname).Elements("Input").Elements("NSTAGE").Value

    def BLK_Get_FeedLocation(self, Blockname, Name):
        return self.BLK.Elements(Blockname).Elements("Input").Elements("FEED_STAGE").Elements(Name).Value

    def BLK_Get_Pressure(self,Blockname):
        return self.BLK.Elements(Blockname).Elements("Input").Elements("PRES1").Value

    def BLK_Get_RefluxRatio(self,Blockname):
        return self.BLK.Elements(Blockname).Elements("Input").Elements("BASIS_RR").Value

    def BLK_Get_ReboilerRatio(self,Blockname):
        return self.BLK.Elements(Blockname).Elements("Input").Elements("BASIS_BR").Value

    def BLK_Get_Condenser_Duty(self,Blockname):
        return self.BLK.Elements().Elements("Output").Elements("COND_DUTY").Value

    def BLK_Get_Reboiler_Duty(self,Blockname):
        return self.BLK.Elements(Blockname).Elements("Output").Elements("REB_DUTY").Value

    def BLK_Get_Column_Stage_Molar_Weights(self,Blockname):
        N_stages = self.BLK.Elements(Blockname).Elements("Input").Elements("NSTAGE").Value
        M = []
        for i in range(1, N_stages + 1):
            M += [self.BLK.Elements(Blockname).Elements("Output").Elements("MW_GAS").Elements(str(i)).Value]
        return M

    def BLK_Get_Column_Stage_Temperatures(self,Blockname):
        N_stages = self.BLK.Elements(Blockname).Elements("Input").Elements("NSTAGE").Value
        T = []
        for i in range(1, N_stages + 1):
            T += [self.BLK.Elements(Blockname).Elements("Output").Elements("B_TEMP").Elements(str(i)).Value]
        return T

    def BLK_Get_Column_Stage_Vapor_Flows(self,Blockname):
        N_stages = self.BLK.Elements(Blockname).Elements("Input").Elements("NSTAGE").Value
        V = []
        for i in range(1, N_stages + 1):
            V += [self.BLK.Elements(Blockname).Elements("Output").Elements("VAP_FLOW").Elements(str(i)).Value]
        return V

    def dummy_Run(self):
        start = time.time()
        self.AspenSimulation.Engine.Run2()
        print(f"Dummy = {time.time() - start}")

    def Run(self) -> bool:
        """Runs simulation, if there is a problem it will rerun twice, returns boolian about successful convergence"""
        tries = 0
        converged = 0
        #iterations = 10
        #self.BLK.Elements("B1").Elements("Input").Elements("MAXOL").Value = iterations

        while tries != 2:
            start = time.time()
            self.AspenSimulation.Engine.Run2()
            print(f"Runtime = {time.time() - start}")
            # print(time.time() - start)
            converged = self.AspenSimulation.Tree.Elements("Data").Elements("Results Summary").Elements(
                           "Run-Status").Elements("Output").Elements("PER_ERROR").Value
            if converged == 0:
                converged = True
                break
            elif converged == 1:
                tries += 1
                converged = False
        return converged


    def CAL_Column_Diameter(self, pressure, n_stages, vapor_flows, stage_mw, stage_temp):
        P = pressure
        f = float(1.6)
        R = float(8.314)
        Effective_Diameter = []

        for i in range(0, n_stages - 1):
            Effective_Diameter += [np.sqrt((4 * vapor_flows[i]) / (3.1416 * f) * np.sqrt(
                R * (stage_temp[i] + 273.15) * stage_mw[i] * 1000 / (P * 1e5)))]

        Diameter = 1.1 * max(Effective_Diameter)
        return Diameter

    def CAL_Column_Height(self, n_stages):
        HETP = 0.5  # HETP constant [m]
        H_0 = 0.4  # Clearance [m]
        return n_stages * HETP + H_0

    def CAL_LMTD(self, tops_temperature):
        T_cool_in = 30  # Supply temperature of cooling water [oC]
        T_cool_out = 40  # Return temperature of cooling water [oC]
        delta_Tm_cnd = (((tops_temperature - T_cool_in) * (tops_temperature - T_cool_out) * (
                (tops_temperature - T_cool_in) + (tops_temperature - T_cool_out)) / 2) ** (1 / 3))
        return delta_Tm_cnd.real

    def CAL_HT_Condenser_Area(self, condenser_duty, tops_temperature):
        K_cnd = 500  # Heat transfer coefficient [W/m2 K]
        delta_Tm_cnd = self.CAL_LMTD(tops_temperature)
        A_cnd = -condenser_duty / (K_cnd * delta_Tm_cnd)
        return A_cnd

    def CAL_HT_Reboiler_Area(self, reboiler_temperature, reboiler_duty):
        K_rbl = 800  # Heat transfer coefficient [W/m2*K] (800, fixed)
        T_steam = 201  # Temperature of 16 bar steam [°C] (201, fixed)
        delta_tm_rbl = T_steam - reboiler_temperature
        A_rbl = reboiler_duty / (K_rbl * delta_tm_rbl)
        return A_rbl

    def CAL_InvestmentCost(self, pressure, n_stages, condenser_duty, reboiler_temperature, reboiler_duty,
                           tops_temperature, vapor_flows, stage_mw, stage_temp):
        # Define in Column Specifications
        L = self.CAL_Column_Height(n_stages)  # Column length [m]
        D = self.CAL_Column_Diameter(pressure, n_stages, vapor_flows, stage_mw, stage_temp)  # Column diameter [m]
        A_cnd = self.CAL_HT_Condenser_Area(condenser_duty, tops_temperature)  # Heat transfer area of condenser [m2]
        A_rbl = self.CAL_HT_Reboiler_Area(reboiler_temperature, reboiler_duty)  # Heat transfer area of reboiler [m2]
        # Predefined values.
        F_m = 1  # Correction factor for column shell material (1.0, fixed)
        F_p = 1  # Correction factor for column pressure (1.0, fixed)
        F_int_m = 0  # Correction factor for internals material [-] (0.0, fixed)
        F_int_t = 0  # Correction factor for tray type [-] (0.0, fixed)
        F_int_s = 1.4  # Correction factor for tray spacing [-] (1.4, fixed)
        F_htx_d = 0.8  # Correction factor for design type: fixed-tube sheet [-] (0.8, fixed)
        F_htx_p = 0  # Correction factor for pressure [-] (0.0, fixed)
        F_htx_m = 1  # Correction factor for material [-] (1.0, fixed)
        M_S = 1638.2  # Marshall & Swift equipment index 2018 (1638.2, fixed)
        F_c = F_m + F_p
        F_int_c = F_int_s + F_int_t + F_int_m
        F_cnd_c = (F_htx_d + F_htx_p) * F_htx_m
        F_rbl_c = (F_htx_d + F_htx_p) * F_htx_m
        C_col = 0.9 * (M_S / 280) * 937.64 * D ** 1.066 * L ** 0.802 * F_c
        C_int = 0.9 * (M_S / 280) * 97.24 * D ** 1.55 * L * F_int_c
        C_cnd = 0.9 * (M_S / 280) * 474.67 * A_cnd ** 0.65 * F_cnd_c
        C_rbl = 0.9 * (M_S / 280) * 474.67 * A_rbl ** 0.65 * F_rbl_c
        C_eqp = (C_col + C_int + C_cnd + C_rbl) / 1000
        F_cap = 0.2  # Capital charge factor (0.2, fixed)
        F_L = 5  # Lang factor (5, fixed)
        C_inv = F_L * C_eqp
        InvestmentCost = F_cap * C_inv
        return InvestmentCost



    def CAL_OperatingCost(self, reboiler_duty, condenser_duty):
        M = 18  # Molar weight of water [g/mol] (18, fixed)
        c_steam = 18  # Steam price [€/t] (18, fixed)
        c_cw = 0.006  # Cooling water price [€/t] (0.006, fixed)
        delta_hv = 34794  # Molar heat of condensation of 16 bar steam [J/mol] (34794, fixed)
        c_p = 4.2  # Heat capacity of water [kJ/(kg*K)] (4.2, fixed)
        T_cool_in = 30  # Supply cooling water temperature [°C] (30, fixed)
        T_cool_out = 40  # Return cooling water temperature [°C] (40, fixed)
        C_op_rbl = reboiler_duty / 1000000 * M * c_steam * 3600 / delta_hv  # €/h
        C_op_cnd = condenser_duty / 1000000 * c_cw * 3600 / (c_p * (T_cool_out - T_cool_in))  # €/h
        C_op = C_op_rbl + C_op_cnd
        return C_op

    def CAL_Annual_OperatingCost(self, reboiler_duty, condenser_duty):
        t_a = 8400
        OperatingCost = self.CAL_OperatingCost(reboiler_duty, condenser_duty) * t_a / 1000
        return OperatingCost





    def CAL_stream_value(self, MoleFlowList,
                         product_specification = 0.95):  # , component_specifications, molar_flows, stream_component_specifications):
        """Calculates the value (per year) of a stream."""

        up_time = 8400 * 3600  # seconds per year, assuming 8400 hours of uptime
        is_purity, component_purities = self.CAL_purity_check(MoleFlowList, product_specification)

        component_specifications = {
            'ethane': {'index': 0, 'molar weight': 30.07, 'price': 125.0 * 0.91, 'mass flow': 0, 'stream value': 0},
            'propane': {'index': 1, 'molar weight': 44.1, 'price': 204.0 * 0.91, 'mass flow': 0, 'stream value': 0},
            'isobutane': {'index': 2, 'molar weight': 58.12, 'price': 272.0 * 0.91, 'mass flow': 0, 'stream value': 0},
            'n_butane': {'index': 3, 'molar weight': 58.12, 'price': 249.0 * 0.91, 'mass flow': 0, 'stream value': 0},
            'isopentane': {'index': 4, 'molar weight': 72.15, 'price': 545.0 * 0.91, 'mass flow': 0, 'stream value': 0},
            'n_pentane': {'index': 5, 'molar weight': 72.15, 'price': 545.0 * 0.91, 'mass flow': 0, 'stream value': 0}
        }  # molar weight = g/mol, price = $/ton *0.91 (exchange rate @ 24-03-2022), mass flow = ton/h, stream value = euro/year
        
        

        for entry in component_specifications:
            if sum(is_purity) > 0:
                component_specifications[entry]['mass flow'] = MoleFlowList[
                                                                   component_specifications[entry]['index']] * \
                                                               component_specifications[entry][
                                                                   'molar weight'] / 1000 * up_time  # ton/year
                component_specifications[entry]['stream value'] = is_purity[component_specifications[entry]['index']] * \
                                                                  component_specifications[entry]['price'] * \
                                                                  component_specifications[entry][
                                                                      'mass flow']  # euro/year
            elif sum(is_purity) == 0:
                component_specifications[entry]['stream value'] = 0

        total_stream_value = sum(d['stream value'] for d in component_specifications.values() if d)

        return total_stream_value, component_purities

    def CAL_purity_check(self, MoleFlowList, product_specification = 0.95):
        # , component_specifications, molar_flows, stream_component_specifications):

        molar_flows = MoleFlowList
        is_purity = np.zeros(len(molar_flows), dtype=int)
        component_purities = np.zeros(len(molar_flows))
        total_flow = sum(molar_flows)

        for entry in range(0, len(molar_flows)):
            component_purities[entry] = molar_flows[entry] / total_flow
            if component_purities[entry] >= product_specification:
                is_purity[entry] = 1
            elif component_purities[entry] < product_specification:
                is_purity[entry] = 0

        return is_purity, component_purities
        




    def running_mean(x, N):
        cumsum = np.cumsum(np.insert(x, 0, 0)) 
        return (cumsum[N:] - cumsum[:-N]) / float(N)







    def print_dictionary2(self, dct):
        """ Takes Dictionary input with two items inside and prints them"""
        print("Items held:")
        for key, value in dct.items():
            print(key, value)



    def print_dictionary(self, dct):
        """ Takes Dictionary input with two items inside and prints them"""
        print("Items held:")
        for item, amount in dct.items():  # dct.iteritems() in Python 2
            print("{} ({})".format(item, amount))









