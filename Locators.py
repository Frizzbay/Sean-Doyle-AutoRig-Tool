import maya.cmds as base


def create_fields(spine_value, finger_value):
    global spine_count
    global finger_count

    print(spine_value)
    print(finger_value)

    # spine_count = 4
    # finger_count = 5


def return_fingers_amount():
    return finger_count


def return_spine_amount():
    return spine_count


def ReturnDoubleElbow():
    global _double_elbow
    return _double_elbow


def create_locators(spine_value, finger_value, double_elbow):  # def = 'Function Definition'

    global spine_count
    global finger_count
    global _double_elbow

    _double_elbow = double_elbow

    spine_count = spine_value
    finger_count = finger_value

    print(spine_count)

    if base.objExists('Loc_Master'):
        print("Loc_Master already exists")
    else:
        base.group(em=True, name="Loc_Master")  # em = Empty.  Creating Empty group

    root = base.spaceLocator(n='Loc_ROOT')  # root = Maya.spaceLocator.  Created locator is named 'Loc_ROOT'
    base.scale(0.1, 0.1, 0.1, root)  # scaling the root
    base.move(0, 1.5, 0, root)  # moving the root
    base.parent(root, "Loc_Master")

    create_spine()


def create_spine():
    for i in range(0, spine_count):
        spine = base.spaceLocator(n='Loc_SPINE_' + str(i))  # Create spaceLocator named spine for each i in spineCount
        base.scale(0.1, 0.1, 0.1, spine)
        if i == 0:
            base.parent(spine, 'Loc_ROOT')
        else:
            base.parent(spine, 'Loc_SPINE_' + str(i - 1))  # Spawn spine under previous spine in i
        base.move(0, 1.75 + (0.25 * i), 0, spine)  # move .25 on Y for each i

    create_head()
    create_arms(1)  # LEFT SIDE
    create_arms(-1)  # RIGHT SIDE
    create_legs(1)
    create_legs(-1)


def create_head():
    neck_start = base.spaceLocator(n='Loc_Neck_Start')
    base.parent(neck_start, 'Loc_SPINE_' + str(return_spine_amount() - 1))
    base.scale(1, 1, 1, neck_start)
    base.move(0, 1.6 + (0.25 * return_spine_amount()), 0, neck_start)

    neck_end = base.spaceLocator(n='Loc_Neck_End')
    base.parent(neck_end, 'Loc_Neck_Start')
    base.scale(1, 1, 1, neck_end)
    base.move(0, 1.75 + (0.25 * return_spine_amount()), 0, neck_end)

    head = base.spaceLocator(n='Loc_Head')
    base.parent(head, 'Loc_Neck_End')
    base.scale(1, 1, 1, head)
    base.move(0, 2 + (0.25 * spine_count), 0, head)

    # JAW
    jaw_end = base.spaceLocator(n='Loc_Jaw_End')
    jaw_start = base.spaceLocator(n='Loc_Jaw_Start')
    base.parent(jaw_start, 'Loc_Head')
    base.parent(jaw_end, jaw_start)
    base.scale(1, 1, 1, jaw_end)
    base.scale(.5, .5, .5, jaw_start)
    base.move(0, 1.9 + (0.25 * spine_count), 0.02, jaw_start)
    base.move(0, 1.9 + (0.25 * spine_count), 0.15, jaw_end)


def create_legs(side):
    if side == 1:
        if base.objExists('L_Leg_GRP'):
            print('LEFT LEG GROUP EXISTS')
        else:
            upper_leg_grp = base.group(em=True, name='L_Leg_GRP')
            base.move(0.15, 1.5, 0, upper_leg_grp)
            base.parent(upper_leg_grp, 'Loc_ROOT')

        upper_leg = base.spaceLocator(n='Loc_L_UpperLeg')
        base.scale(0.1, 0.1, 0.1, upper_leg)
        base.move(0.15, 1.5, 0, upper_leg)
        base.parent(upper_leg, 'L_Leg_GRP')

        # Lower Leg
        lower_leg = base.spaceLocator(name='Loc_L_LowerLeg')
        base.scale(.1, .1, .1, lower_leg)
        base.move(0.15, 0.75, 0.05, lower_leg)
        base.parent(lower_leg, 'Loc_L_UpperLeg')

        # foot
        foot = base.spaceLocator(n='Loc_L_Foot')
        base.scale(0.1, 0.1, 0.1, foot)
        base.move(0.15, 0.2, 0, foot)
        base.parent(foot, 'Loc_L_LowerLeg')

        # Foot Ball
        foot_ball = base.spaceLocator(name='Loc_L_Foot_Ball')
        base.scale(0.1, 0.1, 0.1, foot_ball)
        base.move(0.15, 0, 0.15, foot_ball)
        base.parent(foot_ball, 'Loc_L_Foot')

        # Toes
        toes = base.spaceLocator(n='Loc_L_Toes')
        base.scale(0.1, 0.1, 0.1, toes)
        base.move(0.15, 0, 0.3, toes)
        base.parent(toes, 'Loc_L_Foot_Ball')

    else:
        if base.objExists('R_Leg_GRP'):
            print('RIGHT LEG GROUP EXISTS')
        else:
            upper_leg_grp = base.group(em=True, name='R_Leg_GRP')
            base.move(-0.15, 1.5, 0, upper_leg_grp)
            base.parent(upper_leg_grp, 'Loc_ROOT')

        upper_leg = base.spaceLocator(n='Loc_R_UpperLeg')
        base.scale(0.1, 0.1, 0.1, upper_leg)
        base.move(-0.15, 1.5, 0, upper_leg)
        base.parent(upper_leg, 'R_Leg_GRP')

        # Lower Leg
        lower_leg = base.spaceLocator(name='Loc_R_LowerLeg')
        base.scale(.1, .1, .1, lower_leg)
        base.move(-0.15, 0.75, 0.05, lower_leg)
        base.parent(lower_leg, 'Loc_R_UpperLeg')

        # foot
        foot = base.spaceLocator(n='Loc_R_Foot')
        base.scale(0.1, 0.1, 0.1, foot)
        base.move(-0.15, 0.2, 0, foot)
        base.parent(foot, 'Loc_R_LowerLeg')

        # Foot Ball
        foot_ball = base.spaceLocator(name='Loc_R_Foot_Ball')
        base.scale(0.1, 0.1, 0.1, foot_ball)
        base.move(-0.15, 0, 0.15, foot_ball)
        base.parent(foot_ball, 'Loc_R_Foot')

        # Toes
        toes = base.spaceLocator(n='Loc_R_Toes')
        base.scale(0.1, 0.1, 0.1, toes)
        base.move(-0.15, 0, 0.3, toes)
        base.parent(toes, 'Loc_R_Foot_Ball')


def create_arms(side):
    global edit_mode

    if side == 1:  # LEFT
        if base.objExists('L_Arm_GRP'):
            print('Arm_GRP ALREADY EXISTS')
        else:
            l_arm = base.group(em=True, name='L_Arm_GRP')
            base.parent(l_arm, 'Loc_SPINE_' + str(spine_count - 1))
            # Parent Arm to spine locator.  String starts at 1. Object starts at 0 so we -1

            # Clavicle
            clavicle = base.spaceLocator(n="Loc_L_Clavicle")
            base.scale(0.1, 0.1, 0.1, clavicle)
            base.parent(clavicle, 'Loc_SPINE_' + str(spine_count - 1))
            base.move(0.1 * side, 1.5 + (0.25 * spine_count), 0.1, clavicle)

            # Upper Arm
            upper_arm = base.spaceLocator(n='Loc_L_UpperArm')
            base.scale(0.1, 0.1, 0.1, upper_arm)
            base.parent(upper_arm, clavicle)

            # Elbow
            if _double_elbow == False:
                elbow = base.spaceLocator(n='Loc_L_Elbow')
                base.scale(0.1, 0.1, 0.1, elbow)
                base.parent(elbow, upper_arm)
                base.move(0.6 * side, 2, -0.2, elbow)
            else:
                elbow = base.spaceLocator(n='Loc_L_Elbow_1')
                base.scale(0.1, 0.1, 0.1, elbow)
                base.parent(elbow, upper_arm)
                base.move(0.58 * side, 2, -0.2, elbow)

                elbow_2 = base.spaceLocator(n='Loc_L_Elbow_2')
                base.scale(0.1, 0.1, 0.1, elbow_2)
                base.parent(elbow_2, elbow)
                base.move(0.62 * side, 1.98, -0.2, elbow_2)

            # Wrist
            wrist = base.spaceLocator(n='Loc_L_Wrist')
            base.scale(0.1, 0.1, 0.1, wrist)
            base.parent(wrist, elbow)

            # Move UpperArm
            base.move(0.35 * side, 1.5 + (0.25 * spine_count), 0, upper_arm)

            # Move Elbow
            base.move(0.6 * side, 2, -0.2, elbow)

            # Move Wrist
            base.move(0.8 * side, 1.5, 0, wrist)

            create_hands(1, wrist)
            # Objects are manipulated in world space but their values are
            #                                       represented locally

    # RIGHT
    else:
        if base.objExists('R_Arm_GRP'):
            print('R_Arm_GRP ALREADY EXISTS')
        else:
            l_arm = base.group(em=True, name='R_Arm_GRP')
            base.parent(l_arm, 'Loc_SPINE_' + str(spine_count - 1))
            # Parent Arm to spine locator.  String starts at 1. Object starts at 0 so we -1

            # Clavicle
            clavicle = base.spaceLocator(n="Loc_R_Clavicle")
            base.scale(0.1, 0.1, 0.1, clavicle)
            base.parent(clavicle, 'Loc_SPINE_' + str(spine_count - 1))
            base.move(0.1 * side, 1.5 + (0.25 * spine_count), 0.1, clavicle)

            # Upper Arm
            upper_arm = base.spaceLocator(n='Loc_R_UpperArm')
            base.scale(0.1, 0.1, 0.1, upper_arm)
            base.parent(upper_arm, clavicle)

            # Elbow
            if _double_elbow == False:
                elbow = base.spaceLocator(n='Loc_R_Elbow')
                base.scale(0.1, 0.1, 0.1, elbow)
                base.parent(elbow, upper_arm)
                base.move(0.6 * side, 2, -0.2, elbow)
            else:
                elbow = base.spaceLocator(n='Loc_R_Elbow_1')
                base.scale(0.1, 0.1, 0.1, elbow)
                base.parent(elbow, upper_arm)
                base.move(0.58 * side, 2, -0.2, elbow)

                elbow_2 = base.spaceLocator(n='Loc_R_Elbow_2')
                base.scale(0.1, 0.1, 0.1, elbow_2)
                base.parent(elbow_2, elbow)
                base.move(0.62 * side, 1.98, -0.2, elbow_2)

            # Wrist
            wrist = base.spaceLocator(n='Loc_R_Wrist')
            base.scale(0.1, 0.1, 0.1, wrist)
            base.parent(wrist, elbow)

            # Move UpperArm
            base.move(0.35 * side, 1.5 + (0.25 * spine_count), 0, upper_arm)

            # Move Elbow
            base.move(0.6 * side, 2, -0.2, elbow)

            # Move Wrist
            base.move(0.8 * side, 1.5, 0, wrist)

            create_hands(-1, wrist)
            # Objects are manipulated in world space but their values are represented locally


def create_hands(side, wrist):
    if side == 1:
        if base.objExists('L_Hand_GRP'):
            print('Create Hands Print')
        else:
            hand = base.group(em=True, name='L_Hand_GRP')
            pos = base.xform(wrist, query=True, t=True, ws=True)  # Query, Translation and World Space
            base.move(pos[0], pos[1], pos[2], hand)
            base.parent(hand, 'Loc_L_Wrist')

            for i in range(0, finger_count):
                create_fingers(1, pos, i)

    else:
        if base.objExists('R_Hand_GRP'):
            print('R_HAND_GRP_Print')
        else:
            hand = base.group(em=True, name='R_Hand_GRP')
            pos = base.xform(wrist, q=True, t=True, ws=True)  # Query, Translation and World Space
            base.move(pos[0], pos[1], pos[2], hand)
            base.parent(hand, 'Loc_R_Wrist')

            for i in range(0, finger_count):
                create_fingers(-1, pos, i)


def create_fingers(side, hand_pos, count):
    for x in range(0, 3):
        if side == 1:  # LEFT
            finger = base.spaceLocator(n='Loc_L_Finger_' + str(count) + '_' + str(x))
            base.scale(.05, .05, .05, finger)
            if x == 0:
                base.parent(finger, 'Loc_L_Wrist')
            else:
                base.parent(finger, 'Loc_L_Finger_' + str(count) + '_' + str(x - 1))
            base.move(hand_pos[0] + (0.1 + (0.1 * x)) * side, hand_pos[1] - (0.1 + (0.1 * x)),
                      hand_pos[2] + -(0.05 * count), finger)
        else:
            finger = base.spaceLocator(n='Loc_R_Finger_' + str(count) + '_' + str(x))
            base.scale(.05, .05, .05, finger)
            if x == 0:
                base.parent(finger, 'Loc_R_Wrist')
            else:
                base.parent(finger, 'Loc_R_Finger_' + str(count) + '_' + str(x - 1))
            base.move(hand_pos[0] + (0.1 + (0.1 * x)) * side, hand_pos[1] - (0.1 + (0.1 * x)),
                      hand_pos[2] + -(0.05 * count), finger)


def mirror_locators():
    all_left_locators = base.ls("Loc_L_*")
    left_locators = base.listRelatives(*all_left_locators, p=True, f=True)
    # listing the relatives of the locators so that we ignore the shapes
    # p = parent, f = full path name gives us the entire name of the object
    all_right_locators = base.ls("Loc_R_*")
    right_locators = base.listRelatives(*all_right_locators, p=True, f=True)

    for i, l in enumerate(left_locators):  # Enumerate lists things 1 by 1
        # Store the left locators in a list one after the other
        pos = base.xform(l, q=True, t=True, ws=True)  # pos = each locator's x,y,z value in world space
        base.move(-pos[0], pos[1], pos[2], right_locators[i])
        # we move the x, y, z translation values recorded in enumerate to match right_locators(except minus on X)


def delete_locators():
    nodes = base.ls("Loc_*")  # ls = list selection, Selecting list with "Loc" in name.  Stopping at *
    base.delete(nodes)
