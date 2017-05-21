import maya.cmds as cmds
import maya.api.OpenMaya as om
from RMPY import RMNameConvention
reload(RMNameConvention)
from RMPY import RMRigTools


class RMSpaceSwitch(object):
    def __init__(self,NameConv = None):
        if not NameConv:
            self.NameConv = RMNameConvention.RMNameConvention()
        else:
            self.NameConv = NameConv
        self.ControlObject = None 
        self.AfectedObjectList = []
        self.SpaceObjectsList = []

    def CreateSpaceSwitchReverse(self, AfectedObject, SpaceObjects, ControlObject, Name = "spaceSwitch", constraintType = "parent", mo = True, sswtype = "enum"): #
        '''
        Creates a simple space Switch that uses a reverse for simple solution it can only hold 2 spaces
        '''
        if len(SpaceObjects) == 2:
            if sswtype == "enum":
                SpaceObjectShortName =[]
                for eachObject in SpaceObjects:
                    SpaceObjectShortName.append(self.NameConv.RMGetAShortName(eachObject))
                self.AddEnumParameters(SpaceObjectShortName, ControlObject, Name = Name)
            else:
                if Name=="":
                    index = 0
                    SwitchName = 'SW'
                    for eachString in SpaceObjects:
                        SwitchName = SwitchName + self.NameConv.RMGetAShortName(eachString).title()
                        index = index + 1
                    Name = SwitchName

                self.AddNumericParameter( ControlObject, Name = Name)

            reverse = cmds.shadingNode('reverse', asUtility=True, name = Name + "SWReverse")
            multiply = cmds.shadingNode('multiplyDivide', asUtility=True, name = Name + "SWMultDiv")

            #cmds.connectAttr(ControlObject + "." + Name, reverse + ".inputX")
            cmds.connectAttr(ControlObject + "." + Name, multiply + ".input1X")
            cmds.setAttr(multiply + ".input2X", 10)
            cmds.setAttr(multiply + ".operation", 2)
            cmds.connectAttr(multiply + ".outputX", reverse + ".inputX")
            
            for eachObject in SpaceObjects:
                if constraintType == "point":
                    parentConstraint = cmds.pointConstraint (eachObject, AfectedObject, mo = mo, name = AfectedObject + "SpaceSwitchConstraint")
                    WA = cmds.pointConstraint (parentConstraint, q = True, weightAliasList = True)
                elif constraintType == "orient":
                    parentConstraint = cmds.orientConstraint (eachObject, AfectedObject, mo = mo, name = AfectedObject + "SpaceSwitchConstraint")
                    WA = cmds.orientConstraint (parentConstraint, q = True, weightAliasList = True)
                elif constraintType == "parent":
                    parentConstraint = cmds.parentConstraint (eachObject, AfectedObject, mo = mo, name = AfectedObject + "SpaceSwitchConstraint")
                    WA = cmds.parentConstraint (parentConstraint, q = True, weightAliasList = True)
            
            cmds.setAttr("%s.interpType"%parentConstraint[0] , 0)

            if self.NameConv.RMIsNameInFormat (AfectedObject):
                reverse = self.NameConv.RMRenameBasedOnBaseName(AfectedObject, reverse, {'name': reverse})
                multiply = self.NameConv.RMRenameBasedOnBaseName(AfectedObject, multiply,{'name': multiply})
                parentConstraint[0] = self.NameConv.RMRenameBasedOnBaseName(AfectedObject, parentConstraint[0]
                                                                            , {'name': Name})

            else:
                reverse = self.NameConv.RMRenameNameInFormat(reverse, {})
                multiply = self.NameConv.RMRenameNameInFormat(multiply, {})
                parentConstraint[0] = self.NameConv.RMRenameNameInFormat(parentConstraint[0], {})

            cmds.connectAttr( multiply + ".outputX", parentConstraint[0] + "." + WA[1])
            cmds.connectAttr( reverse  + ".outputX", parentConstraint[0]+ "." + WA[0])
            
            #cmds.connectAttr(ControlObject + "." + Name, parentConstraint[0] + "." + WA[1])
            #cmds.connectAttr(reverse + ".outputX", parentConstraint[0] + "." + WA[0])


    def CreateSpaceSwitch(self, AfectedObject, SpaceObjects, ControlObject, Name = "spaceSwitch",constraintType = "parent", mo = True):
        '''
        Creates a new SpaceSwitch using conditions so it can accept multiple spaces, 
        and it is compatible with the add and remove from Space Switch functions.
        Valid constraintTypes are "parent" , "point", "orient"
        '''
        SpaceObjectShortName =[]
        for eachObject in SpaceObjects:
            SpaceObjectShortName.append(self.NameConv.RMGetAShortName(eachObject))

        self.AddEnumParameters(SpaceObjectShortName, ControlObject, Name = Name)

        index = 0
        for eachObject in SpaceObjects:
            if constraintType == "point":
                parentConstraint = cmds.pointConstraint (eachObject, AfectedObject, mo = mo, name = self.NameConv.RMGetAShortName(AfectedObject) + "SpaceSwitchConstraint")
            
            elif constraintType == "orient":
                parentConstraint = cmds.orientConstraint (eachObject, AfectedObject, mo = mo, name = self.NameConv.RMGetAShortName(AfectedObject) + "SpaceSwitchConstraint")
            
            else:
                parentConstraint = cmds.parentConstraint (eachObject, AfectedObject, mo = mo, name = self.NameConv.RMGetAShortName(AfectedObject) + "SpaceSwitchConstraint")

            Switch = cmds.shadingNode('condition', asUtility=True, name = Name + "SWCondition")
            cmds.connectAttr(ControlObject + "." + Name, Switch + ".firstTerm")
            cmds.setAttr (Switch +".secondTerm", index)
            cmds.setAttr (Switch +".operation", 0)
            cmds.setAttr (Switch +".colorIfTrueR", 1)
            cmds.setAttr (Switch +".colorIfFalseR", 0)
            if constraintType == "point":
                WA = cmds.pointConstraint (parentConstraint, q = True, weightAliasList = True)
                TL = cmds.pointConstraint (parentConstraint, q = True, targetList = True)
            elif constraintType == "orient":
                WA = cmds.orientConstraint (parentConstraint, q = True, weightAliasList = True)
                TL = cmds.orientConstraint (parentConstraint, q = True, targetList = True)
            else:
                WA = cmds.parentConstraint (parentConstraint, q = True, weightAliasList = True)
                TL = cmds.parentConstraint (parentConstraint, q = True, targetList = True)

            cmds.connectAttr (Switch + ".outColorR", parentConstraint[0] + "." + WA[index])
            if self.NameConv.RMIsNameInFormat(AfectedObject):
                Switch = self.NameConv.RMRenameBasedOnBaseName(AfectedObject, Switch, {'name': Switch})
            else:
                Switch = self.NameConv.RMRenameNameInFormat(Switch, {})
            index += 1
        
        if self.NameConv.RMIsNameInFormat(AfectedObject):
            parentConstraint[0] = self.NameConv.RMRenameBasedOnBaseName(AfectedObject,parentConstraint[0], {'name': parentConstraint[0]})
        else:
            parentConstraint[0] = self.NameConv.RMRenameNameInFormat(parentConstraint[0], {})
    
    def IsSpaceSwitch(self, Control, SpaceSwitchName = "spaceSwitch"):
        AttributeList = cmds.listAttr(Control)
        if SpaceSwitchName  in AttributeList:
            if cmds.getAttr (Control + "." + SpaceSwitchName, type = True) == 'enum':
                Connections = cmds.listConnections (Control + "." + SpaceSwitchName)
                if Connections != None:
                    for eachConnection in Connections:
                        if cmds.objectType(eachConnection) == 'condition':
                            ConstraintsConnections = cmds.listConnections(eachConnection+'.outColorR')
                            for eachConstraint in ConstraintsConnections:
                                if cmds.objectType(eachConstraint) in ['parentConstraint', 'orientConstraint', 'orientConstraint']:
                                    return True
        return False

    def GetSpaceSwitchDic(self, control, SpaceSwitchName = "spaceSwitch"):
        Enums = self.getControlEnumsRelations(control,SpaceSwitchName = "spaceSwitch")
        ConstraintDictionary = self.ConstraintsDictionary(Enums[Enums.keys()[0]] ['condition'])
        return {'enums' : Enums , 'constraints' : ConstraintDictionary }

    def GetAfectedObjectsList(self,ControlObject,SpaceSwitchName = "spaceSwitch"):
        SpaceSwDic = self.GetSpaceSwitchDic(ControlObject, SpaceSwitchName = SpaceSwitchName)
        ReturnObjectsList=[]
        for keys in SpaceSwDic['constraints']:
            ReturnObjectsList.append(SpaceSwDic['constraints'][keys]['object'])
        return ReturnObjectsList

    def AddAffectedObject(self,ControlObject, AfectedObject,SpaceSwitchName = "spaceSwitch"):
        SpaceSwDic = self.GetSpaceSwitchDic(ControlObject,SpaceSwitchName = SpaceSwitchName)
        index = 0
        for eachEnum in SpaceSwDic['enums']:
            parentConstraint = cmds.parentConstraint (SpaceSwDic['enums'][eachEnum]['object'], AfectedObject, mo = True, name = self.NameConv.RMGetAShortName(AfectedObject) + "SpaceSwitchConstraint")
            WA = cmds.parentConstraint (parentConstraint[0], q = True, weightAliasList = True)
            cmds.connectAttr (SpaceSwDic['enums'][eachEnum]['condition'] + ".outColorR", parentConstraint[0] + "." + WA[index])
            index += 1
    def RemoveAffectedObject(self, ControlObject, AfectedObject, SpaceSwitchName = "spaceSwitch"):

        SpaceSwDic = self.GetSpaceSwitchDic(ControlObject, SpaceSwitchName = SpaceSwitchName)
        
        for allConstraints in SpaceSwDic['constraints']:
            if SpaceSwDic['constraints'][allConstraints]['object'] == AfectedObject:
                cmds.delete(allConstraints)

        if len(SpaceSwDic['constraints'].keys()) == 1:
            for eachPlug in SpaceSwDic['enums']:
                cmds.delete(SpaceSwDic['enums'][eachPlug]['condition'])

            self.DeleteSpaceSwitchAttr(ControlObject, SpaceSwitchName)
            


    def AddSpaceObject(self, ControlObject, SpaceObject, SpaceSwitchName = "spaceSwitch"):
        SpaceSwDic = self.GetSpaceSwitchDic( ControlObject, SpaceSwitchName = SpaceSwitchName)
        
        EnumDic = self.AddEnumParameters([self.NameConv.RMGetAShortName(SpaceObject)],ControlObject)

        Switch = cmds.shadingNode('condition', asUtility=True, name = SpaceSwitchName + "SWCondition")
        cmds.connectAttr(ControlObject + "." + SpaceSwitchName, Switch + ".firstTerm")
        cmds.setAttr (Switch +".secondTerm", EnumDic[self.NameConv.RMGetAShortName(SpaceObject)])
        cmds.setAttr (Switch +".operation", 0)
        cmds.setAttr (Switch +".colorIfTrueR", 1)
        cmds.setAttr (Switch +".colorIfFalseR", 0)

        if self.NameConv.RMIsNameInFormat(ControlObject):
            Switch = self.NameConv.RMRenameBasedOnBaseName(ControlObject, Switch, {'name': Switch})
        else:
            Switch = self.NameConv.RMRenameNameInFormat(Switch, {})

        for eachConstraint in SpaceSwDic['constraints']:
            Object = SpaceSwDic['constraints'][eachConstraint]['object']
            parentConstraint = cmds.parentConstraint (SpaceObject, Object, mo = True)
            WA = cmds.parentConstraint (parentConstraint, q = True, weightAliasList = True)
            TL = cmds.parentConstraint (parentConstraint, q = True, targetList = True)
            if SpaceObject in TL:
                cmds.connectAttr (Switch + ".outColorR", parentConstraint[0] + "." + WA[TL.index(SpaceObject)])
            else:
                print "Error, cant find spaceobject in constraint targetList"

    def RemoveSpaceObject(self, ControlObject, SpaceObject, SpaceSwitchName = "spaceSwitch"):
        SpaceSwDic = self.GetSpaceSwitchDic( ControlObject, SpaceSwitchName = SpaceSwitchName)

        for eachConstraint in SpaceSwDic['constraints']:
            Object = SpaceSwDic['constraints'][eachConstraint]['object']
            cmds.parentConstraint (SpaceObject, Object, remove = True)

        for eachEnum in SpaceSwDic['enums']:
            if  SpaceSwDic['enums'][eachEnum]['object'] == SpaceObject:
                self.deleteEnumParameter(ControlObject,eachEnum)
                cmds.delete(SpaceSwDic['enums'][eachEnum]['condition'])
        
        enumDic = self.getEnumDictionary ( ControlObject, SpaceSwitchName = SpaceSwitchName)

        if enumDic:
            for eachEnum in enumDic:
                if eachEnum in SpaceSwDic['enums']:
                    EnumCond = SpaceSwDic['enums'][eachEnum]['condition']
                    cmds.setAttr (EnumCond +".secondTerm", enumDic[eachEnum])

    def GetSpaceObjectsList(self, ControlObject, SpaceSwitchName = "spaceSwitch"):
        SpaceSwDic = self.GetSpaceSwitchDic( ControlObject, SpaceSwitchName = SpaceSwitchName)
        ObjList=[]
        for eachEnum in SpaceSwDic['enums']:
             ObjList.append(SpaceSwDic['enums'][eachEnum]['object'])
        return ObjList

    def AddNumericParameter(self, Object, Name = 'spaceSwitch', valueRange = [0,10]):
        AttributeList = cmds.listAttr(Object)
        if Name  in AttributeList:
            #print "the Object Allready has an Attribute with this name, the type is:",cmds.getAttr (Object + "." + Name,type = True)
            return False
        else :
            cmds.addAttr(Object,at = "float", ln = Name,  hnv = 1, hxv = 1, h = 0, k = 1, smn = valueRange[0], smx = valueRange[1])
            return True

    def deleteEnumParameter(self, Object, Enum, SpaceSwitchName = 'spaceSwitch'):
        AttributeList = cmds.listAttr(Object)
        if SpaceSwitchName in AttributeList:
            if cmds.getAttr (Object + "." + SpaceSwitchName,type=True)=='enum':
                getControlEnums =self.getControlEnums(Object,SpaceSwitchName = SpaceSwitchName)
                if len(getControlEnums) > 1:
                    if Enum in getControlEnums:
                        getControlEnums.remove(Enum)
                        cmds.addAttr(Object + '.' + SpaceSwitchName, e=True, en =":".join(getControlEnums))
                else:
                    self.DeleteSpaceSwitchAttr(Object, SpaceSwitchName)

    def AddEnumParameters(self, Enum, Object, Name = 'spaceSwitch'):
        AttributeList = cmds.listAttr(Object)
        if Name  in AttributeList:
            if cmds.getAttr (Object + "." + Name,type=True)=='enum':
                #print "the Object Allready has an spaceSwitch"
                #print "Current Valid types are", cmds.addAttr (Object + "." + Name,q = True,enumName=True)
                EnumsInObject = self.getControlEnums(Object)
                for eachEnum in Enum:
                    if not eachEnum in EnumsInObject:
                        EnumsInObject.append(eachEnum)
                cmds.addAttr(Object + '.' + Name, e=True,ln = Name, en =":".join(EnumsInObject))
                index = 0
                returnIndexDic = {}
                for eachEnum in EnumsInObject:
                    returnIndexDic[eachEnum] = index
                    index += 1
                return returnIndexDic
        else :
            cmds.addAttr(Object , at = "enum" , ln = Name , k = 1, en =":".join(Enum))
        return None

    def DeleteSpaceSwitchAttr (self, Object, Name = 'spaceSwitch'):
        AttributeList = cmds.listAttr(Object)
        if Name  in AttributeList:
            cmds.deleteAttr (Object,at = Name)
        else:
            print "The Attribute %s could not be found on obj %s" % (Name , Object)

    def ConstraintsDictionary (self, Condition):
        returnedDic = {}
        ObjectsConnected = cmds.listConnections(Condition +'.outColorR')
        for eachConstraint in ObjectsConnected:
            returnedDic[eachConstraint] = self.getParentConstraintDic(eachConstraint)
        return returnedDic


    def getSwitchPlugsDictionary(self, Condition):
        returnedDic = {}
        ObjectsConnected = cmds.listConnections(Condition +'.outColorR')
        plugs = cmds.listConnections(Condition +'.outColorR', plugs = True)
        for eachPlug in plugs:
            splitPlug = eachPlug.split(".")
            if splitPlug[0] in ObjectsConnected:
                returnedDic[splitPlug[0]] = (splitPlug[1])
        return returnedDic

    def getParentConstraintDic (self, parentConstraint) :
        returnedDic = {'alias':{}, "object":None }
        aliasDic={}
        if cmds.objectType(parentConstraint)=="parentConstraint":
            WA = cmds.parentConstraint (parentConstraint, q = True, weightAliasList = True)
            TL = cmds.parentConstraint (parentConstraint, q = True, targetList = True)
        
        elif cmds.objectType(parentConstraint)=="orientConstraint":
            WA = cmds.orientConstraint (parentConstraint, q = True, weightAliasList = True)
            TL = cmds.orientConstraint (parentConstraint, q = True, targetList = True)
        
        elif cmds.objectType(parentConstraint)=="pointConstraint":
            WA = cmds.pointConstraint (parentConstraint, q = True, weightAliasList = True)
            TL = cmds.pointConstraint (parentConstraint, q = True, targetList = True)
        
        else:
            "error No constraint Type identified"
        
        if len(WA) == len(TL):
            for eachWAIndex in range(0,len(WA)):
                aliasDic[WA[eachWAIndex]] = TL[eachWAIndex]
        
        returnedDic["object"] = cmds.listConnections(parentConstraint + ".constraintRotateX")[0]
        returnedDic["alias"] = aliasDic
        return returnedDic

    def getEnumDictionary(self,Node,SpaceSwitchName = 'spaceSwitch'):
        AttributeList = cmds.listAttr(Node)
        if SpaceSwitchName  in AttributeList:
            if cmds.getAttr (Node + "." + SpaceSwitchName,type=True)=='enum':
                ValidValues = cmds.addAttr(Node+"."+SpaceSwitchName,q = True,enumName=True)
                returnDictionary = {}
                index = 0
                for eachValue in ValidValues.split(":"):
                    returnDictionary[eachValue] = index
                    index+=1
                return returnDictionary
        return None



    def getControlEnums (self, Node, SpaceSwitchName = 'spaceSwitch'):
        AttributeList = cmds.listAttr(Node)
        if SpaceSwitchName  in AttributeList:
            if cmds.getAttr (Node + "." + SpaceSwitchName,type=True)=='enum':
                ValidValues = cmds.addAttr(Node+"."+SpaceSwitchName,q = True,enumName=True)
                ValidValuesList = ValidValues.split(":")
                return ValidValuesList
        else:
            return []

    def getControlEnumsRelations(self, Node, SpaceSwitchName = 'spaceSwitch'):
        EnumRelationDic = {}
        AsummedConditions = cmds.listConnections( Node+'.'+SpaceSwitchName)
        enumList = self.getControlEnums(Node, SpaceSwitchName = 'spaceSwitch')
        for eachAssumedCondition in AsummedConditions:
            if cmds.objectType(eachAssumedCondition) == 'condition':
                index = cmds.getAttr(eachAssumedCondition+".secondTerm")
                EnumRelationDic[enumList[int(index)]] = {}
                EnumRelationDic[enumList[int(index)]]['condition']= eachAssumedCondition
                EnumRelationDic[enumList[int(index)]]['index'] = int(index)
        for eachCondition in EnumRelationDic:
            EnumRelationDic[eachCondition]['plugs'] = self.getSwitchPlugsDictionary(EnumRelationDic[eachCondition]['condition'])

        for eachEnumRD in EnumRelationDic:
            EnumRelationDic [eachEnumRD]['object'] = ""
            for eachPlug in EnumRelationDic[eachEnumRD]['plugs']:
                ConstraintDic = self.getParentConstraintDic(eachPlug)
                if EnumRelationDic[eachEnumRD]['object'] == "":
                    EnumRelationDic[eachEnumRD]['object'] = ConstraintDic['alias'][EnumRelationDic[eachEnumRD]['plugs'][eachPlug]]
                elif EnumRelationDic[eachEnumRD]['object'] != ConstraintDic['alias'][EnumRelationDic[eachEnumRD]['plugs'][eachPlug]]:
                    print "Object mismatch  on Plug" , EnumRelationDic[eachEnumRD]['object'] , ConstraintDic['alias'][EnumRelationDic[eachEnumRD]['plugs'][eachPlug]]
        return EnumRelationDic

    def RMCreateListConstraintSwitch(self,Constrained, Constraints ,ControlObject, SpaceSwitchName = 'spaceSwitch', reverse = False):
        SWMultDiv = ""
        if (self.AddNumericParameter (ControlObject, Name = SpaceSwitchName)):
            SWMultDiv = cmds.shadingNode("multiplyDivide",asUtility = True ,name = SpaceSwitchName + "SWMultDivide" )
            SWMultDiv = self.NameConv.RMRenameBasedOnBaseName(ControlObject, SWMultDiv, {'name': SWMultDiv})
            cmds.connectAttr(ControlObject+"."+SpaceSwitchName ,SWMultDiv+".input1X")
            cmds.setAttr(SWMultDiv+".input2X",10)
            cmds.setAttr(SWMultDiv+".operation",2)
        
        else:
            
            SWMultDiv = cmds.listConnections(ControlObject + "." + SpaceSwitchName, type = "multiplyDivide")[0]

        if reverse == True:
            ConnectionsList = cmds.listConnections(SWMultDiv + ".outputX", type = "reverse")
            reverseSW = ""
            if ConnectionsList and len(ConnectionsList) >= 1:
                reverseSW = ConnectionsList[0]
            else :
                reverseSW = cmds.shadingNode('reverse', asUtility=True, name = SpaceSwitchName + "SWReverse")
                reverseSW = self.NameConv.RMRenameBasedOnBaseName(ControlObject, reverseSW, {'name' :"SWReverse"})
                cmds.connectAttr( SWMultDiv + ".outputX", reverseSW + ".inputX")

                if self.NameConv.RMIsNameInFormat (ControlObject):
                    reverseSW = self.NameConv.RMRenameBasedOnBaseName(ControlObject,reverseSW, {'name': reverseSW})
                else:
                    reverseSW = self.NameConv.RMRenameNameInFormat(reverseSW,{})

            self.RMListConstraint(Constrained, Constraints, reverseSW + ".outputX")

        else:

            self.RMListConstraint(Constrained, Constraints, SWMultDiv + ".outputX")
    
    
    def RMListConstraint(self,Constrained, Constraint, Connection):
        index = 0
        for eachObject in Constrained:
            constraint = cmds.parentConstraint(Constraint[index] , eachObject, name = "SpaceSwitch" + self.NameConv.RMGetAShortName(eachObject))[0]
            constraint = self.NameConv.RMRenameBasedOnBaseName(eachObject, constraint, {'name': self.NameConv.RMGetAShortName(constraint)})
            WA = cmds.parentConstraint (constraint, q = True, weightAliasList = True)
            TL = cmds.parentConstraint (constraint, q = True, targetList = True)
            ConstraintIndex = TL.index(Constraint[index])
            cmds.connectAttr(Connection, constraint + "." + WA[ConstraintIndex])
            index +=  1

    def ConstraintVisibility(self, Objects , ControlObject , SpaceSwitchName = 'spaceSwitch', reverse = False ):
        if (self.AddNumericParameter (ControlObject, Name = SpaceSwitchName)):
            SWMultDiv = cmds.shadingNode("multiplyDivide",asUtility = True ,name = SpaceSwitchName + "SWMultDivide" )
            SWMultDiv = self.NameConv.RMRenameBasedOnBaseName(ControlObject, SWMultDiv, {'name': SWMultDiv})
            cmds.connectAttr(ControlObject+"."+SpaceSwitchName ,SWMultDiv+".input1X")
            cmds.setAttr(SWMultDiv+".input2X",10)
            cmds.setAttr(SWMultDiv+".operation",2)
        else:
            SWMultDiv = cmds.listConnections(ControlObject + "." + SpaceSwitchName, type = "multiplyDivide")[0]

        if reverse == True:
            ConnectionsList = cmds.listConnections (SWMultDiv + ".outputX", type = "reverse")
            reverseSW = ""
            if ConnectionsList and len(ConnectionsList) >= 1:
                reverseSW = ConnectionsList[0]
            else :
                reverseSW = cmds.shadingNode('reverse', asUtility=True, name = SpaceSwitchName + "SWReverse")
                reverseSW = self.NameConv.RMRenameBasedOnBaseName(ControlObject, reverseSW, {'name': "SWReverse"})
                cmds.connectAttr( SWMultDiv + ".outputX", reverseSW + ".inputX")

                if self.NameConv.RMIsNameInFormat (ControlObject):
                    reverseSW = self.NameConv.RMRenameBasedOnBaseName(ControlObject,reverseSW, {'name': reverseSW})
                else:
                    reverseSW = self.NameConv.RMRenameNameInFormat(reverseSW,{})
            for eachObject in Objects:
                cmds.connectAttr(reverseSW + ".outputX", eachObject + ".visibility")
        
        else:
            for eachObject in Objects:
                cmds.connectAttr(SWMultDiv + ".outputX", eachObject + ".visibility")



#SW.DeletSpaceSwitchAttr('pCube1')
#SW.CreateSpaceSwitch('group1',['pSphere1','pSphere2'], 'pCube1')
#Node = "pCube1"

#SW.DeleteSpaceSwitchAttr(Node)

#SpaceSwitchName = "spaceSwitch"

#pprint.pprint (SW.GetSpaceSwitchDic(Node))

#print SW.IsSpaceSwitch("pSphere2")
# 

#SW.AddEnumParameters(["Hola","Mundo"], Node, SpaceSwitchName)






