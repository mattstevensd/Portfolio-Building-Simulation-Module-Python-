import math as mat

import numpy as np

import matplotlib.pyplot as plt

import csv

class Stock_Asset():

    def __init__(self,asset_name,interest_expectation,interest_variance):
        self.interest_expectation = interest_expectation
        self.interest_variance = interest_variance
        self.asset_name = asset_name

class Investment_Portfolio():

    def __init__(self, stock_list):
        self.stock_list = stock_list
        pass
    
    #main method for running monte simulation and creating analytic reports
    def montecarlo_simulation(self, number_of_simulations, years, withdrawal_list = None, COLA = 0, withdrawal_years = 'all'):

        num_of_stocks = len(self.stock_list)

        #simuation if there is no withdrawal
        if withdrawal_list == None:

            sim_raw_data = self.no_withdrawal_monte_simulation(number_of_simulations, years, num_of_stocks)

        #simulation with withdrawal
        else:

            sim_raw_data = self.yes_withdrawal_monte_simulation(number_of_simulations, years, withdrawal_list, COLA, withdrawal_years, num_of_stocks)
        
        #calculates final_value_raw_data list
        finalvalue_raw_data = []
        for i in sim_raw_data:
            finalvalue_raw_data.append(i[num_of_stocks+1])

        #plot histogram of final portfolio values
        #self.raw_data_histogram_plot(sim_raw_data,num_of_stocks)

        #export raw data to excel file

        self.csv_export_raw_data(sim_raw_data, num_of_stocks)
            
        #export metrics to excel file

        self.csv_export_analytic_report(sim_raw_data, num_of_stocks, number_of_simulations, years)
        
        return
    

    #Methods For Monte Carlo Simulaiton Method \/
    #-------------------------------------------------------------------------------------------------------------------------------------------------------------#
    #method returns monte raw data for a no withdrawal situation
    def no_withdrawal_monte_simulation(self, number_of_simulations, years, num_of_stocks):

        sim_raw_data = []

        #run therough each case of the simulation and return raw data list
        for k in range(number_of_simulations):
            
            #initilize data matrix to correct size and fill with year 0 values
            list1 = [0]*(years+1)
            value_matrix = []
            for l in range(num_of_stocks):
                value_matrix.append(list1)
                value_matrix[l][0] = self.stock_list[l][1]

            #loop through stocks to return yearly asset value over all the years for each stock
            for i in range(num_of_stocks):

                current_exp = self.stock_list[i][0].interest_expectation

                current_var = self.stock_list[i][0].interest_variance

                for j in range(years):

                    current_value = value_matrix[i][j]

                    random_interest = np.random.normal(current_exp , current_var)

                    compounded_value = current_value*(random_interest+1)

                    if compounded_value < 0:
                        compounded_value = 0

                    value_matrix[i][j+1] = compounded_value
        
            #define total final portfolio total value
            portfolio_total = 0

            for m in range(num_of_stocks):
                final_stock_value = value_matrix[m][years]
                portfolio_total = portfolio_total + final_stock_value
                
            #add simulation number, final portfolio values for each stock and total value to list and append to simulation raw data
            raw_data_list = []
            raw_data_list.append(k+1)
            for i in range(num_of_stocks):
                raw_data_list.append(value_matrix[i][years])
            
            raw_data_list.append(portfolio_total)

            sim_raw_data.append(raw_data_list)

        return sim_raw_data
    
    #method returns monte raw data for a withdrawal situation
    def yes_withdrawal_monte_simulation(self, number_of_simulations, years, withdrawal_list, COLA, withdrawal_years, num_of_stocks):
        
        sim_raw_data = []

        #sets withdrawal years set to all years for default value
        if withdrawal_years == 'all':
            withdrawal_years = set()
        for i in range(years):
            withdrawal_years.add(i+1)
        
        #loops though all simulations
        for k in range(number_of_simulations):
            
            #defining value matrix for each simulation (tracks change in assets year to year over all assets (2dimensional))
            list1 = [0]*(years+1)
            value_matrix = []
            for l in range(num_of_stocks):
                value_matrix.append(list1)
                value_matrix[l][0] = self.stock_list[l][1]

            #chooses stock/asset 'i' to simulate
            for i in range(num_of_stocks):

                current_exp = self.stock_list[i][0].interest_expectation

                current_var = self.stock_list[i][0].interest_variance

                stock_name = self.stock_list[i][0]

                stock_withdrawal_value = 0

                #sets withdrawal value for specifc stock/asset
                for n in withdrawal_list:
                    if n[0] == stock_name:
                        stock_withdrawal_value = n[1]
                
                #tracks change in asset 'i' over all years including deducting withdrawal when necessary; records value in each year to 'value_matrix'
                for j in range(years): 

                    current_value = value_matrix[i][j]

                    current_year = j + 1

                    random_interest = np.random.normal(current_exp , current_var)

                    compounded_value = current_value*(random_interest+1)

                    if current_year in withdrawal_years:
                        compounded_value = compounded_value - stock_withdrawal_value*((1+(COLA/100)**(j+1)))
                        
                    if compounded_value < 0:
                        compounded_value = 0

                    value_matrix[i][j+1] = compounded_value
                
                #define total final portfolio total value
                portfolio_total = 0

                for m in range(num_of_stocks):
                    final_stock_value = value_matrix[m][years]
                    portfolio_total = portfolio_total + final_stock_value
                
                #add simulation number, final portfolio values for each stock and total value to list and append to simulation raw data
                raw_data_list = []
                raw_data_list.append(k+1)
                for i in range(num_of_stocks):
                    raw_data_list.append(value_matrix[i][years])
                
                raw_data_list.append(portfolio_total)

                sim_raw_data.append(raw_data_list)
        return sim_raw_data

    #method plots histogram of final portoflio value raw data
    def raw_data_histogram_plot(self, sim_raw_data, num_of_stocks):

        finalvalue_raw_data = []
        for i in sim_raw_data:
            finalvalue_raw_data.append(i[num_of_stocks+1])
        
        plt.hist(finalvalue_raw_data, bins = 1000)
        plt.show() 
        return

    #method exports monte simulation raw data to csv file
    def csv_export_raw_data(self, sim_raw_data, num_of_stocks):

        with open("monte_simulation_raw_data.csv", mode='w') as csvfile:
            field_names = ['Simulation']

            for i in self.stock_list:
                field_names.append(i[0].asset_name)
            
            field_names.append('Total')

            raw_data_writer = csv.DictWriter(csvfile, fieldnames = field_names)
            raw_data_writer.writeheader()

            for i in sim_raw_data:
                raw_data_writing_Dict = {}
                raw_data_writing_Dict['Simulation'] = i[0]
                raw_data_writing_Dict['Total'] = i[num_of_stocks+1]

                for j in range(num_of_stocks):
                    current_key = field_names[j+1]
                    raw_data_writing_Dict[current_key] = i[j+1]
                
                raw_data_writer.writerow(raw_data_writing_Dict)

        return

    #method exports csv analytic report
    def csv_export_analytic_report(self, sim_raw_data, num_of_stocks, number_of_simulations, years):

        with open("monte_simulation_analytics_report.csv",mode='w') as csvfile:

            #define field names for resulting csv file
            field_names = ['Statistic']

            for i in self.stock_list:
                field_names.append(i[0].asset_name)
            
            field_names.append('Total Portfolio')

            #create dictionary writer object and create table header
            analytic_data_writer = csv.DictWriter(csvfile, fieldnames = field_names)
            analytic_data_writer.writeheader()

            #write empirical mean statistic, x-year interest statistic, and CAGR
            mean_interest_CAGR_dictlist = self.empirical_mean_dict(sim_raw_data,number_of_simulations, years)
            analytic_data_writer.writerow(mean_interest_CAGR_dictlist[0])
            analytic_data_writer.writerow(mean_interest_CAGR_dictlist[1])
            analytic_data_writer.writerow(mean_interest_CAGR_dictlist[2])

            #write under par probability statistic
            probability_stats_dictlist = self.probabilitystats_dict(sim_raw_data,number_of_simulations)
            analytic_data_writer.writerow(probability_stats_dictlist[0])
            analytic_data_writer.writerow(probability_stats_dictlist[1])

        return

    #returns empirical mean dict stat for csv dict writer (includes mean interet and mean CAGR dicts)
    def empirical_mean_dict(self,sim_raw_data, number_of_simulations, years):

        mean_dict = {}
        total_interest_dict = {}
        CAGR_dict = {}

        mean_dict['Statistic'] = 'Empirical Mean'
        CAGR_dict['Statistic'] = 'CAGR'

        x = str(years)
        y = x + '-year Interest'
        total_interest_dict['Statistic'] = y

        #calculate average for each stock and add to dictionary

        current_index = 1
        for i in self.stock_list:
            current_mean = 0

            for j in sim_raw_data:

                current_mean = current_mean + j[current_index]/number_of_simulations
            
            mean_dict[i[0].asset_name] = current_mean
            total_interest_dict[i[0].asset_name] = ((current_mean - i[1])/i[1])*100
            CAGR_dict[i[0].asset_name] = (((1+((current_mean - i[1])/i[1]))**(1/years)) - 1)*100

            current_index = current_index + 1
        
        total_mean = 0

        for j in sim_raw_data:
            total_mean = total_mean + j[current_index]/number_of_simulations
        
        initial_total = 0
        for j in self.stock_list:
            initial_total = initial_total + j[1]

        mean_dict['Total Portfolio'] = total_mean
        total_interest_dict['Total Portfolio'] = ((total_mean - initial_total)/initial_total)*100
        CAGR_dict['Total Portfolio'] = (((1+((total_mean - initial_total)/initial_total))**(1/years)) - 1)*100
        
        return [mean_dict,total_interest_dict,CAGR_dict]

    #returns dictionaries for under par probability and insolvent probability for csv dict writer
    def probabilitystats_dict(self, sim_raw_data, number_of_simulations):

        insolventprob_dict = {}
        underparprob_dict = {}

        insolventprob_dict['Statistic'] = 'Insolvent Probability'
        underparprob_dict['Statistic'] = 'Under Par Probability'
        
        sim_insolvent = 0
        sim_under_par = 0

        current_index = 1
        for i in self.stock_list:

            for j in sim_raw_data:
                if j[current_index] == 0:
                    sim_insolvent = sim_insolvent + 1
                if j[current_index] < i[1]:
                    sim_under_par = sim_under_par + 1
            
            insolventprob_dict[i[0].asset_name] = (sim_insolvent/number_of_simulations)*100
            underparprob_dict[i[0].asset_name] = (sim_under_par/number_of_simulations)*100

            current_index = current_index + 1

        sim_insolvent = 0
        sim_under_par = 0

        for j in sim_raw_data:
            if j[current_index] == 0:
                sim_insolvent = sim_insolvent + 1
            if j[current_index] < i[1]:
                sim_under_par = sim_under_par + 1
        
        insolventprob_dict['Total Portfolio'] = (sim_insolvent/number_of_simulations)*100
        underparprob_dict['Total Portfolio'] = (sim_under_par/number_of_simulations)*100


        return [underparprob_dict, insolventprob_dict]

    #-------------------------------------------------------------------------------------------------------------------------------------------------------------#
