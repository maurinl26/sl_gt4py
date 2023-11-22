import numpy as np

# TODO: fonction à itérer sur les id, jd
def filter(
    tracer_e: np.ndarray,
    tracer: np.ndarray,
    i_d: int, 
    j_d: int,
    nx: int,
    ny: int 
):
    """_summary_

    Args:
        tracer_e (np.ndarray): Grid point tracer at t + dt
        tracer (np.ndarray): Grid point tracer at t 
        i_d (int): departure point index 
        j_d (int): departure point index

        nx (int): _description_
        ny (int): _description_
    """
    
    # Sup du champ autour du point interpolé
    # Noyaux d'interpolation max
    tracer_sup = np.empty((nx, ny))
    for i in range(nx):
        for j in range(ny):
            tracer_sup[i, j] = max(tracer[i_d, j_d], tracer[i_d, j_d], tracer[i_d + 1, j_d], tracer[i_d + 1, j_d + 1])
    
    # Surplus
    overshoot = np.max(tracer_e - tracer_sup, 0)
    
    ###### Bottom left corner 
    i, j = 0, 0
    slot_4 = max(tracer_sup[0,0] - tracer_e[0+1, 0], 0)
    slot_5 = max(tracer_sup[0,0] - tracer_e[0+1, 0+1], 0)
    slot_6 = max(tracer_sup[0,0] - tracer_e[0, 0+1], 0)

    total_disp = slot_4 + slot_5 + slot_6
                      
    if total_disp > overshoot[0, 0]:
        tracer_e[0+1, 0] += (slot_4 / total_disp) * overshoot[0, 0]
        tracer_e[0+1, 0+1] += (slot_5 / total_disp) * overshoot[0, 0]
        tracer_e[0, 0+1] += (slot_6 / total_disp) * overshoot[0, 0]


    ####### Bottom right corner 
    # Distribution en cas d'overshoot
    i, j = nx - 1, 0
    
    slot_6 = max(tracer_sup[i,j] - tracer_e[i, j+1], 0)
    slot_7 = max(tracer_sup[i,j] - tracer_e[i-1, j+1], 0)
    slot_8 = max(tracer_sup[i,j] - tracer_e[i-1, j], 0)
            
    total_disp = slot_6 + slot_7 + slot_8
         
    if total_disp > overshoot[i, j]:
        tracer_e[i, j+1] += (slot_6 / total_disp) * overshoot[i, j]
        tracer_e[i-1, j+1] += (slot_7 / total_disp) * overshoot[i, j]
        tracer_e[i-1, j] += (slot_8 / total_disp) * overshoot[i, j]
  
  
    ######## Upper left corner
    i, j = 0, ny - 1
    slot_2 = max(tracer_sup[i,j] - tracer_e[i, j-1], 0)
    slot_3 = max(tracer_sup[i,j] - tracer_e[i+1 , j-1], 0)
    slot_4 = max(tracer_sup[i,j] - tracer_e[i+1, j], 0)

    total_disp = slot_2 + slot_3 + slot_4
                    
    if total_disp > overshoot[i, j]:
        tracer_e[i, j-1] += (slot_2 / total_disp) * overshoot[i, j]
        tracer_e[i+1, j-1] += (slot_3 / total_disp) * overshoot[i, j]
        tracer_e[i+1, j] += (slot_4 / total_disp) * overshoot[i, j]
 
    
    ######## Upper right corner 
    i, j = nx - 1, ny - 1
    # Distribution en cas d'overshoot
    slot_1 = max(tracer_sup[i,j] - tracer_e[i-1, j-1], 0)
    slot_2 = max(tracer_sup[i,j] - tracer_e[i, j-1], 0)
    slot_8 = max(tracer_sup[i,j] - tracer_e[i-1, j], 0)
            
    total_disp = slot_1 + slot_2 + slot_8
        
    if total_disp > overshoot[i, j]:
        tracer_e[i-1, j-1] += (slot_1 / total_disp) * overshoot[i, j]
        tracer_e[i, j-1] += (slot_2 / total_disp) * overshoot[i, j]
        tracer_e[i-1, j] += (slot_8 / total_disp) * overshoot[i, j]
    
    
    ####### left border 
    i = 0
    for j in range(1, ny - 1):
        slot_2 = max(tracer_sup[i,j] - tracer_e[i, j-1], 0)
        slot_3 = max(tracer_sup[i,j] - tracer_e[i+1 , j-1], 0)
        slot_4 = max(tracer_sup[i,j] - tracer_e[i+1, j], 0)
        slot_5 = max(tracer_sup[i,j] - tracer_e[i+1, j+1], 0)
        slot_6 = max(tracer_sup[i,j] - tracer_e[i, j+1], 0)

                
        total_disp = (
                    slot_2 + slot_3 + slot_4
                    + slot_5 + slot_6
                )
                        
        if total_disp > overshoot[i, j]:
            tracer_e[i, j-1] += (slot_2 / total_disp) * overshoot[i, j]
            tracer_e[i+1, j-1] += (slot_3 / total_disp) * overshoot[i, j]
            tracer_e[i+1, j] += (slot_4 / total_disp) * overshoot[i, j]
            tracer_e[i+1, j+1] += (slot_5 / total_disp) * overshoot[i, j]
            tracer_e[i, j+1] += (slot_6 / total_disp) * overshoot[i, j]

  
    ######## Right border
    i = nx - 1
    for j in range(1, ny - 1):
        slot_1 = max(tracer_sup[i,j] - tracer_e[i-1, j-1], 0)
        slot_2 = max(tracer_sup[i,j] - tracer_e[i, j-1], 0)
        slot_6 = max(tracer_sup[i,j] - tracer_e[i, j+1], 0)
        slot_7 = max(tracer_sup[i,j] - tracer_e[i-1, j+1], 0)
        slot_8 = max(tracer_sup[i,j] - tracer_e[i-1, j], 0)
                
        total_disp = (
                    slot_1 + slot_2 + slot_6 + slot_7 + slot_8
                )
                        
        if total_disp > overshoot[i, j]:
            tracer_e[i-1, j-1] += (slot_1 / total_disp) * overshoot[i, j]
            tracer_e[i, j-1] += (slot_2 / total_disp) * overshoot[i, j]
            tracer_e[i, j+1] += (slot_6 / total_disp) * overshoot[i, j]
            tracer_e[i-1, j+1] += (slot_7 / total_disp) * overshoot[i, j]
            tracer_e[i-1, j] += (slot_8 / total_disp) * overshoot[i, j]
    
    
    ####### Bottom border
    j = 0
    for i in range(1, nx - 1):
        slot_4 = max(tracer_sup[i,j] - tracer_e[i+1, j], 0)
        slot_5 = max(tracer_sup[i,j] - tracer_e[i+1, j+1], 0)
        slot_6 = max(tracer_sup[i,j] - tracer_e[i, j+1], 0)
        slot_7 = max(tracer_sup[i,j] - tracer_e[i-1, j+1], 0)
        slot_8 = max(tracer_sup[i,j] - tracer_e[i-1, j], 0)
                
        total_disp = (
                    slot_4
                    + slot_5 + slot_6 + slot_7 + slot_8
                )
                        
        if total_disp > overshoot[i, j]:
            tracer_e[i+1, j] += (slot_4 / total_disp) * overshoot[i, j]
            tracer_e[i+1, j+1] += (slot_5 / total_disp) * overshoot[i, j]
            tracer_e[i, j+1] += (slot_6 / total_disp) * overshoot[i, j]
            tracer_e[i-1, j+1] += (slot_7 / total_disp) * overshoot[i, j]
            tracer_e[i-1, j] += (slot_8 / total_disp) * overshoot[i, j]
    
    
    ####### Upper border 
    j = ny - 1
    for i in range(1, nx - 1):
        slot_1 = max(tracer_sup[i,j] - tracer_e[i-1, j-1], 0)
        slot_2 = max(tracer_sup[i,j] - tracer_e[i, j-1], 0)
        slot_3 = max(tracer_sup[i,j] - tracer_e[i+1 , j-1], 0)
        slot_4 = max(tracer_sup[i,j] - tracer_e[i+1, j], 0)
        slot_8 = max(tracer_sup[i,j] - tracer_e[i-1, j], 0)
                
        total_disp = (
                    slot_1 + slot_2 + slot_3 + slot_4
                    + slot_8
                )
                        
        if total_disp > overshoot[i, j]:
            tracer_e[i-1, j-1] += (slot_1 / total_disp) * overshoot[i, j]
            tracer_e[i, j-1] += (slot_2 / total_disp) * overshoot[i, j]
            tracer_e[i+1, j-1] += (slot_3 / total_disp) * overshoot[i, j]
            tracer_e[i+1, j] += (slot_4 / total_disp) * overshoot[i, j]
            tracer_e[i-1, j] += (slot_8 / total_disp) * overshoot[i, j]
    
    
    # Inner domain
    for i in range(1, nx - 1):
        for j in range(1, ny - 1):
            # Distribution en cas d'overshoot
            slot_1 = max(tracer_sup[i,j] - tracer_e[i-1, j-1], 0)
            slot_2 = max(tracer_sup[i,j] - tracer_e[i, j-1], 0)
            slot_3 = max(tracer_sup[i,j] - tracer_e[i+1 , j-1], 0)
            slot_4 = max(tracer_sup[i,j] - tracer_e[i+1, j], 0)
            slot_5 = max(tracer_sup[i,j] - tracer_e[i+1, j+1], 0)
            slot_6 = max(tracer_sup[i,j] - tracer_e[i, j+1], 0)
            slot_7 = max(tracer_sup[i,j] - tracer_e[i-1, j+1], 0)
            slot_8 = max(tracer_sup[i,j] - tracer_e[i-1, j], 0)
            
            total_disp = (
                slot_1 + slot_2 + slot_3 + slot_4
                + slot_5 + slot_6 + slot_7 + slot_8
            )
                    
            # inner domain
            if total_disp > overshoot[i, j]:
                tracer_e[i-1, j-1] += (slot_1 / total_disp) * overshoot[i, j]
                tracer_e[i, j-1] += (slot_2 / total_disp) * overshoot[i, j]
                tracer_e[i+1, j-1] += (slot_3 / total_disp) * overshoot[i, j]
                tracer_e[i+1, j] += (slot_4 / total_disp) * overshoot[i, j]
                tracer_e[i+1, j+1] += (slot_5 / total_disp) * overshoot[i, j]
                tracer_e[i, j+1] += (slot_6 / total_disp) * overshoot[i, j]
                tracer_e[i-1, j+1] += (slot_7 / total_disp) * overshoot[i, j]
                tracer_e[i-1, j] += (slot_8 / total_disp) * overshoot[i, j]
  
                

            
