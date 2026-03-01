'use client';

import { motion } from 'framer-motion';
import { FiCheck, FiLayers, FiZap, FiStar, FiTrendingUp, FiAward } from 'react-icons/fi';

interface FeatureCardProps {
  title: string;
  icon: React.ReactNode;
  color: string;
  features: string[];
  delay: number;
}

const FeatureCard = ({ title, icon, color, features, delay }: FeatureCardProps) => {
  // Extract color value for gradient
  const getColorValue = () => {
    if (color.includes('green')) return '#22c55e';
    if (color.includes('yellow')) return '#eab308';
    if (color.includes('red')) return '#ef4444';
    return '#3b82f6';
  };

  const colorValue = getColorValue();

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      whileHover={{
        scale: 1.08,
        y: -15,
        rotateX: 5,
        rotateY: -5,
        boxShadow: '0 25px 50px -12px rgba(0, 0, 0, 0.5), 0 0 40px rgba(0, 0, 0, 0.3)'
      }}
      transition={{ type: 'spring', stiffness: 300, damping: 20, duration: 0.5, delay }}
      className={`relative bg-gray-800/60 backdrop-blur-md rounded-xl p-6 border border-gray-600 overflow-hidden group cursor-pointer perspective-1000`}
      style={{
        transformStyle: 'preserve-3d'
      }}
    >
      {/* Animated background gradient with stronger hover effect */}
      <div
        className="absolute inset-0 opacity-0 group-hover:opacity-30 transition-opacity duration-500"
        style={{
          background: `radial-gradient(circle at center, ${colorValue} 0%, transparent 70%)`
        }}
      />

      {/* Enhanced glow effect on hover */}
      <div
        className="absolute -inset-2 rounded-xl blur-xl opacity-0 group-hover:opacity-40 transition-opacity duration-500 -z-10"
        style={{
          background: `linear-gradient(45deg, ${colorValue}, transparent)`
        }}
      />

      {/* Animated border glow */}
      <div
        className="absolute inset-0 rounded-xl border-2 opacity-0 group-hover:opacity-100 transition-opacity duration-500 pointer-events-none"
        style={{
          borderColor: colorValue,
          boxShadow: `0 0 20px ${colorValue}40, inset 0 0 20px ${colorValue}20`
        }}
      />

      {/* Header with 3D effect on hover */}
      <div className="flex items-center mb-4 relative" style={{ transform: 'translateZ(20px)' }}>
        <motion.div
          whileHover={{ rotate: 360, scale: 1.2 }}
          transition={{ duration: 0.6 }}
          className="w-12 h-12 rounded-xl flex items-center justify-center mr-3 shadow-lg"
          style={{
            background: `linear-gradient(135deg, ${colorValue}, ${colorValue}aa)`
          }}
        >
          {icon}
        </motion.div>
        <h2
          className="text-2xl font-bold"
          style={{
            color: colorValue,
            textShadow: `0 0 20px ${colorValue}60`
          }}
        >
          {title}
        </h2>
      </div>

      {/* Features list with stagger animation and hover reveal */}
      <ul className="space-y-3 relative" style={{ transform: 'translateZ(10px)' }}>
        {features.map((feature, index) => (
          <motion.li
            key={index}
            initial={{ opacity: 0, x: -10 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.3, delay: delay + 0.3 + (index * 0.08) }}
            whileHover={{
              x: 8,
              scale: 1.02,
              backgroundColor: `${colorValue}20`
            }}
            className="flex items-start text-sm text-gray-200 p-2 rounded-lg transition-colors"
          >
            <motion.span
              className="w-5 h-5 mr-3 mt-0.5 flex-shrink-0 rounded-full flex items-center justify-center"
              style={{
                background: colorValue,
                color: 'white'
              }}
              whileHover={{ rotate: 180 }}
              transition={{ duration: 0.3 }}
            >
              <FiCheck size={12} strokeWidth={3} />
            </motion.span>
            <span className="font-medium">{feature}</span>
          </motion.li>
        ))}
      </ul>

      {/* Decorative corner with animation */}
      <motion.div
        className="absolute top-0 right-0 w-20 h-20 rounded-bl-full pointer-events-none"
        style={{
          background: `radial-gradient(circle at top right, ${colorValue}, transparent)`
        }}
        initial={{ opacity: 0.3 }}
        whileHover={{ opacity: 0.6, scale: 1.2 }}
        transition={{ duration: 0.3 }}
      />

      {/* Bottom accent line */}
      <motion.div
        className="absolute bottom-0 left-0 right-0 h-1"
        style={{
          background: `linear-gradient(90deg, transparent, ${colorValue}, transparent)`
        }}
        initial={{ scaleX: 0 }}
        whileHover={{ scaleX: 1 }}
        transition={{ duration: 0.4 }}
      />
    </motion.div>
  );
};

interface AnimatedFeatureCardsProps {
  onOpenChat: () => void;
}

const AnimatedFeatureCards = ({ onOpenChat }: AnimatedFeatureCardsProps) => {
  const basicFeatures = [
    'Create tasks with title & description',
    'Set priority levels (High, Medium, Low)',
    'Add tags for organization',
    'Mark tasks as complete',
    'Delete unwanted tasks',
    'Basic task editing'
  ];

  const intermediateFeatures = [
    'Search tasks by title/description',
    'Filter by status, priority, tags',
    'Sort by date, priority, title',
    'Bulk operations on multiple tasks',
    'Task export (CSV, PDF, Print)',
    'Quick task actions'
  ];

  const advancedFeatures = [
    'AI-powered ChatAgent assistant',
    'Voice commands & responses',
    'Multi-language support (EN, UR, Roman)',
    'Natural language task creation',
    'Google search integration',
    'Smart conversation history'
  ];

  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
      {/* Basic Features Card */}
      <FeatureCard
        title="Basic"
        icon={<FiStar className="text-white" />}
        color="bg-green-500"
        features={basicFeatures}
        delay={0}
      />

      {/* Intermediate Features Card */}
      <FeatureCard
        title="Intermediate"
        icon={<FiLayers className="text-white" />}
        color="bg-yellow-500"
        features={intermediateFeatures}
        delay={0.2}
      />

      {/* Advanced Features Card */}
      <FeatureCard
        title="Advanced"
        icon={<FiZap className="text-white" />}
        color="bg-red-500"
        features={advancedFeatures}
        delay={0.4}
      />
    </div>
  );
};

// Stats Card Component for additional dashboard enhancement
interface StatsCardProps {
  title: string;
  value: string | number;
  icon: React.ReactNode;
  color: string;
  trend?: string;
}

const StatsCard = ({ title, value, icon, color, trend }: StatsCardProps) => {
  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.9 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ duration: 0.3 }}
      whileHover={{ scale: 1.02, y: -5 }}
      className="bg-gray-800/50 backdrop-blur-sm rounded-xl p-4 border border-gray-700"
    >
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm text-gray-400">{title}</p>
          <p className="text-2xl font-bold text-white mt-1">{value}</p>
          {trend && (
            <p className="text-xs text-green-400 mt-1">{trend}</p>
          )}
        </div>
        <div className={`w-12 h-12 rounded-lg ${color} flex items-center justify-center`}>
          {icon}
        </div>
      </div>
    </motion.div>
  );
};

export { AnimatedFeatureCards, StatsCard, FeatureCard };
export default AnimatedFeatureCards;
