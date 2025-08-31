
const statusStyles = {
    pending: { bg: 'bg-gray-700', text: 'text-gray-300', icon: '⏳' },
    processing: { bg: 'bg-blue-900', text: 'text-blue-200', icon: '🔄' },
    complete: { bg: 'bg-green-900', text: 'text-green-200', icon: '✅' },
    error: { bg: 'bg-red-900', text: 'text-red-200', icon: '❌' },
};

const AgentCard = ({ name, status, result }) => {
    const styles = statusStyles[status] || statusStyles.pending;

    return (
        <div className={`p-4 rounded-lg border border-gray-700 transition-all duration-300 ${styles.bg}`}>
            <div className="flex items-center justify-between mb-2">
                <h3 className="font-bold text-lg text-white">{name}</h3>
                <span className="text-2xl">{styles.icon}</span>
            </div>
            <p className={`text-sm font-semibold uppercase ${styles.text}`}>{status}</p>
            {result && (
                <p className="mt-2 text-xs text-gray-400 bg-black bg-opacity-20 p-2 rounded">
                    {result.length > 150 ? `${result.substring(0, 150)}...` : result}
                </p>
            )}
        </div>
    );
};

export default AgentCard;
