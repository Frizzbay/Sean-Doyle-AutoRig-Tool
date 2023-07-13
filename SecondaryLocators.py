import maya.cmds as base

from math import pow, sqrt, cos, acos, radians


class SecondaryLocators:
    # self refers to the instance of the class that is created from __init__ and can be called anything.
    # init initialises the object and executes instructions at the time of creation
    def __init__(self):
        self.create_sec_locators_windows()

    def create_sec_locators_windows(self):

        base.window("Secondary Controllers")
        base.rowColumnLayout(nc=1)
        base.button(label="Create Reverse Foot roll", w=200, c=self.create_reverse_footroll)
        base.separator(h=10)
        base.text("Twist Amount", l="Amount of twist joints")
        self.arm_twist = base.intField(minValue=2, maxValue=10, value=4)
        base.button(label="Create Forearm Twist", w=200, c=self.armTwist)
        # base.button(l="Create Forearm Twist", w=200,
        #             c="create_forearm_twist(" + str(base.intField(arm_twist, query=True, value=True)) + ")")
        # self.arm_twist = base.intSliderGrp(l="Arm Twist Amount", min=4, max=10, value=4, step=1, field=True)
        base.separator(h=10)
        base.button(l="Volume Locators", w=200, c=self.create_volume_locators)
        base.separator(h=10)
        base.button(l="Delete Locators", w=200, c=self.delete_secondary_locators)
        self.check_group(self)
        base.showWindow()

    def armTwist(self, buttonCallback):
        _amount = base.intField(self.arm_twist, q=True, v=True)
        self.create_forearm_twist(self, _amount)

    def check_group(self, void):
        if base.objExists("SECONDARY"):
            print("SECONDARY GROUP ALREADY EXISTS")
        else:
            base.group(em=True, n="SECONDARY")

        self.set_colors(self)

    def create_reverse_footroll(self, void):
        # L_Heel
        base.select(deselect=True)
        l_reverse_heel = base.spaceLocator(n="Loc_L_INV_Heel")
        base.scale(0.05, 0.05, 0.05, l_reverse_heel)

        l_heel_loc = base.xform(base.ls("Loc_L_Foot"), q=True, t=True, ws=True)
        base.move(l_heel_loc[0], l_heel_loc[1] - 0.1, l_heel_loc[2], l_reverse_heel)
        base.parent(l_reverse_heel, "SECONDARY")

        # R_Heel
        r_reverse_heel = base.spaceLocator(n="Loc_R_INV_Heel")
        base.scale(0.05, 0.05, 0.05, r_reverse_heel)

        r_heel_loc = base.xform(base.ls("Loc_R_Foot"), q=True, t=True, ws=True)
        base.move(r_heel_loc[0], r_heel_loc[1] - 0.1, r_heel_loc[2], r_reverse_heel)
        base.parent(r_reverse_heel, 'SECONDARY')

        # L_Toes
        l_toe_loc = base.xform(base.ls("Loc_L_Toes"), q=True, t=True, ws=True)
        l_rev_toes = base.spaceLocator(n="Loc_L_INV_Toes")
        base.scale(0.05, 0.05, 0.05, l_rev_toes)
        base.move(l_toe_loc[0], l_toe_loc[1], l_toe_loc[2], l_rev_toes)
        base.parent(l_rev_toes, 'Loc_L_INV_Heel')

        # R_Toes
        r_toe_loc = base.xform(base.ls("Loc_R_Toes"), q=True, t=True, ws=True)
        r_rev_toes = base.spaceLocator(n="Loc_R_INV_Toes")
        base.scale(0.05, 0.05, 0.05, r_rev_toes)
        base.move(r_toe_loc[0], r_toe_loc[1], r_toe_loc[2], r_rev_toes)
        base.parent(r_rev_toes, 'Loc_R_INV_Heel')

        # L_Foot ball
        l_ball_loc = base.xform(base.ls("Loc_L_Foot_Ball"), q=True, t=True, ws=True)
        l_rev_ball = base.spaceLocator(n="Loc_L_INV_Ball")
        base.scale(0.05, 0.05, 0.05, l_rev_ball)
        base.move(l_ball_loc[0], l_ball_loc[1], l_ball_loc[2], l_rev_ball)
        base.parent(l_rev_ball, 'Loc_L_INV_Toes')

        # R_Foot ball
        r_ball_loc = base.xform(base.ls("Loc_R_Foot_Ball"), q=True, t=True, ws=True)
        r_rev_ball = base.spaceLocator(n="Loc_R_INV_Ball")
        base.scale(0.05, 0.05, 0.05, r_rev_ball)
        base.move(r_ball_loc[0], r_ball_loc[1], r_ball_loc[2], r_rev_ball)
        base.parent(r_rev_ball, 'Loc_R_INV_Toes')

        # L_Ankle
        l_ankle_loc = base.xform(base.ls("Loc_L_Foot"), q=True, t=True, ws=True)
        l_rev_ankle = base.spaceLocator(n="Loc_L_INV_Ankle")
        base.scale(0.05, 0.05, 0.05, l_rev_ankle)
        base.move(l_ankle_loc[0], l_ankle_loc[1], l_ankle_loc[2], l_rev_ankle)
        base.parent(l_rev_ankle, 'Loc_L_INV_Ball')

        # R_Ankle
        r_ankle_loc = base.xform(base.ls("Loc_R_Foot"), q=True, t=True, ws=True)
        r_rev_ankle = base.spaceLocator(n="Loc_R_INV_Ankle")
        base.scale(0.05, 0.05, 0.05, r_rev_ankle)
        base.move(r_ankle_loc[0], r_ankle_loc[1], r_ankle_loc[2], r_rev_ankle)
        base.parent(r_rev_ankle, 'Loc_R_INV_Ball')

    def create_forearm_twist(self, void, amount):
        base.select(deselect=True)
        if base.objExists("Loc_L_Elbow_1"):
            l_elbow_pos = base.xform("Loc_L_Elbow_2", q = True, t = True, ws = True)
        else:
            l_elbow_pos = base.xform(base.ls('Loc_L_Elbow'), q=True, t=True, ws=True)

        l_wrist_pos = base.xform(base.ls('Loc_L_Wrist'), q=True, t=True, ws=True)

        l_vector_y = l_wrist_pos[1] - l_elbow_pos[1]
        l_vector_x = l_wrist_pos[0] - l_elbow_pos[0]
        l_vector_z = l_wrist_pos[2] - l_elbow_pos[2]

        # Amount is assumed to be 0
        for i in range(amount - 1):
            l_twist_loc = base.spaceLocator(n='Loc_L_ArmTwist_' + str(i))
            base.move(l_elbow_pos[0] + (l_vector_x / amount) + ((l_vector_x / amount) * i),
                      l_elbow_pos[1] + (l_vector_y / amount) + ((l_vector_y / amount) * i),
                      l_elbow_pos[2] + (l_vector_z / amount) + ((l_vector_z / amount) * i), l_twist_loc)
            base.scale(0.05, 0.05, 0.05, l_twist_loc)
            base.parent(l_twist_loc, 'SECONDARY')

        if base.objExists("Loc_R_Elbow_1"):
            r_elbow_pos = base.xform("Loc_R_Elbow_2", q=True, t=True, ws=True)
        else:
            r_elbow_pos = base.xform(base.ls('Loc_R_Elbow'), q=True, t=True, ws=True)

        r_wrist_pos = base.xform(base.ls('Loc_R_Wrist'), q=True, t=True, ws=True)

        r_vector_y = r_wrist_pos[1] - r_elbow_pos[1]
        r_vector_x = r_wrist_pos[0] - r_elbow_pos[0]
        r_vector_z = r_wrist_pos[2] - r_elbow_pos[2]

        for j in range(amount - 1):
            r_twist_loc = base.spaceLocator(n='Loc_R_ArmTwist_' + str(j))
            base.move(r_elbow_pos[0] + (r_vector_x / amount) + ((r_vector_x / amount) * j),
                      r_elbow_pos[1] + (r_vector_y / amount) + ((r_vector_y / amount) * j),
                      r_elbow_pos[2] + (r_vector_z / amount) + ((r_vector_z / amount) * j), r_twist_loc)
            base.scale(0.05, 0.05, 0.05, r_twist_loc)
            base.parent(r_twist_loc, 'SECONDARY')

    def create_volume_locators(self, void):

        spine_locs = base.ls("Loc_SPINE_*", type='transform')
        print(spine_locs)

        for i, x in enumerate(spine_locs):
            spine_location = base.xform(spine_locs[i], q=True, t=True, ws=True)
            print(i)
            print(len(spine_locs))
            if i == len(spine_locs) - 1:
                volume_loc = base.spaceLocator(n="Loc_Breathing")
                base.move(spine_location[0], spine_location[1] - 0.1, spine_location[2] + 0.3, volume_loc)
                base.scale(0.07, 0.07, 0.07, volume_loc)
                base.parent(volume_loc, "SECONDARY")
            else:
                volume_loc = base.spaceLocator(n="Loc_Volume_" + str(i))
                base.move(spine_location[0], spine_location[1], spine_location[2] + 0.4, volume_loc)
                base.scale(0.07, 0.07, 0.07, volume_loc)
                base.parent(volume_loc, "SECONDARY")

                l_chest_volume = base.spaceLocator(n="Loc_L_ChestVolume_" + str(i))
                base.move(spine_location[0] + 0.25, spine_location[1], spine_location[2] + 0.15, l_chest_volume)
                r_chest_volume = base.spaceLocator(n="Loc_R_ChestVolume_" + str(i))
                base.move(spine_location[0] - 0.25, spine_location[1], spine_location[2] + 0.15, r_chest_volume)
                base.scale(0.07, 0.07, 0.07, l_chest_volume)
                base.scale(0.07, 0.07, 0.07, r_chest_volume)
                base.parent(l_chest_volume, "SECONDARY")
                base.parent(r_chest_volume, "SECONDARY")

    def set_colors(self, void):
        base.setAttr('SECONDARY.overrideEnabled', 1)
        base.setAttr('SECONDARY.overrideRGBColors', 1)
        base.setAttr('SECONDARY.overrideColorRGB', 1, 1, 1)

    def delete_secondary_locators(self, void):
        base.delete(base.ls('SECONDARY'))
