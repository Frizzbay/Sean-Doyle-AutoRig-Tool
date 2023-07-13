import maya.cmds as base


def create_constraints(finger_count, spine_count):
    # left
    l_wrist_ctrl = base.ls("CTRL_L_Wrist", type="transform")
    l_wrist_ik = base.ls("IK_L_Arm")  # don't need to declare type = 'transform' because the IK has no shape
    l_wrist_joint = base.ls("RIG_L_Wrist")

    # right
    r_wrist_ctrl = base.ls("CTRL_R_Wrist", type="transform")
    r_wrist_ik = base.ls("IK_R_Arm")  # don't need to declare type = 'transform' because the IK has no shape
    r_wrist_joint = base.ls("RIG_R_Wrist")

    # First object controls other object, maintainOffset keeps everything at its current position
    base.pointConstraint(l_wrist_ctrl, l_wrist_ik, maintainOffset=True)
    base.orientConstraint(l_wrist_ctrl, l_wrist_joint, mo=True)
    base.connectAttr("CTRL_L_Wrist.Elbow_PV", "IK_L_Arm.twist")

    base.pointConstraint(r_wrist_ctrl, r_wrist_ik, maintainOffset=True)
    base.orientConstraint(r_wrist_ctrl, r_wrist_joint, mo=True)
    base.connectAttr("CTRL_R_Wrist.Elbow_PV", "IK_R_Arm.twist")

    base.orientConstraint("CTRL_L_Clavicle", "RIG_L_Clavicle", maintainOffset=True)
    base.orientConstraint("CTRL_R_Clavicle", "RIG_R_Clavicle", maintainOffset=True)
    base.orientConstraint("CTRL_NECK", "RIG_Neck_Start", maintainOffset=True)
    base.orientConstraint("CTRL_HEAD", "RIG_Neck_End", maintainOffset=True)
    base.orientConstraint("CTRL_JAW", "RIG_Jaw_Start", maintainOffset=True)
    if base.objExists("CTRL_BREATHING"):
        base.orientConstraint("CTRL_BREATHING", "RIG_BREATHING_START", maintainOffset=True)

    base.connectAttr("CTRL_SPINE_" + str(spine_count - 1) + ".rotateY", "IK_Spine.twist")

    if base.objExists("RIG_L_ArmTwist_0"):
        l_twist_joints = base.ls("RIG_L_ArmTwist_*")
        r_twist_joints = base.ls("RIG_R_ArmTwist_*")
        # for each twist joint we create a multiplyDivide shading node
        for i, x in enumerate(l_twist_joints):
            # Creating a multiplyDivide node in the node editor
            l_wrist_multiply = base.shadingNode("multiplyDivide", asUtility=True, name="L_ArmTwist_Node_" + str(i))
            # operation 1 is equal to 'Multiply' on the drop-down menu on the node itself.  0 = No Operation, 1 = Multiply, 2 = Divide, 3 = Power
            base.setAttr(l_wrist_multiply + ".operation", 1)
            # Sets the actual value of the input to 1 and then 1 divided by the amount of joints so that all the twist joints rotate at the appropriate rates
            base.setAttr(l_wrist_multiply + ".input2Y", 1 - (1 / len(l_twist_joints) * (i + 1)))
            #         Iteration starts at 0.  Say there is 3 Twist joints.  1 DIVIDED BY 3 = 0.333. 0.333 TIMES 0 EQUALS 0. PLUS 1 = 1.333. THEN 1 - 1.333 GIVES 0.666 Which is the rate at which that joint will rotate.  I don't know if this explanation is good but the maths actually does check out if you use a calculater.  I think it's easier if you do.
            #         INPUT
            base.connectAttr("CTRL_L_Wrist.rotateY", "L_ArmTwist_Node_" + str(i) + ".input1Y")
            #         OUTPUT
            base.connectAttr("L_ArmTwist_Node_" + str(i) + ".outputY", "RIG_L_ArmTwist_*" + str(i) + ".rotateX")

            r_wrist_multiply = base.shadingNode("multiplyDivide", asUtility=True, name="R_ArmTwist_Node_" + str(i))
            # operation 1 is equal to 'Multiply' on the drop-down menu on the node itself.  0 = No Operation, 1 = Multiply, 2 = Divide, 3 = Power
            base.setAttr(r_wrist_multiply + ".operation", 1)
            # Sets the actual value of the input to 1 and then 1 divided by the amount of joints so that all the twist joints rotate at the appropriate rates
            base.setAttr(r_wrist_multiply + ".input2Y", 1 - (1 / len(r_twist_joints) * (i + 1)))
            #         Iteration starts at 0.  Say there is 3 Twist joints.  1 DIVIDED BY 3 = 0.333. 0.333 TIMES 0 EQUALS 0. PLUS 1 = 1.333. THEN 1 - 1.333 GIVES 0.666 Which is the rate at which that joint will rotate.  I don't know if this explanation is good but the maths actually does check out if you use a calculater.  I think it's easier if you do.
            #         INPUT
            base.connectAttr("CTRL_R_Wrist.rotateY", "R_ArmTwist_Node_" + str(i) + ".input1Y")
            #         OUTPUT
            base.connectAttr("R_ArmTwist_Node_" + str(i) + ".outputY", "RIG_R_ArmTwist_*" + str(i) + ".rotateX")

    clusters = base.ls("Spine_Cluster_*_Handle", type='transform')
    spine_ctrl = base.ls("CTRL_SPINE_*", type='transform')

    for j, cl in enumerate(clusters):
        if j > 0:
            base.parent(cl, spine_ctrl[j - 1])
        else:
            base.parent(cl, "CTRL_PELVIS")

    for k in range(0, finger_count):
        l_all_fingers = base.ls("RIG_L_Finger_" + str(k) + "_*")
        r_all_fingers = base.ls("RIG_R_Finger_" + str(k) + "_*")

        for L in range(0, 3):
            if k > 0:
                base.connectAttr("CTRL_L_Finger_" + str(k) + "_" + str(L) + ".rotateZ", l_all_fingers[L] + ".rotateZ")
                base.connectAttr("CTRL_R_Finger_" + str(k) + "_" + str(L) + ".rotateZ", r_all_fingers[L] + ".rotateZ")
                base.connectAttr("CTRL_L_Finger_" + str(k) + "_" + str(L) + ".rotateX", l_all_fingers[L] + ".rotateY")
                base.connectAttr("CTRL_R_Finger_" + str(k) + "_" + str(L) + ".rotateX", r_all_fingers[L] + ".rotateY")
            else:
                base.connectAttr("CTRL_L_Finger_" + str(k) + "_" + str(L) + ".rotateZ", l_all_fingers[L] + ".rotateZ")
                base.connectAttr("CTRL_R_Finger_" + str(k) + "_" + str(L) + ".rotateZ", r_all_fingers[L] + ".rotateZ")
                base.connectAttr("CTRL_L_Finger_" + str(k) + "_" + str(L) + ".rotateX", l_all_fingers[L] + ".rotateY")
                base.connectAttr("CTRL_R_Finger_" + str(k) + "_" + str(L) + ".rotateX", r_all_fingers[L] + ".rotateY")

    if base.objExists("RIG_L_INV_Heel"):
        base.pointConstraint("RIG_L_INV_Toes", "IK_L_Toes", maintainOffset=True)
        base.pointConstraint("RIG_L_INV_Ball", "IK_L_FootBall", maintainOffset=True)
        base.pointConstraint("RIG_L_INV_Ankle", "IK_L_Leg", maintainOffset=True)

        base.pointConstraint("RIG_R_INV_Toes", "IK_R_Toes", maintainOffset=True)
        base.pointConstraint("RIG_R_INV_Ball", "IK_R_FootBall", maintainOffset=True)
        base.pointConstraint("RIG_R_INV_Ankle", "IK_R_Leg", maintainOffset=True)

        base.pointConstraint("CTRL_L_Foot", "RIG_L_INV_Heel", maintainOffset=True)
        base.orientConstraint("CTRL_L_Foot", "RIG_L_INV_Heel", maintainOffset=True)

        base.pointConstraint("CTRL_R_Foot", "RIG_R_INV_Heel", maintainOffset=True)
        base.orientConstraint("CTRL_R_Foot", "RIG_R_INV_Heel", maintainOffset=True)

        base.connectAttr("CTRL_L_Foot.Foot_Roll", "RIG_L_INV_Ball.rotateX")
        base.connectAttr("CTRL_L_Foot.Ball_Roll", "RIG_L_INV_Toes.rotateX")

        base.connectAttr("CTRL_R_Foot.Foot_Roll", "RIG_R_INV_Ball.rotateX")
        base.connectAttr("CTRL_R_Foot.Ball_Roll", "RIG_R_INV_Toes.rotateX")

    else:
        base.parent("IK_L_Toes", "IK_L_FootBall")
        base.parent("IK_L_FootBall", "IK_L_Leg")

        base.parent("IK_R_Toes", "IK_R_FootBall")
        base.parent("IK_R_FootBall", "IK_R_Leg")

        base.pointConstraint("CTRL_R_Foot", "IK_R_Leg", maintainOffset=True)
        base.orientConstraint("CTRL_R_Foot", "IK_R_Leg", maintainOffset=True)

        base.pointConstraint("CTRL_L_Foot", "IK_L_Leg", maintainOffset=True)
        base.orientConstraint("CTRL_L_Foot", "IK_L_Leg", maintainOffset=True)

    # Feet Constraints

    # Left
    base.setAttr("IK_L_Leg.poleVectorX", 1)
    base.setAttr("IK_L_Leg.poleVectorZ", 0)
    l_foot_average = base.shadingNode("plusMinusAverage", asUtility=True, name="L_Foot_Node")
    base.setAttr(l_foot_average + ".operation", 2)
    base.connectAttr("CTRL_L_Foot.Knee_Fix", l_foot_average + ".input1D[0]")
    base.connectAttr("CTRL_L_Foot.Knee_Twist", l_foot_average + ".input1D[1]")
    base.connectAttr(l_foot_average + ".output1D", "IK_L_Leg.twist")
    base.setAttr("CTRL_L_Foot.Knee_Fix", 90)

    # Right
    base.setAttr("IK_R_Leg.poleVectorX", 1)
    base.setAttr("IK_R_Leg.poleVectorZ", 0)
    r_foot_average = base.shadingNode("plusMinusAverage", asUtility=True, name="R_Foot_Node")
    base.setAttr(r_foot_average + ".operation", 2)
    base.connectAttr("CTRL_R_Foot.Knee_Fix", r_foot_average + ".input1D[0]")
    base.connectAttr("CTRL_R_Foot.Knee_Twist", r_foot_average + ".input1D[1]")
    base.connectAttr(r_foot_average + ".output1D", "IK_R_Leg.twist")
    base.setAttr("CTRL_R_Foot.Knee_Fix", 90)

    # base.setAttr()
    print('CONSTRAINTS CREATED')


def bind_skin():
    sel = base.ls(sl = True)
    if len(sel) == 0:
        base.confirmDialog(title = "Empty Selection", message = "You have to select a mesh", button = ['Ok'])
    #     Dialogue box pops up telling you what you shit.
    else:
        for i in range(0, len(sel)):
            base.skinCluster(sel[i], "RIG_ROOT", bindMethod = 3, skinMethod = 1, dropoffRate = 0.1, name="Mesh" + str(i))
# bindMethod = 3 = geodesicVoxel(Need multiple objects for this otherwise it doesn't work)
# Maya creates skinCluster1 when skin is initially bound.
            base.geomBind('Mesh'+str(i), bindMethod = 3, geodesicVoxelParams = [256, 1])
# geodesicVoxelParams = 256 is to do with the skinning resolution. "1 validates the 256 resolution selection.  Whatever that means"

    _rig = base.select("RIG")
    base.createDisplayLayer(noRecurse = True, name = "RIG_LAYER")
    _ik = base.ls("IK_*")
    base.editDisplayLayerMembers("RIG_LAYER", _ik)
# Adds _ik to current later

    _ctrl = base.select("MASTER_CONTROLLER")
    base.createDisplayLayer(nr = True, name = "CONTROLLERS")
