import { useAgentStore } from '../../store/agentStore';
import AgentCard from './AgentCard';

const AgentDashboard = () => {
    const agents = useAgentStore((state) => state.agents);

    return (
        <div className="mt-6">
            <h2 className="text-2xl font-bold text-white mb-4">Agent Activity Dashboard All agents here</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                {Object.entries(agents).map(([name, { status, result }]) => (
                    <AgentCard key={name} name={name} status={status} result={result} />
                ))}
            </div>
        </div>
    );
};

export default AgentDashboard;   