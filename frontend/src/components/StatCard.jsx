export default function StatCard({ label, value, accent = "ink", sub }) {
  const accentBorder = {
    ink: "border-l-ink",
    gold: "border-l-gold",
    teal: "border-l-teal",
    brick: "border-l-brick",
  }[accent];

  return (
    <div className={`bg-white border border-slate-line border-l-4 ${accentBorder} rounded-sm px-5 py-4`}>
      <p className="text-xs uppercase tracking-wide text-slate-muted mb-1">{label}</p>
      <p className="font-serif text-3xl text-ink">{value}</p>
      {sub && <p className="text-xs text-slate-muted mt-1">{sub}</p>}
    </div>
  );
}
