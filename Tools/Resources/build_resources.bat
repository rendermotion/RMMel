pyside-uic --from-imports RMINTRigTools.ui > ../UI/RMFormRigTools.py
pyside-uic --from-imports RMRigDisplay.ui > ../UI/RMFormRigDisplay.py
pyside-uic --from-imports RMblendShapeEditor.ui > ../UI/RMFormBlendShapeEditor.py
pyside-uic --from-imports RMCopyPosition.ui > ../UI/RMFormCopyPosition.py
pyside-uic --from-imports FacialLink.ui > ../UI/RMFormFacialLink.py
pyside-uic --from-imports RMSpaceSwitchTool.ui > ../UI/RMFormSpaceSwitch.py
pyside-uic --from-imports Autorig.ui > ../UI/RMFormAutorig.py
pyside-uic --from-imports RMVisibilityTool.ui > ../UI/RMFormVisibilityTool.py
pyside-uic --from-imports GenericPropRigTool.ui > ../UI/RMFormGenericPropRigTool.py
pyside-uic --from-imports RMFormLaces.ui > ../UI/RMFormLaces.py
pyside-uic --from-imports BlendShapeCreatorHelper.ui > ../UI/RMFormBSCreatorHelper.py
pyside-uic --from-imports RMFacialRig.ui > ../UI/RMFormFacialRig.py


maya -m API