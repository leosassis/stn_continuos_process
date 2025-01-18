
def set_solver_options(solver) -> None:
    solver.options['MIPGap'] = 0.01  # Set MIP gap
    solver.options['TimeLimit'] = 1200  # Set time limit