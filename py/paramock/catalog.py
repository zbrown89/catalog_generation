
import healpy as hp
import numpy as np

class catalog:

    def __init__(self):
        self._centers = None
        self._rims    = None
        self._flats   = None
        self._clumps_center = None
        self._clumps_flat   = None

    @property
    def centers(self):
        return self._centers
    @centers.setter
    def centers(self, centers):
        self._centers = centers

    @property
    def rims(self):
        return self._rims
    @rims.setter
    def rims(self, rims):
        self._rims = rims

    @property
    def flats(self):
        return self._flats
    @flats.setter
    def flats(self, flats):
        self._flats = flats

    @property
    def clumps_center(self):
        return self._clumps_center
    @clumps_center.setter
    def clumps_center(self, clumps_center):
        self._clumps_center = clumps_center

    @property
    def clumps_flat(self):
        return self._clumps_flat
    @clumps_flat.setter
    def clumps_flat(self, clumps_flat):
        self._clumps_flat = clumps_flat

    def flatten(self):
        rs      = []
        decs    = []
        ras     = []
        types   = []
        parents = []
        names   = []
        try:
            for key in self.centers:
                rs.append(self.centers[key].r)
                decs.append(self.centers[key].dec)
                ras.append(self.centers[key].ra)
                types.append(self.centers[key].TYPE)
                parents.append(self.centers[key].parent)
                names.append(self.centers[key].name)
        except Exception as e:
            no_centers = True
        try:
            for key in self.rims:
                rs.append(self.rims[key].r)
                decs.append(self.rims[key].dec)
                ras.append(self.rims[key].ra)
                types.append(self.rims[key].TYPE)
                parents.append(self.rims[key].parent)
                names.append(self.rims[key].name)
        except Exception as e:
            no_rims = True
        try:
            for key in self.flats:
                rs.append(self.flats[key].r)
                decs.append(self.flats[key].dec)
                ras.append(self.flats[key].ra)
                types.append(self.flats[key].TYPE)
                parents.append(self.flats[key].parent)
                names.append(self.flats[key].name)
        except Exception as e:
            no_flats = True
        try:
            for key in self.clumps_center:
                rs.append(self.clumps_center[key].r)
                decs.append(self.clumps_center[key].dec)
                ras.append(self.clumps_center[key].ra)
                types.append(self.clumps_center[key].TYPE)
                parents.append(self.clumps_center[key].parent)
                names.append(self.clumps_center[key].name)
        except Exception as e:
            no_cc = True
        try:
            for key in self.clumps_flat:
                rs.append(self.clumps_flat[key].r)
                decs.append(self.clumps_flat[key].dec)
                ras.append(self.clumps_flat[key].ra)
                types.append(self.clumps_flat[key].TYPE)
                parents.append(self.clumps_flat[key].parent)
                names.append(self.clumps_flat[key].name)
        except Exception as e:
            no_cf = True
        return rs, ras, decs, types, parents, names

    def plot(self, idx):
        # the position of the galaxy with idx is retrieved first
        # the position of the other galaxies will be plotted with respect to this galaxy
        x_cen, y_cen, z_cen, b_cen = self.get_points(idx)
        from mpl_toolkits.mplot3d import Axes3D
        import matplotlib.pyplot as plt
        fig = plt.figure()
        ax  = fig.add_subplot(111, projection='3d')
        x, y, z, c = self.get_points(idx, get_childs=True)
        ax.scatter(xs=np.asarray(x).flatten()-x_cen[0],
                   ys=np.asarray(y).flatten()-y_cen[0],
                   zs=np.asarray(z).flatten()-z_cen[0],
                   c=c, s=6)
        plt.show()
        
    def get_points(self, idx, get_childs=False):
        x = []
        y = []
        z = []
        c = []
        if len(idx.split("cen_"))>1:
            unit_vector = hp.ang2vec(self.centers[idx].phi, self.centers[idx].theta, lonlat=True)
            curr_vector = (unit_vector * self.centers[idx].r)[0]
            #print(curr_vector)
            x.append(curr_vector[0])
            y.append(curr_vector[1])
            z.append(curr_vector[2])
            c.append("b")
            if not get_childs:
                return x, y, z, c
            for key in self.centers[idx].childs:
                x_, y_, z_, c_ = self.get_points(key, get_childs)
                x.append(x_[0])
                y.append(y_[0])
                z.append(z_[0])
                c.append(c_[0])
        if len(idx.split("rim_"))>1:
            unit_vector = hp.ang2vec(self.rims[idx].phi, self.rims[idx].theta, lonlat=True)
            curr_vector = (unit_vector * self.rims[idx].r)[0]
            x.append(curr_vector[0])
            y.append(curr_vector[1])
            z.append(curr_vector[2])
            c.append("red")
            if not get_childs:
                return x, y, z, c
            for key in self.rims[idx].childs:
                x_, y_, z_, c_ = self.get_points(key, get_childs)
                x.append(x_[0])
                y.append(y_[0])
                z.append(z_[0])
                c.append(c_[0])
        if len(idx.split("cenClump_"))>1:
            unit_vector = hp.ang2vec(self.clumps_center[idx].phi, self.clumps_center[idx].theta, lonlat=True)
            curr_vector = (unit_vector * self.clumps_center[idx].r)[0]
            x.append(curr_vector[0])
            y.append(curr_vector[1])
            z.append(curr_vector[2])
            c.append("green")
        if len(idx.split("flatClump_"))>1:
            unit_vector = hp.ang2vec(self.clumps_flat[idx].phi, self.clumps_flat[idx].theta, lonlat=True)
            curr_vector = (unit_vector * self.clumps_flat[idx].r)[0]
            x.append(curr_vector[0])
            y.append(curr_vector[1])
            z.append(curr_vector[2])
            c.append("blue")
        return x, y, z, c
            
    def info(self, idx, print_childs=False):
        if len(idx.split("cen_"))>1:
            self.centers[idx].info()
            if not print_childs:
                return
            for key in self.centers[idx].childs:
                self.info(key, print_childs)
        if len(idx.split("rim_"))>1:
            self.rims[idx].info()
            if not print_childs:
                return
            for key in self.rims[idx].childs:
                self.info(key, print_childs)
        if len(idx.split("cenClump_"))>1:
            self.clumps_center[idx].info()
        if len(idx.split("flatClump_"))>1:
            self.clumps_flat[idx].info()

    def get_seed(self, idx):
        split_idx = idx.split()
        # first lets do the clumps, that is the hard one
        if len(split_idx[0].split("cen"))>1:
            # this means the seed is either a center galaxy or a rim galaxy
            seed_type = "cen"
            # decode the rest of the idx and find the respective seed
            seed_idx1 = int(split_idx[1])
            seed_idx2 = int(split_idx[2])
            self.info("{}_{}".format(seed_type, seed_idx1), print_childs=True)
        else:
            # that means the seed is a flat galaxy
            seed_type = "flat"
