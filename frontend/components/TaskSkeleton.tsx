import React from 'react';
import { motion } from 'framer-motion';

export const TaskSkeleton: React.FC = () => {
  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      className="rounded-lg border shadow-sm overflow-hidden bg-white dark:bg-gray-800"
    >
      <div className="p-5">
        <div className="animate-pulse">
          <div className="h-4 bg-gray-200 dark:bg-gray-700 rounded w-3/4 mb-2"></div>
          <div className="h-3 bg-gray-200 dark:bg-gray-700 rounded w-1/2 mb-4"></div>

          <div className="flex flex-wrap gap-2 mb-4">
            <div className="h-6 bg-gray-200 dark:bg-gray-700 rounded-full w-16"></div>
            <div className="h-6 bg-gray-200 dark:bg-gray-700 rounded-full w-20"></div>
          </div>

          <div className="h-8 bg-gray-200 dark:bg-gray-700 rounded w-full mt-4"></div>
        </div>
      </div>
    </motion.div>
  );
};