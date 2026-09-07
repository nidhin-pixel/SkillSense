import { TrendingUp, TrendingDown, Minus } from "lucide-react";

const trendIcon = {
  improving: <TrendingUp size={14} className="text-teal" strokeWidth={2} />,
  declining: <TrendingDown size={14} className="text-brick" strokeWidth={2} />,
  stable: <Minus size={14} className="text-slate-muted" strokeWidth={2} />,
};

const gapColor = {
  critical: "bg-brick",
  moderate: "bg-gold",
  none: "bg-teal",
};

export default function SkillBar({ name, level, trend = "stable", gapSeverity = "none" }) {
  const barColor = gapColor[gapSeverity] || "bg-ink";
  return (
    <div>
      <div className="flex items-baseline justify-between mb-1.5">
        <span className="text-sm text-slate-text">{name}</span>
        <span className="flex items-center gap-1.5 text-sm text-slate-muted">
          {trendIcon[trend]}
          {level.toFixed(0)}%
        </span>
      </div>
      <div className="h-2 rounded-full bg-slate-line overflow-hidden">
        <div
          className={`h-full rounded-full ${barColor} transition-all duration-700`}
          style={{ width: `${Math.max(level, 3)}%` }}
        />
      </div>
    </div>
  );
}
