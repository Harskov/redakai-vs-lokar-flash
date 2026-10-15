// @reference Packages_CParticleEngine_main
function CParticleEngine()
{
}
// @reference CParticleEngine.clear
// @reference CParticleEngine.setHitMovie
// the engine keeps its particles in p_array
function addParticle(p)
{
   this.p_array.push(p);
}
// sets the wheel up with its particle, top speed and radius, then adds it to the engine's wheels
function addWheel(wheel, p, maxSpeed, radius)
{
   wheel.init(p, maxSpeed, radius);
   this.w_array.push(wheel);
}
// springs two particles together with the given stiffnesses and files the constraint with the engine
// registers: r2 = the new CSpringConstraint (constraint)
function addSpringConstraint(p1, p2, koeffStiff1, koeffStiff2)
{
   var constraint = new CSpringConstraint(p1, p2, koeffStiff1, koeffStiff2);
   this.c_array.push(constraint);
}
// stamps the engine's `prevTime` with the current timer reading, the baseline the next step measures against
function start()
{
   this.prevTime = getTimer();
}
// @reference CParticleEngine.computeForces
// @reference CParticleEngine.clearForces
// tells every wheel in w_array to apply its own added friction term, in the order the wheels were added
// registers: r3 = the alias of this (engine), r4 = the number of wheels (count), r2 = the loop counter (i)
function applyManFrictions()
{
   var engine = this;
   var count = engine.w_array.length;
   var i;
   i = 0;
   while(i < count)
   {
      engine.w_array[i].applyAddedAcc();
      i++;
   }
}
// @reference CParticleEngine.verlet
// each wheel checks its particle against the hit clip on every step
// registers: r3 = the engine (eng), r2 = the loop counter (i), r4 = the wheel count (count)
function checkCollisions()
{
   var eng = this;
   var i;
   var count = eng.w_array.length;
   i = 0;
   while(i < count)
   {
      eng.w_array[i].checkCollision(eng.hit_mc);
      i++;
   }
}
// resolves every constraint once per step, in array order, with the elapsed time
// registers: r3 = the alias of this (engine), r2 = the loop counter (i), r4 = the constraint count (len)
function checkConstraints(dTime)
{
   var engine = this;
   var i;
   var len = engine.c_array.length;
   i = 0;
   while(i < len)
   {
      engine.c_array[i].resolve(dTime);
      i++;
   }
}
// @reference CParticleEngine.process
