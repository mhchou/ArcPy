import arcpy

ws = arcpy.GetParameterAsText(0)
fc= arcpy.GetParameterAsText(1)
FID_field = arcpy.GetParameterAsText(2)
FID1 = arcpy.GetParameterAsText(3)
FID2 = arcpy.GetParameterAsText(4)
field_names = arcpy.GetParameterAsText(5)
fields = field_names.split(';')
workspace = ws
arcpy.AddMessage('workspace: '+workspace)

xyfields = ["SHAPE@X","SHAPE@Y"]
p = []
list1 = []
list2 = []

query = "{} = '{}'".format(FID_field, FID1)
with arcpy.da.SearchCursor(fc, ["SHAPE@XY"], where_clause=query) as search:
    for i in search:
        p += i
if field_names != '':    
    with arcpy.da.SearchCursor(fc, fields, where_clause=query) as search:
        for i in search:
            list1 += i
        
query = "{} = '{}'".format(FID_field, FID2)
with arcpy.da.SearchCursor(fc, ["SHAPE@XY"], where_clause=query) as search:
    for i in search:
        p += i  
if field_names != '':         
    with arcpy.da.SearchCursor(fc, fields, where_clause=query) as search:
        for i in search:
            list2 += i
        
xy = [p[0][0],p[0][1],p[1][0],p[1][1]]

edit = arcpy.da.Editor(workspace)
edit.startEditing(False, True) #undo/redo; versioned data
edit.startOperation()

changetopoint2 = "{} = '{}'".format(FID_field, FID1)
with arcpy.da.UpdateCursor(fc, xyfields, where_clause=changetopoint2) as firstchange:
    for first in firstchange:
        first[0]=(xy[2])
        first[1]=(xy[3])
        firstchange.updateRow(first)
        continue
if field_names != '': 
    with arcpy.da.UpdateCursor(fc, fields, where_clause=changetopoint2) as firstchange:
        for first in firstchange:
            for i in range(len(fields)):
                first[i]=(list2[i])
                firstchange.updateRow(first)
                continue

changetopoint1 = "{} = '{}'".format(FID_field, FID2)
with arcpy.da.UpdateCursor(fc, xyfields, where_clause=changetopoint1) as secondchange:
    for second in secondchange:
        second[0]=(xy[0])
        second[1]=(xy[1])
        secondchange.updateRow(second)
        continue
if field_names != '': 
    with arcpy.da.UpdateCursor(fc, fields, where_clause=changetopoint1) as secondchange:
        for second in secondchange:
            for i in range(len(fields)):
                second[i]=(list1[i])
                secondchange.updateRow(second)
                continue    
                
edit.stopOperation()
edit.stopEditing(True)
del search
del firstchange
del secondchange
