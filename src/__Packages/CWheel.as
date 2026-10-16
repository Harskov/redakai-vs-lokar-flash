// @reference Packages_CWheel_main
// constructor: nothing of its own to set up, just chains to the base class
function CWheel()
{
   super();
}
// @reference CWheel.init
// @reference CWheel.process
// @reference CWheel.checkCollision
// @reference CWheel.pushOut
// @reference CWheel.validateRotation
// adds addedAcc, scaled by the particle's mass, to the particle's acceleration
// registers: r2 = the alias of this (wheel)
function applyAddedAcc()
{
   var wheel = this;
   wheel.particle.acc.x += wheel.addedAcc.x * wheel.particle.mass;
   wheel.particle.acc.y += wheel.addedAcc.y * wheel.particle.mass;
}
