**Objective & Structure:** The physical simulations (Monte Carlo, Heat Equation or whatever) will be developed purely as .py scripts and save raw data outputs (e.g., .npy files). We may use Jupyter Notebooks exclusively as a frontend to load these results, generate performance plots, and format the final report.

Folder Structure Example:

📁 phase_3/
├── README.md
├── 📁 src/                               <-- The Engine (Terminal only)
│   ├── montecarlo_mpi.py
│   └── heat_equation_mpi.py
├── 📁 data/                              <-- Simulation outputs (Ignored by Git)
│   ├── mc_results.npy
│   └── heat_matrices.npy
└── 📄 Final_Project_Report.ipynb         <-- The Interface (Data loading, plots, and theory)