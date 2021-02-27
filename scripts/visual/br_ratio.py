import detector
import numpy as np 
import ROOT as root 

precision = 0.750
pi = 3.1415

def integral(function, x_range):
	npts = int((x_range[1] - x_range[0])*precision)
	step_size = (x_range[1] - x_range[0])/float(npts)
	pt_sum = 0.

	for n in range(npts):
		x = x_range[0] + float(n)*step_size
		pt_sum += function(x)*step_size

	return pt_sum

def integral2d(function, x_range, y_range):
	npts_y = (int((y_range[1] - y_range[0])*precision))
	pt_sum = 0.
	step_size = (y_range[1] - y_range[0])/float(npts_y)
	for n in range(npts_y):
		y = y_range[0] + float(n)*step_size

		def new_function(x):
			return function(x, y)

		pt_sum += integral(new_function, x_range)*step_size

	return pt_sum

def integral3d(function, x_range, y_range, z_range):
	npts_z = (int((z_range[1] - z_range[0])*precision))
	pt_sum = 0.
	step_size = (z_range[1] - z_range[0])/float(npts_z)
	for n in range(npts_z):
		z = z_range[0] + step_size*float(n)

		def new_function(x, y):
			return function(x, y, z)

		pt_sum += integral2d(new_function, x_range, y_range)*step_size

	return pt_sum


def identity(x, y, z):
	return x**2

def decay_pdf(x, y, z, gamma, tau):
	r = np.sqrt(x**2 + y**2 + z**2)
	v = np.sqrt(1. - 1./(gamma**2))

	pdf = (gamma / (v*tau)) * np.exp( -1.*r*gamma / (v * tau) )
	pdf = pdf / (4 * pi * r**2)

	return pdf

def decay_pdf_fix_gamma_tau(gamma, tau):
	def pdf(x, y, z):
		return decay_pdf(x, y, z, gamma, tau)
	return pdf

NPTS = 100

tau_min  = 10.
tau_max = 100000.

n_orders_of_magnitude = int(np.log10(tau_max/tau_min))
first_order = int(np.log10(tau_min))

N_Higgs = 10000000000.0
taus = []

for k in range(n_orders_of_magnitude):
	order = first_order + k 
	taus += [2*(n+1)*(10**order) for n in range(5) ]

print(taus)

m_higss = 125.0
m_a = [2.0, 10.0, 25.0]
eff = [0.05, 0.07, 0.10]
plots = [root.TGraph(len(taus)) for m in m_a]

fixed = decay_pdf_fix_gamma_tau(m_higss/(4.), 10. )

val = (integral3d( fixed, [-50., 50.], [60., 90.], [70., 170.]    ))

print(val)

for nm, m in enumerate(m_a):
	for k in range(len(taus)):
		tau = taus[k]
		fixed = decay_pdf_fix_gamma_tau(m_higss/(2*m), tau )

		val = (integral3d( fixed, [-50., 50.], [60., 90.], [70., 170.]    ))

		print(val)

		br = 6./(val*eff[nm]*N_Higgs)
		if br > 1.:
			continue
		plots[nm].SetPoint(k, tau, br)

canvas = root.TCanvas("c1")
canvas.SetLogx()
canvas.SetLogy()



for n, plot in enumerate(plots):
	plot.SetLineColor(n+2)

	if n == 0:
		plot.Draw("AC")
	else:
		plot.Draw("SAME C")

canvas.Print("pr.png", ".png")