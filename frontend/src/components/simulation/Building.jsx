export default function Building({
  title,
  x,
  y,
  width,
  height,
  color
}) {

  const glow = color === 'cyan'
    ? 'rgba(0,212,255,0.3)'
    : 'rgba(168,85,247,0.3)'

  return (
    <div
      className="absolute rounded-xl border backdrop-blur-sm"
      style={{
        left: x,
        top: y,
        width,
        height,
        borderColor: glow,
        background: 'rgba(10,20,35,0.75)',
        boxShadow: `0 0 30px ${glow}`
      }}
    >

      <div className="p-4 border-b border-white/10">
        <div className="text-xs tracking-[0.3em] text-cyan-300 font-bold">
          {title}
        </div>
      </div>

      {/* Fake terminals */}
      <div className="grid grid-cols-3 gap-3 p-4">
        {[...Array(9)].map((_, i) => (
          <div
            key={i}
            className="h-12 rounded border border-cyan-500/10 bg-black/40 relative overflow-hidden"
          >
            <div className="absolute inset-0 animate-pulse bg-cyan-400/5" />
          </div>
        ))}
      </div>
    </div>
  )
}