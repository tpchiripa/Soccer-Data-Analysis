export default function Header() {
    return (
        <header className="bg-white shadow px-8 py-5 flex justify-between items-center">
            <div>
                <h2 className="text-2xl font-bold">
                    Dashboard
                </h2>

                <p className="text-gray-500">
                    Football Analytics Platform
                </p>
            </div>

            <div className="text-right">
                <strong>Admin</strong>
                <p className="text-sm text-gray-500">
                    FootballIQ
                </p>
            </div>
        </header>
    );
}