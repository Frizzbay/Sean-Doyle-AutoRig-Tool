import maya.cmds as base
import importlib
import Locators
import Joints
import SecondaryLocators as SL
import Controller
import CreateIK
import Constraints
import FaceJoints as FJ

import os

reload_locators = importlib.reload(Locators)
reload_joints = importlib.reload(Joints)
reload_SL = importlib.reload(SL)
reload_controller = importlib.reload(Controller)
reload_IK = importlib.reload(CreateIK)
reload_constraints = importlib.reload(Constraints)
reload_FJ = importlib.reload(FJ)

global selected
global prefix


class AutoRigger:
    # self refers to the instance of the class that is created from __init__ and can be called anything.
    # init initialises the object and executes instructions at the time of creation
    def __init__(self):
        base.currentUnit(linear='meter')
        base.grid(size=12, spacing=5, divisions=5)
        # print(os.path_dirname(os.path.realpath(__file__)))
        self.BuildUI()

    def BuildUI(self):
        # Create the basic window
        base.window("Auto Rigger")

        # base.rowColumnLayout(nc=2)  # nc means 'Number of columns'
        base.columnLayout(adj=True)

        settings_text = base.text('Settings', l='Rig Settings')
        base.separator(st='none')
        base.text(label='Prefix', w=100)
        prefix = base.textFieldGrp(w=100, text='Test', editable=True)
        base.text(label="Amount of Spines", w=100)
        self.spine_count = base.intSliderGrp(l="Spine Count", minValue=1, maxValue=10, value=4, step=1, field=True)
        # self.spine_count = base.intField(minValue=1, maxValue=10, value=4)
        base.text(l="Amount of Fingers", w=100)
        self.finger_count = base.intSliderGrp(l="Finger Count", minValue=1, maxValue=10, value=5, step=1, field=True)
        # self.finger_count = base.intField(minValue=1, maxValue=10, value=5)
        base.separator(st='none')
        self.double_elbow = base.checkBox(l='Double Elbow', align='left')

        base.button(l="Create Base Locators", width=200, command=self.DoLocators)
        base.separator(st='none')
        base.button(l="Delete Locators", width=200, command="Locators.delete_locators()")
        base.separator(st='none')
        base.button(l="Create Secondary Locators", width=200, command="SL.SecondaryLocators()")
        base.separator(st='none')
        base.button(l="Create Facial Locators", w=200, c=self.face_locators)
        base.separator(st='none')
        base.button(l="Mirror L->R", w=200, c="Locators.mirror_locators()")
        base.separator(st='none')
        base.button(l="Joints Window", w=200, c='Joints.create_joints_window()')
        base.separator(st='none')
        base.button(l="Finalize Rig", w=200, c=self.finalize_rig)
        base.button(l="Bind Skin", w=200, c="Constraints.bind_skin()")
        base.separator(st='none')
        # base.button(l="FACE CONSTRAINTS", w=200, c="FJ.FaceJoints().add_constraints(self)")

        base.setParent('..')
        ch4 = base.rowColumnLayout(nc=1, cal=(1, 'right'), adjustableColumn=True)
        base.button(l="Add Facial Joints", w=200, c=self.FaceJoints)
        base.separator(st='none')

        base.separator(st='none')

        # Show the actual window
        base.showWindow()

    def DoLocators(self, void):
        _spineCount = base.intSliderGrp(self.spine_count, q=True, v=True)
        _fingerCount = base.intSliderGrp(self.finger_count, q=True, v=True)
        _doubleElbow = base.checkBox(self.double_elbow, q=True, v=True)

        Locators.create_locators(_spineCount, _fingerCount, _doubleElbow)

    def face_locators(self, void):
        FJ.FaceJoints().create_face_window(self)

    def FaceJoints(self, void):
        FJ.FaceJoints().create_joints(self)

    def finalize_rig(self, void):
        _spineCount = base.intSliderGrp(self.spine_count, q=True, v=True)
        _fingerCount = base.intSliderGrp(self.finger_count, q=True, v=True)

        Controller.create_controller(_spineCount, _fingerCount)
        CreateIK.IK_handles()
        Constraints.create_constraints(_fingerCount, _spineCount)
        if base.objExists('FACE_LOC_GRP'):
            FJ.FaceJoints().add_constraints(self)

