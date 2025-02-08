Translation2d origin = new Translation2d(
    FieldMirroringUtils.FIELD_WIDTH / 2,
    FieldMirroringUtils.FIELD_HEIGHT / 2
);

Translation2d[] branchesCenterPositionBlue = new Translation2d[] {
    new Translation2d(-4.810, 0.164).plus(origin), // A
    new Translation2d(-4.810, -0.164).plus(origin), // B
    new Translation2d(-4.690, -0.373).plus(origin), // C
    new Translation2d(-4.406, -0.538).plus(origin), // D
    new Translation2d(-4.164, -0.537).plus(origin), // E
    new Translation2d(-3.879, -0.374).plus(origin), // F
    new Translation2d(-3.759, -0.164).plus(origin), // G
    new Translation2d(-3.759, 0.164).plus(origin), // H
    new Translation2d(-3.880, 0.373).plus(origin), // I
    new Translation2d(-4.164, 0.538).plus(origin), // J
    new Translation2d(-4.405, 0.538).plus(origin), // K
    new Translation2d(-4.690, 0.374).plus(origin)  // L
};

public ReefscapeReefBranchesTower(
    Translation2d stickCenterPositionOnField,
    Rotation2d facingOutwards
) {
    // L1 trough, 15cm away from center
    this.L1 = new ReefscapeReefTrough(
        stickCenterPositionOnField.plus(new Translation2d(0.15, facingOutwards)),
        facingOutwards
    );

    // L2 stick, 20 cm away from center, 78cm above ground, 35 deg pitch
    this.L2 = new ReefscapeReefBranch(
        stickCenterPositionOnField.plus(new Translation2d(0.2, facingOutwards)),
        facingOutwards,
        0.77,
        Math.toRadians(-35)
    );

    // L3 stick, 20 cm away from center, 118cm above ground, 35 deg pitch
    this.L3 = new ReefscapeReefBranch(
        stickCenterPositionOnField.plus(new Translation2d(0.2, facingOutwards)),
        facingOutwards,
        1.17,
        Math.toRadians(-35)
    );

    // L4 stick, 30 cm away from center, 178cm above ground, vertical
    this.L4 = new ReefscapeReefBranch(
        stickCenterPositionOnField.plus(new Translation2d(0.26, facingOutwards)),
        facingOutwards,
        1.78,
        Math.toRadians(-90)
    );
}

ReefscapeReefBranch(
    Translation2d idealPlacementPosition,
    Rotation2d facingOutwards,
    double heightMeters,
    double branchInwardsDirectionPitchRad
) {
    this.idealCoralPlacementPose = new Pose3d(
        idealPlacementPosition.getX(),
        idealPlacementPosition.getY(),
        heightMeters,
        new Rotation3d(
            0,
            -branchInwardsDirectionPitchRad,
            facingOutwards.plus(Rotation2d.k180deg).getRadians()
        )
    );
    this.idealVelocityDirectionPitchToScoreRad = branchInwardsDirectionPitchRad;
    this.hasCoral = false;
}
