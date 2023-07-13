import maya.cmds as base


def create_controller(spine_count, finger_count):
    # arrow = base.curve(point=[(1, 0, 0), (1, 0, 2), (2, 0, 2), (0, 0, 4), (-2, 0, 2), (-1, 0, 2), (-1, 0, 0), (1, 0, 0)], degree=1)

    create_master()
    create_pelvis()
    create_wrists()

    create_feet()
    create_spines(spine_count)
    create_clavicles(spine_count)
    create_neck(spine_count)
    create_head()

    if base.objExists("RIG_BREATHING_START"):
        create_breathing(spine_count)

    create_fingers(finger_count)


def create_master():
    # Master CTRL
    master_ctrl = base.circle(normal=(0, 1, 0), center=(0, 0, 0), radius=1, degree=1, sections=16, name="MASTER_CONTROLLER")
    selection = base.select("MASTER_CONTROLLER.cv[1]", "MASTER_CONTROLLER.cv[3]", "MASTER_CONTROLLER.cv[5]", "MASTER_CONTROLLER.cv[7]",
                            "MASTER_CONTROLLER.cv[9]",
                            "MASTER_CONTROLLER.cv[11]",
                            "MASTER_CONTROLLER.cv[13]", "MASTER_CONTROLLER.cv[15]")
    base.scale(0.7, 0.7, 0.7, selection)

    # Make identity just means im freezing the transforms of whatever object.  Its more complicated than that but that is what it is doing in basic terms.
    base.makeIdentity(master_ctrl, apply=True, translate=1, rotate=1, scale=1)
    # Translate, rotate and scale are booleans. We are saying 'YES' to freeze the transformations of t, r and s.


def create_pelvis():
    # Pelvis CTRL
    pelvis_ctrl = base.circle(normal=(0, 1, 0), center=(0, 0, 0), radius=1, degree=1, sections=16, name="CTRL_PELVIS")
    root_pos = base.xform(base.ls("RIG_ROOT", type='joint'), q=True, translation=True, worldSpace=True)
    base.move(root_pos[0], root_pos[1], root_pos[2], pelvis_ctrl)
    base.scale(0.5, 0.5, 0.5, pelvis_ctrl)
    # Make identity just means im freezing the transforms of whatever object.  Its more complicated than that but that is what it is doing in basic terms.
    base.makeIdentity(pelvis_ctrl, apply=True, translate=1, rotate=1, scale=1)
    base.parent(pelvis_ctrl, "MASTER_CONTROLLER")

    # Spine CTRLs


def create_wrists():
    sides = ['L', 'R']

    for side in sides:
        ctrl1 = base.circle(normal=(0, 1, 0), center=(0, 0, 0), radius=1, degree=1, sections=16, name="CTRL_" + side + "_Wrist0")
        ctrl2 = base.circle(normal=(0, 1, 0), center=(0, 0, 0), radius=1, degree=1, sections=16, name="CTRL_" + side + "_Wrist1")
        ctrl3 = base.circle(normal=(0, 1, 0), center=(0, 0, 0), radius=1, degree=1, sections=16, name="CTRL_" + side + "_Wrist2")

        wrist_ctrl = base.group(em=True, name="CTRL_" + side + "_Wrist")
        curves = [ctrl1, ctrl2, ctrl3]
        for cv in curves:
            curve_shape = base.listRelatives(cv, shapes=True)
            base.parent(curve_shape, wrist_ctrl, shape=True, relative=True)
            #         grabs the shape and
            base.delete(cv)
        base.select("CTRL_" + side + "_Wrist")
        base.addAttr(shortName="PV", longName="Elbow_PV", attributeType="double", defaultValue=0, minValue=-100, maxValue=100, keyable=True)
        base.scale(0.07, 0.07, 0.07, wrist_ctrl)

        wrist_pos = base.xform(base.ls("RIG_" + side + "_Wrist"), query=True, translation=True, worldSpace=True)
        wrist_rot = base.joint(base.ls("RIG_" + side + "_Wrist"), query=True, orientation=True)
        if base.objExists("RIG_L_ArmTwist_*"):
            arm_twists = base.ls("RIG_L_ArmTwist_*")
            print(base.xform(base.ls("RIG_" + side + "_ArmTwist_" + str(len(arm_twists) - 1)), query=True, worldSpace=True, rotation=True))
            wrist_rotation = base.xform(base.ls("RIG_" + side + "_ArmTwist_" + str(len(arm_twists) - 1)), query=True, worldSpace=True, rotation=True)
        else:
            wrist_rotation = base.xform(base.ls("RIG_" + side + "_Elbow"), query=True, worldSpace=True, rotation=True)
        base.move(wrist_pos[0], wrist_pos[1], wrist_pos[2], wrist_ctrl)
        wrist_grp = base.group(em=True, name="CTRL_GRP_" + side + "_Wrist")
        base.move(wrist_pos[0], wrist_pos[1], wrist_pos[2], wrist_grp)
        base.parent(wrist_ctrl, wrist_grp)

        base.rotate(0, 0, -wrist_rotation[0], wrist_grp)
        base.parent(wrist_grp, "MASTER_CONTROLLER")

    # # OLD but good information #############################################
    #
    # l_wrist_ctrl = base.circle(normal=(0, 1, 0), center=(0, 0, 0), radius=1, degree=1, sections=16, name="CTRL_L_Wrist")
    # l_selection = base.select("CTRL_L_Wrist.cv[1]", "CTRL_L_Wrist.cv[3]", "CTRL_L_Wrist.cv[5]", "CTRL_L_Wrist.cv[7]",
    #                           "CTRL_L_Wrist.cv[9]",
    #                           "CTRL_L_Wrist.cv[11]",
    #                           "CTRL_L_Wrist.cv[13]", "CTRL_L_Wrist.cv[15]")
    # base.scale(0.7, 0.7, 0.7, l_selection)
    # base.scale(0.4, 0.4, 0.4, l_wrist_ctrl)
    #
    # l_wrist_pos = base.xform(base.ls("RIG_L_Wrist"), q=True, t=True, ws=True)
    # l_wrist_rot = base.joint(base.ls("RIG_L_Wrist"), q=True, orientation=True)
    #
    # # MAYA rotation matrix actually works backwards with PYTHON.  So in this case the order of operations is actually Z,Y,X.
    # # The wrist_ctrl gets rotated on the X axis to match that of the wrist joint and ignore the Z and Y.  Convoluted af.
    # base.move(l_wrist_pos[0], l_wrist_pos[1], l_wrist_pos[2], l_wrist_ctrl)
    # base.rotate(0, 0, l_wrist_rot[0], l_wrist_ctrl)
    #
    # # Make identity just means im freezing the transforms of whatever object.  Its more complicated than that but that is what it is doing in basic terms.
    # base.makeIdentity(l_wrist_ctrl, apply=True, translate=1, rotate=1, scale=1)
    # base.parent(l_wrist_ctrl, "MASTER_CONTROLLER")
    #
    # # Left Wrist CTRLS
    # r_wrist_ctrl = base.circle(normal=(0, 1, 0), center=(0, 0, 0), radius=1, degree=1, sections=16, name="CTRL_R_Wrist")
    # r_selection = base.select("CTRL_R_Wrist.cv[1]", "CTRL_R_Wrist.cv[3]", "CTRL_R_Wrist.cv[5]", "CTRL_R_Wrist.cv[7]",
    #                           "CTRL_R_Wrist.cv[9]",
    #                           "CTRL_R_Wrist.cv[11]",
    #                           "CTRL_R_Wrist.cv[13]", "CTRL_R_Wrist.cv[15]")
    # base.scale(0.7, 0.7, 0.7, r_selection)
    # base.scale(0.4, 0.4, 0.4, r_wrist_ctrl)
    #
    # r_wrist_pos = base.xform(base.ls("RIG_R_Wrist"), q=True, t=True, ws=True)
    # r_wrist_rot = base.joint(base.ls("RIG_R_Wrist"), q=True, orientation=True)
    #
    # # MAYA rotation matrix actually works backwards with PYTHON.  So in this case the order of operations is actually Z,Y,X.
    # # The wrist_ctrl gets rotated on the X axis to match that of the wrist joint and ignore the Z and Y.  Convoluted af.
    # base.move(r_wrist_pos[0], r_wrist_pos[1], r_wrist_pos[2], r_wrist_ctrl)
    # base.rotate(0, 0, r_wrist_rot[0], r_wrist_ctrl)
    #
    # # Make identity just means im freezing the transforms of whatever object.  Its more complicated than that but that is what it is doing in basic terms.
    # base.makeIdentity(r_wrist_ctrl, apply=True, translate=1, rotate=1, scale=1)
    # base.parent(r_wrist_ctrl, "MASTER_CONTROLLER")


def create_clavicles(spine_count):
    # Clavicle CTRLS
    l_clavicle = base.curve(
        point=[(1, 0, 0), (1, 1, 1), (1, 1.5, 2), (1, 1.7, 3), (1, 1.5, 4), (1, 1, 5), (1, 0, 6), (-1, 0, 6), (-1, 1, 5), (-1, 1.5, 4), (-1, 1.7, 3),
               (-1, 1.5, 2), (-1, 1, 1), (-1, 0, 0)], degree=1, name="CTRL_L_Clavicle")
    r_clavicle = base.curve(
        point=[(1, 0, 0), (1, 1, 1), (1, 1.5, 2), (1, 1.7, 3), (1, 1.5, 4), (1, 1, 5), (1, 0, 6), (-1, 0, 6), (-1, 1, 5), (-1, 1.5, 4), (-1, 1.7, 3),
               (-1, 1.5, 2), (-1, 1, 1), (-1, 0, 0)], degree=1, name="CTRL_R_Clavicle")

    base.scale(0.02, 0.02, 0.02, l_clavicle)
    base.scale(0.02, 0.02, 0.02, r_clavicle)

    l_arm_pos = base.xform(base.ls("RIG_L_UpperArm"), query=True, translation=True, worldSpace=True)
    r_arm_pos = base.xform(base.ls("RIG_R_UpperArm"), query=True, translation=True, worldSpace=True)

    l_clavicle_pos = base.xform(base.ls("RIG_L_Clavicle"), query=True, translation=True, worldSpace=True)
    r_clavicle_pos = base.xform(base.ls("RIG_R_Clavicle"), query=True, translation=True, worldSpace=True)

    base.move(l_arm_pos[0], l_arm_pos[1] + 0.125, l_arm_pos[2] - 0.1, l_clavicle)
    base.move(r_arm_pos[0], r_arm_pos[1] + 0.125, r_arm_pos[2] - 0.1, r_clavicle)

    base.move(l_clavicle_pos[0], l_clavicle_pos[1], l_clavicle_pos[2], l_clavicle + ".scalePivot", l_clavicle + ".rotatePivot")
    base.move(r_clavicle_pos[0], r_clavicle_pos[1], r_clavicle_pos[2], r_clavicle + ".scalePivot", r_clavicle + ".rotatePivot")

    base.makeIdentity(l_clavicle, apply=True, translate=1, rotate=1, scale=1)
    base.makeIdentity(r_clavicle, apply=True, translate=1, rotate=1, scale=1)

    base.parent(l_clavicle, "CTRL_SPINE_" + str(spine_count - 1))
    base.parent(r_clavicle, "CTRL_SPINE_" + str(spine_count - 1))


def create_spines(spine_count):
    # Spine CTRLS
    for i in range(0, spine_count):
        spine_pos = base.xform(base.ls("RIG_SPINE_" + str(i)), query=True, translation=True, worldSpace=True)
        spine = base.curve(point=[(0, spine_pos[1], spine_pos[2]), (0, spine_pos[1], spine_pos[2] - 1), (0, spine_pos[1] + 0.1, spine_pos[2] - 1.1),
                                  (0, spine_pos[1] + 0.1, spine_pos[2] - 1.4), (0, spine_pos[1] - 0.1, spine_pos[2] - 1.4),
                                  (0, spine_pos[1] - 0.1, spine_pos[2] - 1.1), (0, spine_pos[1], spine_pos[2] - 1)], degree=1,
                           name="CTRL_SPINE_" + str(i))
        base.move(spine_pos[0], spine_pos[1], spine_pos[2], spine + ".scalePivot", spine + ".rotatePivot")
        base.scale(0.5, 0.5, 0.5, spine)
        if i == 0:
            base.parent(spine, "CTRL_PELVIS")
        else:
            base.parent(spine, "CTRL_SPINE_" + str(i - 1))


def create_neck(spine_count):
    # Neck CTRLS
    neck = base.curve(p=[(0.5, 0, 0), (0.25, -0.25, -0.5), (-0.25, -0.25, -0.5), (-0.5, 0, 0), (-0.25, -0.25, 0.5), (0.25, -0.25, 0.5), (0.5, 0, 0)],
                      degree=1, name="CTRL_NECK")
    neck_pos = base.xform(base.ls("RIG_Neck_Start"), q=True, translation=True, ws=True)
    base.scale(0.3, 0.3, 0.3, neck)
    base.move(neck_pos[0], neck_pos[1] + 0.1, neck_pos[2], neck)
    base.move(neck_pos[0], neck_pos[1], neck_pos[2], neck + ".scalePivot", neck + ".rotatePivot")
    base.parent(neck, "CTRL_SPINE_" + str(spine_count - 1))

    # Make identity just means im freezing the transforms of whatever object.  Its more complicated than that but that is what it is doing in basic terms.
    base.makeIdentity(neck, apply=True, translate=1, rotate=1, scale=1)
    # Translate, rotate and scale are booleans. We are saying 'YES' to freeze the transformations of t, r and s.


def create_breathing(spine_count):
    # Breathing CTRLS
    breathing = base.curve(p=[(0, 0, 0), (0.1, 0.1, 0), (0, 0.2, 0), (-0.1, 0.1, 0), (0, 0, 0)], degree=1, name="CTRL_BREATHING")

    base.move(0, 0.1, 0, breathing + ".scalePivot", breathing + ".rotatePivot")  # Moves the pivot to the center of the curve when it is made
    base.scale(1, 1, 1, breathing)

    breathing_end_pos = base.xform(base.ls("RIG_BREATHING_END"), query=True, translation=True, worldSpace=True)
    breathing_start_pos = base.xform(base.ls("RIG_BREATHING_START"), query=True, translation=True, worldSpace=True)

    base.move(breathing_end_pos[0], breathing_end_pos[1] - 0.1, breathing_end_pos[2] + 0.1, breathing)
    # Moving the CTRL to the BREATHING_END joints position. The CTRL is not centered but instead uses the first vertex in the curve when moved. This is probably just how maya does things. So we move it manually on the Y and Z so that the CTRL is centered and slightly out.
    base.move(breathing_start_pos[0], breathing_start_pos[1], breathing_start_pos[2], breathing + ".scalePivot", breathing + ".rotatePivot")
    # Gets the position of the BREATHING_START joint so that we can move the pivot over to there instead.  I think this seems wrong TBH and might want to change it later
    base.parent(breathing, "CTRL_SPINE_" + str(spine_count - 1))
    base.makeIdentity(breathing, apply=True, translate=True, rotate=True, scale=True)


def create_head():
    # Head CTRLS
    head = base.curve(
        p=[(0.5, 0, 0), (0.25, -0.25, -0.5), (0.25, -0.5, -0.5), (0, -0.6, -0.5), (-0.25, -0.5, -0.5), (-0.25, -0.25, -0.5), (-0.5, 0, 0),
           (-0.25, -0.25, 0.5), (-0.25, -0.5, 0.5), (0, -0.6, 0.5), (0.25, -0.5, 0.5), (0.25, -0.25, 0.5), (0.5, 0, 0)], degree=1, name="CTRL_HEAD")
    base.scale(0.3, 0.3, 0.3, head)
    head_pos = base.xform(base.ls("RIG_Head"), query=True, translation=True, worldSpace=True)
    neck_pos = base.xform(base.ls("RIG_Neck_End"), query=True, translation=True, worldSpace=True)
    base.move(head_pos[0], head_pos[1], head_pos[2], head)
    base.move(neck_pos[0], neck_pos[1], neck_pos[2], head + ".scalePivot", head + ".rotatePivot")
    base.parent(head, "CTRL_NECK")
    base.makeIdentity(head, apply=True, translate=True, rotate=True, scale=True)

    # Jaw
    jaw = base.curve(p=[(0, 0, 0), (0.1, 0.1, 0), (0, 0.2, 0), (-0.1, 0.1, 0), (0, 0, 0)], degree=1, name="CTRL_JAW")
    base.move(0, 0.1, 0, jaw + ".scalePivot", jaw + ".rotatePivot")
    base.scale(0.3, 0.3, 0.3, jaw)
    jaw_pos = base.xform(base.ls("RIG_Jaw_End"), query=True, translation=True, worldSpace=True)
    jaw_start_pos = base.xform(base.ls("RIG_Jaw_Start"), query=True, translation=True, worldSpace=True)
    base.move(jaw_pos[0], jaw_pos[1] - 0.1, jaw_pos[2] + 0.1, jaw)
    base.move(jaw_start_pos[0], jaw_start_pos[1], jaw_start_pos[2], jaw + ".scalePivot", jaw + ".rotatePivot")
    base.parent(jaw, "CTRL_HEAD")
    base.makeIdentity(jaw, apply=True, translate=True, rotate=True, scale=True)


def create_feet():
    # Feet CTRLS
    l_arrow = base.curve(p=[(1, 0, 0), (1, 0, 2), (2, 0, 2), (0, 0, 6), (-2, 0, 2), (-1, 0, 2), (-1, 0, 0), (1, 0, 0)], degree=1, name="CTRL_L_Foot")
    base.addAttr(shortName="KF", longName="Knee_Twist", attributeType='double', defaultValue=0, minValue=-100, maxValue=100, keyable=True)
    base.addAttr(shortName="KR", longName="Knee_Fix", attributeType='double', defaultValue=0, minValue=0, maxValue=100, keyable=True)
    base.addAttr(shortName="FR", longName="Foot_Roll", attributeType='double', defaultValue=0, minValue=0, maxValue=100, keyable=True)
    base.addAttr(shortName="BR", longName="Ball_Roll", attributeType='double', defaultValue=0, minValue=0, maxValue=100, keyable=True)

    r_arrow = base.curve(p=[(1, 0, 0), (1, 0, 2), (2, 0, 2), (0, 0, 6), (-2, 0, 2), (-1, 0, 2), (-1, 0, 0), (1, 0, 0)], degree=1, name="CTRL_R_Foot")
    base.addAttr(shortName="KF", longName="Knee_Twist", attributeType='double', defaultValue=0, minValue=-100, maxValue=100, keyable=True)
    base.addAttr(shortName="KR", longName="Knee_Fix", attributeType='double', defaultValue=0, minValue=0, maxValue=100, keyable=True)
    base.addAttr(shortName="FR", longName="Foot_Roll", attributeType='double', defaultValue=0, minValue=0, maxValue=100, keyable=True)
    base.addAttr(shortName="BR", longName="Ball_Roll", attributeType='double', defaultValue=0, minValue=0, maxValue=100, keyable=True)

    base.scale(0.08, 0.08, 0.08, l_arrow)
    base.scale(0.08, 0.08, 0.08, r_arrow)

    l_foot_pos = base.xform(base.ls("RIG_L_Foot"), query=True, translation=True, worldSpace=True)
    r_foot_pos = base.xform(base.ls("RIG_R_Foot"), query=True, translation=True, worldSpace=True)

    base.move(l_foot_pos[0], 0, l_foot_pos[2], l_arrow)
    base.move(r_foot_pos[0], 0, r_foot_pos[2], r_arrow)

    base.makeIdentity(l_arrow, apply=True, translate=True, rotate=True, scale=True)
    base.makeIdentity(r_arrow, apply=True, translate=True, rotate=True, scale=True)

    base.parent(l_arrow, "MASTER_CONTROLLER")
    base.parent(r_arrow, "MASTER_CONTROLLER")


def create_fingers(finger_count):
    sides = ['L', 'R']

    for side in sides:
        for i in range(0, finger_count):
            for j in range(0, 3):
                finger_rotation = base.xform(base.ls("Loc_" + side + "_Finger_" + str(i) + "_" + str(j)), query=True, worldSpace=True, rotation=True)
                finger_position = base.xform(base.ls("Loc_" + side + "_Finger_" + str(i) + "_" + str(j)), query=True, worldSpace=True, translation=True)

                all_fingers = base.ls("RIG_" + side + "_Finger_" + str(i) + "_" + str(j))

                finger = base.curve(p=[(0, 0, 0), (0, 0, 0.5), (0.2, 0, 0.7), (0, 0, 0.9), (-0.2, 0, 0.7), (0, 0, 0.5)], degree=1,
                                    name="CTRL_" + side + "_Finger_" + str(i) + "_" + str(j))
                base.rotate(-90, 0, 0, finger)

                for k, fi in enumerate(all_fingers):
                    finger_pos = base.xform(fi, query=True, translation=True, worldSpace=True)
                    finger_rot = base.joint(fi, query=True, orientation=True)
                    base.scale(0.1, 0.1, 0.1, finger)
                    base.move(finger_pos[0], finger_pos[1], finger_pos[2], finger)

                finger_grp = base.group(empty=True, name="CTRL_GRP_" + side + "_Finger_" + str(i) + "_" + str(j))
                base.move(finger_position[0], finger_position[1], finger_position[2], finger_grp)
                base.rotate(0, finger_rotation[1], 0, finger_grp)
                base.makeIdentity(finger, apply=True, t=1, r=1, s=1)
                base.makeIdentity(finger_grp, apply=True, t=1, r=1, s=1)
                base.parent(finger, finger_grp)
                base.rotate(0, finger_rotation[1], 0, finger_grp, r=True)

                if j > 0:
                    base.parent(finger_grp, "CTRL_" + side + "_Finger_" + str(i) + "_" + str(j - 1))
                else:
                    base.parent(finger_grp, "CTRL_" + side + "_Wrist")
