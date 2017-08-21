#############################################################
####################  SATELLITE TLE  ########################
#############################################################

import os, time
from BeamPlot.TimeMethods  import tm
from BeamPlot.Settings     import floc, STrack as ST, fault, read


class TLE_config(object):

    def __init__(self, sat, tmax, uid=ST['login'],lim=None):
        self.sat = sat.ID                              # Associate class instance to NORAD ID
        print "Sat is %s" % self.sat
        self.tlefile = floc['TLEpath']%self.sat        # Define TLE database location for sat
        print "looking in %s " % self.tlefile
       
        # Use tail to check last TLE, update if required
        tmax = tm(tmax)
        print "tmax is %s" % tmax
        result = read['tail'](self.tlefile)
        #print "result is %s" % result
        tlelast = tm(result, 'tle') if result else tm(ST['newTLE'])
        #print "tlelast was %s"  % tlelast
        tlelast.utc = tlelast.utc + 100000
        #print "tlelast is now %s" % tlelast
        #print "tm(ST['newTLE'] is %s" % tm(ST['newTLE'])
        #print "tlelast is %s " % tlelast
        print 'Sat %s: Checking database...'%self.sat,
        
        # If required, repeatedly pull tles from SpaceTrack until all>tmax 
        while tlelast < tmax:   
            #wait for 5 secs as you are only allowed 20 queries per minute
            time.sleep(5)            
            dfrom, dupto = tm(tlelast-ST['safety']), tm(tlelast+ST['chunk'])
            query = ST['query']%(self.sat,dfrom,dupto,'limit/%d/' if lim else "")
            print "Requesting update from SpaceTrack:\n\n%s\n"%query
            os.system(ST['request']%(uid[0],uid[1],query,ST['cookies'],ST['dload']))
            print 'Validating and distributing to database...',
            #print ST['dload']
            with open(ST['dload']) as f:
                for d in f:
                    tlestring = '%s,%s\n'%(d.strip(),f.next().strip())
                    tletime = tm(tlestring, 'tle')
                    if tletime > tlelast:
                        open(self.tlefile,'a').write(tlestring)
                        tlelast = tletime
            if dupto > tmax:
                break
            tlelast=tm(tlelast+chunk)
        print 'OK'
        
        self.data = open(self.validate())              # Validate then mount database
        self.load()                                    # Load initial TLE
    
    def load(self):
        self.data.seek(0)                              # For backtracking
        self.now = self.data.next().strip()            # Set first available TLE
        self.nxt = self.data.next().strip()            # Set next available TLE
    
    def mount(self, t):
        t = tm(t)                                      # Convert to tm time
        if tm(self.now, 'tle') > t:                    # For backtracking
	    self.load()
        while tm(self.nxt, 'tle') <= t:  
           # Find last TLE before t
           try:              
              self.now = self.nxt
              self.nxt = self.data.next().strip()
           except StopIteration:
               break
        return self.now

    def validate(self):
        #tprev = None
        #for line in open(self.tlefile):
        #    tle1, tle2 =  line.strip().split(',')
        #    if tle1[2:7]!=self.sat:                              # Verify TLE belongs to sat
        #        raise AttributeError(fault[1]%(tle1[:32],self.sat))
        #    for i in (tle1,tle2):                                # Verify len./checksum
        #        check = sum(int(c) for c in i[:-1].replace('-','1') if c.isdigit())
        #        if not len(i)==69 or not str(check)[-1]==i[-1]:
        #            raise AttributeError(fault[2]%(tle1[:32],self.sat))
        #    tnow = tm(tle1, 'tle')                               # Verify sequential dates
        #    if not tprev or tnow>=tprev:
        #        tprev=tm(tnow)
        #    else:
        #        raise AttributeError(fault[3]%(tle1[:32],self.sat))
        return self.tlefile

###END###
