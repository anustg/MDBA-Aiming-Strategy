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

		num_bundle=18
		sm=2.4
		Model=one_key_start(
			casedir=casedir, 
			tower_h=200., # 150-300
			Q_rec=111.e6/0.51*sm, #2.4 is sm
			T_in=290+273.15,
			T_out=565+273.15,
			HTF='salt',
			rec_material='Incoloy800H',
			r_diameter=19, #15-25 sodium, 15-30
			r_height=20, #15-30 
			fluxlimitpath='../data/201015_N08811_thermoElasticPeakFlux_velocity_salt',
			SM=sm,
			oversizing=1., 	
			delta_r2=0.9, # sw thesis last chapter
			delta_r3=1.9, #
			hst_w=12.305, 
			hst_h=9.752,
			mirror_reflectivity=0.88,
			slope_error=0.0026,
			sunshape='pillbox',
			sunshape_param=4.65e-3*180./np.pi,
			num_rays=int(1e7),
			latitude=37.56,
			num_bundle=num_bundle
			)

		Model.big_field_generation()
		Model.annual_big_field()
		Model.determine_field()
		# input the number of tube bundles, number of flowpaths, pipe outer diameter and flow path pattern
		Model.flow_path_salt(num_bundle=num_bundle,num_fp=2,D0=45.,pattern='NES-NWS') 
		Model.MDBA_aiming_new(dni=930.,phi=0.,elevation=75.89)
		Model.annual_trimmed_field()


	def test_touching(self):
		if os.path.exists(self.tablefile):
			successed=1
		self.assertEqual(successed,1)
		#os.system('rm *.vtk')


if __name__ == '__main__':
	unittest.main()

