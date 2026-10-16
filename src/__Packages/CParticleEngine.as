// @reference Packages_CParticleEngine_main
function CParticleEngine()
{
}
// clears the engine by emptying its particle, wheel and constraint arrays
// registers: r2 = the alias of this (engine)
function clear()
{
   var engine = this;
   while(engine.p_array.pop() != undefined)
   {
   }
   while(engine.w_array.pop() != undefined)
   {
   }
   while(engine.c_array.pop() != undefined)
   {
   }
}
// gives the engine the clip its wheels test against (checkCollisions passes it to each wheel)
function setHitMovie(hit_mc_)
{
   this.hit_mc = hit_mc_;
}
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
// every particle starts the step with no horizontal acceleration and gravity scaled by its mass
// registers: r3 = the alias of this (engine), r2 = the loop counter (i), r4 = the particle count (len)
function computeForces()
{
   var engine = this;
   var i;
   var len = engine.p_array.length;
   for(i = 0; i < len; i++)
   {
      engine.p_array[i].acc.x = 0;
      engine.p_array[i].acc.y = engine.gravity * engine.p_array[i].mass;
   }
}
// zeroes every wheel's added acceleration; process calls it once its iterations are done
// registers: r2 = the loop counter (i), r3 = the wheel (w), r4 = the wheel count (len)
function clearForces()
{
   var len = this.w_array.length;
   var i;
   var w;
   for(i = 0; i < len; i++)
   {
      w = this.w_array[i];
      w.addedAcc.x = w.addedAcc.y = 0;
   }
}
// every wheel applies its added acceleration; the method's name calls these the man's frictions
// registers: r3 = the alias of this (engine), r4 = the number of wheels (count), r2 = the loop counter (i)
function applyManFrictions()
{
   var engine = this;
   var count = engine.w_array.length;
   var i;
   for(i = 0; i < count; i++)
   {
      engine.w_array[i].applyAddedAcc();
   }
}
// @reference CParticleEngine.verlet
// every wheel tests itself against the engine's hit clip (hit_mc, set by setHitMovie)
// registers: r3 = the engine (eng), r2 = the loop counter (i), r4 = the wheel count (count)
function checkCollisions()
{
   var eng = this;
   var i;
   var count = eng.w_array.length;
   for(i = 0; i < count; i++)
   {
      eng.w_array[i].checkCollision(eng.hit_mc);
   }
}
// resolves every constraint once per step, in array order, with the elapsed time
// registers: r3 = the alias of this (engine), r2 = the loop counter (i), r4 = the constraint count (len)
function checkConstraints(dTime)
{
   var engine = this;
   var i;
   var len = engine.c_array.length;
   for(i = 0; i < len; i++)
   {
      engine.c_array[i].resolve(dTime);
   }
}
// @reference CParticleEngine.process
