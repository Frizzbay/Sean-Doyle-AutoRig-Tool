import maya.cmds as base
import Locators

import importlib

reload_locators = importlib.reload(Locators)


def create_joints_window():
    global setPrefix
    setPrefix = "test"

    base.window("Joint Creation")
    base.rowColumnLayout(nc=1)
    base.button(l="Create Joints", w=200, c="Joints.create_joints()")
    base.button(l="Set Orientation", w=200, c="Joints.set_joint_orientation()")
    base.button(l="Delete Joints", w=200, c="Joints.delete_joints()")
    base.showWindow()


def create_joints():
    base.select(deselect=True)
    spine_amount = base.ls("Loc_SPINE_*", type='transform')
    fingers_amount = base.ls("Loc_L_Finger_*_0", type='transform')

    if base.objExists('RIG'):
        print("RIG already exists!")
    else:
        joint_grp = base.group(em=True, name='RIG')

        #  CREATE SPINE JOINTS
    root = base.ls("Loc_ROOT")

    all_spines = base.ls("Loc_SPINE_*", type='locator')
    spine = base.listRelatives(*all_spines, p=True, f=True)  # p = parent, f = full name

    root_pos = base.xform(root, query=True, translation=True, ws=True)
    root_joint = base.joint(radius=4.0, position=root_pos, name="RIG_ROOT")
    # base.parent(root_joint, world=True, absolute=True)  - How to un-parent something if needed

    base.parent(root_joint, w=True, a=True)
    base.parent(root_joint, "RIG", absolute=True)

    for i, s in enumerate(spine):
        pos = base.xform(s, q=True, t=True, ws=True)
        joint = base.joint(radius=4.0, p=pos, name="RIG_SPINE_" + str(i))

    create_head_joints(len(spine_amount))
    create_arm_joints(len(spine_amount))
    create_finger_joints(len(fingers_amount))

    if base.objExists("Loc_Volume_0"):
        create_volume_joints()

    if base.objExists("Loc_L_INV_Heel*"):
        create_inverse_foot_roll()
    else:
        print("CANT FOOTROLL")

    create_legs()
    set_joint_orientation()


def create_volume_joints():
    all_spines = base.ls("RIG_SPINE_*", type="joint")
    volume_loc = base.ls("Loc_Volume_*", type="transform")
    l_chest_volume = base.ls("Loc_L_ChestVolume_*", type="transform")
    r_chest_volume = base.ls("Loc_R_ChestVolume_*", type="transform")
    print(all_spines)
    print(volume_loc)
    for i, s in enumerate(all_spines):
        if i == len(all_spines) - 1:
            # If the iteration(i) and the spine amount(all_spines) is 0 then this happens
            base.select(s)
            start_pos = base.xform(s, q=True, t=True, ws=True)
            pos = base.xform(base.ls("Loc_Breathing", type="transform"), q=True, t=True, ws=True)
            base.joint(radius=0.8, position=(start_pos[0], start_pos[1], start_pos[2] + 0.05), name="RIG_BREATHING_START")
            base.joint(radius=0.8, position=pos, name="RIG_BREATHING_END")
        else:
            base.select(s)
            pos = base.xform(volume_loc[i], query=True, translation=True, worldSpace=True)
            l_chest_pos = base.xform(l_chest_volume[i], query=True, translation=True, worldSpace=True)
            r_chest_pos = base.xform(r_chest_volume[i], query=True, translation=True, worldSpace=True)

            volume_joint = base.joint(radius=0.8, p=pos, name="RIG_VOLUME_" + str(i))
            base.select(s)
            l_chest_volume_joint = base.joint(radius=0.8, p=l_chest_pos, name="RIG_L_CHEST_VOLUME_" + str(i))
            base.select(s)
            r_chest_volume_joint = base.joint(radius=0.8, p=r_chest_pos, name="RIG_R_CHEST_VOLUME_" + str(i))


def create_head_joints(spine_amount):
    base.select(deselect=True)
    base.select("RIG_SPINE_" + str(spine_amount - 1))

    base.joint(radius=4, p=base.xform(base.ls("Loc_Neck_Start"), q=True, t=True, ws=True), name="RIG_Neck_Start")
    base.joint(radius=4, p=base.xform(base.ls("Loc_Neck_End"), q=True, t=True, ws=True), name="RIG_Neck_End")
    base.joint(radius=4, p=base.xform(base.ls("Loc_Head"), q=True, t=True, ws=True), name="RIG_Head")

    base.select(deselect=True)
    base.select("RIG_Neck_End")

    jaw_joint_start = base.joint(radius=4, p=base.xform(base.ls("Loc_Jaw_Start"), q=True, t=True, ws=True),
                                 name="RIG_Jaw_Start")
    jaw_joint_end = base.joint(radius=4, p=base.xform(base.ls("Loc_Jaw_End"), q=True, t=True, ws=True),
                               name="RIG_Jaw_End")


def create_arm_joints(spine_amount):
    base.select(deselect=True)
    base.select("RIG_SPINE_" + str(spine_amount - 1))

    l_clavicle_joint = base.joint(radius=4, position=base.xform(base.ls("Loc_L_Clavicle"), q=True, t=True, ws=True), name="RIG_L_Clavicle")
    l_upper_arm_joint = base.joint(radius=4, position=base.xform(base.ls("Loc_L_UpperArm"), q=True, t=True, ws=True), name="RIG_L_UpperArm")

    if base.objExists("Loc_R_Elbow_2"):

        l_elbow_joint = base.joint(radius=4, position=base.xform(base.ls("Loc_L_Elbow_1"), q=True, t=True, ws=True), name="RIG_L_Elbow_1")
        l_elbow_joint = base.joint(radius=4, position=base.xform(base.ls("Loc_L_Elbow_2"), q=True, t=True, ws=True), name="RIG_L_Elbow_2")
    else:
        l_elbow_joint = base.joint(radius=4, position=base.xform(base.ls("Loc_L_Elbow"), q=True, t=True, ws=True), name="RIG_L_Elbow")

    if base.objExists("Loc_L_ArmTwist_*"):
        l_arm_twists = base.ls("Loc_L_ArmTwist_*", type='transform')
        print(l_arm_twists)
        for i, a in enumerate(l_arm_twists):
            l_twist_joint = base.joint(radius=4, position=base.xform(a, q=True, t=True, ws=True), name="RIG_L_ArmTwist_" + str(i))
    else:
        print("")
    l_wrist_joint = base.joint(radius=4, position=base.xform(base.ls("Loc_L_Wrist"), q=True, t=True, ws=True), name="RIG_L_Wrist")

    base.select(deselect=True)
    base.select("RIG_SPINE_" + str(spine_amount - 1))

    r_clavicle_joint = base.joint(radius=4, position=base.xform(base.ls("Loc_R_Clavicle"), q=True, t=True, ws=True), name="RIG_R_Clavicle")
    r_upper_arm_joint = base.joint(radius=4, position=base.xform(base.ls("Loc_R_UpperArm"), q=True, t=True, ws=True), name="RIG_R_UpperArm")

    if base.objExists("Loc_R_Elbow_2"):

        r_elbow_joint = base.joint(radius=4, position=base.xform(base.ls("Loc_R_Elbow_1"), q=True, t=True, ws=True), name="RIG_R_Elbow_1")
        r_elbow_joint = base.joint(radius=4, position=base.xform(base.ls("Loc_R_Elbow_2"), q=True, t=True, ws=True), name="RIG_R_Elbow_2")
    else:
        r_elbow_joint = base.joint(radius=4, position=base.xform(base.ls("Loc_R_Elbow"), q=True, t=True, ws=True), name="RIG_R_Elbow")

    if base.objExists("Loc_R_ArmTwist_*"):
        r_arm_twists = base.ls("Loc_R_ArmTwist_*", type='transform')
        print(r_arm_twists)
        for i, a in enumerate(r_arm_twists):
            r_twist_joint = base.joint(radius=4, position=base.xform(a, q=True, t=True, ws=True),
                                       name="RIG_R_ArmTwist_" + str(i))
    else:
        print("")
    r_wrist_joint = base.joint(radius=4, position=base.xform(base.ls("Loc_R_Wrist"), q=True, t=True, ws=True), name="RIG_R_Wrist")


def create_finger_joints(fingers_amount):
    for x in range(0, fingers_amount):
        create_finger(x)


def create_finger(i):
    base.select(deselect=True)
    base.select("RIG_L_Wrist")
    all_fingers = base.ls("Loc_L_Finger_" + str(i) + "_*", type='transform')
    fingers = base.listRelatives(all_fingers, p=True, s=False)

    for x, f in enumerate(all_fingers):
        pos = base.xform(f, q=True, t=True, ws=True)
        j = base.joint(radius=4, p=pos, name="RIG_L_Finger_" + str(i) + "_" + str(x))

    base.select(deselect=True)
    base.select("RIG_R_Wrist")
    r_all_fingers = base.ls("Loc_R_Finger_" + str(i) + "_*", type='transform')
    r_fingers = base.listRelatives(r_all_fingers, parent=True, shapes=False)

    for y, g in enumerate(r_all_fingers):
        r_pos = base.xform(g, q=True, t=True, ws=True)
        r_j = base.joint(radius=4, p=r_pos, name="RIG_R_Finger_" + str(i) + "_" + str(y))


def create_legs():
    base.select(deselect=True)
    base.select("RIG_ROOT")

    l_upper_leg_joint = base.joint(radius=4, p=base.xform(base.ls('Loc_L_UpperLeg', type='transform'), q=True, t=True, ws=True), name="RIG_L_UpperLeg")
    l_knee_joint = base.joint(radius=4, p=base.xform(base.ls('Loc_L_LowerLeg', type='transform'), q=True, t=True, ws=True), name="RIG_L_Knee")
    l_foot_joint = base.joint(radius=4, p=base.xform(base.ls('Loc_L_Foot', type='transform'), q=True, t=True, ws=True), name="RIG_L_Foot")
    l_ball_joint = base.joint(radius=4, p=base.xform(base.ls('Loc_L_Foot_Ball', type='transform'), q=True, t=True, ws=True), name="RIG_L_Ball")
    l_toes_joint = base.joint(radius=4, p=base.xform(base.ls('Loc_L_Toes', type='transform'), q=True, t=True, ws=True), name="RIG_L_Toes")

    base.select(deselect=True)
    base.select("RIG_ROOT")

    l_upper_leg_joint = base.joint(radius=4, p=base.xform(base.ls('Loc_R_UpperLeg', type='transform'), q=True, t=True, ws=True), name="RIG_R_UpperLeg")
    l_knee_joint = base.joint(radius=4, p=base.xform(base.ls('Loc_R_LowerLeg', type='transform'), q=True, t=True, ws=True), name="RIG_R_Knee")
    l_foot_joint = base.joint(radius=4, p=base.xform(base.ls('Loc_R_Foot', type='transform'), q=True, t=True, ws=True), name="RIG_R_Foot")
    l_ball_joint = base.joint(radius=4, p=base.xform(base.ls('Loc_R_Foot_Ball', type='transform'), q=True, t=True, ws=True), name="RIG_R_Ball")
    l_toes_joint = base.joint(radius=4, p=base.xform(base.ls('Loc_R_Toes', type='transform'), q=True, t=True, ws=True), name="RIG_R_Toes")


def create_inverse_foot_roll():
    base.select(deselect=True)
    l_heel = base.joint(radius=4.0, p=base.xform(base.ls('Loc_L_INV_Heel'), q=True, t=True, ws=True), name="RIG_L_INV_Heel")
    l_toes = base.joint(radius=4.0, p=base.xform(base.ls('Loc_L_INV_Toes'), q=True, t=True, ws=True), name="RIG_L_INV_Toes")
    l_ball = base.joint(radius=4.0, p=base.xform(base.ls('Loc_L_INV_Ball'), q=True, t=True, ws=True), name="RIG_L_INV_Ball")
    l_ankle = base.joint(radius=4.0, p=base.xform(base.ls('Loc_L_INV_Ankle'), q=True, t=True, ws=True), name="RIG_L_INV_Ankle")
    base.parent(l_heel, "RIG")

    base.select(deselect=True)
    r_heel = base.joint(radius=4.0, p=base.xform(base.ls('Loc_R_INV_Heel'), q=True, t=True, ws=True), name="RIG_R_INV_Heel")
    r_toes = base.joint(radius=4.0, p=base.xform(base.ls('Loc_R_INV_Toes'), q=True, t=True, ws=True), name="RIG_R_INV_Toes")
    r_ball = base.joint(radius=4.0, p=base.xform(base.ls('Loc_R_INV_Ball'), q=True, t=True, ws=True), name="RIG_R_INV_Ball")
    r_ankle = base.joint(radius=4.0, p=base.xform(base.ls('Loc_R_INV_Ankle'), q=True, t=True, ws=True), name="RIG_R_INV_Ankle")
    base.parent(r_heel, "RIG")


def set_joint_orientation():
    base.select("RIG_ROOT")
    base.joint(edit=True, children=True, orientJoint="xyz", secondaryAxisOrient='xup')


def delete_joints():
    base.select(deselect=True)
    base.delete(base.ls('RIG'))
