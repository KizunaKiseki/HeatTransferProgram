import numpy as np
import matplotlib.pyplot as pl

import matplotlib
import matplotlib.cm as cm
import matplotlib.patches as patches
import matplotlib.path as path

from snippets.storage import ℕ1,ℕ2
from snippets.storage import get_nodes


def plot_evolution(Πs,βs,Δts):
	figure = pl.figure()
	axes = figure.add_subplot(1,1,1)
	axes.set_xlabel('Time, $t$ [hr]')
	axes.set_ylabel('Temperature, $T$ [K]')
	ls = ['-','--',':']
	for (k,(Π,β,Δt)) in enumerate(zip(Πs,βs,Δts)):
		t,T = Π.T
		axes.plot(t/3600,T,f'{ls[k]}C{k}',label=f'β={β:s}; Δt={Δt:s}')
	axes.legend()
	return figure


def draw_problem(mesh):
	x,y = get_nodes(mesh)
	
	figure,axes = setup_figure()
	draw_interior(axes,mesh,x,y)
	draw_exterior(axes,mesh,x,y)
	draw_nodes(axes,mesh,x,y)
	return figure


def draw_solution(mesh,T):
	x,y = get_nodes(mesh)
	
	figure,axes = setup_figure()
	draw_field(axes,mesh,x,y,T,'Temperature, $T$ [K]')
	draw_cells(axes,mesh,x,y)
	draw_exterior(axes,mesh,x,y)
	draw_nodes(axes,mesh,x,y)
	return figure


def setup_figure():
	figure = pl.figure()
	axes = figure. add_subplot(1,1,1)
	axes.set_aspect(1.0)
	axes.set_adjustable('datalim')
	axes.set_frame_on(False)
	axes.set_xticks([])
	axes.set_yticks([])
	return figure,axes


def draw_nodes(axes,mesh,x,y):
	axes.plot(x,y,'ko',ms=1,zorder=7)


def draw_field(axes,mesh,x,y,f,name):
	tri = mesh['IE'][ℕ2].values
	axes.tricontour(x,y,tri,f,levels=25,zorder=4,linewidths=0.5)
	c = axes.tricontourf(x,y,tri,f,levels=25)
	axes.get_figure().colorbar(c,ax=axes,label=name)


def draw_cells(axes,mesh,x,y):
	M = np.array([
		[1/3,1/3,1/3],
		[1/2,1/2, 0 ],
		[1/3,1/3,1/3],
		[ 0 ,1/2,1/2],
		[1/3,1/3,1/3],
		[1/2, 0 ,1/2]
		])
	
	n = mesh['IE'][ℕ2].values
	f = lambda x: (M@x[n].T).T.flatten()
	verticies = np.column_stack([f(x),f(y)])
	
	codes = [path.Path.MOVETO,path.Path.LINETO]*(verticies.shape[0]//2)
	pathdata = path.Path(verticies,codes)
	pathpatch = patches.PathPatch(pathdata,lw=0.3,alpha=0.5,zorder=5)
	axes.add_patch(pathpatch)


def draw_interior(axes,mesh,x,y):
	tri = mesh['IE'][ℕ2].values
	con = mesh['IE']['cid'].values
	colors = [matplotlib.colors.to_rgba(color) for color in mesh['IC']['color'].values]
	cmap = matplotlib.colors.ListedColormap(colors)
	axes.tripcolor(x,y,tri,con,cmap=cmap,edgecolor='k',lw=0.1)


def draw_exterior(axes,mesh,x,y):
	edg = mesh['BE'][ℕ1].values
	con = mesh['BE']['cid'].values
	colors = mesh['BC']['color'][con]
	for e,c in zip(edg,colors):
		axes.plot(x[e],y[e],'-',color=c,lw=4,zorder=6)


def plot_sparse(D,label='Coefficient Magnitude, $A_{ij} [-]$',partition=None):
	fig = pl.figure(figsize=(7.5,4))
	ax = fig.subplots(1,1)
	
	ax.set_xlabel('Column, $j$ [$\\#$]')
	ax.set_ylabel('Row, $i$ [$\\#$]')
	ax.set_xticks([])
	ax.set_yticks([])
	ax.xaxis.tick_top()
	ax.xaxis.set_label_position('top')
	
	# Draw matrix
	keys = np.array(list(D.keys()))
	a = np.array(list(D.values()))
	i = keys.shape[0]-keys[:,0]-1
	j = keys[:,1]
	scale = max(abs(a.min()),abs(a.max()))
	
	height = ax.get_window_extent().transformed(ax.get_figure().dpi_scale_trans.inverted()).height # inches
	dy = height/i.size
	fudge = 25
	size = (fudge*dy*72)**2 # convert to points!
	
	cmap = cm.get_cmap('viridis',9)
	c = ax.scatter(j,i,marker='o',linewidths=0,s=size,c=a,vmin=-scale,vmax=scale,cmap=cmap)
	if partition:
		ax.axhline(keys.shape[0]-partition-1+0.5,linestyle='-',color='k',linewidth=0.5)
		ax.axvline(partition-1+0.5,linestyle='-',color='k',linewidth=0.5)
	ax.set_xlim(j.min()-0.5,j.max()+0.5)
	ax.set_ylim(i.min()-0.5,i.max()+0.5)
	fig = ax.get_figure()
	fig.colorbar(c,ax=ax,label=label)
	ax.set_aspect(1.0)
	ax.set_anchor('C')
	
	return fig


def draw_element(mesh,kₑ):
	Nₙ = mesh['XY'].shape[0]
	Nₑ = mesh['IE'].shape[0]
	K = sp.dok_array((Nₙ,Nₙ))
	
	S = np.array([[0,1,0],[0,0,1]])
	E = np.array([[1,1,0],[0,1,1],[1,0,1]])/2
	M = np.array([[1,1,1],[1,1,1],[1,1,1]])/3
	R = np.array([[0,1],[-1,0]])
	D = np.array([[1,0,-1],[-1,1,0],[0,-1,1]])
	
	xₙ,yₙ = get_nodes(mesh)
	nodes = mesh['IE'][ℕ2].values
	
	n = nodes[kₑ]
	xₜ = xₙ[n]
	yₜ = yₙ[n]
	
	cid = mesh['IE']['cid'][kₑ]
	k = mesh['IC']['k'][cid]
	
	x = build_x(xₜ,yₜ)
	X = build_X(xₜ,yₜ)
	
	figure = pl.figure()
	axes = figure.add_subplot(1,1,1)
	axes.set_aspect('equal')
	
	axes.plot(x[:,0],x[:,1],'ks')
	axes.fill(x[:,0],x[:,1],color='C1',alpha=0.2)
	
	e = E@x
	m = M@x
	axes.plot(e[:,0],e[:,1],'ko')
	axes.plot(m[:,0],m[:,1],'kh')
	
	us = (E-M)@x
	axes.quiver(m[:,0],m[:,1],us[:,0],us[:,1],scale=1.0,scale_units='xy',color='C0')
	
	f = (E+M)@x/2
	uf = us@R
	axes.plot(f[:,0],f[:,1],'kd')
	axes.quiver(f[:,0],f[:,1],uf[:,0],uf[:,1],scale=1.0,scale_units='xy',color='C3')
	
	q = -D@uf
	l = np.abs(D)@e/2
	axes.plot(l[:,0],l[:,1],'kv')
	axes.quiver(l[:,0],l[:,1],q[:,0]/2,q[:,1]/2,scale=1.0,scale_units='xy',color='C4')
	
	return figure
