import numpy as np
import scipy.sparse as sp

from Project.snippets.storage import ℕ1,ℕ2
from Project.snippets.storage import get_nodes

import matplotlib.pyplot as pl
import Project.snippets.plotting as plotting


Δz = 0.01 # m


def build_x(x,y):
	x = np.array([x,y]).T
	return x


def build_X(x,y):
	X = np.array([[1,1,1],x-x.mean(),y-y.mean()]).T
	return X


def build_capacity(mesh):
	Nₙ = mesh['XY'].shape[0]
	Nₑ = mesh['IE'].shape[0]
	C = sp.dok_array((Nₙ,Nₙ))
	
	xₙ,yₙ = get_nodes(mesh)
	nodes = mesh['IE'][ℕ2].values
	for kₑ in range(Nₑ):
		n = nodes[kₑ]
		xₜ = xₙ[n]
		yₜ = yₙ[n]
		
		# TODO: Implement Equations 22
		
		C[I,J] += Cₑ
	
	return C


def build_conduction(mesh):
	Nₙ = mesh['XY'].shape[0]
	Nₑ = mesh['IE'].shape[0]
	K = sp.dok_array((Nₙ,Nₙ))
	
	xₙ,yₙ = get_nodes(mesh)
	nodes = mesh['IE'][ℕ2].values
	for kₑ in range(Nₑ):
		n = nodes[kₑ]
		xₜ = xₙ[n]
		yₜ = yₙ[n]
		
		# TODO: Implement Equation 18
  
		pass
		
		I = n.reshape(3,1)
		J = n.reshape(1,3)
		K[I,J] += Kₑ
	
	return K


def build_generation(mesh):
	Nₙ = mesh['XY'].shape[0]
	Nₑ = mesh['IE'].shape[0]
	E = np.zeros(Nₙ)
	
	xₙ,yₙ = get_nodes(mesh)
	nodes = mesh['IE'][ℕ2].values
	for kₑ in range(Nₑ):
		n = nodes[kₑ]
		xₜ = xₙ[n]
		yₜ = yₙ[n]
		
		# TODO: Equation 26 ??? 
		# TODO: Implement one for steady and transient (if statements)
  
		pass
		
		E[n] += e*V
	
	return E


def steady_BCs(mesh,K,E):
	Nₑ = mesh['BE'].shape[0]
	xₙ,yₙ = get_nodes(mesh)
	nodes = mesh['BE'][ℕ1].values
	
	for kₑ in range(Nₑ):
		n = nodes[kₑ]
		cid = mesh['BE']['cid'][kₑ]
		qₑ = mesh['BC']['q'][cid]
		
		if np.isfinite(qₑ):
      
			# TODO: Implement Equation 39 
			pass
	
	for kₑ in range(Nₑ):
		n = nodes[kₑ]
		cid = mesh['BE']['cid'][kₑ]
		Tₑ = mesh['BC']['T'][cid]
		if np.isfinite(Tₑ):
      
			# TODO: Fixed Temperature???
			pass


def transient_BCs(mesh,C,K,E,T):
	Nₑ = mesh['BE'].shape[0]
	xₙ,yₙ = get_nodes(mesh)
	nodes = mesh['BE'][ℕ1].values
	for kₑ in range(Nₑ):
		n = nodes[kₑ]
		
		cid = mesh['BE']['cid'][kₑ]
		Tₑ = mesh['BC']['T'][cid]
		qₑ = mesh['BC']['q'][cid]
		if np.isfinite(Tₑ):
			# TODO: 
			pass
		if np.isfinite(qₑ):
			# TODO: Implement Equation 39 and multiply it by delta t
			pass
