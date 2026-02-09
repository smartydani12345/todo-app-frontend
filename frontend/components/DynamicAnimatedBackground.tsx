// components/DynamicAnimatedBackground.tsx
'use client';

import { motion } from 'framer-motion';

interface AnimatedBackgroundProps {
  count?: number;
}

const DynamicAnimatedBackground = ({ count = 20 }: AnimatedBackgroundProps) => {
  return (
    <>
      {[...Array(count)].map((_, i) => (
        <motion.div
          key={i}
          className="absolute rounded-full bg-gradient-to-r from-blue-500/10 to-purple-500/10"
          style={{
            top: `${(i * 137.508) % 100}%`,
            left: `${(i * 232.631) % 100}%`,
            width: `${50 + (i * 7) % 201}px`,
            height: `${50 + (i * 11) % 201}px`,
          }}
          animate={{
            x: [0, (i % 2 === 0 ? 1 : -1) * (50 + i % 51)],
            y: [0, (i % 3 === 0 ? 1 : -1) * (30 + i % 41)],
          }}
          transition={{
            duration: 10 + (i % 11),
            repeat: Infinity,
            repeatType: "reverse",
            ease: "easeInOut"
          }}
        />
      ))}
    </>
  );
};

export default DynamicAnimatedBackground;