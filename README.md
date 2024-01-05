# Portfolio-Building-Simulation-Module-Python-
Description: Module for building asset portfolio and simulating random outcomes of portfolio over a specified period of time (allow for portfolio withdrawal).

There are two classes in the InvestmentClasses module:

1. Asset Class: This class allows you to define an asset (stock, commodity, etc.). You must assign the asset a yearly interest rate expectation and variance (calculated from historical data) which the simulation will use to model the asset as a normally distributed random variable (Note: will only be useful if it makes sense to model such asset in this manner).

2. Portfolio Class: Can define a portfolio by adding a list of assets and there corresponding investments as the initialization input (Ex: [[Asset1,10],[Asset2,50]]). This class includes a simulaiton method that allow you to simulate the portfolio performance over a specified number of years. This simulation outputs a histogram, a CSV file containg the raw data, and a CSV file containing an analytics report.

What is being worked on:
Historical Data as an Asset Class Input: would like to be able to input the historical data of the assset as an input instead of rate expectation and variance. The portfolio class would then have a method that calculates the best covaraince matrix for modelling the various assets in the portfolio.
Other Assets: Modelling things like futures and options isn't really viable as they don't have "interest rates". Would like to build in an option for this.
