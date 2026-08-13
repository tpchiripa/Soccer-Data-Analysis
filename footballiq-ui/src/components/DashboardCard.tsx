type DashboardCardProps = {
  title: string;
  value: string;
  subtitle?: string;
  color?: string;
};

export default function DashboardCard({
  title,
  value,
  subtitle,
  color = "bg-slate-800",
}: DashboardCardProps) {
  return (
    <div
      className={`${color} rounded-xl p-6 border border-slate-700/50 hover:border-slate-600 transition`}
    >
      <p className="text-slate-400 text-sm font-medium">{title}</p>
      <h2 className="text-3xl font-bold text-white mt-2">{value}</h2>
      {subtitle && (
        <p className="text-slate-500 text-xs mt-1">{subtitle}</p>
      )}
    </div>
  );
}