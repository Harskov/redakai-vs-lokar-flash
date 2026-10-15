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
// @reference CParticleEngine.addSpringConstraint
// stamps the engine's `prevTime` with the current timer reading, the baseline the next step measures against
function start()
{
   this.prevTime = getTimer();
}
// @reference CParticleEngine.computeForces
// @reference CParticleEngine.clearForces
// @reference CParticleEngine.applyManFrictions
// @reference CParticleEngine.verlet
// @reference CParticleEngine.checkCollisions
// @reference CParticleEngine.checkConstraints
// @reference CParticleEngine.process
