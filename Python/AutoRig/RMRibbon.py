import maya.cmds as cmds
import maya.api.OpenMaya as om
import RMNameConvention
import RMRigTools
import RMRigShapeControls
import pymel.core as pm



class RMRibbon(object):
    def __init__ (self):
        self.kinematics = []
        self.joints = []
        self.controls = []
        self.baseObjects = []
        self.jointStructure = []
        self.folicules = []
        self.resetControls = []
        self.allControls = []




    def nurbPlaneBetweenObjects(self, Object01, Object02):
        VP1 = om.MVector(cmds.xform(Object01,a=True,ws=True,q=True,rp=True))
        VP2 = om.MVector(cmds.xform(Object02,a=True,ws=True,q=True,rp=True))
        longitud = VP1 - VP2
        NameConv = RMNameConvention.RMNameConvention()
        plano = cmds.nurbsPlane (ax = [0 ,1 ,0] , p =  [(longitud.length())/2, 0, 0], w = longitud.length(), lr= .05, d = 3, u = 8, v = 1, ch = 0, name = NameConv.RMSetNameInFormat(Name = "%sTo%sPlane"%(NameConv.RMGetAShortName(Object01),NameConv.RMGetAShortName(Object02)),Side = NameConv.RMGetFromName(Object02,"Side"), System = "Ribbons")  )

        RMRigTools.RMAlign (Object01, plano[0], 3)
        return plano[0]

    #nurbPlaneBetweenObjects("joint1","joint2")
    def RibbonCreation(self, Object01,Object02,foliculeNumber=5):
        self.baseObjects.append(Object01)
        self.baseObjects.append(Object02)


        NameConv = RMNameConvention.RMNameConvention()
        VP1 = om.MVector(cmds.xform(Object01,a=True,ws=True,q=True,rp=True))
        VP2 = om.MVector(cmds.xform(Object02,a=True,ws=True,q=True,rp=True))
        plano = self.nurbPlaneBetweenObjects(Object01,Object02)
        planoShape = cmds.listRelatives(plano, shapes = True )[0]
        cmds.select(cl = True)
        RibbonSize = VP1 - VP2

        print "plano = %s" % plano
        print "len = %s" % RibbonSize.length()
        
        MainSkeleton = cmds.group(em = True, name = NameConv.RMSetNameInFormat(Name = "%sTo%sRibbon"    %(NameConv.RMGetAShortName(Object01), NameConv.RMGetAShortName(Object02)), Side = NameConv.RMGetFromName(Object02,"Side"), System = "Ribbons"))
        HairGroup    = cmds.group(em = True, name = NameConv.RMSetNameInFormat(Name = "%sTo%sHairSystem"%(NameConv.RMGetAShortName(Object01), NameConv.RMGetAShortName(Object02)), Side = NameConv.RMGetFromName(Object02,"Side"), System = "Ribbons"))

        nstep = 1.0/(foliculeNumber - 1.0)
        Hys = pm.language.Mel.eval('createNode hairSystem')
        Hys = "hairSystem1"
        ArrayJoints = []
        HairSystemIndex = [0]

        folicules = [] 

        for n in range(foliculeNumber):
            pm.language.Mel.eval('createHairCurveNode("%s", "%s" ,%s ,.5 , 1 ,0 ,0 ,0 ,0 ,"" ,1.0 ,{%s} ,"" ,"" ,2 );'%(Hys,planoShape, nstep*n,n))
            NewFolicule = NameConv.RMRenameNameInFormat("follicle1", Side = NameConv.RMGetFromName(Object02,"Side"))
            folicules.append(NewFolicule )
            cmds.parent(NewFolicule, HairGroup )
        self.folicules = folicules
        cmds.delete(cmds.listRelatives(Hys, p = True))
        index = 0
        skinedJoints = cmds.group(em = True, name = NameConv.RMSetNameInFormat(Name = "%sTo%sskinedJoints"%(NameConv.RMGetAShortName(Object01), NameConv.RMGetAShortName(Object02)), Side = NameConv.RMGetFromName(Object02,"Side"), System = "Ribbons"))
        for eachFolicule in folicules:
            ArrayJoints.append(cmds.joint(name = NameConv.RMSetNameInFormat(Name = "%sTo%sRibbonJoints" % (NameConv.RMGetAShortName(Object01), NameConv.RMGetAShortName(Object02)), Side = NameConv.RMGetFromName(Object02,"Side"), System = "Ribbons") ) )
            RMRigTools.RMAlign(eachFolicule, ArrayJoints[index],3)
            cmds.parentConstraint( eachFolicule, ArrayJoints[index])
            index +=1
        self.jointStructure = ArrayJoints

        controles = []
        resetControles = []
        locatorControlesList = []
        locatorLookAtList    = []
        jointsLookAtList     = []
        groupLookAtList      = []

        GroupControls = cmds.group( empty=True, name = NameConv.RMSetNameInFormat(Name = "%sTo%sControls"%(NameConv.RMGetAShortName(Object01), NameConv.RMGetAShortName(Object02)), Side = NameConv.RMGetFromName(Object02,"Side"), System = "Ribbons"))
        GroupJoints   = cmds.group( empty=True, name = NameConv.RMSetNameInFormat(Name = "%sTo%sGroupJointsLookAt"%(NameConv.RMGetAShortName(Object01), NameConv.RMGetAShortName(Object02)), Side = NameConv.RMGetFromName(Object02,"Side"), System = "Ribbons"))
        RigControls = RMRigShapeControls.RMRigShapeControls()

        self.allControls.append(GroupControls)
        self.joints.append(GroupJoints)

        for iloop in range(3):

            resetControlGroup , control = RigControls.RMCircularControl( Object01, radius = RibbonSize.length()/ 3 , name = NameConv.RMSetNameInFormat(Name = "%sTo%sCtrl"%(NameConv.RMGetAShortName(Object01), NameConv.RMGetAShortName(Object02)) ,Side = NameConv.RMGetFromName(Object02,"Side"), Type = 'ctrl', System = "Ribbons") )
            controles.append ( control )
            resetControles.append( resetControlGroup )

            locatorControl = cmds.spaceLocator ( name = NameConv.RMSetNameInFormat(Name = "%sTo%sLocatorCntrl"%(NameConv.RMGetAShortName(Object01), NameConv.RMGetAShortName(Object02)), Type = 'spaceLocator',Side = NameConv.RMGetFromName(Object02,"Side"), System = "Ribbons"))
            locatorControlesList.append(locatorControl[0])
            RMRigTools.RMAlign( Object01, locatorControl[0], 3)

            locatorLookAt = cmds.spaceLocator ( name = NameConv.RMSetNameInFormat(Name = "%sTo%sLocatorLookAt"%(NameConv.RMGetAShortName(Object01), NameConv.RMGetAShortName(Object02)),Type = 'spaceLocator', Side = NameConv.RMGetFromName(Object02,"Side"), System = "Ribbons"))
            locatorLookAtList.append(locatorLookAt[0])
            RMRigTools.RMAlign( Object01, locatorLookAt[0], 3)

            cmds.select(clear = True)

            jointsLookAt = cmds.joint(name = NameConv.RMSetNameInFormat(Name = "%sTo%sJointsLookAt"%(NameConv.RMGetAShortName(Object01), NameConv.RMGetAShortName(Object02)),Type = 'joint', Side = NameConv.RMGetFromName(Object02,"Side"), System = "Ribbons"))
            jointsLookAtList.append( jointsLookAt )
            RMRigTools.RMAlign( Object01, jointsLookAt, 3)

            groupLookAt = cmds.group(empty = True, name = NameConv.RMSetNameInFormat(Name = "%sTo%sGroupLookAt"%(NameConv.RMGetAShortName(Object01), NameConv.RMGetAShortName(Object02)),Type = 'transform' ,Side = NameConv.RMGetFromName(Object02,"Side"), System = "Ribbons"))
            self.kinematics.append(groupLookAt)
            groupLookAtList.append( groupLookAt )
            RMRigTools.RMAlign( Object01, groupLookAt, 3)

            cmds.parent(groupLookAtList, MainSkeleton)


            cmds.move ( RibbonSize.length()/2*iloop , 0, 0, resetControlGroup, r=True,os=True, moveX   = True )
            cmds.move ( RibbonSize.length()/2*iloop , 0, 0, locatorControl, r=True,os=True, moveX   = True )
            cmds.move ( RibbonSize.length()/2*iloop , 0, 1, locatorLookAt, r=True,os=True, moveXYZ = True )
            cmds.move ( RibbonSize.length()/2*iloop , 0, 0, jointsLookAt, r=True,os=True, moveX   = True )
            cmds.move ( RibbonSize.length()/2*iloop , 0, 0, groupLookAt  , r=True,os=True, moveX   = True)

            cmds.parent (resetControlGroup , GroupControls)
            cmds.parent (locatorControl    , groupLookAt)
            cmds.parent (locatorLookAt     , groupLookAt)
            cmds.parent (jointsLookAt      , GroupJoints)

            cmds.makeIdentity( control     , apply=True, t=1, r = 0, s = 1, n = 0)
            cmds.makeIdentity( jointsLookAt, apply=True, t=1, r = 0, s = 1, n = 0)

            cmds.parentConstraint(locatorControl, jointsLookAt)
            cmds.parentConstraint(control       , groupLookAt)
        print "Controles[1]:%s"           %controles[1]
        print "locatorControlesList[1]:%s"%locatorControlesList[0]
        print "groupLookAtList[1]:%s"%groupLookAtList[0]
        print "locatorLookAtList:%s"%locatorLookAtList
        self.controls = controles
        self.resetControls = resetControles
        self.resetControls = resetControles
        cmds.aimConstraint(controles[1], locatorControlesList[0] , aim = [1,0,0], upVector = [0,0,1], wut='object', worldUpObject = locatorLookAtList[0])
        cmds.aimConstraint(controles[1], locatorControlesList[2] , aim = [1,0,0], upVector = [0,0,1], wut='object', worldUpObject = locatorLookAtList[2])

        cmds.parent(GroupJoints, MainSkeleton)

        cmds.select ( plano   , replace=True )
        print jointsLookAtList
        for eachJoint in jointsLookAtList:
            cmds.select (eachJoint , add=True )
        cmds.SmoothBindSkin()
        cmds.parent (plano, HairGroup)

if __name__ == '__main__':
    Ribbon=RMRibbon()
    Ribbon.RibbonCreation('joint1', 'joint2', foliculeNumber = 4)





