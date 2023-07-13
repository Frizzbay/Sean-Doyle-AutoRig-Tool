import maya.cmds as base
import Locators
import importlib

reload_locators = importlib.reload(Locators)


def IK_handles():
    if not base.objExists("RIG_L_ArmTwist_*"):
        # Even though there is only one object in the list ("Rig_L_UpperArm") we need to use [0] to
        # make sure we are selecting the first object in that list
        base.ikHandle(n="IK_L_Arm", startJoint=base.ls("RIG_L_UpperArm")[0], endEffector=base.ls("RIG_L_Wrist")[0], solver="ikRPsolver")
        base.ikHandle(n="IK_R_Arm", startJoint=base.ls("RIG_R_UpperArm")[0], endEffector=base.ls("RIG_R_Wrist")[0], solver="ikRPsolver")
    else:
        base.ikHandle(n="IK_L_Arm", startJoint=base.ls("RIG_L_UpperArm")[0], endEffector=base.ls("RIG_L_ArmTwist_0")[0], solver="ikRPsolver")
        base.ikHandle(n="IK_R_Arm", startJoint=base.ls("RIG_R_UpperArm")[0], endEffector=base.ls("RIG_R_ArmTwist_0")[0], solver="ikRPsolver")

        left_wrist_pos = base.xform(base.ls("RIG_L_Wrist"), q=True, translation=True, worldSpace=True)
        right_wrist_pos = base.xform(base.ls("RIG_R_Wrist"), q=True, translation=True, worldSpace=True)

        leftIK = base.ikHandle("IK_L_Arm", q=True, ee=True)
        rightIK = base.ikHandle("IK_R_Arm", q=True, ee=True)

        # The left and right IK endEffectors pivots are moved to the wrist position when we have ArmTwist joints otherwise the
        # ArmTwist joints will bend along the spline which is not what we want.  Comment out these two lines of code if you cannot remember
        # the result of not having them.
        base.move(left_wrist_pos[0], left_wrist_pos[1], left_wrist_pos[2], leftIK + ".scalePivot", leftIK + ".rotatePivot")
        base.move(right_wrist_pos[0], right_wrist_pos[1], right_wrist_pos[2], rightIK + ".scalePivot", rightIK + ".rotatePivot")

    base.ikHandle(n="IK_L_Leg", startJoint=base.ls("RIG_L_UpperLeg")[0], endEffector=base.ls("RIG_L_Foot")[0], solver="ikRPsolver")
    base.ikHandle(n="IK_R_Leg", startJoint=base.ls("RIG_R_UpperLeg")[0], endEffector=base.ls("RIG_R_Foot")[0], solver="ikRPsolver")
    # ##############################################################################################################################

    base.ikHandle(n="IK_L_FootBall", startJoint=base.ls("RIG_L_Foot")[0], endEffector=base.ls("RIG_L_Ball")[0], solver="ikSCsolver")
    base.ikHandle(n="IK_L_Toes", startJoint=base.ls("RIG_L_Ball")[0], endEffector=base.ls("RIG_L_Toes")[0], solver="ikSCsolver")

    base.ikHandle(n="IK_R_FootBall", startJoint=base.ls("RIG_R_Foot")[0], endEffector=base.ls("RIG_R_Ball")[0], solver="ikSCsolver")
    base.ikHandle(n="IK_R_Toes", startJoint=base.ls("RIG_R_Ball")[0], endEffector=base.ls("RIG_R_Toes")[0], solver="ikSCsolver")

    ######################################################
    rootPos = base.xform(base.ls("RIG_ROOT", type="joint"), q=True, t=True, ws=True)
    spines = base.ls("RIG_SPINE_*", type="joint")

    spinePos = []

    for i, sp in enumerate(spines):
        spinePos.append(base.xform(spines[i], q=True, t=True, ws=True))
    #     Adds all the spines to the list with each loop

    base.curve(point=[(rootPos[0]), (rootPos[1]), (rootPos[2])], n="SpineCurve", degree=1.0)

    # Loops for each spine in the enumerator
    for j, sp in enumerate(spinePos):
        base.curve("SpineCurve", append=True, p=[(spinePos[j][0], spinePos[j][1], spinePos[j][2])])
    # Appends points to the end of an existing curve

    curveCV = base.ls("SpineCurve.cv[0:]", flatten=True)
    # lists the control vertexes in the spine curve
    # Flatten = Flattens the returned list of objects so that each component is identified individually.
    for k, cv in enumerate(curveCV):
        c = base.cluster(cv, cv, n="Spine_Cluster_" + str(k) + "_")

        if k > 0:
            base.parent(c, "Spine_Cluster_" + str(k - 1) + "_Handle")

    if base.objExists("Loc_SPINE_*"):
        spine_amount = base.ls("Loc_SPINE_*", type='transform')
    else:
        spine_amount = base.ls("RIG_SPINE_*")

    base.ikHandle(n="IK_Spine", startJoint="RIG_ROOT", endEffector="RIG_SPINE_" + str(len(spine_amount) - 1), sol="ikSplineSolver", curve="SpineCurve", createCurve = False)
