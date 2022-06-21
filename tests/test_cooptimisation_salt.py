#! /bin/env python3

from __future__ import division
import unittest

import os
import numpy as np


class TestCooptimisationSalt(unittest.TestCase):
	def setUp(self):

		from mdbapy.one_key_co_optimisation import one_key_start
		from mdbapy.cal_sun import SunPosition
		from mdbapy.cal_layout_r import radial_stagger, aiming_cylinder
		from mdbapy.Deviation_aiming_new3 import aiming
		from mdbapy.Open_CSPERB import eval_v_max, Cyl_receiver
		from mdbapy.Open_CSPERB_plots import tower_receiver_plots
		from mdbapy.HC import Na
		from mdbapy.Tube_materials import Inconel740H
		from mdbapy.Flux_reader import read_data
		from mdbapy.Loss_analysis import receiver_correlation
		from mdbapy.output_motab import output_motab, output_matadata_motab
		from mdbapy.python_postprocessing import proces_raw_results, get_heliostat_to_receiver_data
		from mdbapy.SOLSTICE import SolsticeScene

		casedir='TEST-COOPTIMISATION-SALT'
		self.tablefile=casedir+'/OELT_Solstice.motab'

		if not os.path.exists(casedir):
			os.makedirs(casedir)

		Model=one_key_start(
			casedir=casedir, 
			tower_h=180., 
			Q_rec=111.e6/0.51*2.4,
			T_in=290+273.15,
			T_out=565+273.15,
			HTF='salt',
			rec_material='Haynes230',
			r_diameter=25.,
			r_height=24.,
			fluxlimitpath='../data/201015_N06230_thermoElasticPeakFlux_velocity_salt',
			SM=2.4,
			oversizing=1., 	
			delta_r2=0.9,
			delta_r3=1.9,
			hst_w=12.,
			hst_h=12.,
			mirror_reflectivity=0.95,
			slope_error=1.5e-3,
			sunshape='pillbox',
			sunshape_param=4.65e-3*180./np.pi,
			num_rays=int(1e6),
			latitude=34.85,
			)

		#Model.big_field_generation()
		#Model.annual_big_field()
		#Model.determine_field()
		
		# input the number of tube bundles, number of flowpaths, pipe outer diameter and flow path pattern
		Model.flow_path_salt(num_bundle=12,num_fp=2,D0=48.26,pattern='NES-NWS') 
		#Model.test_DS_aiming()
		Model.annual_trimmed_field()


	def test_touching(self):
		if os.path.exists(self.tablefile):
			successed=1
		self.assertEqual(successed,1)
		#os.system('rm *.vtk')


if __name__ == '__main__':
	unittest.main()

