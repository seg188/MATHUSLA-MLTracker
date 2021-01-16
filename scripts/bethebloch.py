import numpy as np
import ROOT as root

#https://www.osti.gov/servlets/purl/6733705/

eV = np.power(10.0, -6.0)
N_A = 6.022*np.power(10.0, 23.0)

#effective Atomic number for C9H10
Z = 64.
A = 128.16
rho = 1.032

r_e = 2.817*np.power(10.0, -13.0)
pi=3.1415
K = 4.*pi*r_e*r_e*(rho/A)*N_A
#MUON CHARGE NMBER
z = 1.0


A_H = 2.016
A_C = 12.0
Z_C = 6.0
Z_H = 1.0
w_H = 10.*A_H/A 
w_C = 9.*A_C/A
I_H = 10.2 #eV
I_C = 6.0 #eV

I = np.exp( (10.*Z_H*np.log(I_H)+ 9.*Z_C*np.log(I_C))/(10*Z_H + 9.*Z_C) )
print(I)
#I = (9.*I_C + 10.*I_H)/19.

hbar_omega = 28.816*np.sqrt(rho*Z/A)*np.power(10.0, -6.0)

#density corecion to ionization loss
delta_bg = np.sqrt(rho*(Z/A))

mu_mass = 105.7*np.power(10.0, 6.0)
m_e = 0.511*np.power(10.0, 6.0)

def beta2(gamma):
	return (1.0 - 1.0/(gamma*gamma))

def W_max(gamma):
	return 2.*m_e*beta2(gamma)*gamma*gamma/(1.+2*gamma*(m_e/mu_mass) + (m_e*m_e/(mu_mass*mu_mass)))

def dEdx(gamma):
	
	ln_arg = 2*m_e*beta2(gamma)*gamma*gamma/(I)

	val = K*z*z*Z*m_e*(1.0/beta2(gamma))*( np.log(ln_arg) - beta2(gamma))
	
	return val*np.power(10.0, -6)




