from pyomo.environ import *


def _constraint_set_x_to_zero_based_on_est(model: ConcreteModel, i: Any, j: Any) -> Constraint:
    """
    Sets to 0 variable X from n = 0 to n = est[i,j] - 1.

    Args:
        - model (ConcreteModel): a Pyomo model instance.
        - i (Any): task index (should belong to production tasks set).
        - j (Any): unit index (should be capable of executing task i).

    Returns:
        Constraint: a constraint enforcing X = 0 for time points before est[i,j} or Constraint.Skip if conditions are not met.
    """
    
    if (
        i in model.S_I_Production_Tasks and 
        j in model.S_J_Executing_I[i] and 
        (i,j) in model.P_Task_Unit_Network and 
        model.P_EST_Task[i,j] > 0 and
        model.P_EST_Task[i,j] <= len(model.S_Time)
    ):
        return sum(
            model.V_X[i,j,n] 
            for n in model.S_Time 
            if 0 <= n <= (model.P_EST_Task[i,j] - 1)
        ) == 0
    else:
        return Constraint.Skip


def _constraint_set_ys_to_zero_based_on_est(model: ConcreteModel, i: Any, j: Any) -> Constraint:
    """
    Sets to 0 variable YS from n = 0 to n = est[i,j] - 1.

    Args:
        - model (ConcreteModel): a Pyomo model instance.
        - i (Any): task index (should belong to production tasks set).
        - j (Any): unit index (should be capable of executing task i).

    Returns:
        Constraint: a constraint enforcing YS = 0 for time points before est[i,j} or Constraint.Skip if conditions are not met.
    """
    
    if (
        i in model.S_I_Production_Tasks and 
        j in model.S_J_Executing_I[i] and 
        (i,j) in model.P_Task_Unit_Network and 
        model.P_EST_Task[i,j] > 0 and
        model.P_EST_Task[i,j] <= len(model.S_Time)
    ):
        return sum(
            model.V_Y_Start[i,j,n] 
            for n in model.S_Time 
            if 0 <= n <= (model.P_EST_Task[i,j] - 1)
        ) == 0
    else:
        return Constraint.Skip


def _constraint_ub_ys_task_ppc(model: ConcreteModel, i: Any, j: Any) -> Constraint:
    """
    Defines an upper bound on the number of startups (YS) for task i. 
    
    Args:
        - model (ConcreteModel): a Pyomo model instance.
        - i (Any): task index (should belong to production tasks set).
        - j (Any): unit index (should be capable of executing task i).

    Returns:
        Constraint: a constraint upper bounding YS or Constraint.Skip if conditions are not met.
    """
    
    if (
        i in model.S_I_Production_Tasks and 
        j in model.S_J_Executing_I[i] and 
        (i,j) in model.P_Task_Unit_Network and
        model.P_EST_Task[i,j] > 0 and
        model.P_EST_Task[i,j] <= len(model.S_Time)
    ):
        return sum(
            model.V_Y_Start[i,j,n] 
            for n in model.S_Time 
            if n >= model.P_EST_Task[i,j]
        ) <= model.P_UB_YS_Task_PPC[i,j]
    else:
        return Constraint.Skip    


def _constraint_ub_ys_unit_opt(model: ConcreteModel, j: Any) -> Constraint:
    """
    Defines an upper bound on the number of runs that can start in a unit (var Y_S[i,j,n]). 
    model.P_UB_YS_Unit_OPT[j] is calculated by solving a knapsack problem.

    Args:
        - model (ConcreteModel): a Pyomo model instance.
        - j (Any): unit index (should be capable of executing task i).

    Returns:
        Constraint: a constraint bounding Y_S[i,j,n] in a unit or Constraint.Skip if conditions are not met.
    """
    
    if (
        model.P_EST_Unit[j] <= len(model.S_Time) and
        model.P_EST_Unit[j] > 0
    ):
        
        return sum(
            model.V_Y_Start[i,j,n] 
            for i in model.S_I_Production_Tasks 
            if (i,j) in model.P_Task_Unit_Network 
            for n in model.S_Time 
            if n >= model.P_EST_Task[i,j]
        ) <= model.P_UB_YS_Unit_OPT[j]
    else:
        return Constraint.Skip
     

def _constraint_ub_x_task_opt(model: ConcreteModel, i: Any, j: Any) -> Constraint:
    """
    Defines an upper bound for X[i,j,n]. 
    model.P_Upper_Bound_X[i,j] is calculated by solving a knapsack problem. 
    This is done because is not straightforward to compute the best combination of taus (ranging from tau_min to tau_max) that will generate the best bound for X[i,j,n].
    
    Args:
        - model (ConcreteModel): a Pyomo model instance.
        - i (Any): task index (should belong to production tasks set).
        - j (Any): unit index (should be capable of executing task i).

    Returns:
        Constraint: a constraint bounding X[i,j,n] or Constraint.Skip if conditions are not met.
    """
    
    if (
        i in model.S_I_Production_Tasks and 
        j in model.S_J_Executing_I[i] and 
        (i,j) in model.P_Task_Unit_Network and
        model.P_EST_Task[i,j] <= len(model.S_Time)
    ):
        return sum(
            model.V_X[i,j,n] 
            for n in model.S_Time 
            if n >= model.P_EST_Task[i,j]
        ) <= model.P_UB_X_Task_OPT[i,j]
    else:
        return Constraint.Skip
        
        
def _constraint_ub_x_unit_opt(model: ConcreteModel, j: Any) -> Constraint:
    """
    Defines an upper bound for X[i,j,n] in a unit. 
    model.P_Upper_Bound_X_Unit[j] is calculated by solving a knapsack problem. 
    This is done because is not straightforward to compute the best combination of taus (ranging from tau_min to tau_max) that will generate the best bound for X[i,j,n] in a unit.
    
    Args:
        - model (ConcreteModel): a Pyomo model instance.
        - i (Any): task index (should belong to production tasks set).
        - j (Any): unit index (should be capable of executing task i).

    Returns:
        Constraint: a constraint bounding X[i,j,n] or Constraint.Skip if conditions are not met.
    """
    
    if (
        model.P_EST_Unit[j] <= len(model.S_Time)
    ):
        
        return sum(
            model.V_X[i,j,n] 
            for i in model.S_I_Production_Tasks 
            if (i,j) in model.P_Task_Unit_Network 
            for n in model.S_Time 
            if n >= model.P_EST_Task[i,j]
        ) <= model.P_UB_X_Unit_OPT[j]
    else:
        return Constraint.Skip
        

def _constraint_clique_x_group_ppc(model: ConcreteModel, k: Any, n: Any) -> Constraint:
    """
    Clique constraint restricting operations (X), during a certain amount of time points n defined by P_EST_Group[k], for tasks in different units consuming the same material k.

    Args:
        - model (ConcreteModel): a Pyomo model instance.
        - k (Any): material index.
        - n (Any): time point index.

    Returns:
        Constraint: a clique constraint on X or Constraint.Skip if conditions are not met.
    """
    
    if (model.P_EST_Group[k] > 0 and
        model.P_EST_Group[k] <= len(model.S_Time) and
        0 <= n <= (model.P_EST_Group[k] - 1)
    ):
        return sum(
            model.V_X[i,j,n]
            for i in (model.S_I_Production_Tasks & model.S_I_Consuming_K[k]) 
            for j in model.S_J_Executing_I[i]                        
        ) <= len(model.S_I_Consuming_K[k]) - 1
    else:
        return Constraint.Skip
        
        
def _constraint_clique_ys_group_ppc(model: ConcreteModel, k: Any, n: Any) -> Constraint:
    """
    Clique constraint restricting startups (YS), during a certain amount of time points n defined by P_EST_Group[k], for tasks in different units consuming the same material k.

    Args:
        - model (ConcreteModel): a Pyomo model instance.
        - k (Any): material index.
        - n (Any): time point index.

    Returns:
        Constraint: a clique constraint on YS or Constraint.Skip if conditions are not met.
    """
    
    if (model.P_EST_Group[k] > 0 and
        model.P_EST_Group[k] <= len(model.S_Time) and
        0 <= n <= (model.P_EST_Group[k] - 1)
    ):
        return sum(
            model.V_Y_Start[i,j,n]
            for i in (model.S_I_Production_Tasks & model.S_I_Consuming_K[k]) 
            for j in model.S_J_Executing_I[i]                         
        ) <= len(model.S_I_Consuming_K[k]) - 1
    else:
        return Constraint.Skip


def load_constraint_set_to_zero_x_est(model: ConcreteModel) -> None:
   """
    Appends to the model a constraint to set to 0 variable X from 0 to est[i,j] - 1 periods.
    
    Args:
        model (ConcreteModel): a Pyomo model instance.
   """    
   
   model.C_Set_X_To_Zero_Based_On_Est = Constraint(model.S_Tasks, model.S_Units, rule = _constraint_set_x_to_zero_based_on_est)
    

def load_constraint_set_to_zero_ys_est(model: ConcreteModel) -> None:
   """
    Appends to the model a constraint to set to 0 variable YS from 0 to est[i,j] - 1 periods.
    
    Args:
        model (ConcreteModel): a Pyomo model instance.
   """    
   
   model.C_Set_YS_To_Zero_Based_On_Est = Constraint(model.S_Tasks, model.S_Units, rule = _constraint_set_ys_to_zero_based_on_est)


def load_constraint_ub_ys_task(model: ConcreteModel) -> None:
   """
    Appends to the model a constraint to define an upper bound on YS for each task.
    
    Args:
        model (ConcreteModel): a Pyomo model instance.
   """    
   
   model.C_Upper_Bound_YS_Task_PPC = Constraint(model.S_Tasks, model.S_Units, rule = _constraint_ub_ys_task_ppc)


def load_constraint_ub_ys_unit(model: ConcreteModel) -> None:
   """
    Appends to the model a constraint to define an upper bound on YS for each unit.
    
    Args:
        model (ConcreteModel): a Pyomo model instance.
   """    
   
   model.C_Upper_Bound_YS_Unit_OPT = Constraint(model.S_Units, rule = _constraint_ub_ys_unit_opt)
   
   
def load_constraint_ub_x_task(model: ConcreteModel) -> None:
   """
    Appends to the model a constraint to define an upper bound on X for each task.
    
    Args:
        model (ConcreteModel): a Pyomo model instance.
   """    
   
   model.C_Upper_Bound_X_Task_OPT = Constraint(model.S_Tasks, model.S_Units, rule = _constraint_ub_x_task_opt)


def load_constraint_ub_x_unit(model: ConcreteModel) -> None:
   """
    Appends to the model a constraint to define an upper bound on X for each unit.
    
    Args:
        model (ConcreteModel): a Pyomo model instance.
   """    
   
   model.C_Upper_Bound_X_Unit_OPT = Constraint(model.S_Units, rule = _constraint_ub_x_unit_opt)   
   
   
def load_constraint_clique_X_group_k(model: ConcreteModel) -> None:
    """
    Appends to the model a constraint to bound variable X when tasks in different units compete for material k.
    
    Args:
        model (ConcreteModel): a Pyomo model instance.
    """   
    
    model.C_Limit_X_Group_PPC = Constraint(model.S_Materials, model.S_Time, rule = _constraint_clique_x_group_ppc)
    
    
def load_constraint_clique_Y_group_k(model: ConcreteModel) -> None:
    """
    Appends to the model a constraint to bound variable YS when tasks in different units compete for material k.
    
    Args:
        model (ConcreteModel): a Pyomo model instance.
    """   
    
    model.C_Limit_YS_Group_PPC = Constraint(model.S_Materials, model.S_Time, rule = _constraint_clique_ys_group_ppc)   