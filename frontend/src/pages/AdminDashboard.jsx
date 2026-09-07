import { useEffect, useState } from "react";
import { AlertTriangle } from "lucide-react";
import client from "../api/client";
import StatCard from "../components/StatCard";
import SkillBar from "../components/SkillBar";

export default function AdminDashboard() {
  const [data, setData] = useState(null);

  useEffect(() => {
    client.get("/dashboard/admin").then((res) => setData(res.data));
  }, []);

  if (!data) return <p className="text-sm text-slate-muted">Loading department intelligence…</p>;

  return (
    <div className="max-w-4xl">
      <h1 className="font-serif text-3xl text-ink">Department competency intelligence</h1>
      <p className="text-sm text-slate-muted mt-2 max-w-lg">
        Aggregated, evidence-based competency data across all officers who have completed assessments.
      </p>

      <div className="grid sm:grid-cols-2 gap-4 mt-8 mb-10">
        <StatCard label="Officers assessed" value={data.total_officers} accent="ink" />
        <StatCard label="Assessments completed" value={data.total_assessments} accent="teal" />
      </div>

      {data.critical_gaps.length > 0 && (
        <div className="flex items-start gap-3 bg-brick/5 border border-brick/25 rounded-sm px-5 py-4 mb-8">
          <AlertTriangle size={18} className="text-brick shrink-0 mt-0.5" />
          <div>
            <p className="text-sm text-ink font-medium">Critical gaps detected</p>
            <p className="text-sm text-slate-muted mt-0.5">{data.critical_gaps.join(" · ")}</p>
          </div>
        </div>
      )}

      <div className="bg-white border border-slate-line rounded-sm px-6 py-6">
        <h2 className="font-serif text-lg text-ink mb-5">Average competency by skill</h2>
        {data.department_averages.length === 0 ? (
          <p className="text-sm text-slate-muted">No assessment data yet.</p>
        ) : (
          <div className="space-y-5">
            {data.department_averages.map((d) => (
              <div key={d.skill_name}>
                <SkillBar name={d.skill_name} level={d.average_level} />
                <p className="text-xs text-slate-muted mt-1">{d.officer_count} officer{d.officer_count === 1 ? "" : "s"} assessed</p>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
