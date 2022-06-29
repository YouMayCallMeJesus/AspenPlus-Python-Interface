# AspenPythonInterface
Aspen Plus to Python interface for the automation of the process synthesis. This API can be used for most equipment inside of the Aspen Plus system. The library consists of around 5000 lines of code which are made up of many smaller functions which each are able to set or get some value in the aspen plus user interface. It is based on the automation server which aspen plus has implemented together with the variable manager. Please read the documentation report if you plan to work with it.



Capabilities:
- Editing flowsheets
- Creating new flowsheet parts
- Setting values in equipment
- running simulations
- exporting results from simulations
- using optimization algorithms to optimize flowsheet


Applications:
- [Bachelorthesis](https://github.com/YouMayCallMeJesus/ReinforcementlearningWithDestillationColumns): Reinforcement learning approach to solve Destillation column sequencing (terrible code!! not worth reading or using) for the improved version go to: [CHRIS](https://github.com/ADChristos/Aspen-RL) or [MIGLEY](https://github.com/lollcat/Aspen-RL)
- Case 1: Varying stagenumber in Destillation column to optimize energy usage
- Case 2: applying genetic algorithm to optimize TAC for destillation column sequence
- Almost all automated optimizations for the design of Aspen Plus programs can be done here since most variables are included in this library.



Equipment included:    (input&output function for each page)
- Streams
- DSTWU
- Flash2
- Radfrac
- Heater
- Mixer
- RPLUG
- RCSTR
- RYIELD



Future implementations:
- Cost analysis for everything (aka combining [this](https://github.com/weepctxb/ChemEngDPpy) sizing and costing library with my library)



Concerning licences and the freedom to use it: You are welcome to use it for any project you have. If you start making significant money with it please email me. For academic research you are ofcourse welcome to use it but please cite me.
If you have a problem with something or any questions send me a email: Richardxtenxhagen@gmail.com



Other peoples work which is in a similar area as this one:
https://github.com/edgarsmdn/Aspen_HYSYS_Python
https://github.com/Shen-SJ/pyAspenPlus/tree/main/pyAspenPlus
https://towardsdatascience.com/automated-aspen-hysys-modelling-4c5187563167

