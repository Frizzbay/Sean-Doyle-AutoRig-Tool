import maya.cmds as base


class FaceJoints():

    def __init__(self):
        pass

    def create_face_window(self, void):

        self.sides = ['L', 'R']

        base.window("Facial Rig")
        base.rowColumnLayout(numberOfColumns=2)
        base.button(l="Create Face Locators", w=200, c=self.Locators)
        base.separator(st='none')
        base.button(l="Mirror L -> R", w=200, c=self.mirror_locators)
        base.showWindow()

    def Locators(self, void):

        base.group(em=True, n="FACE_LOC_GRP")
        self.side_multiplier = 1
        # eyelids
        self.eye_locators(self)
        # mouth
        self.mouth_locators(self)
        # eyebrows
        self.eyebrow_locators(self)
        # smiling muscle
        self.smile_muscles(self)
        # add spaceLocators

        self.add_locators(self)

    def eye_locators(self, void):

        if base.objExists('L_Eye'):  # Need 'L_Eye' mesh object for this to work
            for side in self.sides:  # Because everything is in the same class we can access sides = ['L','R'] through self.sides

                eye_center_loc = base.spaceLocator(n="Loc_Face_" + side + "_EyeCenter")
                base.scale(0.01, 0.01, 0.01, eye_center_loc)
                eye_pos = base.xform(base.ls(side + "_Eye.rotatePivot"), query=True, translation=True, worldSpace=True)
                base.move(eye_pos[0], eye_pos[1], eye_pos[2], eye_center_loc)
                base.parent(eye_center_loc, "FACE_LOC_GRP")

                eye_aim_loc = base.spaceLocator(n="Loc_Face_" + side + "_EyeAim")
                base.scale(0.01, 0.01, 0.01, eye_aim_loc)
                base.move(eye_pos[0] - (0.004 * self.side_multiplier), eye_pos[1], eye_pos[2] + 0.025, eye_aim_loc)
                base.parent(eye_aim_loc, "FACE_LOC_GRP")

                upper_lid = base.curve(p=[(0, 0, 0), (0.05 * self.side_multiplier, 0.02, 0), (0.1 * self.side_multiplier, 0.04, 0),
                                          (0.15 * self.side_multiplier, 0.02, 0), (0.2 * self.side_multiplier, 0, 0)],
                                       n="CV_" + side + "_UpperEyeLid")
                base.scale(0.1, 0.1, 0.1, upper_lid)
                base.parent(upper_lid, "FACE_LOC_GRP")
                eye_aim_pos = base.xform(eye_aim_loc, q=True, translation=True, worldSpace=True)
                base.move(eye_aim_pos[0], eye_aim_pos[1] + 0.005, eye_aim_pos[2], upper_lid)

                lower_lid = base.curve(p=[(0, 0, 0), (0.05 * self.side_multiplier, -0.02, 0), (0.1 * self.side_multiplier, -0.04, 0),
                                          (0.15 * self.side_multiplier, -0.02, 0), (0.2 * self.side_multiplier, 0, 0)],
                                       n="CV_" + side + "_LowerEyeLid")
                base.scale(0.1, 0.1, 0.1, lower_lid)
                base.move(eye_aim_pos[0] - (0.004 * self.side_multiplier), eye_aim_pos[1] - 0.005, eye_aim_pos[2], lower_lid)
                base.parent(lower_lid, "FACE_LOC_GRP")
                self.side_multiplier = -1

        else:
            base.confirmDialog(title="Eyes missing", message="The eyes ( L_Eye - R_Eye ) could not be found", button=['Ok'])

    def mouth_locators(self, void):
        self.side_multiplier = 1

        for side in self.sides:
            jaw_loc = base.xform(base.ls("Loc_Jaw_End", type='transform'), q=True, t=True, ws=True)

            upper_mouth = base.curve(p=[(0, 0, 0), (0.02 * self.side_multiplier, -0.001, -0.001), (0.04 * self.side_multiplier, -0.002, -0.002),
                                        (0.06 * self.side_multiplier, -0.004, -0.003)], n="CV_" + side + "_UpperMouth")
            base.scale(0.3, 0.3, 0.3, upper_mouth)
            base.move(jaw_loc[0], jaw_loc[1] + 0.05, jaw_loc[2] + 0.02, upper_mouth)
            base.parent(upper_mouth, "FACE_LOC_GRP")

            lower_mouth = base.curve(p=[(0, 0, 0), (0.02 * self.side_multiplier, 0.001, -0.001), (0.04 * self.side_multiplier, 0.002, -0.002),
                                        (0.06 * self.side_multiplier, 0.004, -0.003)], n="CV_" + side + "_LowerMouth")
            base.scale(0.3, 0.3, 0.3, lower_mouth)
            base.move(jaw_loc[0], jaw_loc[1] + 0.03, jaw_loc[2] + 0.02, lower_mouth)
            base.parent(lower_mouth, "FACE_LOC_GRP")

            self.side_multiplier = -1

    def eyebrow_locators(self, void):
        self.side_multiplier = 1
        for side in self.sides:
            eye_loc_pos = base.xform(base.ls("Loc_Face_" + side + "_EyeAim"), q=True, t=True, ws=True)

            eye_brow = base.curve(
                p=[(0, 0, 0), (0.1 * self.side_multiplier, 0.1, 0), (0.2 * self.side_multiplier, 0.15, 0), (0.3 * self.side_multiplier, 0.1, 0)],
                n="CV_" + side + "_EyeBrow")
            base.scale(0.1, 0.1, 0.1, eye_brow)
            base.move(eye_loc_pos[0] - (0.02 * self.side_multiplier), eye_loc_pos[1] + 0.004, eye_loc_pos[2] + 0.01, eye_brow)
            base.parent(eye_brow, "FACE_LOC_GRP")

            forehead_brow = base.curve(
                p=[(0, 0, 0), (0.1 * self.side_multiplier, 0.1, 0), (0.25 * self.side_multiplier, 0.15, 0), (0.4 * self.side_multiplier, 0.1, 0)],
                n="CV_" + side + "_ForeHeadBrow")
            base.scale(0.1, 0.1, 0.1, forehead_brow)
            base.move(eye_loc_pos[0] - (0.02 * self.side_multiplier), eye_loc_pos[1] + 0.03, eye_loc_pos[2] + 0.007, forehead_brow)
            base.parent(forehead_brow, "FACE_LOC_GRP")

            self.side_multiplier = -1

    def smile_muscles(self, void):
        self.side_multiplier = 1
        for side in self.sides:
            jaw_loc = base.xform(base.ls("Loc_Jaw_End", type='transform'), q=True, t=True, ws=True)
            smile_muscle = base.curve(
                p=[(0, 0, 0), (0.15 * self.side_multiplier, -0.2, 0), (0.2 * self.side_multiplier, -0.4, 0), (0.25 * self.side_multiplier, -0.6, 0)],
                n="CV_" + side + "_Smile_Muscle")
            base.scale(0.1, 0.1, 0.1, smile_muscle)
            base.move(jaw_loc[0] + (0.01 * self.side_multiplier), jaw_loc[1] + 0.1, jaw_loc[2] + 0.015, smile_muscle)
            base.parent(smile_muscle, "FACE_LOC_GRP")

            self.side_multiplier = -1

    def add_locators(self, void):
        all_curves = base.ls("CV_*")  # Only the face locator curve names start with "CV_" so we don't grab every curve.
        dummy_loc = base.spaceLocator(n="Loc_Face_Head_Dummy")

        if base.objExists("Loc_Neck_End"):
            neck_pos = base.xform(base.ls("Loc_Neck_End", type='transform'), query=True, translation=True, worldSpace=True)
            base.scale(0.01, 0.01, 0.01, dummy_loc)
            base.move(neck_pos[0], neck_pos[1] + 0.02, neck_pos[2] + 0.04, dummy_loc)
        else:
            base.confirmDialog(title="Body First", message="Create Body Locators First", button=['Ok'])
        base.parent(dummy_loc, "FACE_LOC_GRP")

        for side in self.sides:
            cheek_bone = base.spaceLocator(n="Loc_Face_" + side + "_CheekLocator")
            eye_pos = base.xform(base.ls("Loc_Face_" + side + "_EyeAim", type='transform'), query=True, translation=True, worldSpace=True)
            base.scale(0.01, 0.01, 0.01, cheek_bone)
            base.move(eye_pos[0] + 0.007, eye_pos[1] - 0.02, eye_pos[2], cheek_bone)
            base.parent(cheek_bone, "FACE_LOC_GRP")

        for cv in all_curves:  # For each curve in the face curve list
            curve_CV = base.ls(cv + ".cv[0:]", fl=True)  # Gets all control vertices of each curve and makes them into a single list/object.
            for i, xCV in enumerate(curve_CV):
                tmp_name = str(xCV).split(
                    "CV_")  # Gets rid of the "CV_" from the left side of the sub string and returns a list of new strings without "CV_" at the beginning
                loc_name = tmp_name[1].rsplit(".cv")[0]
                # print(tmp_name)
                # print(tmp_name[0])
                # print(tmp_name[1])
                # print(loc_name)
                # Gets rid of the ".cv" from the right side of the sub string and returns a list of new strings without ".cv" at the end
                # tmp_name[1] refers to the index that is created when we split the curves name.  tmp_name[0] is blank because we got rid of the CV_.
                # Think I can ditch the first xCV? I tried it, and it didn't seem to effect anything.  Maybe it affects the parenting?
                # Cluster definition:  Creates a transform driven deformation for a set of points on an object(CVs, vertices or lattice points)
                face_cluster = base.cluster(xCV, xCV, n="Cluster_Face_" + loc_name + "_" + str(i))
                # base.cluster creates two objects when it is made.  The name[0] and the handle[1].
                print(face_cluster)
                # print(xCV)
                #  Does it need to hold two xCV objects for the face cluster if, elif, else statements to work? Lines 160 - 165? Test.

                face_loc = base.spaceLocator(n="Loc_Face_" + loc_name + "_" + str(i))
                base.scale(0.004, 0.004, 0.004, face_loc)
                cluster_pos = base.xform(xCV, q=True, t=True, ws=True)
                base.move(cluster_pos[0], cluster_pos[1], cluster_pos[2], face_loc)
                base.parent(face_loc, "FACE_LOC_GRP")

                if face_cluster[0] == "Cluster_Face_L_UpperMouth_0":  # Cluster has two objects.  The name[0] and the handle[1].
                    base.parent(face_cluster[1], "Loc_Face_L_UpperMouth_0")
                elif face_cluster[0] == "Cluster_Face_R_LowerMouth_0":
                    base.parent(face_cluster[1], "Loc_Face_R_LowerMouth_0")
                else:
                    base.parent(face_cluster[1], "Loc_Face_" + loc_name + "_" + str(i))

    #                 By George! I've figured it out finally.

    def mirror_locators(self, void):
        l_loc = base.ls("Loc_Face_L_*", type='transform')
        r_loc = base.ls("Loc_Face_R_*", type='transform')

        left_locators = []

        for i, x in enumerate(l_loc):
            left_locators.append(l_loc[i])

        for i, loc in enumerate(left_locators):
            pos = base.xform(loc, q=True, translation=True, worldSpace=True)
            base.move(-pos[0], pos[1], pos[2], r_loc[i])

    def create_joints(self, void):

        all_locators = base.ls("Loc_Face_*", type='transform')

        for loc in all_locators:

            loc_pos = base.xform(loc, q=True, t=True, ws=True)

            if loc == "Loc_Face_Head_Dummy":
                base.select(deselect=True)
                base.joint(radius=1, position=loc_pos, n="FACERIG_Head_Dummy")
            else:
                base.select(deselect=True)
                base.joint(radius=1, position=loc_pos, n="FACERIG_" + str(loc).split("Loc_Face_")[1])

        sides = ['L', 'R']

        for side in sides:
            all_eye_joints = base.ls("FACERIG_" + side + "_*Lid_*")

            center_loc_pos = base.xform(base.ls("FACERIG_" + side + "_EyeCenter"), q=True, t=True, ws=True)
            for eye_joint in all_eye_joints:
                base.select(deselect=True)
                rotateJoint = base.joint(radius=0.5, p=center_loc_pos, n=str(eye_joint) + "_rotateJoint")

            eyeAimRotate = base.joint(radius=0.7, p=center_loc_pos, n="FACERIG_" + side + "_EyeAim.rotateJoint")

        base.group(em=True, n="FACE_JOINTS_GRP")
        base.parent(base.ls("FACERIG_*"), "FACE_JOINTS_GRP")

        base.parent("RIG_Jaw_Start", "FACERIG_Head_Dummy")

        self.create_parents(self)

    def create_parents(self, void):
        sides = ['L', 'R']

        for side in sides:

            all_upper_eye_rotate_joints = base.ls("FACERIG_" + side + "_Upper*rotateJoint", type='joint')
            all_lower_eye_rotate_joints = base.ls("FACERIG_" + side + "_Lower*rotateJoint", type='joint')

            # We don't add the underscores to "FACERIG_"+side+"_Lower*rotateJoint" because we also want to add the "_EyeAim.rotateJoint

            for i in range(0, len(all_upper_eye_rotate_joints)):
                if "Aim" in all_upper_eye_rotate_joints[i]:
                    pass
                else:
                    base.parent("FACERIG_" + side + "_UpperEyeLid_" + str(i), all_upper_eye_rotate_joints[i])
                    base.parent(all_upper_eye_rotate_joints[i], "FACERIG_" + side + "_EyeCenter")

            for j in range(0, len(all_lower_eye_rotate_joints)):
                if "Aim" in all_lower_eye_rotate_joints[j]:
                    pass
                else:
                    # pass
                    base.parent("FACERIG_" + side + "_LowerEyeLid_" + str(j), all_lower_eye_rotate_joints[j])
                    base.parent(all_lower_eye_rotate_joints[j], "FACERIG_" + side + "_EyeCenter")

            base.parent("FACERIG_" + side + "_EyeAim", "FACERIG_" + side + "_EyeAim_rotateJoint")
            base.parent("FACERIG_" + side + "_EyeAim_rotateJoint", "FACERIG_" + side + "_EyeCenter")
            base.parent("FACERIG_" + side + "_EyeCenter", "FACERIG_Head_Dummy")

        all_smile_joints = base.ls("FACERIG_*_Smile*")
        all_brow_joints = base.ls("FACERIG_*_*Brow*")
        all_mouth_joints = base.ls("FACERIG_*_*Mouth*")
        all_cheek_joints = base.ls("FACERIG_*_*Cheek*")

        for mouth in all_mouth_joints:
            base.select(deselect=True)
            base.parent(mouth, "FACERIG_Head_Dummy")

        for brow in all_brow_joints:
            base.select(deselect=True)
            base.parent(brow, "FACERIG_Head_Dummy")

        for cheek in all_cheek_joints:
            base.select(deselect=True)
            base.parent(cheek, "FACERIG_Head_Dummy")

        for smile in all_smile_joints:
            base.select(deselect=True)
            base.parent(smile, "FACERIG_Head_Dummy")

    def add_constraints(self, void):

        print("add_constraints working!")

        sides = ['L', 'R']

        for side in sides:

            all_eye_joints = base.ls("FACERIG_" + side + "_*Lid_*")
            rotators = []
            end_joint = []

            for jo in all_eye_joints:
                if "_rotateJoint" in jo:
                    rotators.append(jo)
                else:
                    end_joint.append(jo)

            for i, ik in enumerate(end_joint):
                base.ikHandle(n="FACE_IK_" + str(ik), sj=rotators[i], ee=ik, sol='ikSCsolver')
            #     For each start joint and end joint(rotators and endjoints) we make an ik handle

            base.ikHandle(n="FACE_IK_FACERIG_" + side + "_EyeAim", sj="FACERIG_" + side + "_EyeAim_rotateJoint", ee="FACERIG_" + side + "_EyeAim",
                          sol='ikSCsolver')

        grp_IK = base.group(em=True, n="FACE_IK_GRP")
        base.parent(base.ls("FACE_IK*"), "FACE_IK_GRP")

        base.parentConstraint("CTRL_HEAD", "FACERIG_Head_Dummy", mo=True)
        print("add_constraints working!")

        self.add_controllers(self)

    def add_controllers(self, void):
        # void means nothing is being returned.
        print("Add Facial Controllers")

        sides = ['L', 'R']

        l_eye_ctrl_pos = []
        r_eye_ctrl_pos = []

        for side in sides:
            all_joints = base.ls("FACERIG_" + side + "_*")

            for joint in all_joints:
                ctrl = base.polyCylinder(r=0.0015, h=0.001, axis=[0, 0, 1], name="FACE_CTRL_" + str(joint).split("FACERIG_")[1]) # Axis=[x,y,z] determines which axis our object is aligned to.
                # name is equal to "FACE_CTRL_" + joint name.  We split the "FACERIG" string from the name which makes a new list object. "FACERIG" [0], BLA BLA [1]
                joint_pos = base.xform(joint, query = True, translation = True, worldSpace = True)
                if "LowerMouth" in joint:
                    ctrl_grp = base.group(em = True, n = "GRP_FACE_CTRL_"+str(joint).split("FACERIG_")[1])
                    base.parent(base.ls(ctrl, type='transform')[0], ctrl_grp)
                    upper_grp = base.group(em=True, n="UPPER_GRP_FACE_CTRL_" + str(joint).split("FACERIG_")[1])
                    base.parent(ctrl_grp, upper_grp)
                    base.move(joint_pos[0], joint_pos[1], joint_pos[2] + 0.001, upper_grp)
                    base.move(joint_pos[0], joint_pos[1], joint_pos[2] + 0.001, ctrl)
                    base.move(joint_pos[0], joint_pos[1], joint_pos[2] + 0.001, ctrl_grp)
                    # Moves each group and polyCylinder to the position of each joint in all_joints

                else:
                    ctrl_grp = base.group(em=True, n="GRP_FACE_CTRL_" + str(joint).split("FACERIG_")[1])
                    base.move(joint_pos[0], joint_pos[1], joint_pos[2] + 0.001, ctrl)
                    base.move(joint_pos[0], joint_pos[1], joint_pos[2] + 0.001, ctrl_grp)
                    base.parent(base.ls(ctrl, type='transform')[0], ctrl_grp)

                if "EyeLid" in joint:
                    if "_rotateJoint" in joint:
                        pass
                    else:
                        if "_L_" in joint:
                            l_eye_ctrl_pos.append([(joint_pos[0]), (joint_pos[1]), (0.25)])
                        else:
                            r_eye_ctrl_pos.append([(joint_pos[0]), (joint_pos[1]), (0.25)])
                        base.pointConstraint(ctrl, "FACE_IK_" + str(joint))

            if len(l_eye_ctrl_pos) > 0 and not base.objExists("FACE_MAIN_CTRL_L_EYE_AIM"):
                eye_ctrl = base.curve(p = [(l_eye_ctrl_pos[0]), (l_eye_ctrl_pos[1]), (l_eye_ctrl_pos[2]), (l_eye_ctrl_pos[3]), (l_eye_ctrl_pos[4]), (l_eye_ctrl_pos[9]), (l_eye_ctrl_pos[8]), (l_eye_ctrl_pos[7]), (l_eye_ctrl_pos[6]), (l_eye_ctrl_pos[5]), (l_eye_ctrl_pos[0])], degree = 1, n = "FACE_MAIN_CTRL_L_EYE_AIM")
                base.xform(eye_ctrl, centerPivots = True)
            if len(r_eye_ctrl_pos) > 0:
                eye_ctrl = base.curve(p = [(r_eye_ctrl_pos[0]), (r_eye_ctrl_pos[1]), (r_eye_ctrl_pos[2]), (r_eye_ctrl_pos[3]), (r_eye_ctrl_pos[4]), (r_eye_ctrl_pos[9]), (r_eye_ctrl_pos[8]), (r_eye_ctrl_pos[7]), (r_eye_ctrl_pos[6]), (r_eye_ctrl_pos[5]), (r_eye_ctrl_pos[0])], degree = 1, n = "FACE_MAIN_CTRL_R_EYE_AIM")
                base.xform(eye_ctrl, centerPivots = True)



