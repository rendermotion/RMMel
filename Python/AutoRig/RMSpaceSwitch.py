import maya.cmds
import maya.api.OpenMaya as om
import RMNameConvention
reload(RMNameConvention)
import RMRigTools
import pprint


class RMSpaceSwitch(object):
    def __init__(self,NameConv = None):
        if not NameConv:
            self.NameConv = RMNameConvention.RMNameConvention()
        else:
            self.NameConv = NameConv
        self.ControlObject = None 
        self.AfectedObjectList = []
        self.SpaceObjectsList = []



    def CreateSpaceSwitchReverse(self,AfectedObject, SpaceObjects, ControlObject, Name = "spaceSwitch", sswtype = "enum"):
        '''
        Creates a simple space Switch that uses a reverse for simple solution it can only hold 2 spaces

        '''
        if sswtype == "enum" and len(SpaceObjects) == 2:
            self.AddEnumParameters(SpaceObjects, ControlObject, Name = Name)

            reverse = cmds.shadingNode('reverse', asUtility=True, name = Name + "SWReverse")
            cmds.connectAttr(ControlObject + "." + Name, reverse + ".inputX")
            
            for eachObject in SpaceObjects:

                parentConstraint = cmds.parentConstraint (eachObject, AfectedObject, mo = True, name = AfectedObject + "SpaceSwitchConstraint")
            
            if self.NameConv.RMIsNameInFormat (AfectedObject):
                reverse = self.NameConv.RMRenameBasedOnBaseName(AfectedObject,reverse, NewName = reverse)
                parentConstraint[0] = self.NameConv.RMRenameBasedOnBaseName (AfectedObject,reverse, NewName = parentConstraint[0])

            else:
                reverse = self.NameConv.RMRenameNameInFormat(reverse)
                parentConstraint[0] = self.NameConv.RMRenameNameInFormat (parentConstraint[0])

            WA = cmds.parentConstraint (parentConstraint, q = True, weightAliasList = True)
            cmds.connectAttr(ControlObject + "." + Name, parentConstraint[0] + "." + WA[1])
            cmds.connectAttr(reverse + ".outputX", parentConstraint[0] + "." + WA[0])


    def CreateSpaceSwitch(self,AfectedObject, SpaceObjects, ControlObject, Name = "spaceSwitch"):
        '''
        Creates a new SpaceSwitch using conditions so it can accept multiple spaces, 
        and it is compatible with the add and remove from Space Switch functions.
        '''
        SpaceObjectShortName =[]
        for i in SpaceObjects:
            SpaceObjectShortName.append(self.NameConv.RMGetAShortName(SpaceObjects))

        self.AddEnumParameters(SpaceObjectShortName, ControlObject, Name = Name)

        index = 0
        for eachObject in SpaceObjects:
            parentConstraint = cmds.parentConstraint (eachObject, AfectedObject, mo = True, name = self.NameConv.RMGetAShortName(AfectedObject) + "SpaceSwitchConstraint")

            Switch = cmds.shadingNode('condition', asUtility=True, name = Name + "SWCondition")
            cmds.connectAttr(ControlObject + "." + Name, Switch + ".firstTerm")
            cmds.setAttr (Switch +".secondTerm", index)
            cmds.setAttr (Switch +".operation", 0)
            cmds.setAttr (Switch +".colorIfTrueR", 1)
            cmds.setAttr (Switch +".colorIfFalseR", 0)
            
            WA = cmds.parentConstraint (parentConstraint, q = True, weightAliasList = True)
            TL = cmds.parentConstraint (parentConstraint, q = True, targetList = True)

            cmds.connectAttr (Switch + ".outColorR", parentConstraint[0] + "." + WA[index])
            if self.NameConv.RMIsNameInFormat(AfectedObject):
                Switch = self.NameConv.RMRenameBasedOnBaseName(AfectedObject, Switch, NewName = Switch)
            else:
                Switch = self.NameConv.RMRenameNameInFormat(Switch)
            index += 1
        
        if self.NameConv.RMIsNameInFormat(AfectedObject):
            parentConstraint[0] = self.NameConv.RMRenameBasedOnBaseName(AfectedObject,reverse, NewName = parentConstraint[0])
        else:
            parentConstraint[0] = self.NameConv.RMRenameNameInFormat(parentConstraint[0])

    def GetSpaceSwitchDic(self, control, SpaceSwitchName = "spaceSwitch"):
        Enums = self.getControlEnumsRelations(Node)
        ConstraintDictionary = self.ConstraintsDictionary (Enums[Enums.keys()[0]]['condition'])

        return {'enums' : Enums , 'constraints' : ConstraintDictionary }


    def GetAfectedObjectsList(self,ControlObject,SpaceSwitchName = "spaceSwitch"):
        SpaceSwDic = GetSpaceSwitchDic(ControlObject, SpaceSwitchName = SpaceSwitchName)
        ReturnObjectsList=[]
        for keys in SpaceSwDic[constraints]:
            ReturnObjectsList.append(SpaceSwDic[constraints][keys]['object'])
        return ReturnObjectsList

    def AddAffectedObject(self,ControlObject, AfectedObject,SpaceSwitchName = "spaceSwitch"):
        SpaceSwDic = GetSpaceSwitchDic(ControlObject,SpaceSwitchName = SpaceSwitchName)
        index = 0
        for eachEnum in SpaceSwDic['enums']:
            parentConstraint = cmds.parentConstraint (SpaceSwDic['enums'][eachEnum]['object'], AfectedObject, mo = True, name = self.NameConv.RMGetAShortName(AfectedObject) + "SpaceSwitchConstraint")
            WA = cmds.parentConstraint (parentConstraint[0], q = True, weightAliasList = True)
            cmds.connectAttr (SpaceSwDic['enums'][eachEnum]['condition'] + ".outColorR", parentConstraint[0] + "." + WA[index])
            index += 1
    def RemoveAffectedObject(self,ControlObject, AfectedObject, SpaceSwitchName = "spaceSwitch"):
        SpaceSwDic = GetSpaceSwitchDic(ControlObject, SpaceSwitchName = SpaceSwitchName)
        
        for allConstraints in SpaceSwDic['constraints']:
            if SpaceSwDic['constraints'][allConstraints]['object'] == AfectedObject:
                cmds.delete(allConstraints)
        if len(SpaceSwDic['constraints'].keys()) > 1:
            for eachPlug in SpaceSwDic['enums']:
                cmds.delete(SpaceSwDic['enums'][eachPlug]['condition'])

    def SpaceObjectsList(self,ControlObject, SpaceSwitchName = "spaceSwitch"):
        SpaceSwDic = GetSpaceSwitchDic( ControlObject, SpaceSwitchName = SpaceSwitchName)
        ObjList=[]
        for eachEnum in SpaceSwDic['enums']:
             ObjList.append(SpaceSwDic['enums'][eachEnum]['object'])
        return ObjList

    def AddSpaceObject(self, ControlObject, SpaceObject):
                

    def RemoveSpaceObject(self):
        pass






    def AddNumericParameter(self,Object, Name = 'spaceSwitch', valueRange = [0,10]):
        AttributeList = cmds.listAttr(Object)
        if Name  in AttributeList:
            print "the Object Allready has an Attribute with this name, the type is:",cmds.getAttr (Object + "." + Name,type=True)
        else :
            cmds.addAttr(Object,at = "float", ln = Name,  hnv = 1, hxv = 1, h = 0, k = 1, smn = valueRange[0], smx = valueRange[1])


    def AddEnumParameters(self, Enum, Object, Name = 'spaceSwitch'):
        AttributeList = cmds.listAttr(Object)
        if Name  in AttributeList:
            if cmds.getAttr (Object + "." + Name,type=True)=='enum':
                print "the Object Allready has an spaceSwitch"
                print "Current Valid types are",cmds.addAttr (Object + "." + Name,q = True,enumName=True)
                EnumsInObject = self.getControlEnums(Object)
                for eachEnum in Enum:
                    if not eachEnum in EnumsInObject:
                        EnumsInObject.append(eachEnum)
                cmds.addAttr(Object + '.' + Name,e=True,ln = Name, en =":".join(EnumsInObject))
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
            returnedDic[eachConstraint] = SW.getParentConstraintDic(eachConstraint)
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
        WA = cmds.parentConstraint (parentConstraint, q = True, weightAliasList = True)
        TL = cmds.parentConstraint (parentConstraint, q = True, targetList = True)
        if len(WA) == len(TL):
            for eachWAIndex in range(0,len(WA)):
                aliasDic[WA[eachWAIndex]] = TL[eachWAIndex]
        
        returnedDic["object"] = cmds.listConnections(parentConstraint + ".constraintRotateX")
        returnedDic["alias"] = aliasDic
        return returnedDic


    def getControlEnums(self, Node, SpaceSwitchName = 'spaceSwitch'):
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
            EnumRelationDic[eachCondition]['plugs'] = SW.getSwitchPlugsDictionary(EnumRelationDic[eachCondition]['condition'])
        


        for eachEnumRD in EnumRelationDic:
            EnumRelationDic [eachEnumRD]['object'] = ""
            for eachPlug in EnumRelationDic[eachEnumRD]['plugs']:
                ConstraintDic = self.getParentConstraintDic(eachPlug)
                if EnumRelationDic[eachEnumRD]['object'] == "":
                    EnumRelationDic[eachEnumRD]['object'] = ConstraintDic['alias'][EnumRelationDic[eachEnumRD]['plugs'][eachPlug]]
                elif EnumRelationDic[eachEnumRD]['object'] != ConstraintDic['alias'][EnumRelationDic[eachEnumRD]['plugs'][eachPlug]]:
                    print "Object mismatch  on Plug" , EnumRelationDic[eachEnumRD]['object'] , ConstraintDic['alias'][EnumRelationDic[eachEnumRD]['plugs'][eachPlug]]
        return EnumRelationDic





SW = RMSpaceSwitch()
#SW.DeletSpaceSwitchAttr('pCube1')
#SW.CreateSpaceSwitch('group1',['pSphere1','pSphere2'], 'pCube1')

#Node = "pCube1"

#SW.DeleteSpaceSwitchAttr(Node)

#SpaceSwitchName = "spaceSwitch"

pprint.pprint (SW.GetSpaceSwitchDic(Node))

#SW.AddEnumParameters(["Hola","Mundo"], Node, SpaceSwitchName)







