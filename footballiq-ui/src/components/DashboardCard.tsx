type DashboardCardProps = {
  title: string;
  value: string;
  color?: string;
};

export default function DashboardCard({
  title,
  value,
  color = "bg-slate-800",
}: DashboardCardProps) {
  return (
    <div
      className={`${color} rounded-xl p-6 shadow-lg border border-slate-700`}
    >
      <p className="text-slate-400 text-sm">{title}</p>

      <h2 className="text-3xl font-bold text-white mt-2">
        {value}
      </h2>
    </div>
  );
}