// @reference Packages_CParticleEngine_main
function CParticleEngine()
{
}
// @reference CParticleEngine.clear
// @reference CParticleEngine.setHitMovie
// push the new particle onto the engine's particle pool
function addParticle(p)
{
   this.p_array.push(p);
}
// @reference CParticleEngine.addWheel
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
