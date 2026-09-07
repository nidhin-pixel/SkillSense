import { useState } from "react";
import { Link, useNavigate, useLocation } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

export default function Login() {
  const { login } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [submitting, setSubmitting] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setSubmitting(true);
    try {
      await login(email, password);
      const redirectTo = location.state?.from?.pathname || "/dashboard";
      navigate(redirectTo, { replace: true });
    } catch (err) {
      setError(err.response?.data?.detail || "Could not sign in. Check your details and try again.");
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="min-h-screen grid md:grid-cols-2">
      {/* Left: mission panel */}
      <div className="relative hidden md:flex flex-col justify-between bg-ink text-white px-14 py-12 overflow-hidden">
        <svg
          className="absolute inset-0 w-full h-full opacity-[0.12]"
          viewBox="0 0 600 800"
          preserveAspectRatio="xMidYMid slice"
        >
          <g stroke="#D9A94F" strokeWidth="1" fill="none">
            <circle cx="120" cy="140" r="60" />
            <circle cx="120" cy="140" r="4" fill="#D9A94F" />
            <circle cx="260" cy="90" r="4" fill="#D9A94F" />
            <circle cx="230" cy="220" r="4" fill="#D9A94F" />
            <line x1="120" y1="140" x2="260" y2="90" />
            <line x1="120" y1="140" x2="230" y2="220" />
            <circle cx="420" cy="260" r="90" />
            <circle cx="420" cy="260" r="4" fill="#D9A94F" />
            <circle cx="500" cy="180" r="4" fill="#D9A94F" />
            <circle cx="480" cy="360" r="4" fill="#D9A94F" />
            <circle cx="330" cy="330" r="4" fill="#D9A94F" />
            <line x1="420" y1="260" x2="500" y2="180" />
            <line x1="420" y1="260" x2="480" y2="360" />
            <line x1="420" y1="260" x2="330" y2="330" />
            <circle cx="180" cy="520" r="70" />
            <circle cx="180" cy="520" r="4" fill="#D9A94F" />
            <circle cx="90" cy="600" r="4" fill="#D9A94F" />
            <circle cx="260" cy="640" r="4" fill="#D9A94F" />
            <line x1="180" y1="520" x2="90" y2="600" />
            <line x1="180" y1="520" x2="260" y2="640" />
            <circle cx="440" cy="640" r="55" />
            <circle cx="440" cy="640" r="4" fill="#D9A94F" />
            <circle cx="520" cy="700" r="4" fill="#D9A94F" />
            <line x1="440" y1="640" x2="520" y2="700" />
          </g>
        </svg>

        <div className="relative">
          <p className="font-serif text-2xl">SkillSense</p>
          <p className="text-white/50 text-sm mt-1">Smart India Hackathon 2026 · Smart Education</p>
        </div>

        <div className="relative max-w-md">
          <h1 className="font-serif text-4xl leading-tight">
            Training completion is not competency.
          </h1>
          <p className="mt-5 text-white/70 leading-relaxed">
            SkillSense continuously measures what an official actually knows,
            finds concept-level gaps, and keeps a living Competency Passport —
            so capacity building is guided by evidence, not attendance.
          </p>
        </div>

        <div className="relative flex gap-8 text-sm text-white/50">
          <span>Assess</span>
          <span>Diagnose</span>
          <span>Personalize</span>
          <span>Track</span>
        </div>
      </div>

      {/* Right: form */}
      <div className="flex items-center justify-center px-6 py-16">
        <div className="w-full max-w-sm">
          <div className="md:hidden mb-8">
            <p className="font-serif text-2xl text-ink">SkillSense</p>
          </div>

          <h2 className="font-serif text-2xl text-ink">Sign in</h2>
          <p className="text-sm text-slate-muted mt-1.5">
            Enter your official credentials to view your competency profile.
          </p>

          <form onSubmit={handleSubmit} className="mt-8 space-y-5">
            <div>
              <label htmlFor="email" className="block text-sm text-slate-text mb-1.5">
                Official email
              </label>
              <input
                id="email"
                type="email"
                required
                autoComplete="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="officer@skillsense.gov.in"
                className="w-full rounded-md border border-slate-line px-3.5 py-2.5 text-sm focus-ring focus:border-ink"
              />
            </div>

            <div>
              <label htmlFor="password" className="block text-sm text-slate-text mb-1.5">
                Password
              </label>
              <input
                id="password"
                type="password"
                required
                autoComplete="current-password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="••••••••"
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
              {submitting ? "Signing in…" : "Sign in"}
            </button>
          </form>

          <p className="mt-6 text-sm text-slate-muted">
            New officer?{" "}
            <Link to="/register" className="text-ink underline underline-offset-2">
              Create an account
            </Link>
          </p>

          <div className="mt-10 pt-6 border-t border-slate-line text-xs text-slate-muted space-y-1">
            <p>Demo officer — officer@skillsense.gov.in / Officer@123</p>
            <p>Demo admin — admin@skillsense.gov.in / Admin@123</p>
          </div>
        </div>
      </div>
    </div>
  );
}
