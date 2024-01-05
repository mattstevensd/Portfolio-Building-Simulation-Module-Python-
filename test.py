import InvestmentClasses as IC

CharlesSCHWAB = IC.Stock_Asset(asset_name='Charles Schwab', interest_expectation=0.14695, interest_variance=0.19677)

MyPortfolio = IC.Investment_Portfolio([[CharlesSCHWAB, 1000000]])

MyPortfolio.montecarlo_simulation(number_of_simulations=100000 , years=7 , withdrawal_list=[[CharlesSCHWAB, 75000]], COLA=2.5)