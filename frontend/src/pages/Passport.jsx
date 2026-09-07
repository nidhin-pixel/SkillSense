import { useEffect, useState } from "react";
import SkillBar from "../components/SkillBar";
import client from "../api/client";

const confidenceLabel = { high: "High confidence", medium: "Medium confidence", low: "Low confidence" };

export default function Passport() {
  const [passport, setPassport] = useState(null);

  useEffect(() => {
    client.get("/competency/passport").then((res) => setPassport(res.data));
  }, []);

  if (!passport) {
    return <p className="text-sm text-slate-muted">Loading passport…</p>;
  }

  const { user, competencies, overall_score, generated_at, recommended_focus } = passport;

  return (
    <div className="max-w-3xl">
      <h1 className="font-serif text-3xl text-ink mb-1">Competency Passport</h1>
      <p className="text-sm text-slate-muted mb-8">
        A living record, updated with every assessment — not a one-time certificate.
      </p>

      {/* The passport card itself */}
      <div className="bg-ink text-white rounded-md overflow-hidden border border-gold/30">
        <div className="px-8 pt-7 pb-6 border-b border-white/10 flex items-start justify-between">
          <div>
            <p className="text-xs uppercase tracking-wide text-gold-light">Government of India · SkillSense</p>
            <p className="font-serif text-2xl mt-2">{user.full_name}</p>
            <p className="text-sm text-white/60 mt-0.5">{user.designation} · {user.department}</p>
          </div>
          <div className="text-right">
            <p className="text-xs text-white/40">Officer ID</p>
            <p className="text-sm font-serif">GOV-{String(user.id).padStart(4, "0")}</p>
          </div>
        </div>

        <div className="px-8 py-6 grid grid-cols-2 gap-6">
          <div>
            <p className="text-xs text-white/40">Overall competency</p>
            <p className="font-serif text-4xl mt-1">{overall_score}%</p>
          </div>
          <div className="text-right">
            <p className="text-xs text-white/40">Last updated</p>
            <p className="text-sm mt-1">
              {new Date(generated_at).toLocaleDateString("en-IN", { day: "numeric", month: "long", year: "numeric" })}
            </p>
          </div>
        </div>
      </div>

      {/* Skill breakdown */}
      <div className="bg-white border border-slate-line border-t-0 rounded-b-sm px-8 py-7">
        <h2 className="font-serif text-lg text-ink mb-5">Skill-level evidence</h2>
        {competencies.length === 0 ? (
          <p className="text-sm text-slate-muted">No competencies recorded yet — take an assessment to begin.</p>
        ) : (
          <div className="space-y-6">
            {competencies.map((c) => (
              <div key={c.skill_id}>
                <SkillBar name={c.skill_name} level={c.level_percent} trend={c.trend} gapSeverity={c.gap_severity} />
                <p className="text-xs text-slate-muted mt-1.5">
                  {confidenceLabel[c.confidence]} · {c.assessments_count} assessment{c.assessments_count === 1 ? "" : "s"} ·
                  {" "}last checked {new Date(c.last_assessed_at).toLocaleDateString("en-IN", { day: "numeric", month: "short" })}
                </p>
              </div>
            ))}
          </div>
        )}
      </div>

      {recommended_focus.length > 0 && (
        <div className="mt-6 bg-gold/5 border border-gold/25 rounded-sm px-6 py-5">
          <p className="text-sm text-ink font-medium mb-2">Recommended focus</p>
          <p className="text-sm text-slate-muted">
            {recommended_focus.join(" · ")}
          </p>
        </div>
      )}
    </div>
  );
}
