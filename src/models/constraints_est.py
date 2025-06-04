from pyomo.environ import *


def _constraint_set_x_to_zero_est(model: ConcreteModel, i: Any, j: Any) -> Constraint:
    """
    Sets to 0 variable X[i,j,n] from n = 0 to n = est[i,j] - 1.

    Args:
        - model (ConcreteModel): a Pyomo model instance.
        - i (Any): task index (should belong to production tasks set).
        - j (Any): unit index (should be capable of executing task i).

    Returns:
        Constraint: a constraint enforcing X[i,j,n] = 0 for time points before est[i,j} or Constraint.Skip if conditions are not met.
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


def _constraint_set_y_to_zero_est(model: ConcreteModel, i: Any, j: Any) -> Constraint:
    """
    Sets to 0 variable Y_S[i,j,n] from n = 0 to n = est[i,j] - 1.

    Args:
        - model (ConcreteModel): a Pyomo model instance.
        - i (Any): task index (should belong to production tasks set).
        - j (Any): unit index (should be capable of executing task i).

    Returns:
        Constraint: a constraint enforcing Y_S[i,j,n] = 0 for time points before est[i,j} or Constraint.Skip if conditions are not met.
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


def _constraint_ppc_upper_bound_ys_task(model: ConcreteModel, i: Any, j: Any) -> Constraint:
    """
    Defines an upper bound on the number of runs task i can start (var Y_S[i,j,n]). 
    
    Args:
        - model (ConcreteModel): a Pyomo model instance.
        - i (Any): task index (should belong to production tasks set).
        - j (Any): unit index (should be capable of executing task i).

    Returns:
        Constraint: a constraint upper bounding Y_S[i,j,n] or Constraint.Skip if conditions are not met.
    """
    
    if (
        i in model.S_I_Production_Tasks and 
        j in model.S_J_Executing_I[i] and 
        (i,j) in model.P_Task_Unit_Network and
        model.P_EST_Task[i,j] >= 0 and
        model.P_EST_Task[i,j] <= len(model.S_Time)
    ):
        return sum(
            model.V_Y_Start[i,j,n] 
            for n in model.S_Time 
            if n >= model.P_EST_Task[i,j]
        ) <= model.P_UB_YS_Task[i,j]
    else:
        return Constraint.Skip    


def _constraint_ppc_upper_bound_ys_unit(model: ConcreteModel, j: Any) -> Constraint:
    """
    Defines an upper bound on the number of runs that can start in a unit (var Y_S[i,j,n]). 
    
    Args:
        - model (ConcreteModel): a Pyomo model instance.
        - j (Any): unit index (should be capable of executing task i).

    Returns:
        Constraint: a constraint bounding Y_S[i,j,n] in a unit or Constraint.Skip if conditions are not met.
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
        ) <= model.P_UB_YS_Unit[j]
    else:
        return Constraint.Skip   
    

def _constraint_ppc_upper_bound_x_task(model: ConcreteModel, i: Any, j: Any) -> Constraint:
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
        ) <= model.P_UB_X_Task[i,j]
    else:
        return Constraint.Skip
        
        
def _constraint_ppc_upper_bound_x_unit(model: ConcreteModel, j: Any) -> Constraint:
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
        j in model.S_Units and
        model.P_EST_Unit[j] > 0 and
        model.P_EST_Unit[j] <= len(model.S_Time)
    ):
        return sum(
            model.V_X[i,j,n] 
            for n in model.S_Time 
            if n >= model.P_EST_Unit[j]
            for i in model.S_I_Production_Tasks 
            if (i,j) in model.P_Task_Unit_Network
        ) <= model.P_UB_X_Unit[j]
    else:
        return Constraint.Skip
    

def _constraint_opt_upper_bound_ys_unit(model: ConcreteModel, j: Any) -> Constraint:
    """
    Defines an upper bound on the number of runs that can start in a unit (var Y_S[i,j,n]). 
    model.P_Upper_Bound_YS_Unit[j] is calculated by solving a knapsack problem.

    Args:
        - model (ConcreteModel): a Pyomo model instance.
        - j (Any): unit index (should be capable of executing task i).

    Returns:
        Constraint: a constraint bounding Y_S[i,j,n] in a unit or Constraint.Skip if conditions are not met.
    """
    if (
        model.P_EST_Unit[j] <= len(model.S_Time)
    ):
        
        return sum(
            model.V_Y_Start[i,j,n] 
            for i in model.S_I_Production_Tasks 
            if (i,j) in model.P_Task_Unit_Network 
            for n in model.S_Time 
            if n >= model.P_EST_Unit[j]
        ) <= model.P_Upper_Bound_YS_Unit[j]
    else:
        return Constraint.Skip
     

def _constraint_opt_upper_bound_x(model: ConcreteModel, i: Any, j: Any) -> Constraint:
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
        ) <= model.P_Upper_Bound_X[i,j]
    else:
        return Constraint.Skip
        
        
def _constraint_opt_upper_bound_x_unit(model: ConcreteModel, j: Any) -> Constraint:
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
            if n >= model.P_EST_Unit[j]
        ) <= model.P_Upper_Bound_X_Unit[j]
    else:
        return Constraint.Skip
        

def _constraint_limit_operations_group(model: ConcreteModel, k: Any, n: Any) -> Constraint:
    
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
        
        
def _constraint_limit_startups_group(model: ConcreteModel, k: Any, n: Any) -> Constraint:
    
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
 
    
def _constraint_upper_bound_ys_unit(model: ConcreteModel, j: Any) -> Constraint:
    
    if (
        model.P_EST_Unit[j] <= len(model.S_Time)
    ):
        
        return sum(
            (model.P_Tau_Min[i,j] + 1) * model.V_Y_Start[i,j,n]
            for i in model.S_I_Production_Tasks 
            if (i,j) in model.P_Task_Unit_Network 
            for n in model.S_Time 
            if n >= model.P_EST_Unit[j]
        ) <= model.P_New_UB_YS_Unit[j]
    else:
        return Constraint.Skip
    
   
def create_constraints_est_f1(model: ConcreteModel) -> None:
    
    
    model.C_EST_X_To_Zero = Constraint(model.S_Tasks, model.S_Units, rule = _constraint_set_x_to_zero_est)
    model.C_EST_Y_To_Zero = Constraint(model.S_Tasks, model.S_Units, rule = _constraint_set_y_to_zero_est)
    model.C_EST_PPC_Upper_Bound_YS_Task = Constraint(model.S_Tasks, model.S_Units, rule = _constraint_ppc_upper_bound_ys_task)
    model.C_EST_PPC_Upper_Bound_YS_Unit = Constraint(model.S_Units, rule = _constraint_ppc_upper_bound_ys_unit)
    model.C_Upper_PPC_Bound_X_Task = Constraint(model.S_Tasks, model.S_Units, rule = _constraint_ppc_upper_bound_x_task)
    model.C_Upper_PPC_Bound_X_Unit = Constraint(model.S_Units, rule = _constraint_ppc_upper_bound_x_unit)
    model.C_Limit_Operations_Group = Constraint(model.S_Materials, model.S_Time, rule = _constraint_limit_operations_group)
    model.C_Limit_Startups_Group = Constraint(model.S_Materials, model.S_Time, rule = _constraint_limit_startups_group)
    model.C_Upper_Bound_YS_Unit = Constraint(model.S_Units, rule = _constraint_upper_bound_ys_unit)
    

def create_constraints_est_f2(model: ConcreteModel) -> None:
    
    
    model.C_EST_X_To_Zero = Constraint(model.S_Tasks, model.S_Units, rule = _constraint_set_x_to_zero_est)
    model.C_EST_Y_To_Zero = Constraint(model.S_Tasks, model.S_Units, rule = _constraint_set_y_to_zero_est)
    model.C_EST_PPC_Upper_Bound_YS = Constraint(model.S_Tasks, model.S_Units, rule = _constraint_ppc_upper_bound_ys_task)
    model.C_EST_OPT_Upper_Bound_YS_Unit = Constraint(model.S_Units, rule = _constraint_opt_upper_bound_ys_unit)
    model.C_Upper_OPT_Bound_X = Constraint(model.S_Tasks, model.S_Units, rule = _constraint_opt_upper_bound_x)
    model.C_Upper_OPT_Bound_X_Unit = Constraint(model.S_Units, rule = _constraint_opt_upper_bound_x_unit)    


def if_start_end(model: ConcreteModel, i: Any, j: Any, n: Any) -> Constraint:
    if (i in model.S_I_Production_Tasks) and j in model.S_J_Executing_I[i] and (n <= (len(model.S_Time) - 1) - model.P_Tau_Max[i,j]):
        return sum(model.V_Y_End[i,j,nprime] for nprime in model.S_Time if nprime >= n + model.P_Tau_Min[i,j] and nprime <= n + model.P_Tau_Max[i,j]) >= model.V_Y_Start[i,j,n]
    else:
        return Constraint.Skip


def max_lenght_run_eq19_reformulation_YS(model: ConcreteModel, i: Any, j: Any, n: Any) -> Constraint:
    if (i,j) in model.P_Task_Unit_Network and i in model.S_I_Production_Tasks:
        return model.V_X[i,j,n] <= sum(model.V_Y_Start[i,j,nprime] for nprime in model.S_Time if ( (nprime >= n - model.P_Tau_Max[i,j] + 1) and (nprime <= n) )) 
    else:
        return Constraint.Skip


def max_lenght_run_eq19_reformulation_YE(model: ConcreteModel, i: Any, j: Any, n: Any) -> Constraint:
    if (i,j) in model.P_Task_Unit_Network and i in model.S_I_Production_Tasks:
        return model.V_X[i,j,n] <= sum(model.V_Y_End[i,j,nprime] for nprime in model.S_Time if ( (nprime >= n + 1) and (nprime <= n + model.P_Tau_Max[i,j]) )) 
    else:
        return Constraint.Skip
    
    
def create_constraints_test(model: ConcreteModel) -> None:
   
    model.If_Start_End = Constraint(model.S_Tasks, model.S_Units, model.S_Time, rule = if_start_end)
    model.C_Max_Lenght_Run_Reformulation_YS_Eq19 = Constraint(model.S_Tasks, model.S_Units, model.S_Time, rule = max_lenght_run_eq19_reformulation_YS) 
    model.C_Max_Lenght_Run_Reformulation_YE_Eq19 = Constraint(model.S_Tasks, model.S_Units, model.S_Time, rule = max_lenght_run_eq19_reformulation_YE)     