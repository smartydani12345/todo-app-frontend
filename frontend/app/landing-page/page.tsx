'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { motion } from 'framer-motion';
import { FiX, FiChevronRight, FiCheck, FiStar, FiClock, FiUsers, FiBarChart2, FiRefreshCw, FiGlobe, FiBook, FiPlay } from 'react-icons/fi';

// Animation wrapper component to handle hydration issues
const AnimatedBackgroundElement = ({ index }: { index: number }) => {
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  // Pre-calculate positions on the server side to ensure consistency
  // Using a deterministic approach based on the index to ensure consistency
  const baseTop = (index * 137.508) % 100; // Golden angle approximation for distribution
  const baseLeft = (index * 232.631) % 100; // Another irrational number for distribution
  const baseWidth = 50 + (index * 7) % 201; // Between 50 and 251
  const baseHeight = 50 + (index * 11) % 201; // Between 50 and 251

  if (!mounted) {
    // Render a static element during SSR to prevent hydration mismatch
    return (
      <div 
        className="absolute rounded-full bg-gradient-to-r from-blue-500/10 to-purple-500/10"
        style={{
          top: `${baseTop}%`,
          left: `${baseLeft}%`,
          width: `${baseWidth}px`,
          height: `${baseHeight}px`,
        }}
      />
    );
  }

  // Render animated element on client
  return (
    <motion.div
      key={index}
      className="absolute rounded-full bg-gradient-to-r from-blue-500/10 to-purple-500/10"
      style={{
        top: `${baseTop}%`,
        left: `${baseLeft}%`,
        width: `${baseWidth}px`,
        height: `${baseHeight}px`,
      }}
      animate={{
        x: [0, (index % 2 === 0 ? 1 : -1) * (50 + index % 51)],
        y: [0, (index % 3 === 0 ? 1 : -1) * (30 + index % 41)],
      }}
      transition={{
        duration: 10 + (index % 11),
        repeat: Infinity,
        repeatType: "reverse",
        ease: "easeInOut"
      }}
    />
  );
};

const LandingPage = () => {
  const [showFeaturesModal, setShowFeaturesModal] = useState(false);
  const [showTutorial, setShowTutorial] = useState(false);
  const [tutorialStep, setTutorialStep] = useState(0);
  const [isMounted, setIsMounted] = useState(false);

  // Initialize client-side only features
  useEffect(() => {
    setIsMounted(true);
  }, []);

  const features = [
    {
      icon: <FiStar className="w-6 h-6" />,
      title: "AI Task Assistant",
      description: "Intelligent task suggestions and prioritization powered by machine learning"
    },
    {
      icon: <FiClock className="w-6 h-6" />,
      title: "Smart Scheduling",
      description: "Automatically schedule tasks based on your availability and priorities"
    },
    {
      icon: <FiUsers className="w-6 h-6" />,
      title: "Team Collaboration",
      description: "Seamlessly collaborate with team members on shared projects"
    },
    {
      icon: <FiBarChart2 className="w-6 h-6" />,
      title: "Advanced Analytics",
      description: "Gain insights into your productivity patterns and trends"
    },
    {
      icon: <FiRefreshCw className="w-6 h-6" />,
      title: "Automated Workflows",
      description: "Set up automated task sequences to streamline your workflow"
    },
    {
      icon: <FiGlobe className="w-6 h-6" />,
      title: "Cross-Platform Sync",
      description: "Access your tasks from any device with real-time synchronization"
    }
  ];

  const tutorialSteps = [
    {
      title: "Creating Tasks",
      description: "Click the 'Add Task' button to create a new task. Enter a title and description, set priority and tags.",
      icon: <FiStar className="w-8 h-8" />
    },
    {
      title: "Setting Priorities",
      description: "Choose from High, Medium, or Low priority to organize your tasks effectively.",
      icon: <FiCheck className="w-8 h-8" />
    },
    {
      title: "Using Tags",
      description: "Add custom tags to categorize your tasks for better organization and filtering.",
      icon: <FiStar className="w-8 h-8" />
    },
    {
      title: "Dashboard Navigation",
      description: "Use the sidebar to navigate between different views and sections of the app.",
      icon: <FiStar className="w-8 h-8" />
    },
    {
      title: "Collaboration Features",
      description: "Share tasks with team members and assign responsibilities directly.",
      icon: <FiUsers className="w-8 h-8" />
    }
  ];

  // Render placeholder during SSR to prevent hydration mismatch
  if (!isMounted) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900 text-white">
        {/* Static navbar during SSR */}
        <nav className="sticky top-0 z-50 bg-gray-900/80 backdrop-blur-sm border-b border-gray-800">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex items-center justify-between h-16">
              <div className="flex items-center">
                <div className="text-xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-blue-400 to-purple-500">
                  TODO EVOLUTION
                </div>
              </div>
              <div className="flex items-center space-x-4">
                <Link href="/login">
                  <button className="px-4 py-2 rounded-lg bg-gradient-to-r from-blue-500 to-indigo-600 transition-all duration-300">
                    Login
                  </button>
                </Link>
                <Link href="/register">
                  <button className="px-4 py-2 rounded-lg bg-gradient-to-r from-purple-500 to-pink-600 transition-all duration-300">
                    Register
                  </button>
                </Link>
              </div>
            </div>
          </div>
        </nav>

        {/* Static hero section during SSR */}
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20 md:py-28">
          <div className="text-center">
            <h1 className="text-3xl md:text-5xl font-extrabold tracking-tight">
              <span className="block">This is not only a TODO-app,</span>
              <span className="block mt-2 bg-clip-text text-transparent bg-gradient-to-r from-blue-400 to-purple-500">
                this is the future. Meet and evolve your workflow over the horizon of productivity.
              </span>
            </h1>

            <p className="mt-6 max-w-3xl mx-auto text-lg md:text-xl text-gray-300">
              Experience the next evolution in task management. Our platform transforms how you organize, prioritize, and accomplish your goals.
              With AI-powered insights and intuitive design, elevate your productivity to unprecedented levels.
            </p>

            <div className="mt-10 flex flex-col sm:flex-row justify-center gap-4">
              <button
                className="px-8 py-3 rounded-lg bg-gradient-to-r from-blue-500 to-indigo-600 transition-all duration-300 flex items-center justify-center"
              >
                Get Explore
              </button>

              <button
                className="px-8 py-3 rounded-lg bg-gradient-to-r from-purple-500 to-pink-600 transition-all duration-300 flex items-center justify-center"
              >
                Experienced
              </button>
            </div>
          </div>
        </div>

        {/* Static background elements during SSR */}
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
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900 text-white">
      {/* Navbar */}
      <nav className="sticky top-0 z-50 bg-gray-900/80 backdrop-blur-sm border-b border-gray-800">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center">
              <motion.div
                className="text-xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-blue-400 to-purple-500"
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ duration: 0.5 }}
              >
                TODO EVOLUTION
              </motion.div>
            </div>
            <div className="flex items-center space-x-4">
              <Link href="/login">
                <motion.button
                  className="px-4 py-2 rounded-lg bg-gradient-to-r from-blue-500 to-indigo-600 hover:from-blue-600 hover:to-indigo-700 transition-all duration-300"
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                >
                  Login
                </motion.button>
              </Link>
              <Link href="/register">
                <motion.button
                  className="px-4 py-2 rounded-lg bg-gradient-to-r from-purple-500 to-pink-600 hover:from-purple-600 hover:to-pink-700 transition-all duration-300"
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                >
                  Register
                </motion.button>
              </Link>
            </div>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <div className="relative overflow-hidden">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20 md:py-28">
          <div className="text-center">
            <motion.h1
              className="text-3xl md:text-5xl font-extrabold tracking-tight"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.7 }}
            >
              <span className="block">This is not only a TODO-app,</span>
              <span className="block mt-2 bg-clip-text text-transparent bg-gradient-to-r from-blue-400 to-purple-500">
                this is the future. Meet and evolve your workflow over the horizon of productivity.
              </span>
            </motion.h1>

            <motion.p
              className="mt-6 max-w-3xl mx-auto text-lg md:text-xl text-gray-300"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.7, delay: 0.2 }}
            >
              Experience the next evolution in task management. Our platform transforms how you organize, prioritize, and accomplish your goals.
              With AI-powered insights and intuitive design, elevate your productivity to unprecedented levels.
            </motion.p>

            <motion.div
              className="mt-10 flex flex-col sm:flex-row justify-center gap-4"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.7, delay: 0.4 }}
            >
              <motion.button
                className="px-8 py-3 rounded-lg bg-gradient-to-r from-blue-500 to-indigo-600 hover:from-blue-600 hover:to-indigo-700 transition-all duration-300 flex items-center justify-center"
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                onClick={() => setShowFeaturesModal(true)}
              >
                Get Explore <FiChevronRight className="ml-2" />
              </motion.button>

              <motion.button
                className="px-8 py-3 rounded-lg bg-gradient-to-r from-purple-500 to-pink-600 hover:from-purple-600 hover:to-pink-700 transition-all duration-300 flex items-center justify-center"
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                onClick={() => {
                  setTutorialStep(0);
                  setShowTutorial(true);
                }}
              >
                Experienced <FiPlay className="ml-2" />
              </motion.button>
            </motion.div>
          </div>
        </div>

        {/* Animated Background Elements */}
        <div className="absolute inset-0 overflow-hidden -z-10">
          {[...Array(20)].map((_, i) => (
            <AnimatedBackgroundElement key={i} index={i} />
          ))}
        </div>
      </div>

      {/* Features Modal */}
      {showFeaturesModal && (
        <div className="fixed inset-0 bg-black/80 backdrop-blur-sm z-50 flex items-center justify-center p-4">
          <motion.div
            className="bg-gray-800 rounded-xl max-w-4xl w-full max-h-[90vh] overflow-y-auto p-6"
            initial={{ opacity: 0, scale: 0.8 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ type: "spring", damping: 20 }}
          >
            <div className="flex justify-between items-center mb-6">
              <h2 className="text-2xl font-bold">App Features</h2>
              <button
                onClick={() => setShowFeaturesModal(false)}
                className="p-2 rounded-full hover:bg-gray-700"
              >
                <FiX className="w-5 h-5" />
              </button>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {features.map((feature, index) => (
                <motion.div
                  key={index}
                  className="bg-gray-900/50 p-6 rounded-lg border border-gray-700"
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: index * 0.1 }}
                >
                  <div className="text-blue-400 mb-3">{feature.icon}</div>
                  <h3 className="text-lg font-semibold mb-2">{feature.title}</h3>
                  <p className="text-gray-400">{feature.description}</p>
                </motion.div>
              ))}
            </div>
          </motion.div>
        </div>
      )}

      {/* Tutorial Modal */}
      {showTutorial && (
        <div className="fixed inset-0 bg-black/80 backdrop-blur-sm z-50 flex items-center justify-center p-4">
          <motion.div
            className="bg-gray-800 rounded-xl max-w-2xl w-full max-h-[90vh] overflow-y-auto p-6"
            initial={{ opacity: 0, scale: 0.8 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ type: "spring", damping: 20 }}
          >
            <div className="flex justify-between items-center mb-6">
              <h2 className="text-2xl font-bold">Hands-On Tutorial</h2>
              <button
                onClick={() => setShowTutorial(false)}
                className="p-2 rounded-full hover:bg-gray-700"
              >
                <FiX className="w-5 h-5" />
              </button>
            </div>

            <div className="mb-6">
              <div className="flex justify-between items-center mb-4">
                <h3 className="text-xl font-semibold">{tutorialSteps[tutorialStep].title}</h3>
                <span className="text-gray-400">{tutorialStep + 1} of {tutorialSteps.length}</span>
              </div>
              <div className="flex items-center justify-center mb-4">
                {tutorialSteps[tutorialStep].icon}
              </div>
              <p className="text-gray-300">{tutorialSteps[tutorialStep].description}</p>
            </div>

            <div className="flex justify-between">
              <button
                className={`px-4 py-2 rounded-lg ${tutorialStep === 0 ? 'bg-gray-700 cursor-not-allowed' : 'bg-gray-700 hover:bg-gray-600'}`}
                onClick={() => tutorialStep > 0 && setTutorialStep(tutorialStep - 1)}
                disabled={tutorialStep === 0}
              >
                Previous
              </button>

              <button
                className="px-4 py-2 rounded-lg bg-gradient-to-r from-blue-500 to-indigo-600 hover:from-blue-600 hover:to-indigo-700"
                onClick={() => {
                  if (tutorialStep < tutorialSteps.length - 1) {
                    setTutorialStep(tutorialStep + 1);
                  } else {
                    setShowTutorial(false);
                  }
                }}
              >
                {tutorialStep < tutorialSteps.length - 1 ? 'Next' : 'Finish'}
              </button>
            </div>

            <div className="mt-6 flex justify-center space-x-2">
              {tutorialSteps.map((_, index) => (
                <button
                  key={index}
                  className={`w-3 h-3 rounded-full ${index === tutorialStep ? 'bg-blue-500' : 'bg-gray-600'}`}
                  onClick={() => setTutorialStep(index)}
                />
              ))}
            </div>
          </motion.div>
        </div>
      )}
    </div>
  );
};

export default LandingPage;