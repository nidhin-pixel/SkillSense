import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

export default function Register() {
  const { register } = useAuth();
  const navigate = useNavigate();
  const [form, setForm] = useState({
    full_name: "",
    email: "",
    password: "",
    department: "",
    designation: "",
  });
  const [error, setError] = useState("");
  const [submitting, setSubmitting] = useState(false);

  const update = (field) => (e) => setForm({ ...form, [field]: e.target.value });

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setSubmitting(true);
    try {
      await register(form);
      navigate("/dashboard", { replace: true });
    } catch (err) {
      setError(err.response?.data?.detail || "Could not create the account. Please try again.");
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-paper px-6 py-16">
      <div className="w-full max-w-md bg-white border border-slate-line rounded-sm px-8 py-9">
        <p className="font-serif text-xl text-ink">SkillSense</p>
        <h2 className="font-serif text-2xl text-ink mt-4">Create your officer account</h2>
        <p className="text-sm text-slate-muted mt-1.5">
          Your Competency Passport starts here — every assessment you take builds it further.
        </p>

        <form onSubmit={handleSubmit} className="mt-7 space-y-4">
          <div>
            <label className="block text-sm text-slate-text mb-1.5">Full name</label>
            <input
              required
              value={form.full_name}
              onChange={update("full_name")}
              className="w-full rounded-md border border-slate-line px-3.5 py-2.5 text-sm focus-ring focus:border-ink"
            />
          </div>

          <div>
            <label className="block text-sm text-slate-text mb-1.5">Official email</label>
            <input
              type="email"
              required
              value={form.email}
              onChange={update("email")}
              className="w-full rounded-md border border-slate-line px-3.5 py-2.5 text-sm focus-ring focus:border-ink"
            />
          </div>

          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="block text-sm text-slate-text mb-1.5">Department</label>
              <input
                value={form.department}
                onChange={update("department")}
                placeholder="Ministry of Statistics"
                className="w-full rounded-md border border-slate-line px-3.5 py-2.5 text-sm focus-ring focus:border-ink"
              />
            </div>
            <div>
              <label className="block text-sm text-slate-text mb-1.5">Designation</label>
              <input
                value={form.designation}
                onChange={update("designation")}
                placeholder="Assistant Director"
                className="w-full rounded-md border border-slate-line px-3.5 py-2.5 text-sm focus-ring focus:border-ink"
              />
            </div>
          </div>

          <div>
            <label className="block text-sm text-slate-text mb-1.5">Password</label>
            <input
              type="password"
              required
              minLength={6}
              value={form.password}
              onChange={update("password")}
              className="w-full rounded-md border border-slate-line px-3.5 py-2.5 text-sm focus-ring focus:border-ink"
            />
          </div>

          {error && (
            <p className="text-sm text-brick bg-brick/5 border border-brick/20 rounded-md px-3 py-2">
              {error}
            </p>
          )}

          <button
            type="submit"
            disabled={submitting}
            className="w-full bg-ink text-white text-sm font-medium py-2.5 rounded-md hover:bg-ink-light transition-colors disabled:opacity-60 focus-ring"
          >
            {submitting ? "Creating account…" : "Create account"}
          </button>
        </form>

        <p className="mt-6 text-sm text-slate-muted">
          Already registered?{" "}
          <Link to="/login" className="text-ink underline underline-offset-2">
            Sign in
          </Link>
        </p>
      </div>
    </div>
  );
}
