"""
Automatically generated by Colaboratory
"""

# import all libraries
from numpy import *
from scipy.stats import norm
import numpy as np
import matplotlib.pyplot as plt

# Pricing a European option using Black-Scholes formula and Monte Carlo simulations 
# Pricing a Barrier option using Monte Carlo simulations 

S0 = 100     # spot price of the underlying stock today 
K = 105      # strike at expiry 
mu = 0.05    # expected return 
sigma = 0.2  # volatility 
r = 0.05     # risk-free rate 
T = 1.0      # years to expiry
Sb = 110     # barrier

# Define variable numSteps to be the number of steps for multi-step MC
# numPaths - number of sample paths used in simulations

numSteps = 10;
numPaths = 10000;

"""#BS European Prices"""

def BS_european_price(S0, K, T, r, sigma):
  
  t = 0 # Value of stock today
  d1 = (log(S0/K) + (r + (0.5 * (sigma **2 ))) * (T-t))/(sigma * sqrt(T-t)) # Calculate d1
  d2 = d1 - (sigma * sqrt (T-t))
  c = (norm.cdf(d1) * S0) - (norm.cdf(d2) * K * np.exp( -r * (T-t))) # call
  p = (norm.cdf(-d2) * K * np.exp(-r * (T-t))) - (norm.cdf(-d1) * S0) # put 
  return c, p

"""# MC European Prices"""

def MC_european_price(S0, K, T, r, mu, sigma, numSteps, numPaths):

  paths = np.zeros((numSteps + 1, numPaths))

  dT = T / numSteps # time steps

  paths[0] = S0 # price at t = 0

  for iPath in range(numPaths):
        for iStep in range(numSteps):
            paths[iStep + 1, iPath] = paths[iStep, iPath] * np.exp((mu - 0.5 * sigma ** 2) * dT 
                                                                    + sigma * np.sqrt(dT) * np.random.normal(0,1))
    
  call = np.zeros((numPaths,1))
  put = np.zeros((numPaths,1))

  for iPath in range(numPaths):
    call[iPath,0] = np.maximum(paths[numSteps,iPath] - K, 0 ) * np.exp(-r * T)
    put[iPath,0] = np.maximum(K - paths[numSteps,iPath], 0) * np.exp(-r * T)

  c = np.mean(call) # mean of all the simulated answers
  p  = np.mean(put) # mean of all the simulated answers

  return c, p, paths

"""## MC Barrier Knock-in Price"""

def MC_barrier_knockin_price(S0, Sb, K, T, r, mu, sigma, numSteps, numPaths):

  paths = np.zeros((numSteps + 1, numPaths))

  dT = T / numSteps

  paths[0] = S0

  for iPath in range(numPaths):
        for iStep in range(numSteps):
            paths[iStep + 1, iPath] = paths[iStep, iPath] * np.exp((mu - 0.5 * sigma ** 2) * dT 
                                                                    + sigma * np.sqrt(dT) * np.random.normal(0,1))

  barrier = np.sum(paths >= Sb ,axis = 0) # check how many times did the prices crosses the barrier

  call = np.zeros((numPaths,1))
  put = np.zeros((numPaths,1))

  for iPath in range(numPaths):
    if barrier[iPath] > 0:              # If barrier is crossed, then payout exists
      call[iPath,0] = np.maximum(paths[numSteps,iPath] - K, 0 ) * np.exp(-r * T)
      put[iPath,0] = np.maximum(K - paths[numSteps,iPath], 0) * np.exp(-r * T)
    else:                               # If barrier is not crossed, then payout is 0
      call[iPath,0] = 0
      put[iPath,0] = 0

  c = np.mean(call)
  p = np.mean(put)
  return c, p

"""
# Implementation
Please note that these are final results after undertaking tests for <br>
numSteps = [10,12,52,252] and <br>
numPaths = [50000,70000, 100000]

All the test results along with values are present in the report.

numSteps = 252 and numPaths = 100000 is chosen
"""

# Implement Black-Scholes pricing formula
call_BS_European_Price, putBS_European_Price = BS_european_price(S0, K, T, r, sigma)

# Implement one-step Monte Carlo pricing procedure for European option
callMC_European_Price_1_step, putMC_European_Price_1_step, path1 = MC_european_price(S0, K, T, r, mu, sigma, 1, 200000)

# Implement multi-step Monte Carlo pricing procedure for European option
callMC_European_Price_multi_step, putMC_European_Price_multi_step, paths_multi = MC_european_price(S0, K, T, r, mu, sigma, 252, 200000)

# Implement one-step Monte Carlo pricing procedure for Barrier option
callMC_Barrier_Knockin_Price_1_step, putMC_Barrier_Knockin_Price_1_step = MC_barrier_knockin_price(S0, Sb, K, T, r, mu, sigma, 1, 200000)

# Implement multi-step Monte Carlo pricing procedure for Barrier option
callMC_Barrier_Knockin_Price_multi_step, putMC_Barrier_Knockin_Price_multi_step = MC_barrier_knockin_price(S0, Sb, K, T, r, mu, sigma, 252, 200000)

print('Black-Scholes price of an European call option is ' + str(call_BS_European_Price))
print('Black-Scholes price of an European put option is ' + str(putBS_European_Price))
print('One-step MC price of an European call option is ' + str(callMC_European_Price_1_step))
print('One-step MC price of an European put option is ' + str(putMC_European_Price_1_step)) 
print('Multi-step MC price of an European call option is ' + str(callMC_European_Price_multi_step)) 
print('Multi-step MC price of an European put option is ' + str(putMC_European_Price_multi_step)) 
print('One-step MC price of an Barrier call option is ' + str(callMC_Barrier_Knockin_Price_1_step)) 
print('One-step MC price of an Barrier put option is ' + str(putMC_Barrier_Knockin_Price_1_step)) 
print('Multi-step MC price of an Barrier call option is ' + str(callMC_Barrier_Knockin_Price_multi_step)) 
print('Multi-step MC price of an Barrier put option is ' + str(putMC_Barrier_Knockin_Price_multi_step))

""" MC Plots"""

# Plot results

plt.figure(figsize=(10,12))
for i in range(numPaths):
  plt.plot(paths_multi[:,i], linewidth = 2)
plt.title('Stock Price Simulation (Multistep)')

"""# Knock-in due to change in volatility"""

# Barrier options with increase volatility 10%
i_sigma = sigma * 1.10
call_BS_European_Price_i, putBS_European_Price_i = BS_european_price(S0, K, T, r,i_sigma)

# Barrier option by decrease volatility 10 % 
d_sigma = sigma * 0.90
call_BS_European_Price_d, putBS_European_Price_d = BS_european_price(S0, K, T, r, d_sigma)

print("By increasing the volatility by 10% ")
print('Black-Scholes price of an European call option is ' + str(call_BS_European_Price_i))
print('Black-Scholes price of an European call option is ' + str(putBS_European_Price_i))
print("\n\n")
print("By decreasing the volatility by 10%")
print('Black-Scholes price of an European call option is ' + str(call_BS_European_Price_d))
print('Black-Scholes price of an European call option is ' + str(putBS_European_Price_d))

