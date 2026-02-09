'use client';

import { useState, useEffect, useRef } from 'react';
import { useRouter } from 'next/navigation';
import apiClient from '../../lib/api-client';
import { isAuthenticated } from '../../lib/tokenUtils';
import toast from 'react-hot-toast';
import { FiPlus, FiEdit, FiTrash2, FiX, FiCheck, FiCalendar, FiTag, FiFilter, FiSearch, FiDownload, FiPrinter, FiSettings, FiChevronDown, FiChevronUp, FiInfo, FiLogOut } from 'react-icons/fi';

interface Task {
  id: number;
  title: string;
  description?: string;
  completed: boolean;
  priority: 'high' | 'medium' | 'low';
  tags: string;
  user_id: string;
  due_date: string | null;
  created_at: string;
  updated_at: string;
}

const Phase2Dashboard = () => {
  const router = useRouter();
  
  // Basic Essentials State
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [newTask, setNewTask] = useState({ title: '', description: '', priority: 'medium' as 'high' | 'medium' | 'low', tags: '' });
  const [editingTask, setEditingTask] = useState<Task | null>(null);
  
  // Intermediate Tools State
  const [searchQuery, setSearchQuery] = useState('');
  const [filterStatus, setFilterStatus] = useState<string>('all');
  const [filterPriority, setFilterPriority] = useState<string>('all');
  const [filterTag, setFilterTag] = useState<string>('');
  const [sortBy, setSortBy] = useState<string>('created_at');
  const [sortOrder, setSortOrder] = useState<string>('desc');
  const [selectedTasks, setSelectedTasks] = useState<number[]>([]);
  
  // Advanced Systems State
  const [showBulkActions, setShowBulkActions] = useState(false);
  const [showExportOptions, setShowExportOptions] = useState(false);
  const [showAnalytics, setShowAnalytics] = useState(false);
  const [showAutomationRules, setShowAutomationRules] = useState(false);
  const [recurringTask, setRecurringTask] = useState({ enabled: false, interval: 'daily' });
  const [taskDependencies, setTaskDependencies] = useState<{[key: number]: number[]}>({});
  
  // Refs for double-click to edit
  const taskRefs = useRef<{[key: number]: HTMLDivElement | null}>({});

  // Check authentication and load tasks
  useEffect(() => {
    if (!isAuthenticated()) {
      router.push('/login');
      return;
    }

    loadTasks();
  }, [router, searchQuery, filterStatus, filterPriority, filterTag, sortBy, sortOrder]);

  const loadTasks = async () => {
    setLoading(true);
    try {
      // Build query parameters for filtering, searching, and sorting
      const params = new URLSearchParams();

      if (searchQuery) params.append('search', searchQuery);
      if (filterStatus !== 'all') params.append('status', filterStatus);
      if (filterPriority !== 'all') params.append('priority', filterPriority);
      if (filterTag) params.append('tag', filterTag);
      params.append('sort_by', sortBy);
      params.append('sort_order', sortOrder);

      const response = await apiClient.get(`/tasks/?${params.toString()}`);
      setTasks(response.data);
    } catch (err: any) {
      if (err.response?.status === 401) {
        // Token might be expired, remove it and redirect to login
        localStorage.removeItem('access_token');
        router.push('/login');
      } else {
        console.error(err);
        setError('Failed to load tasks');
        toast.error('Failed to load tasks');
      }
    } finally {
      setLoading(false);
    }
  };

  // Basic Essentials Functions
  const handleAddTask = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      // Prepare form data to match backend expectations (form-data)
      const formData = new FormData();
      formData.append('title', newTask.title);
      formData.append('description', newTask.description);
      formData.append('priority', newTask.priority);
      formData.append('tags', newTask.tags);

      const response = await apiClient.post('/tasks/', formData);

      setTasks([...tasks, response.data]);
      setNewTask({ title: '', description: '', priority: 'medium', tags: '' });
      toast.success('Task added successfully!');
    } catch (err: any) {
      console.error(err);
      setError('Failed to add task');
      toast.error('Failed to add task');
    }
  };

  const handleUpdateTask = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!editingTask) return;

    try {
      // Prepare form data to match backend expectations (form-data)
      const formData = new FormData();
      formData.append('title', editingTask.title);
      formData.append('description', editingTask.description || '');
      formData.append('completed', editingTask.completed.toString());
      formData.append('priority', editingTask.priority);
      formData.append('tags', editingTask.tags || '');

      const response = await apiClient.put(`/tasks/${editingTask.id}`, formData);

      // Update the task in the state with the response data
      setTasks(tasks.map(t => t.id === editingTask.id ? response.data : t));
      setEditingTask(null);
      toast.success('Task updated successfully!');
    } catch (err: any) {
      console.error(err);
      setError('Failed to update task');
      toast.error('Failed to update task');
    }
  };

  const handleDeleteTask = async (taskId: number) => {
    if (!window.confirm('Are you sure you want to delete this task?')) {
      return; // User cancelled the deletion
    }

    try {
      await apiClient.delete(`/tasks/${taskId}`);
      setTasks(tasks.filter(task => task.id !== taskId));
      toast.success('Task deleted successfully!');
    } catch (err: any) {
      console.error(err);
      setError('Failed to delete task');
      toast.error('Failed to delete task');
    }
  };

  const handleToggleComplete = async (taskId: number) => {
    const task = tasks.find(t => t.id === taskId);
    if (!task) return;

    try {
      // Prepare form data to match backend expectations (form-data)
      const formData = new FormData();
      formData.append('completed', (!task.completed).toString());

      const response = await apiClient.patch(`/tasks/${taskId}/complete`, formData);

      // Update the task in the state with the response data
      setTasks(tasks.map(t => t.id === taskId ? response.data : t));
      toast.success(`Task marked as ${task.completed ? 'incomplete' : 'complete'}!`);
    } catch (err: any) {
      console.error(err);
      setError('Failed to update task');
      toast.error('Failed to update task');
    }
  };

  // Intermediate Tools Functions
  const handleSearchChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setSearchQuery(e.target.value);
  };

  const handleSelectTask = (taskId: number) => {
    if (selectedTasks.includes(taskId)) {
      setSelectedTasks(selectedTasks.filter(id => id !== taskId));
    } else {
      setSelectedTasks([...selectedTasks, taskId]);
    }
  };

  const handleSelectAllTasks = () => {
    if (selectedTasks.length === filteredAndSortedTasks.length) {
      setSelectedTasks([]);
    } else {
      setSelectedTasks(filteredAndSortedTasks.map(task => task.id));
    }
  };

  // Advanced Systems Functions
  const handleBulkDelete = async () => {
    if (selectedTasks.length === 0) return;
    
    if (!window.confirm(`Are you sure you want to delete ${selectedTasks.length} task(s)?`)) {
      return;
    }

    try {
      // Delete all selected tasks
      for (const taskId of selectedTasks) {
        await apiClient.delete(`/tasks/${taskId}`);
      }
      
      setTasks(tasks.filter(task => !selectedTasks.includes(task.id)));
      setSelectedTasks([]);
      toast.success(`${selectedTasks.length} task(s) deleted successfully!`);
    } catch (err: any) {
      console.error(err);
      setError('Failed to delete some tasks');
      toast.error('Failed to delete some tasks');
    }
  };

  const handleBulkComplete = async () => {
    if (selectedTasks.length === 0) return;

    try {
      // Mark all selected tasks as complete
      for (const taskId of selectedTasks) {
        const formData = new FormData();
        formData.append('completed', 'true');
        await apiClient.patch(`/tasks/${taskId}/complete`, formData);
      }
      
      setTasks(tasks.map(task => 
        selectedTasks.includes(task.id) ? { ...task, completed: true } : task
      ));
      setSelectedTasks([]);
      toast.success(`${selectedTasks.length} task(s) marked as complete!`);
    } catch (err: any) {
      console.error(err);
      setError('Failed to update some tasks');
      toast.error('Failed to update some tasks');
    }
  };

  const handleExport = (format: 'csv' | 'pdf' | 'print') => {
    if (format === 'print') {
      window.print();
      return;
    }
    
    // For CSV and PDF, we would typically make an API call to generate the file
    // For now, we'll just show a toast notification
    toast.success(`Exporting tasks as ${format.toUpperCase()}...`);
    setShowExportOptions(false);
  };

  // Filter and sort tasks based on state
  const filteredAndSortedTasks = tasks
    .filter(task => {
      const matchesSearch = !searchQuery ||
        task.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
        (task.description && task.description.toLowerCase().includes(searchQuery.toLowerCase()));
      const matchesStatus = filterStatus === 'all' ||
        (filterStatus === 'completed' && task.completed) ||
        (filterStatus === 'incomplete' && !task.completed);
      const matchesPriority = filterPriority === 'all' || task.priority === filterPriority;
      const matchesTag = !filterTag ||
        (task.tags && task.tags.toLowerCase().includes(filterTag.toLowerCase()));

      return matchesSearch && matchesStatus && matchesPriority && matchesTag;
    })
    .sort((a, b) => {
      let aValue: string | number | boolean = a[sortBy as keyof Task];
      let bValue: string | number | boolean = b[sortBy as keyof Task];

      // Handle date comparison
      if (sortBy === 'created_at' || sortBy === 'due_date') {
        aValue = new Date(aValue as string).getTime;
        bValue = new Date(bValue as string).getTime;
      }

      if (sortOrder === 'asc') {
        return aValue > bValue ? 1 : -1;
      } else {
        return aValue < bValue ? 1 : -1;
      }
    });

  const handleLogout = () => {
    localStorage.removeItem('access_token');
    router.push('/login');
  };

  // Double-click to edit functionality
  const handleDoubleClick = (task: Task) => {
    setEditingTask(task);
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mx-auto"></div>
          <p className="mt-4 text-lg text-gray-300">Loading tasks...</p>
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
              <h1 className="text-xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-blue-400 to-purple-500">
                TODO EVOLUTION
              </h1>
            </div>
            <div className="flex items-center space-x-4">
              <button
                onClick={handleLogout}
                className="px-4 py-2 rounded-lg bg-gradient-to-r from-red-500 to-red-600 hover:from-red-600 hover:to-red-700 transition-all duration-300 flex items-center"
              >
                <FiLogOut className="mr-2" /> Logout
              </button>
            </div>
          </div>
        </div>
      </nav>

      <div className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        <div className="px-4 py-6 sm:px-0">
          {/* Dashboard Header */}
          <div className="mb-8">
            <h1 className="text-3xl font-bold text-white">Task Dashboard</h1>
            <p className="text-gray-400 mt-2">Manage your tasks with our advanced productivity tools</p>
          </div>

          {/* Three Feature Sections */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
            {/* Basic Box */}
            <div className="bg-gray-800/50 backdrop-blur-sm rounded-xl p-6 border border-gray-700">
              <div className="flex items-center mb-4">
                <div className="w-3 h-3 bg-green-500 rounded-full mr-2"></div>
                <h2 className="text-xl font-bold text-green-400">🟢 Basic</h2>
              </div>
              
              <form onSubmit={editingTask ? handleUpdateTask : handleAddTask} className="space-y-4">
                <div>
                  <label htmlFor="title" className="block text-sm font-medium text-gray-300 mb-1">
                    Task Title *
                  </label>
                  <input
                    type="text"
                    name="title"
                    id="title"
                    required
                    value={editingTask ? editingTask.title : newTask.title}
                    onChange={(e) => editingTask
                      ? setEditingTask({...editingTask, title: e.target.value})
                      : setNewTask({...newTask, title: e.target.value})}
                    className="w-full rounded-lg border border-gray-600 bg-gray-700 py-2 px-3 text-white focus:border-blue-500 focus:ring-blue-500 sm:text-sm"
                    placeholder="Enter task title"
                  />
                </div>

                <div>
                  <label htmlFor="description" className="block text-sm font-medium text-gray-300 mb-1">
                    Description
                  </label>
                  <textarea
                    id="description"
                    name="description"
                    rows={2}
                    value={editingTask ? editingTask.description || '' : newTask.description}
                    onChange={(e) => editingTask
                      ? setEditingTask({...editingTask, description: e.target.value})
                      : setNewTask({...newTask, description: e.target.value})}
                    className="w-full rounded-lg border border-gray-600 bg-gray-700 py-2 px-3 text-white focus:border-blue-500 focus:ring-blue-500 sm:text-sm"
                    placeholder="Task description"
                  />
                </div>

                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                  <div>
                    <label htmlFor="priority" className="block text-sm font-medium text-gray-300 mb-1">
                      Priority
                    </label>
                    <select
                      id="priority"
                      name="priority"
                      value={editingTask ? editingTask.priority : newTask.priority}
                      onChange={(e) => editingTask
                        ? setEditingTask({...editingTask, priority: e.target.value as 'high' | 'medium' | 'low'})
                        : setNewTask({...newTask, priority: e.target.value as 'high' | 'medium' | 'low'})}
                      className="w-full rounded-lg border border-gray-600 bg-gray-700 py-2 px-3 text-white focus:border-blue-500 focus:ring-blue-500 sm:text-sm"
                    >
                      <option value="low">Low</option>
                      <option value="medium">Medium</option>
                      <option value="high">High</option>
                    </select>
                  </div>

                  <div>
                    <label htmlFor="tags" className="block text-sm font-medium text-gray-300 mb-1">
                      Tags
                    </label>
                    <input
                      type="text"
                      name="tags"
                      id="tags"
                      value={editingTask ? editingTask.tags || '' : newTask.tags}
                      onChange={(e) => editingTask
                        ? setEditingTask({...editingTask, tags: e.target.value})
                        : setNewTask({...newTask, tags: e.target.value})}
                      className="w-full rounded-lg border border-gray-600 bg-gray-700 py-2 px-3 text-white focus:border-blue-500 focus:ring-blue-500 sm:text-sm"
                      placeholder="work, personal"
                    />
                  </div>
                </div>

                <div className="flex flex-col sm:flex-row justify-end space-y-2 sm:space-y-0 sm:space-x-3 pt-2">
                  {editingTask && (
                    <button
                      type="button"
                      onClick={() => setEditingTask(null)}
                      className="px-4 py-2 rounded-lg bg-gray-700 hover:bg-gray-600 text-white"
                    >
                      Exit Task
                    </button>
                  )}
                  <button
                    type="submit"
                    className="px-4 py-2 rounded-lg bg-blue-600 hover:bg-blue-700 text-white"
                  >
                    {editingTask ? 'Update Task' : 'Add Task'}
                  </button>
                </div>
              </form>
            </div>

            {/* Intermediate Box */}
            <div className="bg-gray-800/50 backdrop-blur-sm rounded-xl p-6 border border-gray-700">
              <div className="flex items-center mb-4">
                <div className="w-3 h-3 bg-yellow-500 rounded-full mr-2"></div>
                <h2 className="text-xl font-bold text-yellow-400">🟡 Intermediate</h2>
              </div>
              
              <div className="space-y-4">
                <div>
                  <label htmlFor="search" className="block text-sm font-medium text-gray-300 mb-1 flex items-center">
                    <FiSearch className="mr-2" /> Search Tasks
                  </label>
                  <input
                    type="text"
                    id="search"
                    value={searchQuery}
                    onChange={handleSearchChange}
                    className="w-full rounded-lg border border-gray-600 bg-gray-700 py-2 px-3 text-white focus:border-blue-500 focus:ring-blue-500 sm:text-sm"
                    placeholder="Search by title or description..."
                  />
                </div>

                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                  <div>
                    <label htmlFor="status-filter" className="block text-sm font-medium text-gray-300 mb-1">
                      Status
                    </label>
                    <select
                      id="status-filter"
                      value={filterStatus}
                      onChange={(e) => setFilterStatus(e.target.value)}
                      className="w-full rounded-lg border border-gray-600 bg-gray-700 py-2 px-3 text-white focus:border-blue-500 focus:ring-blue-500 sm:text-sm"
                    >
                      <option value="all">All</option>
                      <option value="completed">Completed</option>
                      <option value="incomplete">Incomplete</option>
                    </select>
                  </div>

                  <div>
                    <label htmlFor="priority-filter" className="block text-sm font-medium text-gray-300 mb-1">
                      Priority
                    </label>
                    <select
                      id="priority-filter"
                      value={filterPriority}
                      onChange={(e) => setFilterPriority(e.target.value)}
                      className="w-full rounded-lg border border-gray-600 bg-gray-700 py-2 px-3 text-white focus:border-blue-500 focus:ring-blue-500 sm:text-sm"
                    >
                      <option value="all">All</option>
                      <option value="high">High</option>
                      <option value="medium">Medium</option>
                      <option value="low">Low</option>
                    </select>
                  </div>
                </div>

                <div>
                  <label htmlFor="tag-filter" className="block text-sm font-medium text-gray-300 mb-1">
                    Filter by Tag
                  </label>
                  <input
                    type="text"
                    id="tag-filter"
                    value={filterTag}
                    onChange={(e) => setFilterTag(e.target.value)}
                    className="w-full rounded-lg border border-gray-600 bg-gray-700 py-2 px-3 text-white focus:border-blue-500 focus:ring-blue-500 sm:text-sm"
                    placeholder="Filter by tag..."
                  />
                </div>

                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                  <div>
                    <label htmlFor="sort-by" className="block text-sm font-medium text-gray-300 mb-1">
                      Sort By
                    </label>
                    <select
                      id="sort-by"
                      value={sortBy}
                      onChange={(e) => setSortBy(e.target.value)}
                      className="w-full rounded-lg border border-gray-600 bg-gray-700 py-2 px-3 text-white focus:border-blue-500 focus:ring-blue-500 sm:text-sm"
                    >
                      <option value="created_at">Created Date</option>
                      <option value="due_date">Due Date</option>
                      <option value="priority">Priority</option>
                      <option value="title">Title</option>
                    </select>
                  </div>

                  <div>
                    <label htmlFor="sort-order" className="block text-sm font-medium text-gray-300 mb-1">
                      Order
                    </label>
                    <select
                      id="sort-order"
                      value={sortOrder}
                      onChange={(e) => setSortOrder(e.target.value)}
                      className="w-full rounded-lg border border-gray-600 bg-gray-700 py-2 px-3 text-white focus:border-blue-500 focus:ring-blue-500 sm:text-sm"
                    >
                      <option value="asc">Ascending</option>
                      <option value="desc">Descending</option>
                    </select>
                  </div>
                </div>
              </div>
            </div>

            {/* Advanced Box */}
            <div className="bg-gray-800/50 backdrop-blur-sm rounded-xl p-6 border border-gray-700">
              <div className="flex items-center mb-4">
                <div className="w-3 h-3 bg-red-500 rounded-full mr-2"></div>
                <h2 className="text-xl font-bold text-red-400">🔴 Advanced</h2>
              </div>
              
              <div className="space-y-4">
                <div className="flex flex-col space-y-3">
                  <button
                    onClick={() => setShowBulkActions(!showBulkActions)}
                    className="w-full flex items-center justify-between px-4 py-2 rounded-lg bg-gray-700 hover:bg-gray-600 text-white"
                  >
                    <span>Bulk Operations</span>
                    {showBulkActions ? <FiChevronUp /> : <FiChevronDown />}
                  </button>
                  
                  {showBulkActions && (
                    <div className="pl-4 border-l-2 border-gray-600 space-y-2">
                      <button
                        onClick={handleBulkComplete}
                        disabled={selectedTasks.length === 0}
                        className={`w-full text-left px-3 py-1 rounded-lg ${selectedTasks.length === 0 ? 'bg-gray-800 text-gray-500' : 'bg-green-700 hover:bg-green-600 text-white'}`}
                      >
                        Mark Selected as Complete
                      </button>
                      <button
                        onClick={handleBulkDelete}
                        disabled={selectedTasks.length === 0}
                        className={`w-full text-left px-3 py-1 rounded-lg ${selectedTasks.length === 0 ? 'bg-gray-800 text-gray-500' : 'bg-red-700 hover:bg-red-600 text-white'}`}
                      >
                        Delete Selected
                      </button>
                      <button
                        onClick={() => setSelectedTasks([])}
                        className="w-full text-left px-3 py-1 rounded-lg bg-gray-700 hover:bg-gray-600 text-white"
                      >
                        Clear Selection
                      </button>
                    </div>
                  )}
                </div>

                <div className="flex flex-col space-y-3">
                  <button
                    onClick={() => setShowExportOptions(!showExportOptions)}
                    className="w-full flex items-center justify-between px-4 py-2 rounded-lg bg-gray-700 hover:bg-gray-600 text-white"
                  >
                    <span>Export Options</span>
                    {showExportOptions ? <FiChevronUp /> : <FiChevronDown />}
                  </button>
                  
                  {showExportOptions && (
                    <div className="pl-4 border-l-2 border-gray-600 space-y-2">
                      <button
                        onClick={() => handleExport('csv')}
                        className="w-full text-left px-3 py-1 rounded-lg bg-blue-700 hover:bg-blue-600 text-white"
                      >
                        Export as CSV
                      </button>
                      <button
                        onClick={() => handleExport('pdf')}
                        className="w-full text-left px-3 py-1 rounded-lg bg-red-700 hover:bg-red-600 text-white"
                      >
                        Export as PDF
                      </button>
                      <button
                        onClick={() => handleExport('print')}
                        className="w-full text-left px-3 py-1 rounded-lg bg-gray-700 hover:bg-gray-600 text-white"
                      >
                        Print Tasks
                      </button>
                    </div>
                  )}
                </div>

                <div className="flex flex-col space-y-3">
                  <button
                    onClick={() => setShowAnalytics(!showAnalytics)}
                    className="w-full flex items-center justify-between px-4 py-2 rounded-lg bg-gray-700 hover:bg-gray-600 text-white"
                  >
                    <span>Analytics & Insights</span>
                    {showAnalytics ? <FiChevronUp /> : <FiChevronDown />}
                  </button>
                  
                  {showAnalytics && (
                    <div className="pl-4 border-l-2 border-gray-600 space-y-2">
                      <div className="text-sm text-gray-300">
                        <p>Total Tasks: {tasks.length}</p>
                        <p>Completed: {tasks.filter(t => t.completed).length}</p>
                        <p>Pending: {tasks.filter(t => !t.completed).length}</p>
                        <p>High Priority: {tasks.filter(t => t.priority === 'high').length}</p>
                      </div>
                    </div>
                  )}
                </div>

                <div className="flex flex-col space-y-3">
                  <button
                    onClick={() => setShowAutomationRules(!showAutomationRules)}
                    className="w-full flex items-center justify-between px-4 py-2 rounded-lg bg-gray-700 hover:bg-gray-600 text-white"
                  >
                    <span>Automation Rules</span>
                    {showAutomationRules ? <FiChevronUp /> : <FiChevronDown />}
                  </button>
                  
                  {showAutomationRules && (
                    <div className="pl-4 border-l-2 border-gray-600 space-y-2">
                      <div className="text-sm text-gray-300">
                        <p>Set up recurring tasks, notifications, and workflows</p>
                        <div className="mt-2">
                          <label className="flex items-center">
                            <input
                              type="checkbox"
                              checked={recurringTask.enabled}
                              onChange={(e) => setRecurringTask({...recurringTask, enabled: e.target.checked})}
                              className="mr-2"
                            />
                            Enable Recurring Tasks
                          </label>
                          {recurringTask.enabled && (
                            <select
                              value={recurringTask.interval}
                              onChange={(e) => setRecurringTask({...recurringTask, interval: e.target.value})}
                              className="mt-2 w-full rounded-lg border border-gray-600 bg-gray-700 py-1 px-2 text-white text-sm"
                            >
                              <option value="daily">Daily</option>
                              <option value="weekly">Weekly</option>
                              <option value="monthly">Monthly</option>
                            </select>
                          )}
                        </div>
                      </div>
                    </div>
                  )}
                </div>
              </div>
            </div>
          </div>

          {error && (
            <div className="bg-red-900/50 border border-red-700 text-red-200 px-4 py-3 rounded mb-4" role="alert">
              {error}
            </div>
          )}

          {/* Task List */}
          <div className="bg-gray-800/50 backdrop-blur-sm rounded-xl border border-gray-700 overflow-hidden">
            <div className="px-4 py-3 flex items-center justify-between border-b border-gray-700">
              <div className="flex items-center">
                <input
                  type="checkbox"
                  checked={selectedTasks.length === filteredAndSortedTasks.length && filteredAndSortedTasks.length > 0}
                  onChange={handleSelectAllTasks}
                  className="h-4 w-4 text-blue-600 rounded"
                />
                <span className="ml-2 text-sm text-gray-300">
                  {selectedTasks.length > 0 
                    ? `${selectedTasks.length} selected` 
                    : `${filteredAndSortedTasks.length} tasks`}
                </span>
              </div>
              <div className="text-sm text-gray-400">
                Sorted by: {sortBy} ({sortOrder})
              </div>
            </div>
            
            <ul className="divide-y divide-gray-700">
              {filteredAndSortedTasks.map((task) => (
                <li 
                  key={task.id} 
                  ref={el => taskRefs.current[task.id] = el}
                  onDoubleClick={() => handleDoubleClick(task)}
                  className={`px-4 py-4 hover:bg-gray-700/50 transition-colors ${selectedTasks.includes(task.id) ? 'bg-gray-700/30' : ''}`}
                >
                  <div className="flex items-center">
                    <input
                      type="checkbox"
                      checked={selectedTasks.includes(task.id)}
                      onChange={() => handleSelectTask(task.id)}
                      className="h-4 w-4 text-blue-600 rounded mr-3"
                    />
                    
                    <input
                      type="checkbox"
                      checked={task.completed}
                      onChange={() => handleToggleComplete(task.id)}
                      className="h-4 w-4 text-blue-600 rounded mr-3"
                    />
                    
                    <div className="flex-1 min-w-0">
                      <p className={`text-sm font-medium truncate ${task.completed ? 'line-through text-gray-500' : 'text-white'}`}>
                        {task.title}
                      </p>
                      {task.description && (
                        <p className="text-sm text-gray-400 truncate">{task.description}</p>
                      )}
                      
                      <div className="mt-1 flex flex-wrap gap-2">
                        <span className={`inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium ${
                          task.priority === 'high' ? 'bg-red-900/50 text-red-300' :
                          task.priority === 'medium' ? 'bg-yellow-900/50 text-yellow-300' :
                          'bg-green-900/50 text-green-300'
                        }`}>
                          {task.priority}
                        </span>
                        
                        {task.tags && task.tags !== '[]' && (
                          <span className="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium bg-blue-900/50 text-blue-300">
                            <FiTag className="mr-1" /> {task.tags}
                          </span>
                        )}
                        
                        {task.due_date && (
                          <span className="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium bg-purple-900/50 text-purple-300">
                            <FiCalendar className="mr-1" /> {new Date(task.due_date).toLocaleDateString()}
                          </span>
                        )}
                      </div>
                    </div>
                    
                    <div className="flex space-x-2 ml-4">
                      <button
                        onClick={() => setEditingTask(task)}
                        className="p-2 rounded-lg hover:bg-gray-700 text-gray-400 hover:text-blue-400"
                        title="Edit task"
                      >
                        <FiEdit className="w-4 h-4" />
                      </button>
                      <button
                        onClick={() => handleDeleteTask(task.id)}
                        className="p-2 rounded-lg hover:bg-gray-700 text-gray-400 hover:text-red-400"
                        title="Delete task"
                      >
                        <FiTrash2 className="w-4 h-4" />
                      </button>
                    </div>
                  </div>
                </li>
              ))}
            </ul>
            
            {filteredAndSortedTasks.length === 0 && (
              <div className="text-center py-12">
                <p className="text-gray-500">
                  No tasks found. {tasks.length === 0 ? 'Add your first task!' : 'Try changing your filters.'}
                </p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Phase2Dashboard;