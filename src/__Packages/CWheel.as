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
   function process(dTime, acc, koeffDamp)
   { /* @reference CWheel.process */ }
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
