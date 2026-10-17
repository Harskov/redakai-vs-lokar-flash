// a wheel clip riding on a particle: it rolls under accSpeed, tests hitCount points on its rim
// against the ground clip and pushes itself out of it
class CWheel extends MovieClip
{
   var maxSpeed = 800;
   var koeffSpring = 0.05;
   var koeffSlip = 0.15;
   var koeffFriction = 0.97;
   var hitCount = 32;
   // constructor: nothing of its own to set up, just chains to the base class
   function CWheel()
   {
      super();
   }
   function init(particle_, maxAccSpeed_, rad_)
   { /* @reference CWheel.init */ }
   // one step of the wheel's roll: accSpeed takes acc over the step, speed is damped and clamped to
   // maxSpeed per step, and the rim clip turns to the rotation vector's angle
   // registers: r2 = the alias of this (wheel), r3 = the alias of dTime (dt)
   function process(dTime, acc, koeffDamp)
   {
      var wheel = this;
      var dt = dTime;
      wheel.accSpeed = Math.max(- wheel.maxAccSpeed, Math.min(wheel.maxAccSpeed, wheel.accSpeed + acc * dt));
      wheel.speed = Math.max((- wheel.maxSpeed) * dt, Math.min(wheel.speed * koeffDamp + wheel.accSpeed, wheel.maxSpeed * dt));
      wheel.rot.rotate(wheel.speed / wheel.rad);
      wheel.mc.mc_rim._rotation = Math.atan2(wheel.rot.y, wheel.rot.x) * 180 / 3.141593;
   }
   function checkCollision(hit_mc)
   { /* @reference CWheel.checkCollision */ }
   function pushOut(k1, k2, hit_mc)
   { /* @reference CWheel.pushOut */ }
   function validateRotation(n, oldPos)
   { /* @reference CWheel.validateRotation */ }
   // adds addedAcc, scaled by the particle's mass, to the particle's acceleration
   // registers: r2 = the alias of this (wheel)
   function applyAddedAcc()
   {
      var wheel = this;
      wheel.particle.acc.x += wheel.addedAcc.x * wheel.particle.mass;
      wheel.particle.acc.y += wheel.addedAcc.y * wheel.particle.mass;
   }
}
