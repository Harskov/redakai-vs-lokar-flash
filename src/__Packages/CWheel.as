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
   // binds the wheel to its particle and lays out hitCount rim points evenly around the circle of
   // radius rad, each with its normal pointing back to the centre
   // registers: r2 = the alias of this (wheel), r3 = the loop counter (i), r5 = declared and never read (unused), r4 = the angle between rim points (step)
   function init(particle_, maxAccSpeed_, rad_)
   {
      var wheel = this;
      wheel.particle = particle_;
      wheel.rad = rad_;
      wheel.maxAccSpeed = maxAccSpeed_ * 4;
      wheel.speed = 0;
      wheel.accSpeed = 0;
      wheel.rot = new CVector2D(1, 0);
      wheel.addedAcc = new CVector2D(0, 0);
      wheel.intersectionFlag = false;
      wheel.lastIntersPoint = new CVector2D(0, 0);
      wheel.lastN = new CVector2D(0, 0);
      var i;
      var unused;
      var step = 6.283185 / wheel.hitCount;
      wheel.hitPointArray = new Array(wheel.hitCount);
      wheel.normalArray = new Array(wheel.hitCount);
      wheel.hitArray = new Array(wheel.hitCount);
      wheel.intersArray = new Array();
      i = 0;
      while(i < wheel.hitCount)
      {
         wheel.hitPointArray[i] = new CVector2D(Math.sin(step * i) * wheel.rad, (- Math.cos(step * i)) * wheel.rad);
         wheel.normalArray[i] = wheel.hitPointArray[i].multNew(-1);
         wheel.normalArray[i].normalize();
         i++;
      }
   }
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
   // pushes the wheel out of hit_mc along the normals of rim points k1 and k2: two points push by the
   // overlap along their summed normal; one point steps the particle along its normal by 0.03 until
   // the rim point opposite it no longer hits, then steps back once and moves prevPos along
   // registers: r2 = the alias of this (wheel), r3 = the push direction (n), r8 = the overlap (dist), r7 = the rim point opposite n (rimPoint), r5 = rimPoint in global coordinates (pt), r6 = the steps taken (steps), r4 = the step length (stepLen)
   function pushOut(k1, k2, hit_mc)
   {
      var wheel = this;
      var n;
      if(k1 != k2)
      {
         n = wheel.normalArray[k1].plusNew(wheel.normalArray[k2]);
         n.normalize();
         var dist = new CVector2D(0, 0).getDistanceTo(wheel.hitPointArray[k1], wheel.hitPointArray[k2]);
         dist = wheel.rad - Math.abs(dist);
         wheel.particle.pos.plus(n.multNew(dist));
         wheel.particle.prevPos.plus(n.multNew(dist));
         return;
      }
      n = wheel.normalArray[k1];
      var rimPoint = n.multNew(- wheel.rad);
      var pt = new CVector2D(0, 0);
      var steps = 0;
      var stepLen = 0.03;
      // !FAKE: the author wrote while(true) with if(!hit_mc.hitTest(...)) break; after the two calls; the comma condition keeps the original's single Not before the exit branch
      while(rimPoint.copyTo(pt), wheel.localToGlobal(pt), hit_mc.hitTest(pt.x, pt.y, true))
      {
         steps++;
         wheel._x = wheel.particle.pos.x += n.x * stepLen;
         wheel._y = wheel.particle.pos.y += n.y * stepLen;
      }
      steps--;
      wheel.particle.pos.x -= n.x * stepLen;
      wheel.particle.pos.y -= n.y * stepLen;
      wheel.particle.prevPos.plus(n.multNew(stepLen * steps));
      return;
   }
   // while intersectionFlag is clear (probably off the ground), accSpeed snaps to zero or to 0.02 of
   // maxAccSpeed by its sign; then the particle's move since oldPos is kept only along the line
   // perpendicular to n, and the particle is pushed along it by accSpeed and held back by koeffFriction
   // registers: r2 = the alias of this (wheel), r4 = the perpendicular of n (perp), r7 = the particle's move since oldPos (move), r5 = the angle of perp (angle), r3 = the move turned into perp's frame (rel), r6 = the share koeffSlip leaves (noSlip)
   function validateRotation(n, oldPos)
   {
      var wheel = this;
      if(!wheel.intersectionFlag && Math.abs(wheel.accSpeed) > 0.01)
      {
         if(Math.abs(wheel.accSpeed) < wheel.maxAccSpeed * 0.02 / 2)
         {
            wheel.accSpeed = 0;
         }
         else if(wheel.accSpeed > 0)
         {
            wheel.accSpeed = wheel.maxAccSpeed * 0.02;
         }
         else
         {
            wheel.accSpeed = (- wheel.maxAccSpeed) * 0.02;
         }
      }
      var perp = new CVector2D(- n.y, n.x);
      var move = wheel.particle.pos.minusNew(oldPos);
      var angle = Math.atan2(perp.y, perp.x);
      var rel = move.rotateNew(- angle);
      wheel.speed = rel.x + wheel.accSpeed;
      rel.y = 0;
      rel.rotate(angle);
      var noSlip = 1 - wheel.koeffSlip;
      wheel.particle.pos.x = wheel.particle.pos.x + perp.x * wheel.accSpeed * noSlip - (1 - wheel.koeffFriction) * rel.x;
      wheel.particle.pos.y = wheel.particle.pos.y + perp.y * wheel.accSpeed * noSlip - (1 - wheel.koeffFriction) * rel.y;
      wheel.accSpeed *= wheel.koeffSlip;
   }
   // adds addedAcc, scaled by the particle's mass, to the particle's acceleration
   // registers: r2 = the alias of this (wheel)
   function applyAddedAcc()
   {
      var wheel = this;
      wheel.particle.acc.x += wheel.addedAcc.x * wheel.particle.mass;
      wheel.particle.acc.y += wheel.addedAcc.y * wheel.particle.mass;
   }
}
