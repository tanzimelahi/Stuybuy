import mdl
from lighting import *

def run(filename):
    """
    This function runs an mdl script
    """
    p = mdl.parseFile(filename)

    if p:
        (commands, symbols) = p
    else:
        print("Parsing failed.")
        return

    view = [0,
            0,
            1];
    ambient = [50,
               50,
               50]
    light = [[0.5,
              0.75,
              1],
             [255,
              255,
              255]]

    #my naming conventions
    A=ambient
    P=light[1]
    L=light[0]
    V=view
    light_list=[]
    default_light=['light',{"location":L,"color":P}]
    color = [0, 0, 0]
    transform = new_matrix()
    ident( transform )
    stack=[]
    stack.append(transform)
    screen = new_screen()
    buffer = new_zbuffer()
    edge=empty_matrix()
    triangle_matrix=empty_matrix()
    step_3d = 100
    consts = ''
    coords = []
    coords1 = []
    symbols['.white'] = ['constants',
                         {'red': [0.2, 0.5, 0.5],
                          'green': [0.2, 0.5, 0.5],
                          'blue': [0.2, 0.5, 0.5]}]
    reflect = '.white'
    basename=""
    frames=0
    is_frames=False
    is_very=False   #really means is_vary
    is_tween=False
    #print(symbols)
    for command in commands:
        if command["op"]=="basename":
            basename=command["args"][0]  
        elif command["op"]=="frames":
            frames=int(command["args"][0])
            is_frames=True
        elif command["op"]=="vary":
            is_very=True
        elif command["op"]=="tween":
            is_tween=True
        
    
    if is_very and is_frames==False:
        print("error vary present but no value given for frames")
        return
    


    if frames<1:
        for command in commands:
            if command["op"]=="light":
                light_name=command["light"]
                info=symbols[light_name]
                light_list.append(info)
            elif command["op"]=="push":
                push(stack)
            elif command["op"]=="pop":
                pop(stack)
            elif command["op"]=="move":
                coord=command["args"]
                a=(coord[0])
                b=(coord[1])
                c=(coord[2])
                transform=move(a,b,c)
                apply(stack[-1],transform)
                stack[-1]=transform
            elif command["op"]=="rotate":
                coord=command["args"]
                axis=coord[0]
                angle=coord[1]
                transform=rotation(angle,axis)
                apply(stack[-1],transform)
                stack[-1]=transform
            elif command["op"]=="scale":
                coord=command["args"]
                sx=(coord[0])
                sy=(coord[1])
                sz=(coord[2])
                transform=scale(sx,sy,sz)
                apply(stack[-1],transform)
                stack[-1]=transform
            elif command["op"]=="sphere":
                coord=command["args"]
                cx=(coord[0])
                cy=(coord[1])
                cz=(coord[2])
                radius=(coord[3])
                constants=command["constants"]
                Ka=[]
                Kd=[]
                Ks=[]
                if constants==None:
                    sphere(triangle_matrix,cx,cy,cz,radius)
                    apply(stack[-1],triangle_matrix)
                    info=symbols[".white"][1]
                    Ka.append(info["red"][0])
                    Ka.append(info["green"][0])
                    Ka.append(info["blue"][0])
                    Kd.append(info["red"][1])
                    Kd.append(info["green"][1])
                    Kd.append(info["blue"][1])
                    Ks.append(info["red"][2])
                    Ks.append(info["green"][2])
                    Ks.append(info["blue"][2])
                    newA=A
                    newP=P
                    newL=L
                    newV=V
                    add_polygons(screen,buffer,triangle_matrix,newA,light_list,newV,Ka,Kd,Ks)
                    triangle_matrix=empty_matrix()
                    
                else:
                    sphere(triangle_matrix,cx,cy,cz,radius)
                    apply(stack[-1],triangle_matrix)
                    info=symbols[constants][1]
                    Ka.append(info["red"][0])
                    Ka.append(info["green"][0])
                    Ka.append(info["blue"][0])
                    Kd.append(info["red"][1])
                    Kd.append(info["green"][1])
                    Kd.append(info["blue"][1])
                    Ks.append(info["red"][2])
                    Ks.append(info["green"][2])
                    Ks.append(info["blue"][2])
                    newA=A
                    newP=P
                    newL=L
                    newV=V
                    add_polygons(screen,buffer,triangle_matrix,newA,light_list,newV,Ka,Kd,Ks)
                    triangle_matrix=empty_matrix()
            elif command["op"]=="torus":
                coord=command["args"]
                cx=coord[0]
                cy=coord[1]
                cz=coord[2]
                r=coord[3]
                R=coord[4]
                torus(triangle_matrix,cx,cy,cz,r,R)
                apply(stack[-1],triangle_matrix)
                constants=command["constants"]
                Ka=[]
                Kd=[]
                Ks=[]
                if constants==None:
                    info=symbols[".white"][1]
                    Ka.append(info["red"][0])
                    Ka.append(info["green"][0])
                    Ka.append(info["blue"][0])
                    Kd.append(info["red"][1])
                    Kd.append(info["green"][1])
                    Kd.append(info["blue"][1])
                    Ks.append(info["red"][2])
                    Ks.append(info["green"][2])
                    Ks.append(info["blue"][2])
                    newA=A
                    newP=P
                    newL=L
                    newV=V
                    add_polygons(screen,buffer,triangle_matrix,newA,light_list,newV,Ka,Kd,Ks)
                    triangle_matrix=empty_matrix()
                else:
                    info=symbols[constants][1]
                    Ka.append(info["red"][0])
                    Ka.append(info["green"][0])
                    Ka.append(info["blue"][0])
                    Kd.append(info["red"][1])
                    Kd.append(info["green"][1])
                    Kd.append(info["blue"][1])
                    Ks.append(info["red"][2])
                    Ks.append(info["green"][2])
                    Ks.append(info["blue"][2])
                    newA=A
                    newP=P
                    newL=L
                    newV=V
                    add_polygons(screen,buffer,triangle_matrix,newA,light_list,newV,Ka,Kd,Ks)
                    triangle_matrix=empty_matrix()
                    
            elif command["op"]=="save":
                coord=command["args"][0]
                coord=coord+".png"
                save_ppm(screen,coord)
            elif command["op"]=="box":
                coord=command["args"]
                x=coord[0]
                y=coord[1]
                z=coord[2]
                width=coord[3]
                height=coord[4]
                depth=coord[5]
                constants=command["constants"]
                Ka=[]
                Kd=[]
                Ks=[]
                box(triangle_matrix,x,y,z,width,height,depth)
                apply(stack[-1],triangle_matrix)
                if constants==None:
                    info=symbols[".white"][1]
                    Ka.append(info["red"][0])
                    Ka.append(info["green"][0])
                    Ka.append(info["blue"][0])
                    Kd.append(info["red"][1])
                    Kd.append(info["green"][1])
                    Kd.append(info["blue"][1])
                    Ks.append(info["red"][2])
                    Ks.append(info["green"][2])
                    Ks.append(info["blue"][2])
                    newA=A
                    newP=P
                    newL=L
                    newV=V
                    add_polygons(screen,buffer,triangle_matrix,newA,light_list,newV,Ka,Kd,Ks)
                    triangle_matrix=empty_matrix()
                else:
                    info=symbols[constants][1]
                    Ka.append(info["red"][0])
                    Ka.append(info["green"][0])
                    Ka.append(info["blue"][0])
                    Kd.append(info["red"][1])
                    Kd.append(info["green"][1])
                    Kd.append(info["blue"][1])
                    Ks.append(info["red"][2])
                    Ks.append(info["green"][2])
                    Ks.append(info["blue"][2])
                    newA=A
                    newP=P   # new P and new L are useless and have no function within this code
                    newL=L
                    newV=V
                    add_polygons(screen,buffer,triangle_matrix,newA,light_list,newV,Ka,Kd,Ks)
                    triangle_matrix=empty_matrix()
            elif command["op"]=="line":
                coord=command["args"]
                x0=(coord[0])
                y0=(coord[1])
                z0=(coord[2])
                x1=(coord[3])
                y1=(coord[4])
                z1=(coord[5])
                add_edge(edge,x0,y0,z0,x1,y1,z1)
                apply(stack[-1],edge)
                add_lines(screen,buffer,edge,color)
                edge=empty_matrix()
            elif command["op"]=="ambient":
                memory=[]
                data=symbols["ambient"]
                memory.append(data[1])
                memory.append(data[2])
                memory.append(data[3])
                A=memory
    elif is_very==True:
        #print("goku")
        knob_data=[]
        for x in range(frames+1):
            knob_data.append({})
        for command in commands:
            if command["op"]=="vary":
                coord=command["args"]
                knob_name=command["knob"]
                start_frame=int((coord[0]))
                end_frame=int((coord[1]))
                start_value=(coord[2])
                end_value=(coord[3])
                increment=(end_value-start_value)/(end_frame-start_frame)
                rise=0
                for frame in range(start_frame,end_frame+1):
                    data=start_value+rise
                    knob_data[frame][knob_name]=data
                    rise+=increment
        #print(knob_data)
        for x in range(frames+1):
            for command in commands:
                if command["op"]=="light":
                    light_name=command["light"]
                    info=symbols[light_name]
                    light_list.append(info)
                if command["op"]=="move":
                    if(command["knob"]==None):
                        coord=command["args"]
                        a=(coord[0])
                        b=(coord[1])
                        c=(coord[2])
                        transform=move(a,b,c)
                        apply(stack[-1],transform)
                        stack[-1]=transform
                    else:
                        value=knob_data[x][command["knob"]]
                        coord=command["args"]
                        a=(coord[0])*value
                        b=(coord[1])*value
                        c=(coord[2])*value
                        transform=move(a,b,c)
                        apply(stack[-1],transform)
                        stack[-1]=transform
                elif command["op"]=="rotate":
                    if command["knob"]==None:
                       coord=command["args"]
                       axis=coord[0]
                       angle=coord[1]
                       transform=rotation(angle,axis)
                       apply(stack[-1],transform)
                       stack[-1]=transform
                    else:
                        value=knob_data[x][command["knob"]]
                        coord=command["args"]
                        axis=coord[0]
                        angle=(coord[1])*value
                        transform=rotation(angle,axis)
                        apply(stack[-1],transform)
                        stack[-1]=transform
                elif command["op"]=="scale":
                    if command["knob"]==None:
                        coord=command["args"]
                        sx=(coord[0])
                        sy=(coord[1])
                        sz=(coord[2])
                        transform=scale(sx,sy,sz)
                        apply(stack[-1],transform)
                        stack[-1]=transform
                    else:
                        value=knob_data[x][command["knob"]]
                        coord=command["args"]
                        sx=(coord[0])
                        sy=(coord[1])
                        sz=(coord[2])
                        xdiff=sx-1
                        ydiff=sy-1
                        zdiff=sz-1
                        xfac=1+xdiff*value
                        yfac=1+ydiff*value
                        zfac=1+zdiff*value
                        transform=scale(xfac,yfac,zfac)
                        apply(stack[-1],transform)
                        stack[-1]=transform
                
                elif command["op"]=="sphere":
                    coord=command["args"]
                    cx=(coord[0])
                    cy=(coord[1])
                    cz=(coord[2])
                    radius=(coord[3])
                    constants=command["constants"]
                    Ka=[]
                    Kd=[]
                    Ks=[]
                    if constants==None:
                        sphere(triangle_matrix,cx,cy,cz,radius)
                        apply(stack[-1],triangle_matrix)
                        info=symbols[".white"][1]
                        Ka.append(info["red"][0])
                        Ka.append(info["green"][0])
                        Ka.append(info["blue"][0])
                        Kd.append(info["red"][1])
                        Kd.append(info["green"][1])
                        Kd.append(info["blue"][1])
                        Ks.append(info["red"][2])
                        Ks.append(info["green"][2])
                        Ks.append(info["blue"][2])
                        newA=A
                        newP=P
                        newL=L
                        newV=V
                        add_polygons(screen,buffer,triangle_matrix,newA,light_list,newV,Ka,Kd,Ks)
                        triangle_matrix=empty_matrix()
                        
                    else:
                        sphere(triangle_matrix,cx,cy,cz,radius)
                        apply(stack[-1],triangle_matrix)
                        info=symbols[constants][1]
                        Ka.append(info["red"][0])
                        Ka.append(info["green"][0])
                        Ka.append(info["blue"][0])
                        Kd.append(info["red"][1])
                        Kd.append(info["green"][1])
                        Kd.append(info["blue"][1])
                        Ks.append(info["red"][2])
                        Ks.append(info["green"][2])
                        Ks.append(info["blue"][2])
                        newA=A
                        newP=P
                        newL=L
                        newV=V
                        add_polygons(screen,buffer,triangle_matrix,newA,light_list,newV,Ka,Kd,Ks)
                        triangle_matrix=empty_matrix()
                elif command["op"]=="torus":
                    coord=command["args"]
                    cx=coord[0]
                    cy=coord[1]
                    cz=coord[2]
                    r=coord[3]
                    R=coord[4]
                    torus(triangle_matrix,cx,cy,cz,r,R)
                    apply(stack[-1],triangle_matrix)
                    constants=command["constants"]
                    Ka=[]
                    Kd=[]
                    Ks=[]
                    if constants==None:
                        info=symbols[".white"][1]
                        Ka.append(info["red"][0])
                        Ka.append(info["green"][0])
                        Ka.append(info["blue"][0])
                        Kd.append(info["red"][1])
                        Kd.append(info["green"][1])
                        Kd.append(info["blue"][1])
                        Ks.append(info["red"][2])
                        Ks.append(info["green"][2])
                        Ks.append(info["blue"][2])
                        newA=A
                        newP=P
                        newL=L
                        newV=V
                        #print(L)
                        #print(V)
                        add_polygons(screen,buffer,triangle_matrix,newA,light_list,newV,Ka,Kd,Ks)
                        triangle_matrix=empty_matrix()
                    else:
                        info=symbols[constants][1]
                        Ka.append(info["red"][0])
                        Ka.append(info["green"][0])
                        Ka.append(info["blue"][0])
                        Kd.append(info["red"][1])
                        Kd.append(info["green"][1])
                        Kd.append(info["blue"][1])
                        Ks.append(info["red"][2])
                        Ks.append(info["green"][2])
                        Ks.append(info["blue"][2])
                        newA=A
                        newP=P
                        newL=L
                        newV=V
                        #print(L)
                        #print(V)
                        add_polygons(screen,buffer,triangle_matrix,newA,light_list,newV,Ka,Kd,Ks)
                        triangle_matrix=empty_matrix()
                elif command["op"]=="box":
                    coord=command["args"]
                    x=coord[0]
                    y=coord[1]
                    z=coord[2]
                    width=coord[3]
                    height=coord[4]
                    depth=coord[5]
                    constants=command["constants"]
                    Ka=[]
                    Kd=[]
                    Ks=[]
                    box(triangle_matrix,x,y,z,width,height,depth)
                    apply(stack[-1],triangle_matrix)
                    if constants==None:
                        info=symbols[".white"][1]
                        Ka.append(info["red"][0])
                        Ka.append(info["green"][0])
                        Ka.append(info["blue"][0])
                        Kd.append(info["red"][1])
                        Kd.append(info["green"][1])
                        Kd.append(info["blue"][1])
                        Ks.append(info["red"][2])
                        Ks.append(info["green"][2])
                        Ks.append(info["blue"][2])
                        newA=A
                        newP=P
                        newL=L
                        newV=V
                        add_polygons(screen,buffer,triangle_matrix,newA,light_list,newV,Ka,Kd,Ks)
                        triangle_matrix=empty_matrix()
                    else:
                        info=symbols[constants][1]
                        Ka.append(info["red"][0])
                        Ka.append(info["green"][0])
                        Ka.append(info["blue"][0])
                        Kd.append(info["red"][1])
                        Kd.append(info["green"][1])
                        Kd.append(info["blue"][1])
                        Ks.append(info["red"][2])
                        Ks.append(info["green"][2])
                        Ks.append(info["blue"][2])
                        newA=A
                        newP=P
                        newL=L
                        newV=V
                        add_polygons(screen,buffer,triangle_matrix,newA,light_list,newV,Ka,Kd,Ks)
                        triangle_matrix=empty_matrix()
                elif command["op"]=="line":
                    coord=command["args"]
                    x0=(coord[0])
                    y0=(coord[1])
                    z0=(coord[2])
                    x1=(coord[3])
                    y1=(coord[4])
                    z1=(coord[5])
                    add_edge(edge,x0,y0,z0,x1,y1,z1)
                    apply(stack[-1],edge)
                    add_lines(screen,buffer,edge,color)
                    edge=empty_matrix()

                elif command["op"]=="ambient":
                    memory=[]
                    data=symbols["ambient"]
                    memory.append(data[1])
                    memory.append(data[2])
                    memory.append(data[3])
                    A=memory

                    
            save_ppm(screen,basename+str(x)+".png")
            clear_screen(screen)
            clear_zbuffer(buffer)
            trans=new_matrix()
            ident(trans)
            stack=[]
            stack.append(trans)
            #print(basename+str(x)+".png")
    else:
        for command in commands:
            if command["op"]=="tween":
                start_frame=int(command['args'][0])
                end_frame=int(command['args'][1])
                frame_number=end_frame-start_frame+1
                knob0=command['knob_list0']
                knob1=command['knob_list1']
                #turning the strings into dicts
                
                knob0=knob0.split("S")
                for x in range(len(knob0)):
                    knob0[x]=knob0[x].split("T")
                    
                knoblist0={}
                knoblist1={}
                
                for x in knob0:
                    knoblist0[x[0]]=float(x[1])
                    
                knob1=knob1.split("S")
                for x in range(len(knob1)):
                    knob1[x]=knob1[x].split("T")
                for x in knob1:
                    knoblist1[x[0]]=float(x[1])
                
                
                    
                
                knoblist=[]
                knoblist.append(knoblist0)
                for x in range(1,frame_number-1):
                    knoblist.append({})
                knoblist.append(knoblist1)
                
                for key in knoblist[0].keys():
                    diff=(knoblist[len(knoblist)-1][key]-knoblist[0][key])/(len(knoblist)-1)
                    for x in range(1,len(knoblist)-1):
                        knoblist[x][key]=knoblist[0][key]+x*diff
        for x in range(frame_number):
            for command in commands:
                if command["op"]=="light":
                    light_name=command["light"]
                    info=symbols[light_name]
                    light_list.append(info)
                if command["op"]=="move":
                    if(command["knob"]==None):
                        coord=command["args"]
                        a=(coord[0])
                        b=(coord[1])
                        c=(coord[2])
                        transform=move(a,b,c)
                        apply(stack[-1],transform)
                        stack[-1]=transform
                    else:
                        value=knoblist[x][command["knob"]]
                        coord=command["args"]
                        a=(coord[0])*value
                        b=(coord[1])*value
                        c=(coord[2])*value
                        transform=move(a,b,c)
                        apply(stack[-1],transform)
                        stack[-1]=transform
                elif command["op"]=="rotate":
                    if command["knob"]==None:
                       coord=command["args"]
                       axis=coord[0]
                       angle=coord[1]
                       transform=rotation(angle,axis)
                       apply(stack[-1],transform)
                       stack[-1]=transform
                    else:
                        value=knoblist[x][command["knob"]]
                        coord=command["args"]
                        axis=coord[0]
                        angle=(coord[1])*value
                        transform=rotation(angle,axis)
                        apply(stack[-1],transform)
                        stack[-1]=transform
                elif command["op"]=="scale":
                    if command["knob"]==None:
                        coord=command["args"]
                        sx=(coord[0])
                        sy=(coord[1])
                        sz=(coord[2])
                        transform=scale(sx,sy,sz)
                        apply(stack[-1],transform)
                        stack[-1]=transform
                    else:
                        value=knoblist[x][command["knob"]]
                        coord=command["args"]
                        sx=(coord[0])
                        sy=(coord[1])
                        sz=(coord[2])
                        xdiff=sx-1
                        ydiff=sy-1
                        zdiff=sz-1
                        xfac=1+xdiff*value
                        yfac=1+ydiff*value
                        zfac=1+zdiff*value
                        transform=scale(xfac,yfac,zfac)
                        apply(stack[-1],transform)
                        stack[-1]=transform
                
                elif command["op"]=="sphere":
                    coord=command["args"]
                    cx=(coord[0])
                    cy=(coord[1])
                    cz=(coord[2])
                    radius=(coord[3])
                    constants=command["constants"]
                    Ka=[]
                    Kd=[]
                    Ks=[]
                    if constants==None:
                        sphere(triangle_matrix,cx,cy,cz,radius)
                        apply(stack[-1],triangle_matrix)
                        info=symbols[".white"][1]
                        Ka.append(info["red"][0])
                        Ka.append(info["green"][0])
                        Ka.append(info["blue"][0])
                        Kd.append(info["red"][1])
                        Kd.append(info["green"][1])
                        Kd.append(info["blue"][1])
                        Ks.append(info["red"][2])
                        Ks.append(info["green"][2])
                        Ks.append(info["blue"][2])
                        newA=A
                        newP=P
                        newL=L
                        newV=V
                        add_polygons(screen,buffer,triangle_matrix,newA,light_list,newV,Ka,Kd,Ks)
                        triangle_matrix=empty_matrix()
                        
                    else:
                        sphere(triangle_matrix,cx,cy,cz,radius)
                        apply(stack[-1],triangle_matrix)
                        info=symbols[constants][1]
                        Ka.append(info["red"][0])
                        Ka.append(info["green"][0])
                        Ka.append(info["blue"][0])
                        Kd.append(info["red"][1])
                        Kd.append(info["green"][1])
                        Kd.append(info["blue"][1])
                        Ks.append(info["red"][2])
                        Ks.append(info["green"][2])
                        Ks.append(info["blue"][2])
                        newA=A
                        newP=P
                        newL=L
                        newV=V
                        add_polygons(screen,buffer,triangle_matrix,newA,light_list,newV,Ka,Kd,Ks)
                        triangle_matrix=empty_matrix()
                elif command["op"]=="torus":
                    coord=command["args"]
                    cx=coord[0]
                    cy=coord[1]
                    cz=coord[2]
                    r=coord[3]
                    R=coord[4]
                    torus(triangle_matrix,cx,cy,cz,r,R)
                    apply(stack[-1],triangle_matrix)
                    constants=command["constants"]
                    Ka=[]
                    Kd=[]
                    Ks=[]
                    if constants==None:
                        info=symbols[".white"][1]
                        Ka.append(info["red"][0])
                        Ka.append(info["green"][0])
                        Ka.append(info["blue"][0])
                        Kd.append(info["red"][1])
                        Kd.append(info["green"][1])
                        Kd.append(info["blue"][1])
                        Ks.append(info["red"][2])
                        Ks.append(info["green"][2])
                        Ks.append(info["blue"][2])
                        newA=A
                        newP=P
                        newL=L
                        newV=V
                        #print(L)
                        #print(V)
                        add_polygons(screen,buffer,triangle_matrix,newA,light_list,newV,Ka,Kd,Ks)
                        triangle_matrix=empty_matrix()
                    else:
                        info=symbols[constants][1]
                        Ka.append(info["red"][0])
                        Ka.append(info["green"][0])
                        Ka.append(info["blue"][0])
                        Kd.append(info["red"][1])
                        Kd.append(info["green"][1])
                        Kd.append(info["blue"][1])
                        Ks.append(info["red"][2])
                        Ks.append(info["green"][2])
                        Ks.append(info["blue"][2])
                        newA=A
                        newP=P
                        newL=L
                        newV=V
                        #print(L)
                        #print(V)
                        add_polygons(screen,buffer,triangle_matrix,newA,light_list,newV,Ka,Kd,Ks)
                        triangle_matrix=empty_matrix()
                elif command["op"]=="box":
                    coord=command["args"]
                    x=coord[0]
                    y=coord[1]
                    z=coord[2]
                    width=coord[3]
                    height=coord[4]
                    depth=coord[5]
                    constants=command["constants"]
                    Ka=[]
                    Kd=[]
                    Ks=[]
                    box(triangle_matrix,x,y,z,width,height,depth)
                    apply(stack[-1],triangle_matrix)
                    if constants==None:
                        info=symbols[".white"][1]
                        Ka.append(info["red"][0])
                        Ka.append(info["green"][0])
                        Ka.append(info["blue"][0])
                        Kd.append(info["red"][1])
                        Kd.append(info["green"][1])
                        Kd.append(info["blue"][1])
                        Ks.append(info["red"][2])
                        Ks.append(info["green"][2])
                        Ks.append(info["blue"][2])
                        newA=A
                        newP=P
                        newL=L
                        newV=V
                        add_polygons(screen,buffer,triangle_matrix,newA,light_list,newV,Ka,Kd,Ks)
                        triangle_matrix=empty_matrix()
                    else:
                        info=symbols[constants][1]
                        Ka.append(info["red"][0])
                        Ka.append(info["green"][0])
                        Ka.append(info["blue"][0])
                        Kd.append(info["red"][1])
                        Kd.append(info["green"][1])
                        Kd.append(info["blue"][1])
                        Ks.append(info["red"][2])
                        Ks.append(info["green"][2])
                        Ks.append(info["blue"][2])
                        newA=A
                        newP=P
                        newL=L
                        newV=V
                        add_polygons(screen,buffer,triangle_matrix,newA,light_list,newV,Ka,Kd,Ks)
                        triangle_matrix=empty_matrix()
                elif command["op"]=="line":
                    coord=command["args"]
                    x0=(coord[0])
                    y0=(coord[1])
                    z0=(coord[2])
                    x1=(coord[3])
                    y1=(coord[4])
                    z1=(coord[5])
                    add_edge(edge,x0,y0,z0,x1,y1,z1)
                    apply(stack[-1],edge)
                    add_lines(screen,buffer,edge,color)
                    edge=empty_matrix()

                elif command["op"]=="ambient":
                    memory=[]
                    data=symbols["ambient"]
                    memory.append(data[1])
                    memory.append(data[2])
                    memory.append(data[3])
                    A=memory

                    
            save_ppm(screen,basename+str(x)+".png")
            clear_screen(screen)
            clear_zbuffer(buffer)
            trans=new_matrix()
            ident(trans)
            stack=[]
            stack.append(trans)
    
                
        
                    
                            
        
                        
                        
        
                    
                        
                
                            
                            
                            
            
run("it.mdl")

            
