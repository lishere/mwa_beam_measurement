##########################################################
##################### CODE SETTINGS ######################
##########################################################

from subprocess          import Popen, PIPE

base_dir='/Users/benjaminmckinley/Code/git_Projects/mwa_beam_measurement'

# Print formatting
lb = "\n"+"*"*70+'\n'

# Fault codes
fault =  {1                : "TLE: %s\nin %s does not belong to satellite",
          2                : "TLE: %s\nin %s fails validity check",
          3                : "TLE: %s\nin %s is not time sequential",
          4                : "Time: Unknown time format",
          5                : "Ops: Undefined operation"}
          
# File locations
floc =   {'satdata'        : base_dir+'/BeamPlot/Data/Sat_Data.csv',
          'TLE'            : base_dir+'/BeamPlot/TLE',
          'TLEpath'        : base_dir+'/BeamPlot/TLE/%s.txt',
          'Nov2015'        : '/data/beam/Oct_16/Obs/Nov2015/satpasses.txt'}
          
# Read from file
read =   {'head'           : lambda f: Popen(['head', '-1', f],
                                             stdout=PIPE,stderr=PIPE).communicate()[0],
          'tail'           : lambda f: Popen(['tail', '-1', f],
                                             stdout=PIPE,stderr=PIPE).communicate()[0]}
          
# SpaceTrack Settings
STrack = {'login'          : ('j.rasti@student.unimelb.edu.au','12monkeysunimelb'),
          'cookies'        : base_dir+'/BeamPlot/Data/TLEcookies.txt',
          'dload'          : base_dir+'/BeamPlot/Data/TLEdownload.txt',
          'newTLE'         : 1420074000,
          'chunk'          : 1000*86400,
          'safety'         : 3*86400,
          'query'          : ("https://www.space-track.org/basicspacedata/query/"
                              "class/tle/NORAD_CAT_ID/%s/EPOCH/%s--%s/%sformat/tle/"),
          'request'        : ("wget --post-data='identity=%s&password=%s&query=%s' "
                              "--cookies=on --keep-session-cookies --save-cookies=%s "
                              "'https://www.space-track.org/ajaxauth/login' -O %s")}
                              
# Position data for calculation of satellite position using PyEphem lat/lon
coords = {'MWA'            :  ('-26.703319', '116.670815', 377.83),
          'Greenbank'      :  ( '38.432155', '-79.839803', 808.),
          'Unimelb'        :  ('-37.796929', '144.964242',  52.),
          'Curtin'         :  ('-32.006195', '115.894418',  18.),
          'Sunbury'        :  ('-37.579492', '114.728898', 220.)}
          
# Define default requirements for desired satellites
req_base = {'status':['Active']}        # don't want inactive sats
#exc_base = {'cls':['OC-F']}             # new class launched after obs round 1&2
#want these new ones now!
exc_base = {}

# Options for plotting of satellite data
pltopt = {'colour'         : lambda s: {'OC-G':'orange','OC-A':'r','OC-B':'indigo',
                                        'OC-C':'cyan','OC-D':'g','NOAA':'royalblue',
                                        'METOP':'lime' ,'METEOR':'darkred'}.get(s.cls,'k'),
          'label'          : lambda s: s.desig,
          'ls'             : lambda s: '-' if s.op=='Orbcomm' else '--',
          'azigap'         : 5,
          'ephemref'       : './Ephemref'}

#Range of observations, taken as max/min from obs_periods
obs_range = (1448335711.12, 1448851982.91)
obs_range_test =  (1448429025, 1448447953)

###END###
