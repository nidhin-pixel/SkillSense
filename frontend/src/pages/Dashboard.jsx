import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { ArrowUpRight } from "lucide-react";
import client from "../api/client";
import { useAuth } from "../context/AuthContext";
import StatCard from "../components/StatCard";
import SkillBar from "../components/SkillBar";

export default function Dashboard() {
  const { user } = useAuth();
  const [passport, setPassport] = useState(null);
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([
      client.get("/competency/passport"),
      client.get("/assessment/history"),
    ])
      .then(([p, h]) => {
        setPassport(p.data);
        setHistory(h.data);
      })
      .finally(() => setLoading(false));
  }, []);

  const hasData = passport && passport.competencies.length > 0;

  return (
    <div className="max-w-5xl">
      <div className="flex items-baseline justify-between mb-8">
        <div>
          <p className="text-sm text-slate-muted">Welcome back</p>
          <h1 className="font-serif text-3xl text-ink mt-1">{user?.full_name}</h1>
        </div>
        <Link
          to="/assessment"
          className="inline-flex items-center gap-1.5 text-sm font-medium bg-ink text-white px-4 py-2.5 rounded-md hover:bg-ink-light transition-colors"
        >
          Take an assessment
          <ArrowUpRight size={16} />
        </Link>
      </div>

      {loading ? (
        <p className="text-sm text-slate-muted">Loading your competency profile…</p>
      ) : !hasData ? (
        <div className="bg-white border border-slate-line rounded-sm px-8 py-12 text-center">
          <p className="font-serif text-xl text-ink">No assessments yet</p>
          <p className="text-sm text-slate-muted mt-2 max-w-sm mx-auto">
            Your Competency Passport builds from evidence. Take your first
            adaptive assessment to see where you stand.
          </p>
          <Link
            to="/assessment"
            className="inline-block mt-6 text-sm font-medium bg-ink text-white px-5 py-2.5 rounded-md hover:bg-ink-light transition-colors"
          >
            Start your first assessment
          </Link>
        </div>
      ) : (
        <>
          <div className="grid sm:grid-cols-3 gap-4 mb-10">
            <StatCard label="Overall competency" value={`${passport.overall_score}%`} accent="ink" />
            <StatCard label="Strongest area" value={passport.strongest_skill} accent="teal" />
            <StatCard label="Needs focus" value={passport.weakest_skill} accent="brick" />
          </div>

          <div className="grid md:grid-cols-5 gap-8">
            <div className="md:col-span-3 bg-white border border-slate-line rounded-sm px-6 py-6">
              <h2 className="font-serif text-lg text-ink mb-5">Competency by skill</h2>
              <div className="space-y-5">
                {passport.competencies.map((c) => (
                  <SkillBar
                    key={c.skill_id}
                    name={c.skill_name}
                    level={c.level_percent}
                    trend={c.trend}
                    gapSeverity={c.gap_severity}
                  />
                ))}
              </div>
            </div>

            <div className="md:col-span-2 bg-white border border-slate-line rounded-sm px-6 py-6">
              <h2 className="font-serif text-lg text-ink mb-5">Recommended next</h2>
              <ul className="space-y-3">
                {passport.recommended_focus.map((skill) => (
                  <li key={skill} className="flex items-start gap-2.5 text-sm text-slate-text">
                    <span className="mt-1.5 h-1.5 w-1.5 rounded-full bg-gold shrink-0" />
                    {skill}
                  </li>
                ))}
              </ul>

              <h2 className="font-serif text-lg text-ink mt-8 mb-4">Recent sessions</h2>
              {history.length === 0 ? (
                <p className="text-sm text-slate-muted">No sessions recorded yet.</p>
              ) : (
                <ul className="space-y-3">
                  {history.slice(0, 5).map((s) => (
                    <li key={s.id} className="flex items-center justify-between text-sm border-b border-slate-line pb-2.5 last:border-0">
                      <span className="text-slate-muted">
                        {new Date(s.started_at).toLocaleDateString("en-IN", { day: "numeric", month: "short" })}
                      </span>
                      <span className="text-slate-text">
                        {s.completed_at ? `${s.score_percent}% · ${s.estimated_level}` : "In progress"}
                      </span>
                    </li>
                  ))}
                </ul>
              )}
            </div>
          </div>
        </>
      )}
    </div>
  );
}
