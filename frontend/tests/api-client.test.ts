import axios from 'axios';
import { apiClient } from '../lib/api-client';

// Mock axios
jest.mock('axios');
const mockedAxios = jest.mocked(axios);

describe('API Client', () => {
  beforeEach(() => {
    // Clear all instances and calls to constructor and all methods:
    mockedAxios.create.mockClear();
    mockedAxios.get.mockClear();
    mockedAxios.post.mockClear();
    mockedAxios.put.mockClear();
    mockedAxios.delete.mockClear();
    mockedAxios.patch.mockClear();
  });

  test('should initialize with correct base URL', () => {
    // Mock the axios.create return value
    const mockAxiosInstance = {
      get: jest.fn(),
      post: jest.fn(),
      put: jest.fn(),
      delete: jest.fn(),
      patch: jest.fn(),
      interceptors: {
        request: { use: jest.fn() },
        response: { use: jest.fn() }
      }
    };

    mockedAxios.create.mockReturnValue(mockAxiosInstance as any);

    // Re-import to trigger the initialization
    const { apiClient } = require('../lib/api-client');

    // Verify that axios.create was called with the correct config
    expect(mockedAxios.create).toHaveBeenCalledWith({
      baseURL: 'http://localhost:8000/api',
      headers: {
        'Content-Type': 'application/json',
      },
    });
  });

  test('should make GET request', async () => {
    const mockResponse = { data: { id: 1, title: 'Test' } };
    mockedAxios.get.mockResolvedValue(mockResponse);

    const result = await apiClient.get('/tasks/1');

    expect(mockedAxios.get).toHaveBeenCalledWith('/tasks/1', undefined);
    expect(result).toEqual(mockResponse);
  });

  test('should make POST request', async () => {
    const postData = { title: 'New Task' };
    const mockResponse = { data: { id: 2, title: 'New Task' } };
    mockedAxios.post.mockResolvedValue(mockResponse);

    const result = await apiClient.post('/tasks', postData);

    expect(mockedAxios.post).toHaveBeenCalledWith('/tasks', postData, undefined);
    expect(result).toEqual(mockResponse);
  });

  test('should make PUT request', async () => {
    const putData = { title: 'Updated Task' };
    const mockResponse = { data: { id: 1, title: 'Updated Task' } };
    mockedAxios.put.mockResolvedValue(mockResponse);

    const result = await apiClient.put('/tasks/1', putData);

    expect(mockedAxios.put).toHaveBeenCalledWith('/tasks/1', putData, undefined);
    expect(result).toEqual(mockResponse);
  });

  test('should make DELETE request', async () => {
    const mockResponse = { data: { message: 'Deleted' } };
    mockedAxios.delete.mockResolvedValue(mockResponse);

    const result = await apiClient.delete('/tasks/1');

    expect(mockedAxios.delete).toHaveBeenCalledWith('/tasks/1', undefined);
    expect(result).toEqual(mockResponse);
  });

  test('should make PATCH request', async () => {
    const patchData = { completed: true };
    const mockResponse = { data: { id: 1, completed: true } };
    mockedAxios.patch.mockResolvedValue(mockResponse);

    const result = await apiClient.patch('/tasks/1/complete', patchData);

    expect(mockedAxios.patch).toHaveBeenCalledWith('/tasks/1/complete', patchData, undefined);
    expect(result).toEqual(mockResponse);
  });
});