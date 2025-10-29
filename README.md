STN Continuous Process Profit Maximization

This project builds and solves a Mixed-Integer Linear Programming (MILP) model for scheduling tasks in continuous process systems based on the State-Task Network (STN) framework. 

The model aims to maximize process profit while respecting operational and material balance constraints.

🧩 Project Structure

├── input_data
│   ├── datasets
│   │   ├── run_00001.json
│   ├── networks.py
├── slurm
│   ├── slurm.sh
├── src
│   ├── data
│   │   ├── instance_generation.py
│   │   ├── postprocessing.py
│   ├── methods
│   │   ├── est_group.py
│   │   ├── est.py
│   │   ├── upper_bound_x_task_opt.py
│   │   └── upper_bound_ys_x_unit_opt.py
│   ├── models
│   │   ├── base_model_build
│   │   ├── constraints_est
│   │   ├── constraints
│   │   ├── formulation_build
│   │   ├── model_solve
│   │   ├── objective
│   │   ├── parameters
│   │   ├── sets
│   │   ├── variables
│   ├── results
│   │   ├── aggregated_results.xlsx
│   │   ├── result_00001.json
│   ├── utils
│   │   ├── utils.py
│   └── visualization
│       ├── plot_results.py
├── .gitignore
├── aggregate_results.py
├── generate_datasets.py
├── main.py
├── performance_charts.ipynb
├── README.md
└── requirements.txt

⚙️ Installation

To install all required dependencies, run: pip install -r requirements.txt 

🚀 Running an Instance

All instance configuration files are stored in the folder: input_data/datasets/

For example, run_00001.json defines parameters that will be used to generate a specific problem instance.

To execute a particular instance, run the following command from the project root: python main.py 1

This will solve the instance file run_00001.json.

📊 Results

The solution of each instance is saved as a JSON file in: src/results/

Example: result_00001.json

Run file aggregate_results.py to generate the Excel file aggregated_results.xlsx. Then, run notebook performance_charts.ipynb to create the performance charts related to the formulations. 

🧠 Key Features

MILP formulation for continuous process scheduling.

STN-based modeling structure for general applicability.

Automated dataset generation and parameterized instance solving.

Result aggregation and visualization tools.

Ready-to-run SLURM submission script for HPC environments.