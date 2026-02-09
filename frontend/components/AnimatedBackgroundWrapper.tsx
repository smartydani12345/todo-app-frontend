// components/AnimatedBackgroundWrapper.tsx
import dynamic from 'next/dynamic';

// Dynamically import the animated background with SSR disabled
const DynamicAnimatedBackground = dynamic(
  () => import('./DynamicAnimatedBackground'),
  { 
    ssr: false,
    loading: () => (
      // Render static elements during loading/ssr
      <div className="absolute inset-0 overflow-hidden -z-10">
        {[...Array(20)].map((_, i) => (
          <div
            key={i}
            className="absolute rounded-full bg-gradient-to-r from-blue-500/10 to-purple-500/10"
            style={{
              top: `${(i * 137.508) % 100}%`,
              left: `${(i * 232.631) % 100}%`,
              width: `${50 + (i * 7) % 201}px`,
              height: `${50 + (i * 11) % 201}px`,
            }}
          />
        ))}
      </div>
    )
  }
);

export default DynamicAnimatedBackground;