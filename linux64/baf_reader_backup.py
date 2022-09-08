class ml1:
	# this is v1
    def __init__(self, fname, mslevel=1):
        import sqlite3, os
        import numpy as np
        import baf2sql
        self.mslevel = mslevel
        self.specs = None
        self.fname = fname
        self.infile = os.path.join('/data', self.fname, "analysis.baf")
        self.bs = baf2sql.BinaryStorage(self.infile)
        sqlite_fn = baf2sql.getSQLiteCacheFilename(self.infile)
        self.con = sqlite3.connect(sqlite_fn)
        self.path = os.path.join('/data', self.fname, f"mm8_sl{mslevel}_v1.sqlite")
        self.ppath = os.path.join('/data', self.fname, f"mm8_sl{mslevel}_v1.p")
        self.query()
    def query(self):
        import sqlite3
        import numpy as np
        q = self.con.execute(f"SELECT s.Id, LineIndexId, LineMzId, LineIntensityId, Rt "
                             f"FROM Spectra s JOIN AcquisitionKeys ak ON s.AcquisitionKey=ak.Id "
                             f"WHERE LineIntensityId NOT NULL AND ak.MsLevel={self.mslevel} ORDER BY Rt")
        data = q.fetchall()
        if len(data) > 0 :
            res = []
            for i in range(len(data)):
                ms_mz = self.bs.readArrayDouble(data[i][1])
                if len(ms_mz) > 0:
                    ares = np.zeros((4, len(ms_mz)))
                    ares[0] = data[i][0]
                    ares[1] = ms_mz
                    ares[2] = self.bs.readArrayDouble(data[i][2])
                    ares[3] = self.bs.readArrayDouble(data[i][3]) # lineIntensityId
                    res.append(ares)
                else:
                    print(f'scanID {i} not found - moving on')
            self.specs = np.concatenate(res, axis=1)
        else:
            self.specs = 0


class Exp:
    def __init__(self, fname, type='edata', verbosity=0):
        import sqlite3, os
        import baf2sql
        self.fname = fname
        self.infile = os.path.join('/data', self.fname, "analysis.baf")
        if verbosity == 1:
            print('connecting to baf binary storage')
        self.bs = baf2sql.BinaryStorage(self.infile)
        if verbosity == 1:
            print('sqlitecache filename')
        sqlite_fn = baf2sql.getSQLiteCacheFilename(self.infile)
        if verbosity == 1:
            print('establish sqlite connection')
        self.con = sqlite3.connect(sqlite_fn)
        self.con.row_factory = sqlite3.Row
        self.outfile_l1 = os.path.join('/data', self.fname, f"mm8v2_{type}_L1.p")
        self.outfile_l2 = os.path.join('/data', self.fname, f"mm8v2_{type}_L2.p")
        self.properties = None
        if verbosity == 1:
            print('collecting experiment properties')
        self.collectProp()
        self.nSpectra = None
        self.nl1Spectra=None
        self.nl2Spectra = None
        self.sdata=None
        if type == 'meta':
            if verbosity == 1:
                print('collecting exp metadata')
            self.collectMeta()
        else:
            if verbosity == 1:
                print('collecting spectral data')
            self.collectSpecL1()
            self.collectSpecL2()
        self.con.close()
    def collectProp(self):
        q=self.con.execute(f"select * from Properties")
        res = [dict(x) for x in q.fetchall()]
        prop = {}; [prop.update({x['Key']: x['Value']}) for x in res]
        self.properties = prop
    def collectMeta(self):
        q = self.con.execute(f"select * from SupportedVariables")
        vlist = [dict(x) for x in q.fetchall()]
        vdict = {x['Variable']: x for x in vlist}
        qst = "SELECT * FROM Spectra as s JOIN AcquisitionKeys as ak ON s.AcquisitionKey=ak.Id ORDER BY Rt"
        res = [dict(x) for x in self.con.execute(qst).fetchall()]
        self.nSpectra = len(res)
        cvar = [x for x in list(res[0].keys()) if ('Id' in x)]
        edat = {x: [] for x in cvar}
        for i in range(self.nSpectra):
            mets = {x: res[i][x] for x in res[i] if not ('Id' in x)}
            q = self.con.execute(f"select * from PerSpectrumVariables WHERE Spectrum = {i}")
            specVar = [dict(x) for x in q.fetchall()]
            mets.update({vdict[k['Variable']]['PermanentName']: k['Value'] for k in specVar})
            edat[cvar[0]].append(mets)
    def collectSpecL1(self):
        import pickle
        q=self.con.execute(f"select * from SupportedVariables")
        vlist=[dict(x) for x in q.fetchall()]
        vdict={x['Variable']: x for x in vlist}
        qst="SELECT * FROM Spectra as s JOIN AcquisitionKeys as ak ON s.AcquisitionKey=ak.Id WHERE Segment=3 AND ScanMode=5 ORDER BY Rt"
        res=[dict(x) for x in self.con.execute(qst).fetchall()]
        self.nL1Spectra=len(res)
        cvar=['sinfo', 'LineIndexId', 'LineMzId', 'LineIntensityId']
        edat = {x : [] for x in cvar}
        for i in range(self.nL1Spectra):
            mets={x:  res[i][x] for x in res[i] if not ('Id' in x)}
            q=self.con.execute(f"select * from PerSpectrumVariables WHERE Spectrum = {res[i]['Id']}")
            specVar=[dict(x) for x in q.fetchall()]
            mets.update({vdict[k['Variable']]['PermanentName']: k['Value'] for k in specVar})
            mets.update({'Id': res[i]['Id']})
            edat[cvar[0]].append(mets)
            for j in cvar[1:]:
                if (res[i][j] is not None):
                    edat[j].append((res[i]['Id'], self.bs.readArrayDouble(res[i][j])))
        self.edataL1=edat
        pickle.dump(self.edataL1, open(self.outfile_l1, 'wb'))
    def collectSpecL2(self):
        import pickle
        q=self.con.execute(f"select * from SupportedVariables")
        vlist=[dict(x) for x in q.fetchall()]
        vdict={x['Variable']: x for x in vlist}
        qst="SELECT * FROM Spectra as s JOIN AcquisitionKeys as ak ON s.AcquisitionKey=ak.Id WHERE Segment=3 AND ScanMode=0 ORDER BY Rt"
        res=[dict(x) for x in self.con.execute(qst).fetchall()]
        self.nL2Spectra=len(res)
        cvar = ['sinfo', 'LineIndexId', 'LineMzId', 'LineIntensityId']
        edat = {x: [] for x in cvar}
        for i in range(self.nL1Spectra):
            mets = {x: res[i][x] for x in res[i] if not ('Id' in x)}
            q = self.con.execute(f"select * from PerSpectrumVariables WHERE Spectrum = {res[i]['Id']}")
            specVar = [dict(x) for x in q.fetchall()]
            mets.update({vdict[k['Variable']]['PermanentName']: k['Value'] for k in specVar})
            mets.update({'Id': res[i]['Id']})
            edat[cvar[0]].append(mets)
            for j in cvar[1:]:
                if (res[i][j] is not None):
                    edat[j].append((res[i]['Id'], self.bs.readArrayDouble(res[i][j])))
        self.edataL2=edat
        pickle.dump(self.edataL2, open(self.outfile_l2, 'wb'))   
