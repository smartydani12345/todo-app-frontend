import { Task, TaskFilters, TaskCreateRequest, TaskUpdateRequest } from '../lib/types';

describe('Task Types', () => {
  test('should define Task interface correctly', () => {
    const task: Task = {
      id: '123e4567-e89b-12d3-a456-426614174000',
      user_id: 'user123',
      title: 'Test Task',
      description: 'Test Description',
      completed: false,
      priority: 'medium',
      tags: ['work', 'important'],
      due_date: '2024-12-31T10:00:00Z',
      created_at: '2024-01-01T10:00:00Z',
      updated_at: '2024-01-01T10:00:00Z'
    };

    expect(task.id).toBe('123e4567-e89b-12d3-a456-426614174000');
    expect(task.user_id).toBe('user123');
    expect(task.title).toBe('Test Task');
    expect(task.description).toBe('Test Description');
    expect(task.completed).toBe(false);
    expect(task.priority).toBe('medium');
    expect(task.tags).toEqual(['work', 'important']);
    expect(task.due_date).toBe('2024-12-31T10:00:00Z');
    expect(task.created_at).toBe('2024-01-01T10:00:00Z');
    expect(task.updated_at).toBe('2024-01-01T10:00:00Z');
  });

  test('should define TaskFilters interface correctly', () => {
    const filters: TaskFilters = {
      status: 'completed',
      priority: 'high',
      tag: 'work',
      search: 'test'
    };

    expect(filters.status).toBe('completed');
    expect(filters.priority).toBe('high');
    expect(filters.tag).toBe('work');
    expect(filters.search).toBe('test');
  });

  test('should define TaskCreateRequest interface correctly', () => {
    const createRequest: TaskCreateRequest = {
      title: 'New Task',
      description: 'New Description',
      priority: 'high',
      tags: ['new', 'tag'],
      due_date: '2024-12-31T10:00:00Z',
      completed: false
    };

    expect(createRequest.title).toBe('New Task');
    expect(createRequest.description).toBe('New Description');
    expect(createRequest.priority).toBe('high');
    expect(createRequest.tags).toEqual(['new', 'tag']);
    expect(createRequest.due_date).toBe('2024-12-31T10:00:00Z');
    expect(createRequest.completed).toBe(false);
  });

  test('should define TaskUpdateRequest interface correctly', () => {
    const updateRequest: TaskUpdateRequest = {
      title: 'Updated Task',
      description: 'Updated Description',
      priority: 'low',
      tags: ['updated'],
      due_date: '2024-11-30T10:00:00Z',
      completed: true
    };

    expect(updateRequest.title).toBe('Updated Task');
    expect(updateRequest.description).toBe('Updated Description');
    expect(updateRequest.priority).toBe('low');
    expect(updateRequest.tags).toEqual(['updated']);
    expect(updateRequest.due_date).toBe('2024-11-30T10:00:00Z');
    expect(updateRequest.completed).toBe(true);
  });

  test('should validate priority values', () => {
    const validPriorities: ('high' | 'medium' | 'low')[] = ['high', 'medium', 'low'];

    validPriorities.forEach(priority => {
      expect(['high', 'medium', 'low']).toContain(priority);
    });
  });
});