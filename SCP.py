# A toy supply chain problem
# data
fixedCost = [120,150,135]
unitCapCost = [40,50,65]
unitTransportCost = [[10,20,15, 16,17], 
                     [5,17,18,15,15], 
                     [13,15,18,15,16]]
demand = [220,150,175,190,240]
maxAllowCapacity = [540,510,600]
# constants
numFacility = len(fixedCost)
numCustomer = len(demand)
# sets
setFacility = range(numFacility)
setCustomer = range(numCustomer)
from gurobipy import GRB,Model
# instantiate the model
SCP = Model("Supply Chain Problem")
# variables
_locate = SCP.addVars(numFacility, vtype=GRB.BINARY, name="y")
_allowCapacity = SCP.addVars(numFacility, name="z")
_transport = SCP.addVars(numFacility, numCustomer, name="x")
# first constraint
for i in setFacility:
    SCP.addConstr(_allowCapacity[i] <= maxAllowCapacity[i] * _locate[i])
# second constraint
for i in setFacility:
    SCP.addConstr(sum(_transport[i,j] for j in setCustomer) <= _allowCapacity[i])
# third constraint
for j in setCustomer:
    SCP.addConstr(sum(_transport[i,j] for i in setFacility) >= demand[i])
    # objective
SCP.setObjective(sum(fixedCost[i]*_locate[i] for i in setFacility) + 
                 sum(unitCapCost[i]*_allowCapacity[i] for i in setFacility) + 
                 sum(unitTransportCost[i][j]*_transport[i,j] for i in setFacility for j in setCustomer) ,
                 GRB.MINIMIZE)
# solve!
SCP.optimize()
status = SCP.status
if status == GRB.OPTIMAL:
    print("the objective is: ",SCP.objVal)
SCP.getAttr('X',_transport)
