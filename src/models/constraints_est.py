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


def _constraint_ub_ys_unit_ppc(model: ConcreteModel, j: Any) -> Constraint:
    """
    Defines an upper bound on the number of startups (YS) in a unit. 
    
    Args:
        - model (ConcreteModel): a Pyomo model instance.
        - j (Any): unit index (should be capable of executing task i).

    Returns:
        Constraint: a constraint bounding YS in a unit or Constraint.Skip if conditions are not met.
    """
    
    if (
        j in model.S_Units and 
        model.P_EST_Unit[j] > 0 and
        model.P_EST_Unit[j] <= len(model.S_Time)
    ):
        return sum(
            model.V_Y_Start[i,j,n] 
            for n in model.S_Time 
            if n >= model.P_EST_Unit[j]    
            for i in model.S_I_Production_Tasks 
            if (i,j) in model.P_Task_Unit_Network                    
        ) <= model.P_UB_YS_Unit_PPC[j]
    else:
        return Constraint.Skip   
    

def _constraint_ub_ys_unit_ppc_new(model: ConcreteModel, j: Any) -> Constraint:
    """
    Based on the maximum number of startups in a unit, defines an upper bound associated with YS and Tau_Miin. 
    
    Args:
        - model (ConcreteModel): a Pyomo model instance.
        - j (Any): unit index (should be capable of executing task i).

    Returns:
        Constraint: a constraint bounding Tau_Min * YS in in a unit or Constraint.Skip if conditions are not met.
    """
    
    if (
        model.P_EST_Unit[j] <= len(model.S_Time)
    ):
        
        return sum(
            (model.P_Tau_Min[i,j] + 1) * model.V_Y_Start[i,j,n]
            for i in model.S_I_Production_Tasks 
            if (i,j) in model.P_Task_Unit_Network 
            for n in model.S_Time 
            if n >= model.P_EST_Unit[j]
        ) <= model.P_UB_YS_Unit_PPC_New[j]
    else:
        return Constraint.Skip
    
    
def _constraint_ub_x_task_ppc(model: ConcreteModel, i: Any, j: Any) -> Constraint:
    """
    Defines an upper bound for X[i,j,n]. 
    Based on the remaining time points in a unit, we compute how many runs are possible considering model.P_Tau_Max[i,j] (less number of Tau_Ends) and then multiply the result by model.P_Tau_Max[i,j].
    
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
        model.P_EST_Task[i,j] > 0 and
        model.P_EST_Task[i,j] <= len(model.S_Time)
    ):
        return sum(
            model.V_X[i,j,n] 
            for n in model.S_Time 
            if n >= model.P_EST_Task[i,j]
        ) <= model.P_UB_X_Task_PPC[i,j]
    else:
        return Constraint.Skip
        
        
def _constraint_ub_x_unit_ppc(model: ConcreteModel, j: Any) -> Constraint:
    """
    Defines an upper bound for X[i,j,n] in a unit. 
    Based on the remaining time points in a unit, we compute how many runs are possible considering the max(model.P_Tau_Max[i,j]) in the unit (less number of Tau_Ends) and then multiply the result by max(model.P_Tau_Max[i,j]).
    
    Args:
        - model (ConcreteModel): a Pyomo model instance.
        - j (Any): unit index (should be capable of executing task i).

    Returns:
        Constraint: a constraint bounding X[i,j,n] in a unit or Constraint.Skip if conditions are not met.
    """
    
    if (
        model.P_EST_Unit[j] > 0 and
        model.P_EST_Unit[j] <= len(model.S_Time)
    ):
        return sum(
            model.V_X[i,j,n] 
            for n in model.S_Time 
            if n >= model.P_EST_Unit[j]
            for i in model.S_I_Production_Tasks 
            if (i,j) in model.P_Task_Unit_Network
        ) <= model.P_UB_X_Unit_PPC[j]
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
 
    
def load_constraints_set_to_zero_x_ys_est(model: ConcreteModel) -> None:
   """
    Appends to the model constraints to set to 0 variables X and YS from 0 to est[i,j] - 1 periods.
    
    Args:
        model (ConcreteModel): a Pyomo model instance.
   """    
   
   model.C_Set_X_To_Zero_Based_On_Est = Constraint(model.S_Tasks, model.S_Units, rule = _constraint_set_x_to_zero_based_on_est)
   model.C_Set_YS_To_Zero_Based_On_Est = Constraint(model.S_Tasks, model.S_Units, rule = _constraint_set_ys_to_zero_based_on_est)
    
   
def load_constraints_preprocessing(model: ConcreteModel) -> None:
    """
    Appends to the model constraints to bound variables X and YS considering bounds obtained via preprocessing.
    
    Args:
        model (ConcreteModel): a Pyomo model instance.
    """   
    
    model.C_Upper_Bound_YS_Task_PPC = Constraint(model.S_Tasks, model.S_Units, rule = _constraint_ub_ys_task_ppc)
    model.C_Upper_Bound_YS_Unit_PPC = Constraint(model.S_Units, rule = _constraint_ub_ys_unit_ppc)
    model.C_Upper_Bound_YS_Unit_PPC_New = Constraint(model.S_Units, rule = _constraint_ub_ys_unit_ppc_new)    
    model.C_Upper_Bound_X_Task_PPC = Constraint(model.S_Tasks, model.S_Units, rule = _constraint_ub_x_task_ppc)
    model.C_Upper_Bound_X_Unit_PPC = Constraint(model.S_Units, rule = _constraint_ub_x_unit_ppc)    
    model.C_Limit_Operations_Group_PPC = Constraint(model.S_Materials, model.S_Time, rule = _constraint_clique_x_group_ppc)
    model.C_Limit_Startups_Group_PPC = Constraint(model.S_Materials, model.S_Time, rule = _constraint_clique_ys_group_ppc)
        

def load_constraints_preprocessing_optimization(model: ConcreteModel) -> None:
    """
    Appends to the model constraints to bound variables X and YS considering bounds obtained via preprocessing and the solution of knapsack problems.
    
    Args:
        model (ConcreteModel): a Pyomo model instance.
    """    
    
    #model.C_Upper_Bound_YS_Task_PPC = Constraint(model.S_Tasks, model.S_Units, rule = _constraint_ub_ys_task_ppc)    
    #model.C_Upper_Bound_YS_Unit_OPT = Constraint(model.S_Units, rule = _constraint_ub_ys_unit_opt)
    #model.C_Upper_Bound_X_Task_OPT = Constraint(model.S_Tasks, model.S_Units, rule = _constraint_ub_x_task_opt)
    #model.C_Upper_Bound_X_Unit_OPT = Constraint(model.S_Units, rule = _constraint_ub_x_unit_opt)        
    model.C_Limit_Operations_Group_PPC = Constraint(model.S_Materials, model.S_Time, rule = _constraint_clique_x_group_ppc)
    model.C_Limit_Startups_Group_PPC = Constraint(model.S_Materials, model.S_Time, rule = _constraint_clique_ys_group_ppc)