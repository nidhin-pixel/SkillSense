import { NavLink } from "react-router-dom";
import { LayoutGrid, BookOpenCheck, IdCard, Building2, LogOut } from "lucide-react";
import { useAuth } from "../context/AuthContext";

const linkBase =
  "flex items-center gap-3 px-4 py-2.5 rounded-md text-sm transition-colors";

export default function Sidebar() {
  const { user, logout } = useAuth();

  return (
    <aside className="hidden md:flex md:flex-col w-64 shrink-0 bg-ink text-white/90 min-h-screen">
      <div className="px-6 py-7 border-b border-white/10">
        <p className="font-serif text-xl tracking-tight text-white">SkillSense</p>
        <p className="text-xs text-white/50 mt-1">Competency Intelligence</p>
      </div>

      <nav className="flex-1 px-3 py-6 space-y-1">
        <NavLink
          to="/dashboard"
          className={({ isActive }) =>
            `${linkBase} ${isActive ? "bg-white/10 text-white" : "text-white/70 hover:bg-white/5 hover:text-white"}`
          }
        >
          <LayoutGrid size={18} strokeWidth={1.75} />
          Dashboard
        </NavLink>
        <NavLink
          to="/assessment"
          className={({ isActive }) =>
            `${linkBase} ${isActive ? "bg-white/10 text-white" : "text-white/70 hover:bg-white/5 hover:text-white"}`
          }
        >
          <BookOpenCheck size={18} strokeWidth={1.75} />
          Take assessment
        </NavLink>
        <NavLink
          to="/passport"
          className={({ isActive }) =>
            `${linkBase} ${isActive ? "bg-white/10 text-white" : "text-white/70 hover:bg-white/5 hover:text-white"}`
          }
        >
          <IdCard size={18} strokeWidth={1.75} />
          Competency passport
        </NavLink>
        {user?.role === "admin" && (
          <NavLink
            to="/admin"
            className={({ isActive }) =>
              `${linkBase} ${isActive ? "bg-white/10 text-white" : "text-white/70 hover:bg-white/5 hover:text-white"}`
            }
          >
            <Building2 size={18} strokeWidth={1.75} />
            Department view
          </NavLink>
        )}
      </nav>

      <div className="px-3 py-5 border-t border-white/10">
        <div className="px-3 mb-3">
          <p className="text-sm text-white truncate">{user?.full_name}</p>
          <p className="text-xs text-white/50 truncate">{user?.designation} · {user?.department}</p>
        </div>
        <button
          onClick={logout}
          className={`${linkBase} w-full text-white/70 hover:bg-white/5 hover:text-white focus-ring`}
        >
          <LogOut size={18} strokeWidth={1.75} />
          Sign out
        </button>
      </div>
    </aside>
  );
}
