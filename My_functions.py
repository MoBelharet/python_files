# +
import matplotlib.pyplot as plt
import matplotlib as mpl

def reverse_colourmap(cmap, name = 'my_cmap_r'):
    """
    In: 
    cmap, name 
    Out:
    my_cmap_r

    Explanation:
    t[0] goes from 0 to 1
    row i:   x  y0  y1 -> t[0] t[1] t[2]
                   /
                  /
    row i+1: x  y0  y1 -> t[n] t[1] t[2]

    so the inverse should do the same:
    row i+1: x  y1  y0 -> 1-t[0] t[2] t[1]
                   /
                  /
    row i:   x  y1  y0 -> 1-t[n] t[2] t[1]
    """        
    reverse = []
    k = []   

    for key in cmap._segmentdata:    
        k.append(key)
        channel = cmap._segmentdata[key]
        data = []

        for t in channel:                    
            data.append((1-t[0],t[2],t[1]))            
        reverse.append(sorted(data))    

    LinearL = dict(zip(k,reverse))
    my_cmap_r = mpl.colors.LinearSegmentedColormap(name, LinearL) 
    return my_cmap_r

##################################################################################################################
# PLOT CURVES
##################################################################################################################

def plot_variables(variables):
    fig = plt.figure(figsize=(10,6))
    nb = int(np.ceil(len(variables)/2))
    cptr = 0
    
    for var in variables:
        cptr+=1
        ax = fig.add_subplot(nb,2,cptr)
        for flag in flags:
            ldict = {}
            exec("v =" +  var + flag , globals(),ldict)
            v = ldict['v'] 
            #print(v.shape)
            if(v.ndim == 1):
                v_mean = v
            elif(v.ndim == 2):
                v_mean = v[:,0]
            else:
                print("coucou")
               
            plt.plot(v_mean[ndt_min:ndt_max])
            
        
        plt.xticks(fontsize=7)
        plt.yticks(fontsize=7)
        plt.title(var , fontsize=12) 
        plt.ylabel("$µmol\ L^{-1}$",fontsize=8)
        plt.xlabel("Time steps",fontsize=8)
        plt.legend(["with FABM", "standard"])

    # Space between subplots
    fig.tight_layout(pad=1.5)

##################################################################################################################
# PLOT VERTICAL PROFILES
##################################################################################################################

def plot_vertical_profiles(variables , dep):

    
    fig = plt.figure(figsize=(10,8))
  
    nb = int(np.ceil(len(variables)/3))
    cptr = 0
    for var in variables:
        cptr+=1
        ax = fig.add_subplot(nb,3,cptr)
        
        for flag in flags:
            ldict = {}
            exec("v =" +  var + flag , globals(),ldict)
            v = ldict['v']
            if(v.ndim > 1):
                v_mean = np.mean(v,axis=0)
            else:
                v_mean = v
            
            plt.plot(v_mean,-dep)

        plt.xticks(fontsize=7)
        plt.yticks(fontsize=7)
        plt.title(var , fontsize=12) 
        plt.xlabel("$µmol\ L^{-1}$",fontsize=8)
        plt.ylabel("Depth (m)",fontsize=8)
        plt.legend(["with FABM", "standard"])

    # Space between subplots
    fig.tight_layout(pad=1.5)

##################################################################################################################
# PLOT HOVMOLLER 
##################################################################################################################
def plot_hovmoller(variables, depth_limits, time_limits):
    depth_min = depth_limits[0]
    depth_max = depth_limits[1]
    dep_min_id = np.asarray(np.where(depth>=depth_min))[0,0]
    dep_max_id = np.asarray(np.where(depth<=depth_max))[0,-1]

    ndt_min = time_limits[0]
    ndt_max = time_limits[1]
    

    fig = plt.figure(figsize=(10,6))
    my_cmap = reverse_colourmap(plt.cm.Spectral)
    
    nb = int(np.ceil(len(variables)/2))
    cptr = 0
    for var in variables:
        cptr+=1
        ax = fig.add_subplot(nb,2,cptr)
        ldict = {}
        exec("v_fabm =" +  var + "_fabm[" + str(ndt_min) + ":" + str(ndt_max) + "," + str(dep_min_id) + ":" + str(dep_max_id) + "]", globals(),ldict)
        v_fabm = ldict['v_fabm']

        v_anomaly = np.transpose(v_fabm)

        x = np.arange(0,v_anomaly.shape[1])*t_step
        [X,dep] = np.meshgrid(x,depth[dep_min_id:dep_max_id])
        
        pc = ax.pcolormesh(X,-dep,v_anomaly,cmap=my_cmap,shading="gouraud") #"shading = "gouraud" "nearest"
        clb=fig.colorbar(pc)
        #pc.set_clim(0,10)
        plt.title(var , fontsize=12)
        plt.xlabel("Time (h)")
        plt.ylabel("Depth (m)")

    # Space between subplots
    fig.tight_layout(pad=1.5)


 
